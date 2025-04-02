
import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";

const Navbar = () => {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      const isScrolled = window.scrollY > 100;
      if (isScrolled !== scrolled) {
        setScrolled(isScrolled);
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, [scrolled]);

  return (
    <nav
      className={cn(
        "fixed top-0 w-full z-50 py-6 px-8 flex justify-between items-center transition-all duration-300",
        scrolled ? "nav-scrolled" : "bg-transparent"
      )}
    >
      <a href="#" className="font-bold text-2xl">
        Crea<span className="text-primary">Vibe</span>
      </a>
      <div className="hidden md:flex space-x-10">
        <a href="#about" className="hover:text-primary transition-colors duration-300 relative after:content-[''] after:absolute after:left-0 after:bottom-0 after:h-[2px] after:w-0 after:bg-primary after:transition-all after:duration-300 hover:after:w-full">
          About
        </a>
        <a href="#projects" className="hover:text-primary transition-colors duration-300 relative after:content-[''] after:absolute after:left-0 after:bottom-0 after:h-[2px] after:w-0 after:bg-primary after:transition-all after:duration-300 hover:after:w-full">
          Projects
        </a>
        <a href="#awards" className="hover:text-primary transition-colors duration-300 relative after:content-[''] after:absolute after:left-0 after:bottom-0 after:h-[2px] after:w-0 after:bg-primary after:transition-all after:duration-300 hover:after:w-full">
          Awards
        </a>
        <a href="#contact" className="hover:text-primary transition-colors duration-300 relative after:content-[''] after:absolute after:left-0 after:bottom-0 after:h-[2px] after:w-0 after:bg-primary after:transition-all after:duration-300 hover:after:w-full">
          Contact
        </a>
      </div>
      <button className="md:hidden text-foreground">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <line x1="4" x2="20" y1="12" y2="12" />
          <line x1="4" x2="20" y1="6" y2="6" />
          <line x1="4" x2="20" y1="18" y2="18" />
        </svg>
      </button>
    </nav>
  );
};

export default Navbar;
