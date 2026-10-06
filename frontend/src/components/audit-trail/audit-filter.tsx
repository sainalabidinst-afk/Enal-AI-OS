'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { JsonViewer } from '@/components/shared/json-viewer';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';

export function AuditFilter() {
  const [packId, setPackId] = useState('');
  const [user, setUser] = useState('');

  const { data, isLoading } = useQuery({
    queryKey: ['audit', 'trail', packId, user],
    queryFn: () => apiClient.get('/api/v1/governance/audit', { params: { pack_id: packId || undefined, user: user || undefined } }),
  });

  if (isLoading) return <LoadingSkeleton className="mt-4 h-64 w-full" />;

  return (
    <div className="mt-4 space-y-4">
      <div className="grid gap-4 md:grid-cols-2">
        <div>
          <label className="block text-sm font-medium">Pack ID</label>
          <input
            className="mt-1 w-full rounded-md border border-border bg-surface-primary px-3 py-2 text-sm outline-none focus:border-primary"
            value={packId}
            onChange={(e) => setPackId(e.target.value)}
          />
        </div>
        <div>
          <label className="block text-sm font-medium">User</label>
          <input
            className="mt-1 w-full rounded-md border border-border bg-surface-primary px-3 py-2 text-sm outline-none focus:border-primary"
            value={user}
            onChange={(e) => setUser(e.target.value)}
          />
        </div>
      </div>
      <JsonViewer data={data?.entries ?? []} />
    </div>
  );
}
