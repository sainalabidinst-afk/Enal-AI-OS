'use client';

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { StatusBadge } from '@/components/shared/status-badge';
import { ProviderStatusBadge } from './provider-status-badge';
import { useToast } from '@/components/shared/toast';
import { Loader2, Activity, Plug } from 'lucide-react';
import { apiClient } from '@/lib/api-client';

interface ProviderCardProps {
  name: string;
  status?: string;
  models?: string[];
}

export function ProviderCard({ name, status, models }: ProviderCardProps) {
  const queryClient = useQueryClient();
  const { addToast } = useToast();

  const connectMutation = useMutation({
    mutationFn: () => apiClient.post('/api/v1/models/route', { taskType: 'health-check', capability: name }),
    onSuccess: () => addToast('success', 'Provider connected'),
    onError: () => addToast('error', 'Failed to connect provider'),
  });

  const healthMutation = useMutation({
    mutationFn: () => apiClient.get('/api/v1/models/health', { params: { provider: name } }),
    onSuccess: (res) => {
      const latency = (res as { latency_ms?: number } | undefined)?.latency_ms;
      addToast('success', `Latency check completed: ${latency ?? 'n/a'}ms`);
      queryClient.invalidateQueries({ queryKey: ['providers'] });
    },
    onError: () => addToast('error', 'Health check failed'),
  });

  return (
    <div className="rounded-lg border border-border bg-surface-secondary p-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold">{name}</h3>
        <ProviderStatusBadge status={status} />
      </div>
      {models && models.length > 0 && (
        <p className="mt-2 text-xs text-text-secondary">Models: {models.join(', ')}</p>
      )}
      <div className="mt-3 flex gap-2">
        <button
          onClick={() => connectMutation.mutate()}
          disabled={connectMutation.isPending}
          className="flex items-center gap-1 rounded-md border border-border px-2 py-1 text-xs hover:bg-surface-hover disabled:opacity-70"
        >
          {connectMutation.isPending ? <Loader2 size={14} className="animate-spin" /> : <Plug size={14} />}
          Connect
        </button>
        <button
          onClick={() => healthMutation.mutate()}
          disabled={healthMutation.isPending}
          className="flex items-center gap-1 rounded-md border border-border px-2 py-1 text-xs hover:bg-surface-hover disabled:opacity-70"
        >
          {healthMutation.isPending ? <Loader2 size={14} className="animate-spin" /> : <Activity size={14} />}
          Test Latency
        </button>
      </div>
    </div>
  );
}
