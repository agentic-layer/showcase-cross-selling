
import React, { useState, useRef } from 'react';
import { Button } from '@/components/ui/button';
import HeroSection from '@/components/HeroSection';
import ChatInterface, { ChatInterfaceRef } from '@/components/ChatInterface';

import CustomerDataTable from '@/components/CustomerDataTable';
import ProductDataTable from '@/components/ProductDataTable';
import ProcessVisualization from '@/components/ProcessVisualization';
import Footer from '@/components/Footer';

const DashboardPage = () => {
  const [showCustomerData, setShowCustomerData] = useState(false);
  const [showProductData, setShowProductData] = useState(false);
  const chatRef = useRef<ChatInterfaceRef>(null);

  const sendTestMessage = () => {
    if (chatRef.current) {
      chatRef.current.sendMessage('Erstelle eine Cross-Selling Strategie für die Kundin Anna Müller.');
    }
  };

  return (
      <div className="min-h-screen bg-background">
        {/* Add logout button to header */}
        <header className="sticky top-0 z-50 w-full bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 border-b border-border">
          <div className="container mx-auto px-6 h-16 flex items-center justify-between">
            {/* Logo */}
            <div className="flex items-center">
              <img
                src="/lovable-uploads/0255c12a-3d19-4910-9df5-d730b57d704f.png"
                alt="QAware Logo"
                className="h-8 w-8"
              />
              <span className="ml-2 font-semibold text-lg">Cross Selling Agent</span>
            </div>

            {/* Navigation */}
            <div className="flex items-center space-x-4">
              <nav className="hidden md:flex space-x-8">
                <a href="#showcase" className="text-foreground hover:text-accent transition-colors">
                  Showcase
                </a>
                <a href="#technologie" className="text-foreground hover:text-accent transition-colors">
                  Technologie
                </a>
              </nav>
            </div>
          </div>
        </header>

        <main>
          <HeroSection />

          {/* Chat Interface */}
          <section id="showcase" className="py-20 px-6">
            <div className="container mx-auto max-w-4xl">
              <div className="text-center mb-12">
                <h2 className="text-4xl font-bold mb-4 text-foreground">
                  Cross-Selling Agent
                </h2>
                <p className="text-muted-foreground text-lg leading-relaxed max-w-2xl mx-auto">
                  Interagieren Sie mit unserem intelligenten Agent, der Kundendaten analysiert und
                  personalisierte Cross-Selling-Strategien entwickelt.
                </p>
              </div>

              <ChatInterface ref={chatRef} />

              <div className="text-center mt-6">
                <Button
                  variant="outline"
                  onClick={sendTestMessage}
                  className="px-6 py-2"
                >
                  Beispielnachricht
                </Button>
              </div>
            </div>
          </section>

          {/* Toggle Buttons for Data Tables */}
          <div className="container mx-auto px-6 py-6">
            <div className="flex justify-center gap-4">
              <Button
                variant="outline"
                onClick={() => setShowCustomerData(!showCustomerData)}
                className="px-6 py-2"
              >
                {showCustomerData ? 'Kundendaten ausblenden' : 'Kundendaten anzeigen'}
              </Button>
              <Button
                variant="outline"
                onClick={() => setShowProductData(!showProductData)}
                className="px-6 py-2"
              >
                {showProductData ? 'Produktdaten ausblenden' : 'Produktdaten anzeigen'}
              </Button>
            </div>
          </div>

          {/* Customer Data Table */}
          {showCustomerData && (
            <div className="container mx-auto px-6 pb-12">
              <CustomerDataTable />
            </div>
          )}

          {/* Product Data Table */}
          {showProductData && (
            <div className="container mx-auto px-6 pb-12">
              <ProductDataTable />
            </div>
          )}

          <ProcessVisualization />
        </main>
        <Footer />
      </div>
  );
};

export default DashboardPage;
