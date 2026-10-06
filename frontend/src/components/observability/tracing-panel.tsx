'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';
import { JsonViewer } from '@/components/shared/json-viewer';

export function TracingPanel() {
  const { data, isLoading } = useQuery({
    queryKey: ['metrics', 'tracing'],
    queryFn: () => apiClient.get('/api/v1/metrics'),
  });

  if (isLoading) return <LoadingSkeleton className="mt-4 h-64 w-full" />;

  const traces = data?.cross_pack ?? [];

  return (
    <div className="mt-4">
      <JsonViewer data={traces} />
    </div>
  );
}
