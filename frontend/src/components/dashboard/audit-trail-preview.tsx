'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';
import { StatusBadge } from '@/components/shared/status-badge';

export function AuditTrailPreview({ limit = 5 }: { limit?: number }) {
  const { data, isLoading } = useQuery({
    queryKey: ['audit'],
    queryFn: () => apiClient.get('/api/v1/governance/audit'),
  });

  if (isLoading) {
    return (
      <div className="mt-4 space-y-2">
        {Array.from({ length: limit }).map((_, i) => (
          <LoadingSkeleton key={i} className="h-10 w-full" />
        ))}
      </div>
    );
  }

  const entries = data?.entries?.slice(0, limit) ?? [];

  return (
    <div className="mt-4 space-y-2">
      {entries.map((entry: { id?: string; action?: string; timestamp?: string; user?: string }) => (
        <div key={entry.id} className="flex items-center justify-between rounded-md border border-border px-3 py-2">
          <div>
            <p className="text-sm font-medium">{entry.action ?? 'Activity'}</p>
            <p className="text-xs text-text-muted">{entry.user ?? 'system'}</p>
          </div>
          <span className="text-xs text-text-secondary">{entry.timestamp ? new Date(entry.timestamp).toLocaleString() : '-'}</span>
        </div>
      ))}
    </div>
  );
}
