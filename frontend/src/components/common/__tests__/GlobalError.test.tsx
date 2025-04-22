import React from 'react';
import { render, screen } from '@testing-library/react';
import { GlobalError, ErrorType } from '../GlobalError';

describe('GlobalError', () => {
  it('affiche un message d\'erreur basé sur le type', () => {
    // Arrange & Act
    render(<GlobalError type={ErrorType.UNEXPECTED} />);
    
    // Assert
    expect(screen.getByText('Erreur inattendue')).toBeInTheDocument();
    expect(screen.getByText('Une erreur inattendue est survenue. Veuillez réessayer.')).toBeInTheDocument();
    expect(screen.getByRole('alert')).toBeInTheDocument();
  });
  
  it('utilise un titre personnalisé si fourni', () => {
    // Arrange
    const customTitle = "Erreur de création";
    
    // Act
    render(<GlobalError type={ErrorType.UNEXPECTED} title={customTitle} />);
    
    // Assert
    expect(screen.getByText(customTitle)).toBeInTheDocument();
    expect(screen.getByText('Une erreur inattendue est survenue. Veuillez réessayer.')).toBeInTheDocument();
  });
  
  it('utilise une description personnalisée si fournie', () => {
    // Arrange
    const customDescription = "Une erreur s'est produite lors de la création du consultant";
    
    // Act
    render(<GlobalError type={ErrorType.UNEXPECTED} description={customDescription} />);
    
    // Assert
    expect(screen.getByText('Erreur inattendue')).toBeInTheDocument();
    expect(screen.getByText(customDescription)).toBeInTheDocument();
  });
  
  it('utilise à la fois un titre et une description personnalisés si fournis', () => {
    // Arrange
    const customTitle = "Erreur de création";
    const customDescription = "Une erreur s'est produite lors de la création du consultant";
    
    // Act
    render(
      <GlobalError 
        type={ErrorType.UNEXPECTED} 
        title={customTitle} 
        description={customDescription} 
      />
    );
    
    // Assert
    expect(screen.getByText(customTitle)).toBeInTheDocument();
    expect(screen.getByText(customDescription)).toBeInTheDocument();
  });
  
  it('applique des classes CSS personnalisées', () => {
    // Arrange
    const customClass = "custom-error-class";
    
    // Act
    render(<GlobalError type={ErrorType.UNEXPECTED} className={customClass} />);
    
    // Assert
    const alertElement = screen.getByRole('alert');
    expect(alertElement).toHaveClass(customClass);
  });
  
  it('affiche l\'icône correspondant au type d\'erreur', () => {
    // Arrange & Act
    const { container } = render(<GlobalError type={ErrorType.SERVICE_UNAVAILABLE} />);
    
    // Assert - Vérifier la présence de l'icône
    expect(screen.getByText('Service indisponible')).toBeInTheDocument();
    // Nous vérifions que l'élément IconSVG est présent
    expect(container.querySelector('svg')).toBeInTheDocument();
  });
  
  it('gère correctement les erreurs de validation', () => {
    // Arrange & Act
    render(<GlobalError type={ErrorType.VALIDATION} />);
    
    // Assert
    expect(screen.getByText('Erreur de validation')).toBeInTheDocument();
    expect(screen.getByText('Veuillez vérifier les données saisies et réessayer.')).toBeInTheDocument();
  });
});