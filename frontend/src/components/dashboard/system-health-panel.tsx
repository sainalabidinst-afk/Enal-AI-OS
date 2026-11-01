'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { StatusBadge } from '@/components/shared/status-badge';
import { LoadingSkeleton, CardSkeleton } from '@/components/shared/loading-skeleton';
import { useToast } from '@/components/shared/toast';
import { Loader2, RefreshCw } from 'lucide-react';

interface HealthResponse {
  status?: string;
  service?: string;
  version?: string;
}

export function SystemHealthPanel() {
  const queryClient = useQueryClient();
  const { addToast } = useToast();

  const { data, isLoading, isError } = useQuery<HealthResponse>({
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

  const status = isError
    ? 'danger'
    : data?.status === 'ok'
      ? 'success'
      : 'neutral';

  return (
    <div className="mt-4 space-y-3">
      <div className="flex items-center justify-between">
        <div>
          <span className="text-sm font-semibold">API health</span>
          <p className="text-xs text-text-muted">Liveness endpoint</p>
        </div>
        <button
          onClick={() => refreshMutation.mutate()}
          disabled={refreshMutation.isPending}
          className="icon-button rounded-md p-2 disabled:opacity-70"
          aria-label="Refresh API health"
        >
          {refreshMutation.isPending ? <Loader2 size={16} className="animate-spin" /> : <RefreshCw size={16} />}
        </button>
      </div>
      <div className="flex items-center justify-between">
        <span className="text-sm text-text-secondary">{data?.service ?? 'Backend API'}</span>
        <StatusBadge
          status={status}
          label={isError ? 'Unavailable' : data?.status === 'ok' ? 'Healthy' : 'Unknown'}
        />
      </div>
      <div className="flex items-center justify-between">
        <span className="text-sm text-text-secondary">API version</span>
        <span className="font-mono text-xs text-text-muted">{data?.version ?? '—'}</span>
      </div>
      <p className="border-t border-border pt-3 text-xs leading-relaxed text-text-muted">
        Database and model-provider health are not reported by this endpoint.
      </p>
    </div>
  );
}
