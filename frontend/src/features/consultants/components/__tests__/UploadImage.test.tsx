import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { UploadImage } from '../UploadImage';

describe('UploadImage', () => {
  // Configuration des mocks
  const mockOnImageSelected = jest.fn();
  
  beforeEach(() => {
    // Reset des mocks avant chaque test
    jest.clearAllMocks();
    // Mock URL.createObjectURL
    URL.createObjectURL = jest.fn(() => 'blob:mock-url');
  });
  
  it('rend le composant avec le label par défaut', () => {
    // Arrange & Act
    render(<UploadImage onImageSelected={mockOnImageSelected} />);
    
    // Assert
    expect(screen.getByText('Photo de profil (optionnelle)')).toBeInTheDocument();
    expect(screen.getByText('Sélectionner une image')).toBeInTheDocument();
    expect(screen.getByText(/Formats acceptés/)).toBeInTheDocument();
  });
  
  it('rend le composant avec un label personnalisé', () => {
    // Arrange
    const customLabel = 'Image de logo';
    
    // Act
    render(<UploadImage onImageSelected={mockOnImageSelected} label={customLabel} />);
    
    // Assert
    expect(screen.getByText(customLabel)).toBeInTheDocument();
  });
  
  it('permet de sélectionner une image valide', async () => {
    // Arrange
    render(<UploadImage onImageSelected={mockOnImageSelected} />);
    
    // Act - Simuler la sélection d'un fichier
    const file = new File(['test content'], 'test.jpg', { type: 'image/jpeg' });
    const fileInput = screen.getByLabelText('Photo de profil (optionnelle)', { selector: 'input[type="file"]' });
    await userEvent.upload(fileInput, file);
    
    // Assert
    expect(mockOnImageSelected).toHaveBeenCalledWith(file);
    expect(URL.createObjectURL).toHaveBeenCalledWith(file);
  });
  
  it('affiche une erreur pour un format de fichier invalide', async () => {
    // Arrange
    render(<UploadImage onImageSelected={mockOnImageSelected} />);
    
    // Act - Simuler la sélection d'un fichier avec un format invalide
    const invalidFile = new File(['test content'], 'test.txt', { type: 'text/plain' });
    const fileInput = screen.getByLabelText('Photo de profil (optionnelle)', { selector: 'input[type="file"]' });
    await userEvent.upload(fileInput, invalidFile);
    
    // Assert
    expect(screen.getByText(/Format d'image non pris en charge/)).toBeInTheDocument();
    expect(mockOnImageSelected).toHaveBeenCalledWith(null);
  });
  
  it('affiche une erreur pour un fichier trop volumineux', async () => {
    // Arrange
    render(<UploadImage onImageSelected={mockOnImageSelected} maxSizeInMB={1} />);
    
    // Act - Créer un faux fichier volumineux
    const largeFile = new File(['x'.repeat(1.5 * 1024 * 1024)], 'large.jpg', { type: 'image/jpeg' });
    Object.defineProperty(largeFile, 'size', { value: 1.5 * 1024 * 1024 });
    
    const fileInput = screen.getByLabelText('Photo de profil (optionnelle)', { selector: 'input[type="file"]' });
    await userEvent.upload(fileInput, largeFile);
    
    // Assert
    expect(screen.getByText(/Taille d'image trop importante/)).toBeInTheDocument();
    expect(mockOnImageSelected).toHaveBeenCalledWith(null);
  });
  
  it('permet d\'effacer une image sélectionnée', async () => {
    // Arrange
    render(<UploadImage onImageSelected={mockOnImageSelected} />);
    
    // Act - Sélectionner puis effacer une image
    const file = new File(['test content'], 'test.jpg', { type: 'image/jpeg' });
    const fileInput = screen.getByLabelText('Photo de profil (optionnelle)', { selector: 'input[type="file"]' });
    await userEvent.upload(fileInput, file);
    
    // Vérifier que l'image a été sélectionnée
    expect(mockOnImageSelected).toHaveBeenCalledWith(file);
    
    // Le bouton "Effacer" devrait maintenant être visible
    const clearButton = screen.getByText('Effacer');
    await userEvent.click(clearButton);
    
    // Assert
    expect(mockOnImageSelected).toHaveBeenCalledWith(null);
  });
  
  it('accepte les formats d\'image personnalisés', async () => {
    // Arrange
    const customFormats = ['.gif'];
    render(<UploadImage onImageSelected={mockOnImageSelected} acceptedFormats={customFormats} />);
    
    // Assert - Vérifier que les formats personnalisés sont affichés
    expect(screen.getByText(/Formats acceptés: .gif/)).toBeInTheDocument();
    
    // Act - Sélectionner un fichier GIF
    const file = new File(['test content'], 'test.gif', { type: 'image/gif' });
    const fileInput = screen.getByLabelText('Photo de profil (optionnelle)', { selector: 'input[type="file"]' });
    await userEvent.upload(fileInput, file);
    
    // Assert
    expect(mockOnImageSelected).toHaveBeenCalledWith(file);
  });
});