'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { JsonViewer } from '@/components/shared/json-viewer';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';
import { StatusBadge } from '@/components/shared/status-badge';

interface QualityGateDetailProps {
  gateId: string;
}

export function QualityGateDetail({ gateId }: QualityGateDetailProps) {
  const { data, isLoading } = useQuery<{ passed?: boolean }>({
    queryKey: ['governance', 'quality-gates', gateId],
    queryFn: () => apiClient.get(`/api/v1/packs/${gateId}`),
    enabled: !!gateId,
  });

  if (isLoading) return <LoadingSkeleton className="mt-4 h-64 w-full" />;

  return (
    <div className="mt-4 space-y-4">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-semibold">Quality Gate {gateId}</h4>
        <StatusBadge status={data?.passed ? 'success' : 'danger'} label={data?.passed ? 'Pass' : 'Fail'} />
      </div>
      <JsonViewer data={data} />
    </div>
  );
}
