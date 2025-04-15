import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ConsultantForm } from '../ConsultantForm';
import { useConsultants } from '../../hooks/useConsultants';
import { uploadService } from '../../services/upload-service';
import { toast } from '@/hooks/use-toast';

// Mock des dépendances
jest.mock('../../hooks/useConsultants');
jest.mock('../../services/upload-service');
jest.mock('@/hooks/use-toast');

describe('ConsultantForm', () => {
  // Configuration des mocks
  const mockCreateConsultant = jest.fn();
  const mockOnSuccess = jest.fn();
  const mockOnCancel = jest.fn();
  const mockUploadFile = jest.fn();

  beforeEach(() => {
    // Reset des mocks
    jest.clearAllMocks();
    
    // Mock du hook useConsultants
    (useConsultants as jest.Mock).mockReturnValue({
      createConsultant: mockCreateConsultant,
      isCreating: false
    });

    // Mock du service d'upload
    (uploadService.uploadFile as jest.Mock) = mockUploadFile;
    mockUploadFile.mockResolvedValue('https://minio.example.com/profiles/photo.jpg');

    // Mock du toast
    (toast as jest.Mock) = jest.fn();
  });

  it('rend le formulaire avec tous les champs requis', () => {
    render(
      <ConsultantForm 
        onSuccess={mockOnSuccess} 
        onCancel={mockOnCancel} 
        userId={1} 
        companyId={1} 
      />
    );

    // Vérifier que tous les champs obligatoires sont présents
    expect(screen.getByLabelText(/Prénom\*/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Nom\*/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Titre\*/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Années d'expérience/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Photo de profil/i)).toBeInTheDocument();
    expect(screen.getByText(/Créer le consultant/i)).toBeInTheDocument();
  });

  // Tests pour chaque champ obligatoire manquant individuellement - FF-US1.1.2
  it.each([
    {
      field: 'nom',
      errorMessage: 'Le champ nom est requis',
      fieldValues: { first_name: 'Martin', title: 'Développeur', experience_years: '5' }
    },
    {
      field: 'prénom',
      errorMessage: 'Le champ prénom est requis',
      fieldValues: { last_name: 'Dupont', title: 'Développeur', experience_years: '5' }
    },
    {
      field: 'titre',
      errorMessage: 'Le champ titre est requis',
      fieldValues: { first_name: 'Martin', last_name: 'Dupont', experience_years: '5' }
    },
    {
      field: 'expérience',
      errorMessage: 'Le champ expérience est requis',
      fieldValues: { first_name: 'Martin', last_name: 'Dupont', title: 'Développeur' }
    }
  ])('affiche l\'erreur "$errorMessage" quand le champ $field est manquant', async ({ field, errorMessage, fieldValues }) => {
    render(
      <ConsultantForm
        onSuccess={mockOnSuccess}
        onCancel={mockOnCancel}
        userId={1}
        companyId={1}
      />
    );
    
    // Remplir tous les autres champs
    if (fieldValues.first_name) {
      await userEvent.type(screen.getByLabelText(/Prénom\*/i), fieldValues.first_name);
    }
    if (fieldValues.last_name) {
      await userEvent.type(screen.getByLabelText(/Nom\*/i), fieldValues.last_name);
    }
    if (fieldValues.title) {
      await userEvent.type(screen.getByLabelText(/Titre\*/i), fieldValues.title);
    }
    if (fieldValues.experience_years) {
      await userEvent.type(screen.getByLabelText(/Années d'expérience\*/i), fieldValues.experience_years);
    }
    
    // Soumettre le formulaire
    const submitButton = screen.getByText(/Créer le consultant/i);
    fireEvent.click(submitButton);
    
    // Vérifier que le message d'erreur spécifique apparaît
    await waitFor(() => {
      expect(screen.getByText(new RegExp(errorMessage, 'i'))).toBeInTheDocument();
    });
    
    // Vérifier que la création n'a pas été appelée
    expect(mockCreateConsultant).not.toHaveBeenCalled();
  });

  it('crée un consultant avec succès quand le formulaire est valide', async () => {
    render(
      <ConsultantForm 
        onSuccess={mockOnSuccess} 
        onCancel={mockOnCancel} 
        userId={1} 
        companyId={1} 
      />
    );
    
    // Remplir le formulaire
    await userEvent.type(screen.getByLabelText(/Prénom\*/i), 'Martin');
    await userEvent.type(screen.getByLabelText(/Nom\*/i), 'Dupont');
    await userEvent.type(screen.getByLabelText(/Titre\*/i), 'Développeur Java');
    await userEvent.type(screen.getByLabelText(/Années d'expérience/i), '5');
    
    // Simuler l'upload d'une photo
    const file = new File(['(binary content)'], 'photo.jpg', { type: 'image/jpeg' });
    const fileInput = screen.getByLabelText(/Photo de profil/i);
    await userEvent.upload(fileInput, file);
    
    // Soumettre le formulaire
    const submitButton = screen.getByText(/Créer le consultant/i);
    fireEvent.click(submitButton);
    
    // Vérifier que l'upload a été appelé
    await waitFor(() => {
      expect(mockUploadFile).toHaveBeenCalledWith(file, 'consultants/profiles');
    });
    
    // Vérifier que la création a été appelée avec les bonnes données
    await waitFor(() => {
      expect(mockCreateConsultant).toHaveBeenCalledWith(expect.objectContaining({
        user_id: 1,
        company_id: 1,
        title: 'Développeur Java',
        experience_years: 5,
        photo_url: 'https://minio.example.com/profiles/photo.jpg',
      }));
    });
    
    // Vérifier que onSuccess a été appelé
    expect(mockOnSuccess).toHaveBeenCalled();
  });

  it('crée un consultant sans photo quand aucune photo n\'est fournie', async () => {
    render(
      <ConsultantForm 
        onSuccess={mockOnSuccess} 
        onCancel={mockOnCancel} 
        userId={1} 
        companyId={1} 
      />
    );
    
    // Remplir le formulaire sans photo
    await userEvent.type(screen.getByLabelText(/Prénom\*/i), 'Alice');
    await userEvent.type(screen.getByLabelText(/Nom\*/i), 'Lee');
    await userEvent.type(screen.getByLabelText(/Titre\*/i), 'QA Analyst');
    
    // Soumettre le formulaire
    const submitButton = screen.getByText(/Créer le consultant/i);
    fireEvent.click(submitButton);
    
    // Vérifier que l'upload n'a pas été appelé
    await waitFor(() => {
      expect(mockUploadFile).not.toHaveBeenCalled();
    });
    
    // Vérifier que la création a été appelée avec les bonnes données
    await waitFor(() => {
      expect(mockCreateConsultant).toHaveBeenCalledWith(expect.objectContaining({
        user_id: 1,
        company_id: 1,
        title: 'QA Analyst',
        photo_url: undefined,
      }));
    });
    
    // Vérifier que onSuccess a été appelé
    expect(mockOnSuccess).toHaveBeenCalled();
  });
});