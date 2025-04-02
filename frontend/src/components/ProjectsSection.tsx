
import React from 'react';
import { useInView } from '../hooks/useInView';
import ProjectCard from './ProjectCard';

const projects = [
  {
    title: 'Handee',
    description: "Handee Template's unique interactive animations, paired with a clean and modern layout, will elevate the appeal of your website.",
    image: 'https://images.unsplash.com/photo-1551650975-87deedd944c3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1974&q=80'
  },
  {
    title: 'Linel',
    description: 'Linel combines minimal aesthetics with powerful scroll animations to create an immersive digital experience.',
    image: 'https://images.unsplash.com/photo-1614332287897-cdc485fa562d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80'
  },
  {
    title: 'Centim',
    description: 'Centim offers bold typography and smooth animations to create a memorable digital presence for modern brands.',
    image: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1115&q=80'
  },
  {
    title: 'Inkenious',
    description: 'Inkenious showcases creativity through artistic animations and thoughtful interactions throughout the user journey.',
    image: 'https://images.unsplash.com/photo-1555421689-3f034debb7a6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80'
  }
];

const ProjectsSection: React.FC = () => {
  const { ref, inView } = useInView<HTMLHeadingElement>({ threshold: 0.1 });

  return (
    <section id="projects" className="py-32">
      <div className="container mx-auto px-8">
        <h2 className={`text-5xl font-bold mb-24 slide-in ${inView ? 'visible' : ''}`} ref={ref}>
          Our Projects
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-24">
          {projects.map((project, index) => (
            <ProjectCard
              key={index}
              title={project.title}
              description={project.description}
              image={project.image}
            />
          ))}
        </div>
      </div>
    </section>
  );
};

export default ProjectsSection;
