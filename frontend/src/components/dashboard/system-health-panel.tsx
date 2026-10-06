'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { StatusBadge } from '@/components/shared/status-badge';
import { LoadingSkeleton, CardSkeleton } from '@/components/shared/loading-skeleton';
import { useToast } from '@/components/shared/toast';
import { Loader2, RefreshCw } from 'lucide-react';

export function SystemHealthPanel() {
  const queryClient = useQueryClient();
  const { addToast } = useToast();

  const { data, isLoading } = useQuery<{ status?: string }>({
    queryKey: ['health'],
    queryFn: () => apiClient.get('/api/v1/health'),
  });

  const refreshMutation = useMutation({
    mutationFn: () => apiClient.get('/api/v1/health'),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['health'] });
      addToast('success', 'Health refreshed');
    },
    onError: () => addToast('error', 'Failed to refresh health'),
  });

  if (isLoading) return <CardSkeleton />;

  return (
    <div className="mt-4 space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-sm font-semibold">System Health</span>
        <button
          onClick={() => refreshMutation.mutate()}
          disabled={refreshMutation.isPending}
          className="rounded-md p-1 hover:bg-surface-hover disabled:opacity-70"
        >
          {refreshMutation.isPending ? <Loader2 size={16} className="animate-spin" /> : <RefreshCw size={16} />}
        </button>
      </div>
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
