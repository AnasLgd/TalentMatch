
import React from 'react';
import { useInView } from '../hooks/useInView';

const AboutSection: React.FC = () => {
  const { ref: titleRef, inView: titleInView } = useInView<HTMLHeadingElement>({ threshold: 0.1 });
  const { ref: contentRef, inView: contentInView } = useInView<HTMLDivElement>({ threshold: 0.1 });
  const { ref: imageRef, inView: imageInView } = useInView<HTMLDivElement>({ threshold: 0.1 });

  return (
    <section id="about" className="scroll-section bg-white py-32">
      <div className="container mx-auto px-8">
        <div className="max-w-4xl mx-auto">
          <h2 className={`text-4xl font-bold mb-16 slide-in ${titleInView ? 'visible' : ''}`} ref={titleRef}>
            About CreaVibe
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-16">
            <div className={`slide-in ${contentInView ? 'visible' : ''}`} ref={contentRef}>
              <p className="text-lg mb-6">
                At CreaVibe, we're passionate about creating websites that captivate and engage users like never before.
              </p>
              <p className="text-lg mb-6">
                We specialize in Scroll Animation, crafting websites that bring visual intrigue and interactivity, making each site more dynamic and unforgettable.
              </p>
              <p className="text-lg">
                Our team combines creative design with technical excellence to deliver digital experiences that truly stand out.
              </p>
            </div>
            <div className={`relative slide-in ${imageInView ? 'visible' : ''}`} ref={imageRef}>
              <div className="absolute -left-6 -top-6 bg-green-200 w-full h-full rounded-md"></div>
              <img
                src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1171&q=80"
                alt="Our team"
                className="rounded-md w-full h-auto z-10 relative object-cover shadow-md"
              />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AboutSection;
