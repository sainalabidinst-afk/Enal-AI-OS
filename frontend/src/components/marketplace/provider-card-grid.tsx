'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { ProviderCard } from './provider-card';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';

export function ProviderCardGrid() {
  const { data, isLoading } = useQuery({
    queryKey: ['providers'],
    queryFn: () => apiClient.get('/api/v1/models/providers'),
  });

  if (isLoading) return <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">{[1,2,3,4,5,6].map(i => <LoadingSkeleton key={i} className="h-32 w-full" />)}</div>;

  const providers = data ?? {};

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {Object.entries(providers).map(([name, info]: [string, { status?: string; models?: string[] }]) => (
        <ProviderCard key={name} name={name} status={info?.status} models={info?.models} />
      ))}
    </div>
  );
}
