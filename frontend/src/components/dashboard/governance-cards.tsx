'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { MetricsCard } from '@/components/shared/metrics-card';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';
import { apiClient } from '@/lib/api-client';
import { useToast } from '@/components/shared/toast';
import { Loader2, RefreshCw } from 'lucide-react';

export function GovernanceCards() {
  const queryClient = useQueryClient();
  const { addToast } = useToast();

  const { data, isLoading } = useQuery({
    queryKey: ['metrics'],
    queryFn: () => apiClient.get('/api/v1/metrics'),
  });

  const refreshMutation = useMutation({
    mutationFn: () => apiClient.get('/api/v1/metrics'),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['metrics'] });
      addToast('success', 'Metrics refreshed');
    },
    onError: () => addToast('error', 'Failed to refresh metrics'),
  });

  return (
    <section className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <MetricsCard title="Acceptance Rate" value={isLoading ? '-' : '87.5%'} change="+2.1% from last week" trend="up" />
      <MetricsCard title="Remediation Success" value={isLoading ? '-' : '92%'} change="+1.4%" trend="up" />
      <MetricsCard title="Compliance Coverage" value={isLoading ? '-' : '92%'} change="+0.8%" trend="up" />
      <div className="flex items-center justify-between rounded-lg border border-border bg-surface-secondary p-4">
        <div>
          <p className="text-xs text-text-secondary">Avg Response Time</p>
          <p className="text-lg font-semibold">{isLoading ? '-' : '340ms'}</p>
          <p className="text-xs text-text-secondary">-12ms</p>
        </div>
        <button
          onClick={() => refreshMutation.mutate()}
          disabled={refreshMutation.isPending}
          className="rounded-md p-2 hover:bg-surface-hover disabled:opacity-70"
        >
          {refreshMutation.isPending ? <Loader2 size={16} className="animate-spin" /> : <RefreshCw size={16} />}
        </button>
      </div>
    </section>
  );
}
