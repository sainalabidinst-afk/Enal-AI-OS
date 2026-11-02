'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { PackCard } from './pack-card';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';

export function PackList({ onSelect }: { onSelect?: (id: string) => void }) {
  const { data, isLoading } = useQuery<{ capabilities?: Array<{ id: string; name: string; description?: string; category?: string }> }>({
    queryKey: ['capability-packs'],
    queryFn: () => apiClient.get('/api/v1/capability-packs'),
  });

  const capabilities = data?.capabilities ?? [];

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {isLoading
        ? Array.from({ length: 6 }).map((_, i) => <LoadingSkeleton key={i} className="h-40 w-full" />)
        : capabilities.map((cap: { id: string; name: string; description?: string; category?: string }) => (
            <PackCard key={cap.id} {...cap} onSelect={() => onSelect?.(cap.id)} />
          ))}
    </div>
  );
}
