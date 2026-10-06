'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';

export function UserProfile() {
  const { data, isLoading } = useQuery({
    queryKey: ['auth', 'me'],
    queryFn: () => apiClient.get('/api/v1/auth/me'),
  });

  if (isLoading) return <LoadingSkeleton className="mt-4 h-24 w-full" />;

  return (
    <div className="mt-4 space-y-2">
      <p className="text-sm text-text-secondary">Username: {data?.username ?? '-'}</p>
      <p className="text-sm text-text-secondary">Roles: {data?.roles?.join(', ') ?? '-'}</p>
      <p className="text-sm text-text-secondary">Permissions: {data?.permissions?.join(', ') ?? '-'}</p>
    </div>
  );
}
