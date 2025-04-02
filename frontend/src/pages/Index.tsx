
import { useEffect } from "react";
import Navbar from "../components/Navbar";
import HeroSection from "../components/HeroSection";
import AboutSection from "../components/AboutSection";
import ProjectsSection from "../components/ProjectsSection";
import CtaSection from "../components/CtaSection";
import ContactSection from "../components/ContactSection";
import Footer from "../components/Footer";
import DynamicCursor from "../components/DynamicCursor";
import ColoredLines from "../components/ColoredLines";
import DecorativeLines from "../components/DecorativeLines";
import SectionConnectors from "../components/SectionConnector";

const Index = () => {
  useEffect(() => {
    // Set up intersection observer for slide-in elements
    const slideObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            slideObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1 }
    );

    // Observe all slide-in elements
    document.querySelectorAll(".slide-in").forEach((el) => {
      slideObserver.observe(el);
    });

    return () => {
      // Clean up the observer when the component unmounts
      document.querySelectorAll(".slide-in").forEach((el) => {
        slideObserver.unobserve(el);
      });
    };
  }, []);

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Lignes décoratives en arrière-plan avec z-index négatifs */}
      <div className="fixed inset-0 z-[-15]">
        <ColoredLines />
      </div>
      <div className="fixed inset-0 z-[-10]">
        <DecorativeLines />
      </div>
      
      <DynamicCursor />
      
      <div className="relative z-1">
        <Navbar />
        <div className="relative">
          <HeroSection />
          <div className="relative">
            <SectionConnectors />
            <AboutSection />
            <ProjectsSection />
            <CtaSection />
            <ContactSection />
            <Footer />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;

