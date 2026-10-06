'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';

export function ContextMemoryPanel() {
  const { data, isLoading } = useQuery({
    queryKey: ['voice', 'context'],
    queryFn: () => apiClient.get('/api/v1/voice/context'),
  });

  if (isLoading) return <LoadingSkeleton className="mt-4 h-24 w-full" />;

  return (
    <pre className="mt-4 overflow-auto rounded-md border border-border bg-surface-primary p-4 font-mono text-xs text-text-secondary">
      {JSON.stringify(data ?? {}, null, 2)}
    </pre>
  );
}
