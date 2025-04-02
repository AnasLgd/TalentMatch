
import React from 'react';
import { useInView } from '../hooks/useInView';

const CtaSection: React.FC = () => {
  const { ref: titleRef, inView: titleInView } = useInView<HTMLHeadingElement>({ threshold: 0.1 });
  const { ref: textRef, inView: textInView } = useInView<HTMLParagraphElement>({ threshold: 0.1 });
  const { ref: buttonRef, inView: buttonInView } = useInView<HTMLAnchorElement>({ threshold: 0.1 });

  return (
    <section className="py-24 bg-card dash-gradient">
      <div className="container mx-auto px-8">
        <div className="max-w-4xl mx-auto text-center glass-effect p-10 rounded-2xl glow-accent">
          <h2 
            className={`h2 mb-6 slide-in ${titleInView ? 'visible' : ''} text-white`}
            ref={titleRef}
          >
            Ready to transform your digital presence?
          </h2>
          <p 
            className={`subtitle mb-10 slide-in ${textInView ? 'visible' : ''} text-muted-foreground`}
            ref={textRef}
          >
            Let us help you create a website that captivates your audience with immersive scroll experiences.
          </p>
          <a 
            href="#contact" 
            className={`btn-accent slide-in ${buttonInView ? 'visible' : ''}`}
            ref={buttonRef}
          >
            Get in Touch
          </a>
        </div>
      </div>
    </section>
  );
};

export default CtaSection;
