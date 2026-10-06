'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { MetricsCard } from '@/components/shared/metrics-card';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';
import { StatusBadge } from '@/components/shared/status-badge';

export function GovernanceStatusPanel() {
  const { data, isLoading } = useQuery<{ total_packs?: number; registered_packs?: number; approved_packs?: number }>({
    queryKey: ['governance', 'status'],
    queryFn: () => apiClient.get('/api/v1/governance/status'),
  });

  if (isLoading) return <LoadingSkeleton className="mt-4 h-64 w-full" />;

  return (
    <div className="mt-4 grid gap-4 md:grid-cols-3">
      <MetricsCard title="Total Packs" value={data?.total_packs ?? '-'} />
      <MetricsCard title="Registered Packs" value={data?.registered_packs ?? '-'} />
      <MetricsCard title="Approved Packs" value={data?.approved_packs ?? '-'} />
    </div>
  );
}
