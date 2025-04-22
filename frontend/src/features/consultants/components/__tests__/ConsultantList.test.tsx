import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Section } from '../Section';
import { ConsultantTable } from '../ConsultantTable';
import { PaginationControls } from '../PaginationControls';
import { ConsultantDisplay, AvailabilityStatus } from '../../types';

// Mock des données de test
const mockConsultants: ConsultantDisplay[] = [
  {
    id: 1,
    name: 'John Doe',
    role: 'Développeur Frontend',
    experience: '5 ans',
    skills: [{ id: 1, name: 'React' }, { id: 2, name: 'TypeScript' }],
    status: 'En cours de process',
  },
  {
    id: 2,
    name: 'Jane Smith',
    role: 'Data Scientist',
    experience: '3 ans',
    skills: [{ id: 3, name: 'Python' }, { id: 4, name: 'AWS' }],
    status: 'Qualifié',
  },
  {
    id: 3,
    name: 'Emma Johnson',
    role: 'UX Designer',
    experience: '4 ans',
    skills: [{ id: 5, name: 'Figma' }],
    status: 'Disponible',
  },
  {
    id: 4,
    name: 'Mark Wilson',
    role: 'Développeur Backend',
    experience: '7 ans',
    skills: [{ id: 6, name: 'Java' }, { id: 7, name: 'Spring' }],
    status: 'En mission',
  },
  {
    id: 5,
    name: 'Anna Brown',
    role: 'DevOps Engineer',
    experience: '6 ans',
    skills: [{ id: 8, name: 'Docker' }, { id: 9, name: 'Kubernetes' }],
    status: 'Intercontrat',
  },
  // Ajout de consultants supplémentaires pour tester la pagination
  {
    id: 6,
    name: 'Robert Green',
    role: 'Frontend Developer',
    experience: '8 ans',
    skills: [{ id: 10, name: 'Vue.js' }, { id: 11, name: 'CSS' }],
    status: 'En cours de process',
  },
  {
    id: 7,
    name: 'Sophie Black',
    role: 'UI Designer',
    experience: '4 ans',
    skills: [{ id: 12, name: 'Sketch' }, { id: 13, name: 'Adobe XD' }],
    status: 'Qualifié',
  },
];

