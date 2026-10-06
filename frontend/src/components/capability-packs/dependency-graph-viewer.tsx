'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';

export function DependencyGraphViewer() {
  const { data, isLoading } = useQuery<{ capabilities?: Array<{ id: string; name: string }> }>({
    queryKey: ['capabilities'],
    queryFn: () => apiClient.get('/api/v1/capabilities'),
  });

  if (isLoading) return <LoadingSkeleton className="mt-4 h-64 w-full" />;

  const nodes = data?.capabilities ?? [];

  return (
    <div className="mt-4 rounded-lg border border-border bg-surface-secondary p-4">
      <h3 className="text-sm font-semibold">Dependency Graph</h3>
      <div className="mt-4 flex flex-wrap gap-3">
        {nodes.map((node: { id: string; name: string }) => (
          <div key={node.id} className="rounded-md border border-border bg-surface-primary px-3 py-2 text-xs">
            <span className="font-medium">{node.name}</span>
            <span className="ml-2 text-text-muted">{node.id}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
