
import React from 'react';

const ProcessVisualization = () => {
  return (
    <section id="technologie" className="py-20 px-6 bg-muted/20">
      <div className="container mx-auto max-w-6xl text-center">
        <h2 className="text-4xl font-bold mb-8 text-foreground">
          Agentenkommunikation
        </h2>

        <div className="w-full min-h-[750px] rounded-lg bg-card border p-8 flex items-center justify-center">
          <div className="relative w-full max-w-4xl h-[550px]">
            {/* Host Agent - Top Center */}
            <div className="absolute top-8 left-1/2 transform -translate-x-1/2 z-10">
              <div className="bg-primary text-primary-foreground rounded-lg p-6 shadow-lg min-w-[180px] text-center">
                <h3 className="font-semibold text-lg mb-2">Host Agent</h3>
                <p className="text-sm opacity-90">Zentrale Steuerung</p>
              </div>
            </div>

            {/* Cross Selling Agent - Middle Left */}
            <div className="absolute top-[200px] left-8 z-10">
              <div className="bg-accent text-accent-foreground rounded-lg p-6 shadow-lg min-w-[180px] text-center">
                <h3 className="font-semibold text-lg mb-2">Cross Selling Agent</h3>
                <p className="text-sm opacity-90">Produktempfehlungen</p>
              </div>
            </div>

            {/* Communications Agent - Middle Right */}
            <div className="absolute top-[200px] right-8 z-10">
              <div className="bg-accent text-accent-foreground rounded-lg p-6 shadow-lg min-w-[180px] text-center">
                <h3 className="font-semibold text-lg mb-2">Communications Agent</h3>
                <p className="text-sm opacity-90">Kundenkommunikation</p>
              </div>
            </div>

            {/* Product DB MCP Server - Bottom Left */}
            <div className="absolute top-[420px] left-8 z-10">
              <div className="bg-muted text-muted-foreground rounded-lg p-6 shadow-lg min-w-[180px] text-center border-2 border-dashed border-border">
                <h3 className="font-semibold text-lg mb-2">Product DB</h3>
                <p className="text-sm opacity-90">MCP Server</p>
              </div>
            </div>

            {/* Customer CRM MCP Server - Bottom Center */}
            <div className="absolute top-[420px] left-1/2 transform -translate-x-1/2 z-10">
              <div className="bg-muted text-muted-foreground rounded-lg p-6 shadow-lg min-w-[180px] text-center border-2 border-dashed border-border">
                <h3 className="font-semibold text-lg mb-2">Customer CRM</h3>
                <p className="text-sm opacity-90">MCP Server</p>
              </div>
            </div>

            {/* Connection Lines using SVG */}
            <svg className="absolute inset-0 w-full h-full pointer-events-none" style={{ zIndex: 1 }}>
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
                <marker
                  id="arrowhead-dashed"
                  markerWidth="10"
                  markerHeight="7"
                  refX="9"
                  refY="3.5"
                  orient="auto"
                >
                  <polygon
                    points="0 0, 10 3.5, 0 7"
                    fill="hsl(var(--muted-foreground))"
                  />
                </marker>
              </defs>

              {/* Line from Host Agent to Cross Selling Agent */}
              <line
                x1="50%"
                y1="128px"
                x2="14%"
                y2="200px"
                stroke="hsl(var(--border))"
                strokeWidth="2"
                markerEnd="url(#arrowhead)"
              />
              {/* Line from Host Agent to Communications Agent */}
              <line
                x1="50%"
                y1="128px"
                x2="86%"
                y2="200px"
                stroke="hsl(var(--border))"
                strokeWidth="2"
                markerEnd="url(#arrowhead)"
              />

              {/* Dashed line from Cross Selling Agent to Product DB */}
              <line
                x1="14%"
                y1="296px"
                x2="14%"
                y2="420px"
                stroke="hsl(var(--muted-foreground))"
                strokeWidth="2"
                strokeDasharray="5,5"
                markerEnd="url(#arrowhead-dashed)"
              />
              {/* Dashed line from Cross Selling Agent to Customer CRM */}
              <line
                x1="14%"
                y1="296px"
                x2="50%"
                y2="420px"
                stroke="hsl(var(--muted-foreground))"
                strokeWidth="2"
                strokeDasharray="5,5"
                markerEnd="url(#arrowhead-dashed)"
              />
              {/* Dashed line from Communications Agent to Customer CRM */}
              <line
                x1="86%"
                y1="296px"
                x2="50%"
                y2="420px"
                stroke="hsl(var(--muted-foreground))"
                strokeWidth="2"
                strokeDasharray="5,5"
                markerEnd="url(#arrowhead-dashed)"
              />
            </svg>

            {/* Agent-to-Agent Communication Labels */}
            <div className="absolute top-[155px] left-[32%] -translate-x-1/2 text-xs text-muted-foreground text-center">
              Produktdaten<br/>& Empfehlungen
            </div>
            <div className="absolute top-[155px] left-[68%] -translate-x-1/2 text-xs text-muted-foreground text-center">
              Kundeninteraktion<br/>& Feedback
            </div>

            {/* MCP Connection Labels */}
            <div className="absolute top-[350px] left-[7%] text-xs text-muted-foreground text-center">
              Produktkatalog
            </div>
            <div className="absolute top-[350px] left-[32%] -translate-x-1/2 text-xs text-muted-foreground text-center">
              Kundendaten
            </div>
            <div className="absolute top-[350px] left-[68%] -translate-x-1/2 text-xs text-muted-foreground text-center">
              Nachrichten
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ProcessVisualization;
