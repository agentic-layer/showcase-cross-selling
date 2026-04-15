
import React from 'react';
import { Phone } from 'lucide-react';

const Header = () => {
  return (
    <header className="sticky top-0 z-50 w-full bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 border-b border-border">
      <div className="container mx-auto px-6 h-16 flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center">
          <img
            src="/lovable-uploads/0255c12a-3d19-4910-9df5-d730b57d704f.png"
            alt="QAware Logo"
            className="h-8 w-8"
          />
          <span className="ml-2 font-semibold text-lg">Claims Agent</span>
        </div>

        {/* Navigation */}
        <nav className="hidden md:flex space-x-8">
          <a href="#showcase" className="text-foreground hover:text-accent transition-colors">
            Showcase
          </a>
          <a href="#technologie" className="text-foreground hover:text-accent transition-colors">
            Technologie
          </a>
          <a href="#kontakt" className="text-foreground hover:text-accent transition-colors">
            Kontakt
          </a>
        </nav>
      </div>
    </header>
  );
};

export default Header;
