'use client';

import { useSearchParams } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { JsonViewer } from '@/components/shared/json-viewer';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';

export default function SearchPage() {
  const searchParams = useSearchParams();
  const q = searchParams.get('q') ?? '';

  const { data, isLoading } = useQuery({
    queryKey: ['search', q],
    queryFn: () => apiClient.get('/api/v1/search', { params: { q } }),
    enabled: q.length > 0,
  });

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Search</h2>
        <p className="text-sm text-text-secondary">Results for &quot;{q}&quot;</p>
      </div>
      {isLoading ? (
        <LoadingSkeleton className="h-64 w-full" />
      ) : (
        <JsonViewer data={data} />
      )}
    </div>
  );
}
