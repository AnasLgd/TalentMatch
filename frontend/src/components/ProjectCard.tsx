
import React from 'react';
import { useInView } from '../hooks/useInView';
import { ArrowUpRight } from 'lucide-react';

interface ProjectCardProps {
  title: string;
  description: string;
  image: string;
}

const ProjectCard: React.FC<ProjectCardProps> = ({ title, description, image }) => {
  const { ref, inView } = useInView<HTMLDivElement>({ threshold: 0.1 });

  return (
    <div className={`project-card slide-in ${inView ? 'visible' : ''}`} ref={ref}>
      <a href="#" className="block relative overflow-hidden rounded-lg">
        <div className="absolute top-4 right-4 bg-card/80 backdrop-blur-sm p-3 rounded-full z-10 border border-white/10">
          <ArrowUpRight className="w-5 h-5 text-primary" />
        </div>
        <div className="relative">
          <div className="absolute inset-0 bg-gradient-to-tr from-black/90 via-transparent to-transparent z-10"></div>
          <img 
            src={image}
            alt={`${title} Project`}
            className="w-full h-80 object-cover"
          />
        </div>
        <div className="absolute bottom-0 left-0 right-0 z-20 p-6">
          <h3 className="text-white text-2xl font-bold">{title}</h3>
        </div>
      </a>
      <div className="mt-6 p-4">
        <p className="text-lg text-muted-foreground">{description}</p>
        <div className="mt-6 flex space-x-4">
          <a href="#" className="btn-primary">Preview</a>
          <a href="#" className="btn-secondary">Details</a>
        </div>
      </div>
    </div>
  );
};

export default ProjectCard;
