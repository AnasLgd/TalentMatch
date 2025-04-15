/**
 * Test E2E pour la validation des champs obligatoires lors de la création d'un consultant
 * Correspond au critère d'acceptation FF-US1.1.2
 */

describe('Validation des champs obligatoires du formulaire consultant', () => {
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

  it('Vérifie la validation du champ nom - affiche un message d\'erreur si vide', () => {
    // Remplir tous les champs sauf le nom
    cy.get('input[name="first_name"]').type('Martin');
    cy.get('input[name="title"]').type('Développeur Java');
    cy.get('input[name="experience_years"]').type('5');
    
    // Soumettre le formulaire
    cy.contains('button', 'Créer le consultant').click();
    
    // Vérifier que le message d'erreur s'affiche
    cy.contains('Le champ nom est requis').should('be.visible');
    
    // Vérifier que le formulaire n'a pas été soumis
    cy.get('@postConsultant').should('not.exist');
  });
  
  it('Vérifie la validation du champ prénom - affiche un message d\'erreur si vide', () => {
    // Remplir tous les champs sauf le prénom
    cy.get('input[name="last_name"]').type('Dupont');
    cy.get('input[name="title"]').type('Développeur Java');
    cy.get('input[name="experience_years"]').type('5');
    
    // Soumettre le formulaire
    cy.contains('button', 'Créer le consultant').click();
    
    // Vérifier que le message d'erreur s'affiche
    cy.contains('Le champ prénom est requis').should('be.visible');
  });
  
  it('Vérifie la validation du champ titre - affiche un message d\'erreur si vide', () => {
    // Remplir tous les champs sauf le titre
    cy.get('input[name="first_name"]').type('Martin');
    cy.get('input[name="last_name"]').type('Dupont');
    cy.get('input[name="experience_years"]').type('5');
    
    // Soumettre le formulaire
    cy.contains('button', 'Créer le consultant').click();
    
    // Vérifier que le message d'erreur s'affiche
    cy.contains('Le champ titre est requis').should('be.visible');
  });
  
  it('Vérifie la validation du champ expérience - affiche un message d\'erreur si vide', () => {
    // Remplir tous les champs sauf l'expérience
    cy.get('input[name="first_name"]').type('Martin');
    cy.get('input[name="last_name"]').type('Dupont');
    cy.get('input[name="title"]').type('Développeur Java');
    
    // Soumettre le formulaire
    cy.contains('button', 'Créer le consultant').click();
    
    // Vérifier que le message d'erreur s'affiche
    cy.contains('Le champ expérience est requis').should('be.visible');
  });
  
  it('Crée un consultant avec succès quand tous les champs obligatoires sont remplis', () => {
    // Intercepter l'appel de création
    cy.intercept('POST', '/api/consultants', { 
      statusCode: 201, 
      body: { 
        id: 1,
        title: 'Développeur Java',
        user: { full_name: 'Martin Dupont' },
        skills: []
      } 
    }).as('postConsultant');
    
    // Remplir tous les champs obligatoires
    cy.get('input[name="first_name"]').type('Martin');
    cy.get('input[name="last_name"]').type('Dupont');
    cy.get('input[name="title"]').type('Développeur Java');
    cy.get('input[name="experience_years"]').type('5');
    
    // Soumettre le formulaire
    cy.contains('button', 'Créer le consultant').click();
    
    // Vérifier que l'appel API a été fait
    cy.wait('@postConsultant');
    
    // Vérifier que le message de succès s'affiche
    cy.contains('Le profil consultant a été créé avec succès').should('be.visible');
    
    // Vérifier que le modal se ferme
    cy.get('dialog').should('not.exist');
  });
});