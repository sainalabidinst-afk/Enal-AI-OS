'use client';

import { StatusBadge } from '@/components/shared/status-badge';
import { ArrowRight } from 'lucide-react';

interface PackCardProps {
  id: string;
  name: string;
  description?: string;
  category?: string;
  onSelect: () => void;
}

export function PackCard({ id, name, description, category, onSelect }: PackCardProps) {
  return (
    <button
      type="button"
      onClick={onSelect}
      className="w-full rounded-lg border border-border bg-surface-secondary p-4 text-left"
    >
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold">{name}</h3>
        <StatusBadge status="success" label={category ?? 'pack'} />
      </div>
      <p className="mt-2 text-xs text-text-secondary">{description}</p>
      <p className="mt-3 text-xs font-mono text-text-muted">{id}</p>
      <span className="mt-3 flex items-center gap-2 text-xs text-primary">
        Open pack
        <ArrowRight size={14} />
      </span>
    </button>
  );
}
