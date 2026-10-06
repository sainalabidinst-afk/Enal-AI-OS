'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { JsonViewer } from '@/components/shared/json-viewer';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';
import { useToast } from '@/components/shared/toast';
import { Loader2, Download } from 'lucide-react';

export function AuditFilter() {
  const [packId, setPackId] = useState('');
  const [user, setUser] = useState('');
  const queryClient = useQueryClient();
  const { addToast } = useToast();

  const { data, isLoading, refetch } = useQuery<{ entries?: Array<{ id?: string; action?: string; timestamp?: string; user?: string }> }>({
    queryKey: ['audit', 'trail', packId, user],
    queryFn: () => apiClient.get('/api/v1/audit', { params: { pack_id: packId as any, user: user as any } }),
    enabled: false,
  });

  const exportMutation = useMutation({
    mutationFn: () => apiClient.get('/api/v1/audit', { params: { pack_id: packId as any, user: user as any } }),
    onSuccess: (res) => {
      const blob = new Blob([JSON.stringify(res, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'audit-trail.json';
      a.click();
      URL.revokeObjectURL(url);
      addToast('success', 'Audit logs exported');
    },
    onError: () => addToast('error', 'Export failed'),
  });

  const handleFilter = (e: React.FormEvent) => {
    e.preventDefault();
    refetch();
  };

  return (
    <div className="mt-4 space-y-4">
      <form onSubmit={handleFilter} className="grid gap-4 md:grid-cols-2">
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
        <div className="md:col-span-2 flex gap-2">
          <button type="submit" className="flex items-center gap-2 rounded-md bg-primary px-4 py-2 text-sm text-white hover:bg-primary-hover">
            Filter
          </button>
          <button
            type="button"
            onClick={() => exportMutation.mutate()}
            disabled={exportMutation.isPending}
            className="flex items-center gap-2 rounded-md border border-border px-4 py-2 text-sm hover:bg-surface-hover disabled:opacity-70"
          >
            {exportMutation.isPending ? <Loader2 size={14} className="animate-spin" /> : <Download size={14} />}
            Export Logs
          </button>
        </div>
      </form>
      {isLoading ? (
        <LoadingSkeleton className="h-64 w-full" />
      ) : (
        <JsonViewer data={data?.entries ?? []} />
      )}
    </div>
  );
}
