'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';
import { JsonViewer } from '@/components/shared/json-viewer';
import { useToast } from '@/components/shared/toast';
import { Loader2, Play } from 'lucide-react';

export function TracingPanel() {
  const queryClient = useQueryClient();
  const { addToast } = useToast();

  const { data, isLoading } = useQuery<{ cross_pack?: Array<{ id?: string; trace?: string }> }>({
    queryKey: ['metrics', 'tracing'],
    queryFn: () => apiClient.get('/api/v1/metrics'),
  });

  const traceMutation = useMutation({
    mutationFn: () => apiClient.get('/api/v1/metrics'),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['metrics', 'tracing'] });
      addToast('success', 'Trace refreshed');
    },
    onError: () => addToast('error', 'Trace failed'),
  });

  const traces = data?.cross_pack ?? [];

  return (
    <div className="mt-4 space-y-3">
      <div className="flex items-center justify-between">
        <p className="text-xs text-text-secondary">Cross-pack traces and correlation IDs.</p>
        <button
          onClick={() => traceMutation.mutate()}
          disabled={traceMutation.isPending}
          className="flex items-center gap-2 rounded-md bg-primary px-3 py-1.5 text-xs text-white hover:bg-primary-hover disabled:opacity-70"
        >
          {traceMutation.isPending && <Loader2 size={14} className="animate-spin" />}
          <Play size={14} />
          Run Trace
        </button>
      </div>
      {isLoading ? <LoadingSkeleton className="h-48 w-full" /> : <JsonViewer data={traces} />}
    </div>
  );
}
