'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { StatusBadge } from '@/components/shared/status-badge';

interface RegimeBadgeProps {
  symbol?: string;
}

export function RegimeBadge({ symbol = 'BTCUSDT' }: RegimeBadgeProps) {
  const { data, isLoading } = useQuery({
    queryKey: ['trading', 'regime', symbol],
    queryFn: () => apiClient.get('/api/v1/trading/regime/live', { params: { symbol } }),
  });

  if (isLoading) return <div className="mt-4 animate-pulse rounded-md bg-surface-tertiary h-8 w-32" />;

  const regime = data?.data?.regime?.regime ?? 'Unknown';
  const confidence = data?.data?.regime?.confidence ?? '-';

  return (
    <div className="mt-4 space-y-2">
      <StatusBadge status="info" label={regime} />
      <p className="text-xs text-text-secondary">Confidence: {typeof confidence === 'number' ? `${Math.round(confidence * 100)}%` : confidence}</p>
    </div>
  );
}
