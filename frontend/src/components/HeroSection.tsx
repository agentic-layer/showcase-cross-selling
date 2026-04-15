
import React from 'react';

const HeroSection = () => {
  return (
    <section className="py-20 px-6">
      <div className="container mx-auto max-w-4xl text-center">
        <h1 className="text-5xl md:text-6xl font-bold mb-6 text-foreground">
          Cross Selling Agent für Versicherer
        </h1>

        <h2 className="text-2xl md:text-3xl font-medium mb-8 text-accent">
          KI‑gestützter Cross‑Selling‑Agent
        </h2>

        <div className="max-w-3xl mx-auto text-lg leading-relaxed text-muted-foreground space-y-6">
          <p>
            Unser intelligenter Cross‑Selling‑Agent analysiert Kunden‑ und Produktdaten Ihrer Versicherung, um maßgeschneiderte Verkaufschancen zu identifizieren – vollautomatisch, datengestützt und kundenorientiert.
            Durch die Verknüpfung von Kundenprofilen, Vertragshistorie und Produktportfolio erkennt der Agent optimale Cross‑Selling‑Potenziale.
          </p>

          <p>
            Dabei entwickelt er spezifische Cross‑Selling‑Strategien für jeden Kunden basierend auf dessen individueller Situation, Lebensereignissen und bestehenden Versicherungslücken, um die passendsten Produktempfehlungen zu generieren.
          </p>

          <p>
            Nach der Strategieentwicklung formuliert der Agent personalisierte Nachrichten, die direkt an den Kunden versendet werden können. Diese sind auf den jeweiligen Kommunikationsstil und die Präferenzen des Kunden abgestimmt – sodass Ihre Vertriebsprozesse effizienter und erfolgreicher werden.
          </p>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
