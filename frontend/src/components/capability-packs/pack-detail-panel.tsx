'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { StatusBadge } from '@/components/shared/status-badge';
import { useToast } from '@/components/shared/toast';
import { Loader2 } from 'lucide-react';

interface PackDetailPanelProps {
  packId: string;
}

export function PackDetailPanel({ packId }: PackDetailPanelProps) {
  const [payload, setPayload] = useState('{}');
  const addToast = useToast((state) => state.addToast);

  const { data, isLoading } = useQuery({
    queryKey: ['capability', packId],
    queryFn: () => apiClient.get(`/api/v1/capabilities/${packId}`),
    enabled: !!packId,
  });

  const executeMutation = useMutation({
    mutationFn: () => apiClient.post(`/api/v1/capabilities/${packId}/execute`, { message: 'Execute via UI', workspace_id: 'default' }),
    onSuccess: () => addToast('success', 'Capability executed'),
    onError: () => addToast('error', 'Execution failed'),
  });

  if (isLoading) return <div className="mt-4 animate-pulse rounded-md bg-surface-tertiary h-32 w-full" />;

  return (
    <div className="mt-4 space-y-4 rounded-lg border border-border bg-surface-secondary p-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold">{data?.name ?? 'Capability Detail'}</h3>
        <StatusBadge status="success" label={data?.category ?? 'pack'} />
      </div>
      <p className="text-xs text-text-secondary">{data?.description}</p>
      <div className="grid gap-4 md:grid-cols-2">
        <div>
          <label className="block text-sm font-medium">Payload (JSON)</label>
          <textarea
            className="mt-1 w-full rounded-md border border-border bg-surface-primary px-3 py-2 text-sm outline-none focus:border-primary font-mono"
            value={payload}
            onChange={(e) => setPayload(e.target.value)}
            rows={4}
          />
        </div>
        <div className="flex items-end">
          <button
            onClick={() => executeMutation.mutate()}
            disabled={executeMutation.isPending}
            className="flex items-center gap-2 rounded-md bg-primary px-4 py-2 text-sm text-white hover:bg-primary-hover disabled:opacity-70"
          >
            {executeMutation.isPending && <Loader2 size={14} className="animate-spin" />}
            Execute
          </button>
        </div>
      </div>
    </div>
  );
}
