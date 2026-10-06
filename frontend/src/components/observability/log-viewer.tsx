'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';
import { JsonViewer } from '@/components/shared/json-viewer';

export function LogViewer() {
  const { data, isLoading } = useQuery<{ analysis?: Array<{ id?: string; message?: string; timestamp?: string }> }>({
    queryKey: ['metrics', 'logs'],
    queryFn: () => apiClient.get('/api/v1/metrics'),
  });

  if (isLoading) return <LoadingSkeleton className="mt-4 h-64 w-full" />;

  const logs = data?.analysis ?? [];

  return (
    <div className="mt-4">
      <JsonViewer data={logs} />
    </div>
  );
}
