'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { MetricsCard } from '@/components/shared/metrics-card';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';
import { StatusBadge } from '@/components/shared/status-badge';
import { useToast } from '@/components/shared/toast';
import { Loader2, Play } from 'lucide-react';

export function GovernanceStatusPanel() {
  const queryClient = useQueryClient();
  const { addToast } = useToast();

  const { data, isLoading } = useQuery<{ total_packs?: number; registered_packs?: number; approved_packs?: number }>({
    queryKey: ['governance', 'status'],
    queryFn: () => apiClient.get('/api/v1/packs'),
  });

  const checkMutation = useMutation({
    mutationFn: () => apiClient.get('/api/v1/packs'),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['governance', 'status'] });
      addToast('success', 'Governance check completed');
    },
    onError: () => addToast('error', 'Governance check failed'),
  });

  return (
    <div className="mt-4 space-y-3">
      <div className="flex items-center justify-between">
        <div className="grid gap-4 md:grid-cols-3 flex-1">
          <MetricsCard title="Total Packs" value={data?.total_packs ?? '-'} />
          <MetricsCard title="Registered Packs" value={data?.registered_packs ?? '-'} />
          <MetricsCard title="Approved Packs" value={data?.approved_packs ?? '-'} />
        </div>
        <button
          onClick={() => checkMutation.mutate()}
          disabled={checkMutation.isPending}
          className="ml-4 flex items-center gap-2 rounded-md bg-primary px-3 py-1.5 text-xs text-white hover:bg-primary-hover disabled:opacity-70"
        >
          {checkMutation.isPending && <Loader2 size={14} className="animate-spin" />}
          <Play size={14} />
          Run Governance Check
        </button>
      </div>
    </div>
  );
}
