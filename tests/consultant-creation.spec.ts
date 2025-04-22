import { test, expect } from '@playwright/test';

// Test pour l'US 1.1 - Création de profil consultant
test.describe('US 1.1 - Création de profil consultant', () => {
  
  // FF-US1.1.1 - Création simple
  test('permet de créer un consultant avec succès', async ({ page }) => {
    // Aller sur la page des consultants
    await page.goto('http://localhost:3001/consultants');
    
    // Cliquer sur le bouton pour créer un nouveau consultant
    await page.getByRole('button', { name: /Ajouter un consultant/i }).click();
    
    // Vérifier que le modal est ouvert
    const modal = page.getByRole('dialog');
    await expect(modal).toBeVisible();
    
    // Remplir le formulaire avec des données valides
    await page.getByRole('textbox', { name: 'Prénom*' }).fill('Martin');
    await page.getByRole('textbox', { name: 'Nom*', exact: true }).fill('Dupont');
    await page.getByRole('textbox', { name: 'Titre*' }).fill('Développeur React');
    await page.getByRole('spinbutton', { name: "Années d'expérience*" }).fill('5');
    
    // Soumettre le formulaire
    await page.getByRole('button', { name: /Créer le consultant/i }).click();
    
    // Vérifier que le modal est fermé (création réussie)
    await expect(modal).not.toBeVisible();
    
    // Vérifier la présence de données dans le tableau (preuve indirecte de succès)
    await expect(page.getByText('Martin Dupont')).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('Développeur React')).toBeVisible({ timeout: 10000 });
  });
  
  // FF-US1.1.2 - Champs requis
  test('affiche des erreurs pour les champs obligatoires manquants', async ({ page }) => {
    // Aller sur la page des consultants
    await page.goto('http://localhost:3001/consultants');
    
    // Cliquer sur le bouton pour créer un nouveau consultant
    await page.getByRole('button', { name: /Ajouter un consultant/i }).click();
    
    // Vérifier que le modal est ouvert
    const modal = page.getByRole('dialog');
    await expect(modal).toBeVisible();
    
    // Soumettre le formulaire sans remplir aucun champ
    await page.getByRole('button', { name: /Créer le consultant/i }).click();
    
    // Vérifier que des messages d'erreur s'affichent pour les champs obligatoires
    await expect(page.getByText(/Le champ prénom est requis/i)).toBeVisible();
    await expect(page.getByText(/Le champ nom est requis/i)).toBeVisible();
    await expect(page.getByText(/Le champ titre est requis/i)).toBeVisible();
    
    // Remplir uniquement certains champs
    await page.getByRole('textbox', { name: 'Prénom*' }).fill('Martin');
    await page.getByRole('textbox', { name: 'Nom*', exact: true }).fill('Dupont');
    
    // Soumettre à nouveau le formulaire
    await page.getByRole('button', { name: /Créer le consultant/i }).click();
    
    // Vérifier que le message d'erreur pour le titre est toujours présent
    await expect(page.getByText(/Le champ titre est requis/i)).toBeVisible();
    
    // Les erreurs pour les champs remplis ne devraient plus être visibles
    await expect(page.getByText(/Le champ prénom est requis/i)).not.toBeVisible();
    await expect(page.getByText(/Le champ nom est requis/i)).not.toBeVisible();
  });
  
  // FF-US1.1.3 - Upload image
  test('permet d\'ajouter et valider une photo de profil', async ({ page }) => {
    // Aller sur la page des consultants
    await page.goto('http://localhost:3001/consultants');
    
    // Cliquer sur le bouton pour créer un nouveau consultant
    await page.getByRole('button', { name: /Ajouter un consultant/i }).click();
    
    // Vérifier que le composant d'upload est visible
    await expect(page.getByText(/Photo de profil/i)).toBeVisible();
    await expect(page.getByText(/Sélectionner une image/i)).toBeVisible();
    
    // Tester l'upload d'un fichier non-image
    const invalidFileInput = page.locator('input[type="file"]');
    await invalidFileInput.setInputFiles({
      name: 'test.txt',
      mimeType: 'text/plain',
      buffer: Buffer.from('Invalid file content')
    });
    
    // Vérifier le message d'erreur pour format invalide
    await expect(page.getByText(/Format d'image non pris en charge/i)).toBeVisible();
    
    // Tester l'upload d'une image valide
    await invalidFileInput.setInputFiles({
      name: 'valid-image.jpg',
      mimeType: 'image/jpeg',
      buffer: Buffer.from('Valid image content')
    });
    
    // Vérifier que la prévisualisation est affichée
    await expect(page.getByText(/Format d'image non pris en charge/i)).not.toBeVisible();
    
    // Vérifier que le bouton "Effacer" est disponible
    await expect(page.getByRole('button', { name: /Effacer/i })).toBeVisible();
    
    // Tester la suppression de l'image
    await page.getByRole('button', { name: /Effacer/i }).click();
    
    // Vérifier que le bouton "Effacer" n'est plus visible
    await expect(page.getByRole('button', { name: /Effacer/i })).not.toBeVisible();
  });
  
  // FF-US1.1.4 - Erreur serveur
  test('affiche une erreur globale en cas d\'échec côté serveur', async ({ page }) => {
    // Aller sur la page des consultants
    await page.goto('http://localhost:3001/consultants');
    
    // Intercepter les requêtes API pour simuler une erreur serveur
    await page.route('**/api/consultants', route => {
      route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ 
          detail: 'Erreur interne du serveur lors de la création du consultant'
        })
      });
    });
    
    // Cliquer sur le bouton pour créer un consultant
    await page.getByRole('button', { name: /Ajouter un consultant/i }).click();
    
    // Remplir le formulaire avec des données valides
    await page.getByRole('textbox', { name: 'Prénom*' }).fill('Martin');
    await page.getByRole('textbox', { name: 'Nom*', exact: true }).fill('Dupont');
    await page.getByRole('textbox', { name: 'Titre*' }).fill('Développeur React');
    await page.getByRole('spinbutton', { name: "Années d'expérience*" }).fill('5');
    
    // Soumettre le formulaire
    await page.getByRole('button', { name: /Créer le consultant/i }).click();
    
    // Vérifier qu'un message d'erreur s'affiche
    await expect(page.getByRole('alert')).toBeVisible();
    await expect(page.getByText(/Erreur/i)).toBeVisible({ timeout: 10000 });
  });
  
  // Test rapide de création avec tous les champs (US 1.1 complète)
  test('permet de créer un consultant complet avec tous les champs optionnels', async ({ page }) => {
    // Aller sur la page des consultants
    await page.goto('http://localhost:3001/consultants');
    
    // Cliquer sur le bouton pour créer un nouveau consultant
    await page.getByRole('button', { name: /Ajouter un consultant/i }).click();
    
    // Remplir tous les champs du formulaire
    await page.getByRole('textbox', { name: 'Prénom*' }).fill('Jeanne');
    await page.getByRole('textbox', { name: 'Nom*', exact: true }).fill('Dubois');
    await page.getByRole('textbox', { name: 'Titre*' }).fill('Architecte Logiciel');
    await page.getByRole('spinbutton', { name: "Années d'expérience*" }).fill('8');
    
    // Ajouter une photo de profil
    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles({
      name: 'profile.jpg',
      mimeType: 'image/jpeg',
      buffer: Buffer.from('Profile image content')
    });
    
    // Remplir les champs optionnels si disponibles
    const biographieField = page.getByRole('textbox', { name: 'Biographie' });
    if (await biographieField.isVisible())
      await biographieField.fill('Expert en architecture logicielle avec 8 ans d\'expérience.');
    
    const linkedinField = page.getByRole('textbox', { name: 'LinkedIn' });
    if (await linkedinField.isVisible())
      await linkedinField.fill('https://linkedin.com/in/jeanne-dubois');
    
    // Soumettre le formulaire
    await page.getByRole('button', { name: /Créer le consultant/i }).click();
    
    // Vérifier que le modal est fermé (création réussie)
    await expect(page.getByRole('dialog')).not.toBeVisible();
    
    // Vérifier la présence de données dans le tableau (preuve indirecte de succès)
    await expect(page.getByText('Jeanne Dubois')).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('Architecte Logiciel')).toBeVisible({ timeout: 10000 });
  });
});