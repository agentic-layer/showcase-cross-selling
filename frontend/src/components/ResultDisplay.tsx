import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { CheckCircle } from 'lucide-react';
import { useClaims } from './ClaimsProvider';
import ClaimSelector from './ClaimSelector';

const ResultDisplay = () => {
  const { selectedClaimData, isLoading } = useClaims();

  const displayData = selectedClaimData ? [
    { label: 'Kunde', value: selectedClaimData.kunde },
    { label: 'Geburtsdatum', value: selectedClaimData.geburtsdatum },
    { label: 'Kundennummer', value: selectedClaimData.kundennummer },
    { label: 'KFZ Kennzeichen', value: selectedClaimData.kfzKennzeichen },
    { label: 'Unfallzeit', value: selectedClaimData.unfallzeit },
    { label: 'Unfallort', value: selectedClaimData.unfallort },
    { label: 'Fahrer zum Unfallzeitpunkt', value: selectedClaimData.fahrer },
    { label: 'Personenschaden', value: selectedClaimData.personenschaden },
    { label: 'Schadenmeldung', value: selectedClaimData.schadenmeldung },
    { label: 'Schadennummer', value: selectedClaimData.schadennummer },
    { label: 'Sentiment', value: selectedClaimData.sentiment },
    { label: 'Zusammenfassung', value: selectedClaimData.zusammenfassung },
    { label: 'Schaden', value: selectedClaimData.schaden },
  ] : [];

  return (
    <section className="py-20 px-6">
      <div className="container mx-auto max-w-6xl">
        <h2 className="text-4xl font-bold mb-12 text-center text-foreground">
          Ergebnis der Schadenmeldung
        </h2>

        {/* Claim Selector */}
        <div className="flex justify-center mb-8">
          <ClaimSelector />
        </div>

        <div className="grid md:grid-cols-2 gap-12 items-start">
          {/* Left Column */}
          <div className="space-y-6">
            <h3 className="text-2xl font-semibold text-foreground mb-4">
              Strukturierte Schadenakte
            </h3>
            <p className="text-muted-foreground text-lg leading-relaxed">
              Hier sehen Sie, wie die vom Agenten erfassten Daten strukturiert, angereichert und in einer Datenbank oder einem CRM gespeichert werden.
            </p>
            <div className="flex items-center space-x-2 text-accent">
              <CheckCircle className="w-5 h-5" />
              <span className="font-medium">Automatische Datenextraktion</span>
            </div>
            <div className="flex items-center space-x-2 text-accent">
              <CheckCircle className="w-5 h-5" />
              <span className="font-medium">Strukturierte Speicherung</span>
            </div>
            <div className="flex items-center space-x-2 text-accent">
              <CheckCircle className="w-5 h-5" />
              <span className="font-medium">Sofortige Weiterleitung</span>
            </div>
          </div>

          {/* Right Column */}
          <Card className="bg-card border-accent/30">
            <CardHeader>
              <CardTitle className="text-xl text-foreground flex items-center">
                <CheckCircle className="w-5 h-5 text-accent mr-2" />
                Erfasste Schadendaten
              </CardTitle>
            </CardHeader>
            <CardContent>
              {isLoading ? (
                <div className="text-center py-8">
                  <p className="text-muted-foreground">Lade Schadendaten...</p>
                </div>
              ) : displayData.length > 0 ? (
                <div className="space-y-4">
                  {displayData.map((item, index) => (
                    <div key={index} className="flex justify-between items-center py-2 border-b border-border/50 last:border-b-0">
                      <span className="text-muted-foreground font-medium">{item.label}:</span>
                      <span className="font-semibold text-right max-w-xs text-foreground">
                        {item.value}
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8">
                  <p className="text-muted-foreground">Keine Schadendaten verfügbar</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
};

export default ResultDisplay;
