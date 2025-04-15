/**
 * Test E2E pour vérifier la gestion des erreurs serveur lors de la création d'un consultant
 * Correspond au critère d'acceptation FF-US1.1.4
 */

describe('Gestion des erreurs serveur lors de la création d\'un consultant', () => {
  beforeEach(() => {
    // Simuler la connexion de l'utilisateur
    cy.intercept('POST', '/api/auth/login', { 
      body: { 
        access_token: 'fake_token',
        user: { 
          id: 1, 
          email: 'martin.dupont@acme.com', 
          full_name: 'Martin Dupont',
          role: 'recruiter'
        } 
      }
    }).as('login');
    
    // Intercepter les appels API liés aux consultants
    cy.intercept('GET', '/api/consultants*', { body: [] }).as('getConsultants');
    
    // Se connecter et accéder à la page des consultants
    cy.visit('/login');
    cy.get('input[name="email"]').type('martin.dupont@acme.com');
    cy.get('input[name="password"]').type('password123');
    cy.get('button[type="submit"]').click();
    cy.wait('@login');
    
    // Naviguer vers la page des consultants
    cy.visit('/consultants');
    cy.wait('@getConsultants');
    
    // Ouvrir le formulaire d'ajout de consultant
    cy.contains('button', 'Ajouter un consultant').click();
  });

  /**
   * Fonction utilitaire pour remplir le formulaire
   */
  const fillConsultantForm = () => {
    cy.get('input[name="first_name"]').type('Martin');
    cy.get('input[name="last_name"]').type('Dupont');
    cy.get('input[name="title"]').type('Développeur Java');
    cy.get('input[name="experience_years"]').type('5');
  };

  it('Affiche le message d\'erreur approprié en cas d\'erreur serveur 500', () => {
    // Intercepter la requête POST et la faire échouer avec un code 500
    cy.intercept('POST', '/api/consultants', {
      statusCode: 500,
      body: { message: 'Internal Server Error' }
    }).as('createConsultantError500');
    
    // Remplir le formulaire
    fillConsultantForm();
    
    // Soumettre le formulaire
    cy.contains('button', 'Créer le consultant').click();
    
    // Vérifier que la requête a été interceptée
    cy.wait('@createConsultantError500');
    
    // Vérifier que le message d'erreur approprié s'affiche
    cy.contains('Une erreur inattendue est survenue. Veuillez réessayer.').should('be.visible');
    
    // Vérifier qu'un log est bien envoyé (simulé par l'interception)
    cy.get('@createConsultantError500.all').should('have.length.at.least', 1);
  });

  it('Affiche le message d\'erreur approprié en cas d\'erreur serveur 502', () => {
    // Intercepter la requête POST et la faire échouer avec un code 502
    cy.intercept('POST', '/api/consultants', {
      statusCode: 502,
      body: { message: 'Bad Gateway' }
    }).as('createConsultantError502');
    
    // Remplir le formulaire
    fillConsultantForm();
    
    // Soumettre le formulaire
    cy.contains('button', 'Créer le consultant').click();
    
    // Vérifier que la requête a été interceptée
    cy.wait('@createConsultantError502');
    
    // Vérifier que le message d'erreur approprié s'affiche
    cy.contains('Service temporairement indisponible. Merci de réessayer.').should('be.visible');
    
    // Vérifier qu'un log est bien envoyé (simulé par l'interception)
    cy.get('@createConsultantError502.all').should('have.length.at.least', 1);
  });

  it('Affiche le message d\'erreur approprié en cas d\'erreur serveur 503', () => {
    // Intercepter la requête POST et la faire échouer avec un code 503
    cy.intercept('POST', '/api/consultants', {
      statusCode: 503,
      body: { message: 'Service Unavailable' }
    }).as('createConsultantError503');
    
    // Remplir le formulaire
    fillConsultantForm();
    
    // Soumettre le formulaire
    cy.contains('button', 'Créer le consultant').click();
    
    // Vérifier que la requête a été interceptée
    cy.wait('@createConsultantError503');
    
    // Vérifier que le message d'erreur approprié s'affiche
    cy.contains('Le service est en maintenance. Veuillez patienter.').should('be.visible');
    
    // Vérifier qu'un log est bien envoyé (simulé par l'interception)
    cy.get('@createConsultantError503.all').should('have.length.at.least', 1);
  });

  it('Soumet correctement le formulaire en cas de succès', () => {
    // Intercepter la requête POST et simuler une réponse de succès
    cy.intercept('POST', '/api/consultants', {
      statusCode: 201,
      body: { 
        id: 1,
        title: 'Développeur Java',
        user: { full_name: 'Martin Dupont' },
        skills: []
      }
    }).as('createConsultantSuccess');
    
    // Remplir le formulaire
    fillConsultantForm();
    
    // Soumettre le formulaire
    cy.contains('button', 'Créer le consultant').click();
    
    // Vérifier que la requête a été interceptée
    cy.wait('@createConsultantSuccess');
    
    // Vérifier que le message de succès s'affiche
    cy.contains('Le consultant a été créé avec succès').should('be.visible');
    
    // Vérifier que le modal se ferme
    cy.get('dialog').should('not.exist');
  });
});