'use client';

import { StatusBadge } from '@/components/shared/status-badge';

interface ProviderStatusBadgeProps {
  status?: string;
}

export function ProviderStatusBadge({ status }: ProviderStatusBadgeProps) {
  const statusKey = status === 'ok' ? 'success' : status === 'degraded' ? 'warning' : 'danger';
  return <StatusBadge status={statusKey} label={status ?? 'unknown'} />;
}
