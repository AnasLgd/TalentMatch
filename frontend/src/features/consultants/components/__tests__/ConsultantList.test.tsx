import React from 'react';
import { render, screen } from '@testing-library/react';
import { Section } from '../Section';
import { ConsultantTable } from '../ConsultantTable';
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

  test('ConsultantTable renders consultants correctly', () => {
    render(<ConsultantTable consultants={mockConsultants} />);
    
    mockConsultants.forEach(consultant => {
      expect(screen.getByText(consultant.name)).toBeInTheDocument();
      expect(screen.getByText(consultant.role)).toBeInTheDocument();
      expect(screen.getByText(consultant.experience)).toBeInTheDocument();
      expect(screen.getByText(consultant.status)).toBeInTheDocument();
      
      // Vérifier que les compétences sont affichées
      consultant.skills.forEach(skill => {
        expect(screen.getByText(skill.name)).toBeInTheDocument();
      });
    });
  });

  test('Four consultant categories render correctly', () => {
    // Filtrer les consultants par catégorie
    const processCandidates = mockConsultants.filter(c => c.status === "En cours de process");
    const qualifiedConsultants = mockConsultants.filter(c => 
      c.status === "Qualifié" || c.status === "Disponible");
    const onMissionConsultants = mockConsultants.filter(c => c.status === "En mission");
    const intercontractConsultants = mockConsultants.filter(c => c.status === "Intercontrat");
    
    // Render les quatre sections avec leurs consultants respectifs
    const { container } = render(
      <div>
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
    expect(screen.getByText("John Doe").closest('div').parentElement?.parentElement?.textContent)
      .toContain("En cours de process");

    expect(screen.getByText("Jane Smith").closest('div').parentElement?.parentElement?.textContent)
      .toContain("Qualifié");
      
    expect(screen.getByText("Emma Johnson").closest('div').parentElement?.parentElement?.textContent)
      .toContain("Disponible");
      
    expect(screen.getByText("Mark Wilson").closest('div').parentElement?.parentElement?.textContent)
      .toContain("En mission");
      
    expect(screen.getByText("Anna Brown").closest('div').parentElement?.parentElement?.textContent)
      .toContain("Intercontrat");
  });
});