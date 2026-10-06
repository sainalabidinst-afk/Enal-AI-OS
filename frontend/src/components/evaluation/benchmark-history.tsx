'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';

export function BenchmarkHistory() {
  const { data, isLoading } = useQuery<Array<{ id?: string; created_at?: string; summary?: string }>>({
    queryKey: ['benchmark', 'history'],
    queryFn: () => apiClient.get('/api/v1/benchmark/history'),
  });

  if (isLoading) return <LoadingSkeleton className="mt-4 h-64 w-full" />;

  const history = data ?? [];

  return (
    <div className="mt-4 space-y-2">
      {history.map((item: { id?: string; created_at?: string; summary?: string }) => (
        <div key={item.id} className="flex items-center justify-between rounded-md border border-border px-3 py-2">
          <div>
            <p className="text-sm font-medium">{item.summary ?? 'Benchmark run'}</p>
            <p className="text-xs text-text-muted">{item.id}</p>
          </div>
          <span className="text-xs text-text-secondary">{item.created_at ? new Date(item.created_at).toLocaleString() : '-'}</span>
        </div>
      ))}
    </div>
  );
}
