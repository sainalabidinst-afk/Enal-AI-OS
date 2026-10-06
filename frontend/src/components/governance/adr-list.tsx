'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { StatusBadge } from '@/components/shared/status-badge';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';
import { useToast } from '@/components/shared/toast';
import { Loader2, Play } from 'lucide-react';

export function ADRList() {
  const queryClient = useQueryClient();
  const { addToast } = useToast();

  const { data, isLoading } = useQuery<Array<{ id: string; title: string; status: string }>>({
    queryKey: ['governance', 'adr'],
    queryFn: () => apiClient.get('/api/v1/packs'),
  });

  const evaluateMutation = useMutation({
    mutationFn: () => apiClient.get('/api/v1/packs'),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['governance', 'adr'] });
      addToast('success', 'ADR list refreshed');
    },
    onError: () => addToast('error', 'Failed to refresh ADR list'),
  });

  const adrs = data ?? [];

  return (
    <div className="mt-4 space-y-2">
      <div className="flex justify-end">
        <button
          onClick={() => evaluateMutation.mutate()}
          disabled={evaluateMutation.isPending}
          className="flex items-center gap-2 rounded-md bg-primary px-3 py-1.5 text-xs text-white hover:bg-primary-hover disabled:opacity-70"
        >
          {evaluateMutation.isPending && <Loader2 size={14} className="animate-spin" />}
          <Play size={14} />
          Run ADR Check
        </button>
      </div>
      {!adrs.length ? (
        <div className="rounded-md border border-dashed border-border px-4 py-6 text-center text-xs text-text-muted">
          No ADR entries found.
        </div>
      ) : (
        adrs.map((adr: { id: string; title: string; status: string }) => (
          <div key={adr.id} className="flex items-center justify-between rounded-md border border-border px-3 py-2">
            <div>
              <p className="text-sm font-medium">{adr.title}</p>
              <p className="text-xs text-text-muted">{adr.id}</p>
            </div>
            <StatusBadge status="info" label={adr.status} />
          </div>
        ))
      )}
    </div>
  );
}
