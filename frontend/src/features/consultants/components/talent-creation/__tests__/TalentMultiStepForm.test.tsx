import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { TalentMultiStepForm } from '../TalentMultiStepForm';
import { consultantService } from '../../../services/consultant-service';

// Mock the services
jest.mock('../../../services/consultant-service', () => ({
  consultantService: {
    createConsultant: jest.fn().mockResolvedValue({ id: 123 }),
  },
}));

// Mock the toast
jest.mock('@/hooks/use-toast', () => ({
  toast: jest.fn(),
  useToast: () => ({
    toast: jest.fn(),
  }),
}));

describe('TalentMultiStepForm', () => {
  const mockProps = {
    companyId: 1,
    onSuccess: jest.fn(),
    onCancel: jest.fn(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders correctly and supports navigation between steps', async () => {
    render(<TalentMultiStepForm {...mockProps} />);
    
    // Should start at the first step
    expect(screen.getByText('Identité & Disponibilité')).toBeInTheDocument();
    
    // Fill required fields in first step
    fireEvent.change(screen.getByPlaceholderText('Prénom'), { 
      target: { value: 'John' } 
    });
    
    fireEvent.change(screen.getByPlaceholderText('Nom'), {
      target: { value: 'Doe' }
    });
    
    fireEvent.change(screen.getByPlaceholderText(/Développeur, DevOps/i), {
      target: { value: 'Développeur React' }
    });
    
    // Navigate to next step
    fireEvent.click(screen.getByText('Suivant'));
    
    // Should be on the second step (Skills)
    await waitFor(() => {
      expect(screen.getByText('Compétences')).toBeInTheDocument();
    });
    
    // Navigate to next step
    fireEvent.click(screen.getByText('Suivant'));
    
    // Should be on the third step (Projects)
    await waitFor(() => {
      expect(screen.getByText('Projets et références')).toBeInTheDocument();
    });
    
    // Navigate to next step
    fireEvent.click(screen.getByText('Suivant'));
    
    // Should be on the fourth step (Soft Skills)
    await waitFor(() => {
      expect(screen.getByText('Soft Skills')).toBeInTheDocument();
    });
    
    // Navigate to next step
    fireEvent.click(screen.getByText('Suivant'));
    
    // Should be on the final step (Summary)
    await waitFor(() => {
      expect(screen.getByText('Récapitulatif du profil')).toBeInTheDocument();
    });
    
    // Navigate back
    fireEvent.click(screen.getByText('Précédent'));
    
    // Should be back on the fourth step
    await waitFor(() => {
      expect(screen.getByText('Soft Skills')).toBeInTheDocument();
    });
  });

  it('pre-fills form fields from CV analysis', async () => {
    const mockCvAnalysisResult = {
      fileId: 1,
      candidate: {
        name: 'Jane Smith',
        email: 'jane@example.com',
        phone: '123456789',
        skills: [
          { name: 'React', level: 'Avancé' },
          { name: 'TypeScript', level: 'Intermédiaire' }
        ],
        experience: [
          { 
            role: 'Frontend Developer', 
            company: 'Tech Corp', 
            period: '2020-2022',
            description: 'Developed web applications using React' 
          }
        ],
        education: []
      }
    };
    
    render(<TalentMultiStepForm {...mockProps} cvAnalysisResult={mockCvAnalysisResult} />);
    
    // Check if first name is pre-filled
    expect(screen.getByDisplayValue('Jane')).toBeInTheDocument();
    
    // Navigate to the skills step
    fireEvent.click(screen.getByText('Suivant'));
    
    // Check if skills are pre-filled
    await waitFor(() => {
      expect(screen.getByText('React')).toBeInTheDocument();
      expect(screen.getByText('TypeScript')).toBeInTheDocument();
    });
  });

  it('submits the form successfully', async () => {
    render(<TalentMultiStepForm {...mockProps} />);
    
    // Fill required fields in first step
    fireEvent.change(screen.getByPlaceholderText('Prénom'), { 
      target: { value: 'John' } 
    });
    
    fireEvent.change(screen.getByPlaceholderText('Nom'), {
      target: { value: 'Doe' }
    });
    
    fireEvent.change(screen.getByPlaceholderText(/Développeur, DevOps/i), {
      target: { value: 'Développeur React' }
    });
    
    // Navigate through all steps
    fireEvent.click(screen.getByText('Suivant')); // to Skills
    fireEvent.click(screen.getByText('Suivant')); // to Projects
    fireEvent.click(screen.getByText('Suivant')); // to Soft Skills
    fireEvent.click(screen.getByText('Suivant')); // to Summary
    
    // Submit form
    fireEvent.click(screen.getByText('Finaliser'));
    
    // Verify service was called
    await waitFor(() => {
      expect(consultantService.createConsultant).toHaveBeenCalledTimes(1);
      expect(consultantService.createConsultant).toHaveBeenCalledWith(
        expect.objectContaining({
          first_name: 'John',
          last_name: 'Doe',
          title: 'Développeur React',
          company_id: 1
        })
      );
      expect(mockProps.onSuccess).toHaveBeenCalledWith(123);
    });
  });
});