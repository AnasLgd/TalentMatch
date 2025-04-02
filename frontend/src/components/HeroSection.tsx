
import React, { useEffect } from 'react';

const HeroSection: React.FC = () => {
  useEffect(() => {
    // Reveal all image elements initially
    const imageElements = document.querySelectorAll('.image-reveal');
    setTimeout(() => {
      imageElements.forEach(el => el.classList.add('reveal'));
    }, 300);

    // Character animation for hero text
    const wordElements = document.querySelectorAll('.word');
    wordElements.forEach(word => {
      word.addEventListener('mouseenter', () => {
        const chars = word.querySelectorAll('.char');
        chars.forEach((char, index) => {
          (char as HTMLElement).style.transitionDelay = `${index * 0.03}s`;
        });
      });
      
      word.addEventListener('mouseleave', () => {
        const chars = word.querySelectorAll('.char');
        chars.forEach(char => {
          (char as HTMLElement).style.transitionDelay = '0s';
        });
      });
    });
  }, []);

  return (
    <section className="scroll-section pt-32 pb-16 relative">
      <div className="container mx-auto px-8">
        <div className="flex flex-col items-center justify-center min-h-screen">
          <h1 className="hero-text text-center mb-16">
            <div className="word">
              <span className="char">S</span>
              <span className="char">P</span>
              <span className="char">A</span>
              <span className="char">R</span>
              <span className="char">K</span>
            </div>
            <div className="word">
              <span className="char">I</span>
              <span className="char">D</span>
              <span className="char">E</span>
              <span className="char">A</span>
              <span className="char">S</span>
              <span className="char">,</span>
            </div>
            <div className="word mt-4">
              <span className="char">M</span>
              <span className="char">A</span>
              <span className="char">G</span>
              <span className="char">N</span>
              <span className="char">I</span>
              <span className="char">F</span>
              <span className="char">Y</span>
            </div>
            <div className="word mt-4">
              <span className="char">I</span>
              <span className="char">M</span>
              <span className="char">P</span>
              <span className="char">A</span>
              <span className="char">C</span>
              <span className="char">T</span>
            </div>
          </h1>

          <div className="relative mt-8 mb-24">
            <div className="absolute -left-16 top-0 bg-[#a5e9b3] w-48 h-48 rounded-full opacity-70 image-reveal"></div>
            <img
              src="https://images.unsplash.com/photo-1551434678-e076c223a692?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80"
              alt="Mobile experience"
              className="hero-image rounded-md w-72 h-auto z-10 relative object-cover shadow-xl image-reveal"
            />
            <div className="absolute -right-16 -bottom-16 bg-[#93e9be] w-36 h-36 rounded-full opacity-80 image-reveal"></div>
          </div>

          <div className="text-center mt-8">
            <p className="subtitle mb-6">
              Scroll down to begin your<br />creative journey.
            </p>
            <div className="bounce">
              <svg width="24" height="40" viewBox="0 0 24 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="1" y="1" width="22" height="38" rx="11" stroke="currentColor" strokeWidth="2" />
                <circle cx="12" cy="12" r="4" fill="currentColor" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <div className="absolute left-8 top-1/2 transform -translate-y-1/2 z-10 hidden lg:block">
        <div className="vertical-text text-gray-300 text-xl tracking-widest font-light">
          CREATIVITY
        </div>
      </div>

      <div className="absolute right-8 top-1/2 transform -translate-y-1/2 z-10 hidden lg:block">
        <div className="vertical-text text-gray-300 text-xl tracking-widest font-light">
          INNOVATION
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
