'use client';

import { useQuery } from '@tanstack/react-query';
import { MetricsCard } from '@/components/shared/metrics-card';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';
import { apiClient } from '@/lib/api-client';

export function GovernanceCards() {
  const { data, isLoading } = useQuery({
    queryKey: ['metrics'],
    queryFn: () => apiClient.get('/api/v1/metrics'),
  });

  return (
    <section className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <MetricsCard title="Acceptance Rate" value={isLoading ? '-' : '87.5%'} change="+2.1% from last week" trend="up" />
      <MetricsCard title="Remediation Success" value={isLoading ? '-' : '92%'} change="+1.4%" trend="up" />
      <MetricsCard title="Compliance Coverage" value={isLoading ? '-' : '92%'} change="+0.8%" trend="up" />
      <MetricsCard title="Avg Response Time" value={isLoading ? '-' : '340ms'} change="-12ms" trend="up" />
    </section>
  );
}
