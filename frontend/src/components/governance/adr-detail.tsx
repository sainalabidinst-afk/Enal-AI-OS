'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { JsonViewer } from '@/components/shared/json-viewer';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';

interface ADRDetailProps {
  adrId: string;
}

export function ADRDetail({ adrId }: ADRDetailProps) {
  const { data, isLoading } = useQuery<{ title?: string; status?: string }>({
    queryKey: ['governance', 'adr', adrId],
    queryFn: () => apiClient.get(`/api/v1/governance/adr/${adrId}`),
    enabled: !!adrId,
  });

  if (isLoading) return <LoadingSkeleton className="mt-4 h-64 w-full" />;

  return (
    <div className="mt-4 space-y-4">
      <div>
        <h4 className="text-sm font-semibold">{data?.title ?? adrId}</h4>
        <p className="text-xs text-text-muted">{data?.status}</p>
      </div>
      <JsonViewer data={data} />
    </div>
  );
}
