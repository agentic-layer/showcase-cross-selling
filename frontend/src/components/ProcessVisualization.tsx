
import React from 'react';

const ProcessVisualization = () => {
  return (
    <section id="technologie" className="py-20 px-6 bg-muted/20">
      <div className="container mx-auto max-w-6xl text-center">
        <h2 className="text-4xl font-bold mb-8 text-foreground">
          Agentenkommunikation
        </h2>

        <div className="w-full min-h-[600px] rounded-lg bg-card border p-8 flex items-center justify-center">
          <div className="relative w-full max-w-4xl h-96">
            {/* Host Agent - Top Center */}
            <div className="absolute top-8 left-1/2 transform -translate-x-1/2 z-10">
              <div className="bg-primary text-primary-foreground rounded-lg p-6 shadow-lg min-w-[180px] text-center">
                <h3 className="font-semibold text-lg mb-2">Host Agent</h3>
                <p className="text-sm opacity-90">Zentrale Steuerung</p>
              </div>
            </div>

            {/* Cross Selling Agent - Bottom Left */}
            <div className="absolute bottom-8 left-8">
              <div className="bg-accent text-accent-foreground rounded-lg p-6 shadow-lg min-w-[180px] text-center">
                <h3 className="font-semibold text-lg mb-2">Cross Selling Agent</h3>
                <p className="text-sm opacity-90">Produktempfehlungen</p>
              </div>
            </div>

            {/* Communications Agent - Bottom Right */}
            <div className="absolute bottom-8 right-8">
              <div className="bg-accent text-accent-foreground rounded-lg p-6 shadow-lg min-w-[180px] text-center">
                <h3 className="font-semibold text-lg mb-2">Communications Agent</h3>
                <p className="text-sm opacity-90">Kundenkommunikation</p>
              </div>
            </div>

            {/* Connection Lines using SVG */}
            <svg className="absolute inset-0 w-full h-full pointer-events-none" style={{ zIndex: 1 }}>
              {/* Line from Host Agent to Cross Selling Agent */}
              <line
                x1="50%"
                y1="110px"
                x2="25%"
                y2="240px"
                stroke="hsl(var(--border))"
                strokeWidth="2"
                markerEnd="url(#arrowhead)"
              />
              {/* Line from Host Agent to Communications Agent */}
              <line
                x1="50%"
                y1="110px"
                x2="75%"
                y2="240px"
                stroke="hsl(var(--border))"
                strokeWidth="2"
                markerEnd="url(#arrowhead)"
              />

              {/* Arrow marker definition */}
              <defs>
                <marker
                  id="arrowhead"
                  markerWidth="10"
                  markerHeight="7"
                  refX="9"
                  refY="3.5"
                  orient="auto"
                >
                  <polygon
                    points="0 0, 10 3.5, 0 7"
                    fill="hsl(var(--border))"
                  />
                </marker>
              </defs>
            </svg>

            {/* Communication Labels */}
            <div className="absolute top-40 left-[calc(25%)] text-xs text-muted-foreground text-center">
              Produktdaten<br/>& Empfehlungen
            </div>
            <div className="absolute top-40 right-[calc(25%)] text-xs text-muted-foreground text-center">
              Kundeninteraktion<br/>& Feedback
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ProcessVisualization;
