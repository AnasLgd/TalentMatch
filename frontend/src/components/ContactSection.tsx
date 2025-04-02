
import React from 'react';
import { useInView } from '../hooks/useInView';
import { Input } from './ui/input';
import { Button } from './ui/button';

const ContactSection: React.FC = () => {
  const { ref: titleRef, inView: titleInView } = useInView<HTMLHeadingElement>({ threshold: 0.1 });
  const { ref: leftColRef, inView: leftColInView } = useInView<HTMLDivElement>({ threshold: 0.1 });
  const { ref: formRef, inView: formInView } = useInView<HTMLDivElement>({ threshold: 0.1 });

  return (
    <section id="contact" className="py-32 bg-white">
      <div className="container mx-auto px-8">
        <div className="max-w-4xl mx-auto">
          <h2 
            className={`text-5xl font-bold mb-16 slide-in ${titleInView ? 'visible' : ''}`}
            ref={titleRef}
          >
            Let's Connect
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-16">
            <div 
              className={`slide-in ${leftColInView ? 'visible' : ''}`}
              ref={leftColRef}
            >
              <p className="text-lg mb-8">
                We're excited to hear about your project and how we can help bring your vision to life.
              </p>
              <div className="mb-6">
                <h3 className="text-xl font-bold mb-2">Email</h3>
                <p className="text-lg">hello@creavibe.com</p>
              </div>
              <div className="mb-6">
                <h3 className="text-xl font-bold mb-2">Phone</h3>
                <p className="text-lg">+1 (234) 567-8901</p>
              </div>
              <div>
                <h3 className="text-xl font-bold mb-2">Follow Us</h3>
                <div className="flex space-x-4">
                  <a href="#" className="text-2xl hover:text-primary transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-instagram"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"></line></svg>
                  </a>
                  <a href="#" className="text-2xl hover:text-primary transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-twitter"><path d="M22 4s-.7 2.1-2 3.4c1.6 10-9.4 17.3-18 11.6 2.2.1 4.4-.6 6-2C3 15.5.5 9.6 3 5c2.2 2.6 5.6 4.1 9 4-.9-4.2 4-6.6 7-3.8 1.1 0 3-1.2 3-1.2z"></path></svg>
                  </a>
                  <a href="#" className="text-2xl hover:text-primary transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-dribbble"><circle cx="12" cy="12" r="10"></circle><path d="M19.13 5.09C15.22 9.14 10 10.44 2.25 10.94"></path><path d="M21.75 12.84c-6.62-1.41-12.14 1-16.38 6.32"></path><path d="M8.56 2.75c4.37 6 6 9.42 8 17.72"></path></svg>
                  </a>
                  <a href="#" className="text-2xl hover:text-primary transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
                      <path d="M2 12h5"></path>
                      <path d="M17 12h5"></path>
                      <path d="M12 2v20"></path>
                    </svg>
                  </a>
                </div>
              </div>
            </div>
            
            <div 
              className={`slide-in ${formInView ? 'visible' : ''}`}
              ref={formRef}
            >
              <form>
                <div className="mb-6">
                  <label htmlFor="name" className="block text-sm font-medium mb-2">Name</label>
                  <Input 
                    type="text" 
                    id="name" 
                    className="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-primary" 
                  />
                </div>
                <div className="mb-6">
                  <label htmlFor="email" className="block text-sm font-medium mb-2">Email</label>
                  <Input 
                    type="email" 
                    id="email" 
                    className="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-primary" 
                  />
                </div>
                <div className="mb-6">
                  <label htmlFor="message" className="block text-sm font-medium mb-2">Message</label>
                  <textarea 
                    id="message" 
                    rows={5} 
                    className="w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary" 
                  />
                </div>
                <Button type="submit" variant="default" className="bg-black text-white hover:bg-gray-800">
                  Send Message
                </Button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ContactSection;
