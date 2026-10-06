'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';
import { StatusBadge } from '@/components/shared/status-badge';

interface PackProgressionPanelProps {
  packId: string;
}

export function PackProgressionPanel({ packId }: PackProgressionPanelProps) {
  const { data, isLoading } = useQuery<{ stages?: Array<{ stage: string; status: string; timestamp?: string; note?: string }> }>({
    queryKey: ['governance', 'packs', packId, 'progression'],
    queryFn: () => apiClient.get(`/api/v1/packs/${packId}`),
    enabled: !!packId,
  });

  if (isLoading) return <LoadingSkeleton className="mt-4 h-64 w-full" />;

  const stages = data?.stages ?? [];

  return (
    <div className="mt-4 space-y-2">
      {stages.map((stage: { stage: string; status: string; timestamp?: string; note?: string }) => (
        <div key={stage.stage} className="flex items-center justify-between rounded-md border border-border px-3 py-2">
          <div>
            <p className="text-sm font-medium">{stage.stage}</p>
            <p className="text-xs text-text-muted">{stage.note}</p>
          </div>
          <div className="text-right">
            <StatusBadge status={stage.status === 'completed' ? 'success' : 'warning'} label={stage.status} />
            <p className="mt-1 text-xs text-text-secondary">{stage.timestamp ? new Date(stage.timestamp).toLocaleString() : '-'}</p>
          </div>
        </div>
      ))}
    </div>
  );
}
