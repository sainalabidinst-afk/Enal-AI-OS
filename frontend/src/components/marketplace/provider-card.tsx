'use client';

import { StatusBadge } from '@/components/shared/status-badge';

interface ProviderCardProps {
  name: string;
  status?: string;
  models?: string[];
}

export function ProviderCard({ name, status, models }: ProviderCardProps) {
  return (
    <div className="rounded-lg border border-border bg-surface-secondary p-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold">{name}</h3>
        <ProviderStatusBadge status={status} />
      </div>
      {models && models.length > 0 && (
        <p className="mt-2 text-xs text-text-secondary">Models: {models.join(', ')}</p>
      )}
    </div>
  );
}
