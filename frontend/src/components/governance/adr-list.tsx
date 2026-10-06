'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { StatusBadge } from '@/components/shared/status-badge';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';

export function ADRList() {
  const { data, isLoading } = useQuery<Array<{ id: string; title: string; status: string }>>({
    queryKey: ['governance', 'adr'],
    queryFn: () => apiClient.get('/api/v1/packs'),
  });

  if (isLoading) return <LoadingSkeleton className="mt-4 h-64 w-full" />;

  const adrs = data ?? [];

  if (!adrs.length) {
    return (
      <div className="mt-4 rounded-md border border-dashed border-border px-4 py-6 text-center text-xs text-text-muted">
        No ADR entries found.
      </div>
    );
  }

  return (
    <div className="mt-4 space-y-2">
      {adrs.map((adr: { id: string; title: string; status: string }) => (
        <div key={adr.id} className="flex items-center justify-between rounded-md border border-border px-3 py-2">
          <div>
            <p className="text-sm font-medium">{adr.title}</p>
            <p className="text-xs text-text-muted">{adr.id}</p>
          </div>
          <StatusBadge status="info" label={adr.status} />
        </div>
      ))}
    </div>
  );
}
