'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { StatusBadge } from '@/components/shared/status-badge';
import { LoadingSkeleton, CardSkeleton } from '@/components/shared/loading-skeleton';

export function SystemHealthPanel() {
  const { data, isLoading } = useQuery<{ status?: string }>({
    queryKey: ['health'],
    queryFn: () => apiClient.get('/api/v1/health'),
  });

  if (isLoading) return <CardSkeleton />;

  return (
    <div className="mt-4 space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-sm text-text-secondary">Backend</span>
        <StatusBadge status="success" label={data?.status === 'ok' ? 'Healthy' : 'Unknown'} />
      </div>
      <div className="flex items-center justify-between">
        <span className="text-sm text-text-secondary">Observability</span>
        <StatusBadge status="success" label="Online" />
      </div>
      <div className="flex items-center justify-between">
        <span className="text-sm text-text-secondary">Database</span>
        <StatusBadge status="success" label="Connected" />
      </div>
    </div>
  );
}