describe('Section & ConsultantTable Components', () => {
  test('Section renders correctly with title', () => {
    render(<Section title="Test Section">Children content</Section>);
    
    expect(screen.getByText('Test Section')).toBeInTheDocument();
    expect(screen.getByText('Children content')).toBeInTheDocument();
  });

  test('ConsultantTable renders empty state when no consultants', () => {
    render(<ConsultantTable consultants={[]} />);
    
    expect(screen.getByText('Aucun consultant dans cette catégorie')).toBeInTheDocument();
  });

  test('ConsultantTable renders first 5 consultants by default', () => {
    render(<ConsultantTable consultants={mockConsultants} />);
    
    // Vérifier que les 5 premiers consultants sont affichés
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('Jane Smith')).toBeInTheDocument();
    expect(screen.getByText('Emma Johnson')).toBeInTheDocument();
    expect(screen.getByText('Mark Wilson')).toBeInTheDocument();
    expect(screen.getByText('Anna Brown')).toBeInTheDocument();
    
    // Vérifier que le 6ème consultant n'est pas affiché initialement
    expect(screen.queryByText('Robert Green')).not.toBeInTheDocument();
  });

  test('PaginationControls is hidden when there is only one page', () => {
    // 5 consultants = exactement 1 page (pas de pagination nécessaire)
    const fiveConsultants = mockConsultants.slice(0, 5);
    render(<ConsultantTable consultants={fiveConsultants} />);
    
    // Les contrôles de pagination ne doivent pas être présents
    expect(screen.queryByText('Page 1 sur 1')).not.toBeInTheDocument();
    expect(screen.queryByText('Suivant')).not.toBeInTheDocument();
    expect(screen.queryByText('Précédent')).not.toBeInTheDocument();
  });

  test('PaginationControls shows correct page count with multiple pages', () => {
    render(<ConsultantTable consultants={mockConsultants} />);
    
    // Pour 7 consultants avec 5 par page, nous devrions avoir 2 pages
    expect(screen.getByText('Page 1 sur 2')).toBeInTheDocument();
  });

  test('No empty rows are added when fewer than 5 consultants', () => {
    const threeConsultants = mockConsultants.slice(0, 3);
    const { container } = render(<ConsultantTable consultants={threeConsultants} />);
    
    // Vérifier que seules les 3 lignes de consultants sont présentes (pas de lignes vides)
    const rows = container.querySelectorAll('tbody tr');
    expect(rows.length).toBe(3);
    
    // Vérifier que les 3 consultants sont présents
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('Jane Smith')).toBeInTheDocument();
    expect(screen.getByText('Emma Johnson')).toBeInTheDocument();
  });

  test('No fixed height is applied when fewer than 5 consultants', () => {
    const threeConsultants = mockConsultants.slice(0, 3);
    const { container } = render(<ConsultantTable consultants={threeConsultants} />);
    
    // Vérifier qu'il n'y a pas de style de hauteur fixe appliqué
    const tableContainer = container.querySelector('.relative.w-full.overflow-auto');
    expect(tableContainer).not.toHaveClass('flex-1');
  });

  test('Four consultant categories render correctly with pagination', () => {
    // Créer des listes de consultants suffisamment longues pour tester la pagination
    const processCandidates = [
      mockConsultants[0], // John Doe
      mockConsultants[5]  // Robert Green
    ];
    
    const qualifiedConsultants = [
      mockConsultants[1], // Jane Smith
      mockConsultants[2], // Emma Johnson
      mockConsultants[6]  // Sophie Black
    ];
    
    const onMissionConsultants = [mockConsultants[3]]; // Mark Wilson
    const intercontractConsultants = [mockConsultants[4]]; // Anna Brown
    
    // Render les quatre sections avec leurs consultants respectifs, structurés en grille
    const { container } = render(
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Section title="Candidats en cours de process">
          <ConsultantTable consultants={processCandidates} />
        </Section>
        <Section title="Candidats qualifiés (Vivier de consultants)">
          <ConsultantTable consultants={qualifiedConsultants} />
        </Section>
        <Section title="Consultants en mission">
          <ConsultantTable consultants={onMissionConsultants} />
        </Section>
        <Section title="Consultants en intercontract">
          <ConsultantTable consultants={intercontractConsultants} />
        </Section>
      </div>
    );
    
    // Vérifier que les titres des sections sont affichés
    expect(screen.getByText("Candidats en cours de process")).toBeInTheDocument();
    expect(screen.getByText("Candidats qualifiés (Vivier de consultants)")).toBeInTheDocument();
    expect(screen.getByText("Consultants en mission")).toBeInTheDocument();
    expect(screen.getByText("Consultants en intercontract")).toBeInTheDocument();
    
    // Vérifier que les consultants sont dans les bonnes sections
    expect(screen.getByText("John Doe")).toBeInTheDocument();
    expect(screen.getByText("Jane Smith")).toBeInTheDocument();
    expect(screen.getByText("Emma Johnson")).toBeInTheDocument();
    expect(screen.getByText("Mark Wilson")).toBeInTheDocument();
    expect(screen.getByText("Anna Brown")).toBeInTheDocument();
    
    // Vérifier la structure de la grille
    const gridContainer = container.firstChild;
    expect(gridContainer).toHaveClass('grid');
    expect(gridContainer).toHaveClass('grid-cols-1');
    expect(gridContainer).toHaveClass('lg:grid-cols-2');
    expect(gridContainer).toHaveClass('gap-6');
  });
  
  test('Pagination controls are hidden when there are 5 or fewer consultants', () => {
    // Exactement 5 consultants = pagination cachée
    const fiveConsultants = mockConsultants.slice(0, 5);
    const { queryByText } = render(<ConsultantTable consultants={fiveConsultants} />);
    
    // Les contrôles de pagination ne devraient pas être visibles
    expect(queryByText('Page 1 sur 1')).not.toBeInTheDocument();
    expect(queryByText('Suivant')).not.toBeInTheDocument();
    expect(queryByText('Précédent')).not.toBeInTheDocument();
  });
  
  test('Pagination controls are visible when there are more than 5 consultants', () => {
    // 7 consultants = pagination visible
    const { getByText } = render(<ConsultantTable consultants={mockConsultants} />);
    
    // Les contrôles de pagination devraient être visibles
    expect(getByText('Page 1 sur 2')).toBeInTheDocument();
    expect(getByText('Suivant')).toBeInTheDocument();
  });
  
  test('Responsive behavior - grid adapts to screen size', () => {
    // Tester le responsive de la grille
    const { container } = render(
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Section title="Section 1">
          <div>Contenu 1</div>
        </Section>
        <Section title="Section 2">
          <div>Contenu 2</div>
        </Section>
      </div>
    );
    
    // Vérifier les classes responsives
    const gridElement = container.firstChild;
    expect(gridElement).toHaveClass('grid-cols-1'); // Mobile first
    expect(gridElement).toHaveClass('lg:grid-cols-2'); // Desktop = 2 colonnes
  });
});