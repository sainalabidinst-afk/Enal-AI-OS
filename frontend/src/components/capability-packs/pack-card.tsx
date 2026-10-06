'use client';

import { StatusBadge } from '@/components/shared/status-badge';

interface PackCardProps {
  id: string;
  name: string;
  description?: string;
  category?: string;
}

export function PackCard({ id, name, description, category }: PackCardProps) {
  return (
    <div className="rounded-lg border border-border bg-surface-secondary p-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold">{name}</h3>
        <StatusBadge status="success" label={category ?? 'pack'} />
      </div>
      <p className="mt-2 text-xs text-text-secondary">{description}</p>
      <p className="mt-3 text-xs font-mono text-text-muted">{id}</p>
    </div>
  );
}
