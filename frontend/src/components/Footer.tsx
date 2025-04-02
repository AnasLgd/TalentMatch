
import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="py-12 bg-black text-white">
      <div className="container mx-auto px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <a href="#" className="font-bold text-2xl">Crea<span className="text-primary">Vibe</span></a>
            <p className="mt-4">Creating captivating digital experiences through innovative scroll animations.</p>
          </div>
          <div>
            <h3 className="text-lg font-bold mb-4">Navigation</h3>
            <ul className="space-y-2">
              <li><a href="#" className="hover:text-primary transition-colors">Home</a></li>
              <li><a href="#about" className="hover:text-primary transition-colors">About</a></li>
              <li><a href="#projects" className="hover:text-primary transition-colors">Projects</a></li>
              <li><a href="#contact" className="hover:text-primary transition-colors">Contact</a></li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-bold mb-4">Projects</h3>
            <ul className="space-y-2">
              <li><a href="#" className="hover:text-primary transition-colors">Handee</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Linel</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Centim</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Inkenious</a></li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-bold mb-4">Legal</h3>
            <ul className="space-y-2">
              <li><a href="#" className="hover:text-primary transition-colors">Privacy Policy</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Terms of Service</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Cookie Policy</a></li>
            </ul>
          </div>
        </div>
        <div className="border-t border-gray-800 mt-12 pt-8 text-center">
          <p>&copy; {new Date().getFullYear()} CreaVibe. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
