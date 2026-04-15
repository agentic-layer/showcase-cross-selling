import React from 'react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Calendar, User } from 'lucide-react';
import { useClaims } from './ClaimsProvider';
import { formatBerlinTime } from '@/lib/dateUtils';

const ClaimSelector = () => {
  const { availableClaims, selectedClaimId, setSelectedClaimId, isLoading } = useClaims();


  if (isLoading) {
    return (
      <div className="w-full max-w-md">
        <div className="h-10 bg-muted animate-pulse rounded-md"></div>
      </div>
    );
  }

  if (availableClaims.length === 0) {
    return (
      <div className="w-full max-w-md">
        <div className="text-sm text-muted-foreground">
          Keine Schäden verfügbar
        </div>
      </div>
    );
  }

  return (
    <div className="w-full max-w-md">
      <label className="text-sm font-medium text-foreground mb-2 block">
        Schaden auswählen
      </label>
      <Select
        value={selectedClaimId || undefined}
        onValueChange={setSelectedClaimId}
      >
        <SelectTrigger className="w-full bg-background border-border h-16 py-3 px-4 text-lg rounded-md">
          <SelectValue placeholder="Schaden auswählen..." />
        </SelectTrigger>
        <SelectContent className="bg-background border-border z-50 max-h-60">
          {availableClaims.map((claim) => (
            <SelectItem
              key={claim.id}
              value={claim.id}
              className="hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground"
            >
              <div className="flex flex-col space-y-1 py-1">
                <div className="flex items-center space-x-2 text-sm font-medium">
                  <User className="w-4 h-4 text-accent" />
                  <span>{claim.first_name} {claim.last_name}</span>
                </div>
                <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                  <Calendar className="w-3 h-3" />
                  <span>{formatBerlinTime(claim.created_at)}</span>
                </div>
                <div className="text-xs text-muted-foreground">
                  Schadennummer: {claim.claim_number}
                </div>
              </div>
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
};

export default ClaimSelector;
