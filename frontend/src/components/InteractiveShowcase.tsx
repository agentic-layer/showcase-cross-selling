
import React, { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Phone, Users } from 'lucide-react';
import { supabase } from '@/integrations/supabase/client';

// TypeScript declaration for the custom element
declare global {
  // eslint-disable-next-line @typescript-eslint/no-namespace
  namespace JSX {
    interface IntrinsicElements {
      'elevenlabs-convai': {
        'agent-id': string;
        variant?: string;
      };
    }
  }
}

interface Customer {
  id: string;
  first_name: string | null;
  last_name: string | null;
  date_of_birth: string | null;
  street: string | null;
  house_number: string | null;
  postal_code: string | null;
  city: string | null;
}

const InteractiveShowcase = () => {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [showCustomers, setShowCustomers] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const fetchCustomers = async () => {
    if (showCustomers) {
      setShowCustomers(false);
      return;
    }

    setIsLoading(true);
    try {
      const { data, error } = await supabase
        .from('customers')
        .select('id, first_name, last_name, date_of_birth, street, house_number, postal_code, city')
        .order('created_at', { ascending: false });

      if (error) {
        console.error('Error fetching customers:', error);
        return;
      }

      setCustomers(data || []);
      setShowCustomers(true);
    } catch (error) {
      console.error('Error fetching customers:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const formatDate = (dateString: string | null) => {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('de-DE', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  return (
    <section id="showcase" className="py-20 px-6 bg-muted/20">
      <div className="container mx-auto max-w-4xl text-center">
        <h2 className="text-4xl font-bold mb-12 text-foreground">
          Schnelle Schadenmeldung zu jeder Zeit
        </h2>

        <Card className="bg-card border-accent/30 shadow-lg">
          <CardContent className="p-12">
            <div className="flex flex-col items-center space-y-6">
              {/* Round phone icon */}
              <div className="w-16 h-16 bg-accent/20 rounded-full flex items-center justify-center">
                <Phone className="w-8 h-8 text-accent" />
              </div>

              <div className="text-center space-y-4">
                <h3 className="text-2xl font-semibold text-foreground">
                  Geben Sie eine Schadenmeldung auf
                </h3>
                <p className="text-muted-foreground max-w-md mx-auto">
                  Sprechen Sie direkt mit unserem KI-gestützten Schadenaufnahme-Agent und geben Sie Ihre Schadenmeldung bequem per Sprache auf.
                </p>
              </div>

              {/* ElevenLabs Conversational AI Widget with full variant */}
              <div className="w-full max-w-md">
                <elevenlabs-convai
                  agent-id="agent_01jzwamqzee4q9qh9m9q5e3x50"
                  variant="full"
                ></elevenlabs-convai>
              </div>

              {/* Customer data button and phone number box */}
              <div className="flex flex-col sm:flex-row items-center gap-4">
                {/* Kundendaten button */}
                <Button
                  onClick={fetchCustomers}
                  disabled={isLoading}
                  className="flex items-center gap-2"
                  variant="outline"
                >
                  <Users className="w-4 h-4" />
                  {isLoading ? 'Lädt...' : showCustomers ? 'Kundendaten ausblenden' : 'Kundendaten'}
                </Button>

                {/* Phone number box */}
                <div className="flex items-center bg-accent/10 border border-accent/30 rounded-lg px-4 py-2">
                  <Phone className="w-4 h-4 mr-2 text-accent" />
                  <span className="text-sm font-medium">089 / 628 28 121</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Customer data table */}
        {showCustomers && (
          <Card className="bg-card border-accent/30 shadow-lg mt-8">
            <CardContent className="p-6">
              <h3 className="text-xl font-semibold text-foreground mb-4 flex items-center">
                <Users className="w-5 h-5 text-accent mr-2" />
                Kundendaten
              </h3>

              {customers.length > 0 ? (
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead className="text-foreground">Vorname</TableHead>
                        <TableHead className="text-foreground">Nachname</TableHead>
                        <TableHead className="text-foreground">Geburtsdatum</TableHead>
                        <TableHead className="text-foreground">Straße</TableHead>
                        <TableHead className="text-foreground">Hausnummer</TableHead>
                        <TableHead className="text-foreground">PLZ</TableHead>
                        <TableHead className="text-foreground">Stadt</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {customers.map((customer) => (
                        <TableRow key={customer.id}>
                          <TableCell className="font-medium">
                            {customer.first_name || '-'}
                          </TableCell>
                          <TableCell>
                            {customer.last_name || '-'}
                          </TableCell>
                          <TableCell>
                            {formatDate(customer.date_of_birth)}
                          </TableCell>
                          <TableCell>
                            {customer.street || '-'}
                          </TableCell>
                          <TableCell>
                            {customer.house_number || '-'}
                          </TableCell>
                          <TableCell>
                            {customer.postal_code || '-'}
                          </TableCell>
                          <TableCell>
                            {customer.city || '-'}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              ) : (
                <div className="text-center py-8">
                  <p className="text-muted-foreground">Keine Kundendaten gefunden.</p>
                </div>
              )}
            </CardContent>
          </Card>
        )}
      </div>
    </section>
  );
};

export default InteractiveShowcase;
