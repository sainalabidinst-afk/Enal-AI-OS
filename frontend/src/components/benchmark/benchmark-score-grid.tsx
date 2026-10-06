'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { StatusBadge } from '@/components/shared/status-badge';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';

export function BenchmarkScoreGrid({ onSelect }: { onSelect?: (vendor: string) => void }) {
  const { data, isLoading } = useQuery<{ capabilities?: Record<string, { avg_score?: number; avg_capability_score?: number }> }>({
    queryKey: ['benchmark', 'dashboard'],
    queryFn: () => apiClient.get('/api/v1/benchmark/dashboard'),
  });

  if (isLoading) return <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">{[1,2,3,4,5,6].map(i => <LoadingSkeleton key={i} className="h-32 w-full" />)}</div>;

  const scores = data?.capabilities ?? {};

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {Object.entries(scores).map(([vendor, score]: [string, { avg_score?: number; avg_capability_score?: number }]) => (
        <button key={vendor} onClick={() => onSelect?.(vendor)} className="rounded-lg border border-border bg-surface-secondary p-4 text-left hover:bg-surface-hover">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold">{vendor}</h3>
            <StatusBadge status={typeof score.avg_score === 'number' && score.avg_score >= 0.8 ? 'success' : 'warning'} label={typeof score.avg_score === 'number' ? `${Math.round(score.avg_score * 100)}%` : '-'} />
          </div>
          <p className="mt-2 text-xs text-text-secondary">Capability Score: {typeof score.avg_capability_score === 'number' ? `${Math.round(score.avg_capability_score * 100)}%` : '-'}</p>
        </button>
      ))}
    </div>
  );
}
