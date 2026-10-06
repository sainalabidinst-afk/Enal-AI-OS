'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';
import { StatusBadge } from '@/components/shared/status-badge';

const eventTypes = ['pack_register', 'evaluation_run', 'capability_execute'] as const;

export function AuditTimeline() {
  const { data, isLoading } = useQuery({
    queryKey: ['audit', 'trail'],
    queryFn: () => apiClient.get('/api/v1/governance/audit'),
  });

  if (isLoading) return <LoadingSkeleton className="mt-4 h-64 w-full" />;

  const entries = data?.entries ?? [];

  return (
    <div className="mt-4 space-y-4">
      {entries.map((entry: { id?: string; action?: string; timestamp?: string; user?: string }) => {
        const eventType = entry.action?.split(' ')[0] ?? 'event';
        const status = eventTypes.includes(eventType as typeof eventTypes[number]) ? 'info' : 'neutral';
        return (
          <div key={entry.id} className="flex gap-4 rounded-md border border-border px-3 py-2">
            <div className="mt-1 h-2 w-2 rounded-full bg-primary" />
            <div className="flex-1">
              <p className="text-sm font-medium">{entry.action ?? 'Activity'}</p>
              <p className="text-xs text-text-muted">{entry.user ?? 'system'}</p>
            </div>
            <div className="text-right">
              <StatusBadge status={status} label={eventType} />
              <p className="mt-1 text-xs text-text-secondary">{entry.timestamp ? new Date(entry.timestamp).toLocaleString() : '-'}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
}
