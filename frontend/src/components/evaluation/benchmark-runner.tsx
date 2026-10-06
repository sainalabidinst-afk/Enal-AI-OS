'use client';

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { cn } from '@/lib/cn';
import { useToast } from '@/components/shared/toast';
import { Loader2 } from 'lucide-react';

export function BenchmarkRunner() {
  const queryClient = useQueryClient();
  const { addToast } = useToast();

  const mutation = useMutation({
    mutationFn: () => apiClient.post('/api/v1/benchmark/run'),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['benchmark'] });
      addToast('success', 'Benchmark run completed');
    },
    onError: () => addToast('error', 'Benchmark run failed'),
  });

  return (
    <div className="flex items-center justify-between rounded-lg border border-border bg-surface-secondary p-4">
      <div>
        <h3 className="text-sm font-semibold">Benchmark Runner</h3>
        <p className="text-xs text-text-secondary">Trigger a full benchmark suite.</p>
      </div>
      <button
        onClick={() => mutation.mutate()}
        disabled={mutation.isPending}
        className={cn('flex items-center gap-2 rounded-md bg-primary px-4 py-2 text-sm text-white hover:bg-primary-hover disabled:opacity-70')}
      >
        {mutation.isPending && <Loader2 size={14} className="animate-spin" />}
        {mutation.isPending ? 'Running...' : 'Run Benchmark'}
      </button>
    </div>
  );
}
