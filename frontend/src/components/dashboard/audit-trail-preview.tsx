'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';
import { StatusBadge } from '@/components/shared/status-badge';
import { useToast } from '@/components/shared/toast';
import { Download } from 'lucide-react';

export function AuditTrailPreview({ limit = 5 }: { limit?: number }) {
  const queryClient = useQueryClient();
  const { addToast } = useToast();

  const { data, isLoading } = useQuery<{ entries?: Array<{ id?: string; action?: string; timestamp?: string; user?: string }> }>({
    queryKey: ['audit'],
    queryFn: () => apiClient.get('/api/v1/audit'),
  });

  const exportMutation = useMutation({
    mutationFn: () => apiClient.get('/api/v1/audit'),
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

  if (isLoading) {
    return (
      <div className="mt-4 space-y-2">
        {Array.from({ length: limit }).map((_, i) => (
          <LoadingSkeleton key={i} className="h-10 w-full" />
        ))}
      </div>
    );
  }

  const entries = data?.entries?.slice(0, limit) ?? [];

  if (!entries.length) {
    return (
      <div className="mt-4 rounded-md border border-dashed border-border px-4 py-6 text-center text-xs text-text-muted">
        No audit activity yet. Register a pack or execute a capability to generate events.
      </div>
    );
  }

  return (
    <div className="mt-4 space-y-2">
      <div className="flex justify-end">
        <button
          onClick={() => exportMutation.mutate()}
          disabled={exportMutation.isPending}
          className="flex items-center gap-1 rounded-md border border-border px-2 py-1 text-xs hover:bg-surface-hover disabled:opacity-70"
        >
          <Download size={14} />
          Export Logs
        </button>
      </div>
      {entries.map((entry: { id?: string; action?: string; timestamp?: string; user?: string }) => (
        <div key={entry.id} className="flex items-center justify-between rounded-md border border-border px-3 py-2">
          <div>
            <p className="text-sm font-medium">{entry.action ?? 'Activity'}</p>
            <p className="text-xs text-text-muted">{entry.user ?? 'system'}</p>
          </div>
          <span className="text-xs text-text-secondary">{entry.timestamp ? new Date(entry.timestamp).toLocaleString() : '-'}</span>
        </div>
      ))}
    </div>
  );
}
