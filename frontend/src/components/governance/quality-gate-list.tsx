'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { StatusBadge } from '@/components/shared/status-badge';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';
import { useToast } from '@/components/shared/toast';
import { Loader2, Play } from 'lucide-react';

export function QualityGateList() {
  const queryClient = useQueryClient();
  const { addToast } = useToast();

  const { data, isLoading } = useQuery<Array<{ gate_id: string; pack_id: string; passed: boolean }>>({
    queryKey: ['governance', 'quality-gates'],
    queryFn: () => apiClient.get('/api/v1/packs'),
  });

  const evaluateMutation = useMutation({
    mutationFn: () => apiClient.get('/api/v1/packs'),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['governance', 'quality-gates'] });
      addToast('success', 'Quality gates evaluated');
    },
    onError: () => addToast('error', 'Quality gate evaluation failed'),
  });

  const gates = data ?? [];

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
          Run Quality Gate Check
        </button>
      </div>
      {gates.map((gate: { gate_id: string; pack_id: string; passed: boolean }) => (
        <div key={gate.gate_id} className="flex items-center justify-between rounded-md border border-border px-3 py-2">
          <div>
            <p className="text-sm font-medium">{gate.gate_id}</p>
            <p className="text-xs text-text-muted">Pack: {gate.pack_id}</p>
          </div>
          <StatusBadge status={gate.passed ? 'success' : 'danger'} label={gate.passed ? 'Pass' : 'Fail'} />
        </div>
      ))}
    </div>
  );
}
