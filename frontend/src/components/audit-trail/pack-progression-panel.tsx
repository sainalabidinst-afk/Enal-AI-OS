'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';
import { StatusBadge } from '@/components/shared/status-badge';
import { useToast } from '@/components/shared/toast';
import { Loader2, Play } from 'lucide-react';

interface PackProgressionPanelProps {
  packId: string;
}

export function PackProgressionPanel({ packId }: PackProgressionPanelProps) {
  const queryClient = useQueryClient();
  const { addToast } = useToast();

  const { data, isLoading } = useQuery<{ stages?: Array<{ stage: string; status: string; timestamp?: string; note?: string }> }>({
    queryKey: ['governance', 'packs', packId, 'progression'],
    queryFn: () => apiClient.get(`/api/v1/packs/${packId}`),
    enabled: !!packId,
  });

  const refreshMutation = useMutation({
    mutationFn: () => apiClient.get(`/api/v1/packs/${packId}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['governance', 'packs', packId, 'progression'] });
      addToast('success', 'Pack progression refreshed');
    },
    onError: () => addToast('error', 'Failed to refresh progression'),
  });

  const stages = data?.stages ?? [];

  return (
    <div className="mt-4 space-y-2">
      <div className="flex justify-end">
        <button
          onClick={() => refreshMutation.mutate()}
          disabled={refreshMutation.isPending}
          className="flex items-center gap-2 rounded-md bg-primary px-3 py-1.5 text-xs text-white hover:bg-primary-hover disabled:opacity-70"
        >
          {refreshMutation.isPending && <Loader2 size={14} className="animate-spin" />}
          <Play size={14} />
          Run Pack Progression
        </button>
      </div>
      {stages.map((stage: { stage: string; status: string; timestamp?: string; note?: string }) => (
        <div key={stage.stage} className="flex items-center justify-between rounded-md border border-border px-3 py-2">
          <div>
            <p className="text-sm font-medium">{stage.stage}</p>
            <p className="text-xs text-text-muted">{stage.note}</p>
          </div>
          <div className="text-right">
            <StatusBadge status={stage.status === 'completed' ? 'success' : 'warning'} label={stage.status} />
            <p className="mt-1 text-xs text-text-secondary">{stage.timestamp ? new Date(stage.timestamp).toLocaleString() : '-'}</p>
          </div>
        </div>
      ))}
    </div>
  );
}
