'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';
import { StatusBadge } from '@/components/shared/status-badge';
import { useToast } from '@/components/shared/toast';
import { Loader2, Plus } from 'lucide-react';
import { useState } from 'react';

export function AlertRulesNotifications() {
  const [ruleName, setRuleName] = useState('');
  const queryClient = useQueryClient();
  const { addToast } = useToast();

  const { data, isLoading } = useQuery<{ trading_regime?: Array<{ event_id?: string; symbol?: string; regime?: string; confidence?: number; status?: string }> }>({
    queryKey: ['metrics', 'alerts'],
    queryFn: () => apiClient.get('/api/v1/metrics/alerts'),
  });

  const createMutation = useMutation({
    mutationFn: (name: string) => apiClient.post('/api/v1/metrics/alerts', { name, condition: 'confidence < 0.5' }),
    onSuccess: () => {
      addToast('success', 'Alert rule created');
      setRuleName('');
      queryClient.invalidateQueries({ queryKey: ['metrics', 'alerts'] });
    },
    onError: () => addToast('error', 'Failed to create alert rule'),
  });

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault();
    if (!ruleName.trim()) return;
    createMutation.mutate(ruleName.trim());
  };

  if (isLoading) return <LoadingSkeleton className="mt-4 h-64 w-full" />;

  const alerts = data?.trading_regime ?? [];

  return (
    <div className="mt-4 space-y-4">
      <form onSubmit={handleCreate} className="flex items-end gap-3">
        <div className="flex-1">
          <label className="block text-xs text-text-secondary">Alert Rule Name</label>
          <input
            className="mt-1 w-full rounded-md border border-border bg-surface-primary px-3 py-2 text-sm outline-none focus:border-primary"
            value={ruleName}
            onChange={(e) => setRuleName(e.target.value)}
            placeholder="e.g. Low confidence regime"
          />
        </div>
        <button type="submit" disabled={createMutation.isPending} className="flex items-center gap-2 rounded-md bg-primary px-3 py-2 text-xs text-white hover:bg-primary-hover disabled:opacity-70">
          {createMutation.isPending && <Loader2 size={14} className="animate-spin" />}
          <Plus size={14} />
          Add Alert Rule
        </button>
      </form>
      <div className="space-y-2">
        {alerts.map((alert: { event_id?: string; symbol?: string; regime?: string; confidence?: number; status?: string }) => (
          <div key={alert.event_id} className="flex items-center justify-between rounded-md border border-border px-3 py-2">
            <div>
              <p className="text-sm font-medium">{alert.symbol ?? 'Alert'}</p>
              <p className="text-xs text-text-muted">Regime: {alert.regime} · Confidence: {alert.confidence}</p>
            </div>
            <StatusBadge status={alert.status === 'active' ? 'danger' : 'success'} label={alert.status ?? 'unknown'} />
          </div>
        ))}
      </div>
    </div>
  );
}
