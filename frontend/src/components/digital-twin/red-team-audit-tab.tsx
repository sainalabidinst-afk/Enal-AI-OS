'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { StatusBadge } from '@/components/shared/status-badge';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';
import { useToast } from '@/components/shared/toast';
import { Loader2, Play } from 'lucide-react';
import { useState } from 'react';

export function RedTeamAuditTab() {
  const [subject, setSubject] = useState('');
  const queryClient = useQueryClient();
  const { addToast } = useToast();

  const { data, isLoading } = useQuery<{ audits?: Array<Record<string, unknown>> }>({
    queryKey: ['twin', 'audit'],
    queryFn: () => apiClient.get('/api/v1/twin/audit'),
    refetchInterval: 10000,
  });

  const runMutation = useMutation({
    mutationFn: () => apiClient.post('/api/v1/twin/red-team', { subject: subject || 'plan', subject_type: 'plan' }),
    onSuccess: () => {
      addToast('success', 'Red team test executed');
      queryClient.invalidateQueries({ queryKey: ['twin', 'audit'] });
    },
    onError: () => addToast('error', 'Red team test failed'),
  });

  if (isLoading) {
    return (
      <div className="rounded-lg border border-border bg-surface-secondary p-4">
        <h3 className="text-sm font-semibold">Red Team Audit</h3>
        <LoadingSkeleton className="mt-4 h-48 w-full" />
      </div>
    );
  }

  const audits = data?.audits || [];

  return (
    <div className="rounded-lg border border-border bg-surface-secondary p-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-semibold">Red Team Audit</h3>
          <p className="mt-1 text-xs text-text-secondary">
            Recent adversarial test results against plans, strategies, and decisions.
          </p>
        </div>
        <button
          onClick={() => runMutation.mutate()}
          disabled={runMutation.isPending}
          className="flex items-center gap-2 rounded-md bg-primary px-3 py-1.5 text-xs text-white hover:bg-primary-hover disabled:opacity-70"
        >
          {runMutation.isPending && <Loader2 size={14} className="animate-spin" />}
          <Play size={14} />
          Run Red Team
        </button>
      </div>
      {audits.length === 0 ? (
        <p className="mt-4 text-xs text-text-secondary">No audits yet. Run a red team test to see results.</p>
      ) : (
        <div className="mt-4 space-y-3">
          {audits.map((audit: Record<string, unknown>) => (
            <div
              key={audit.audit_id as string | null | undefined}
              className="rounded-md border border-border bg-surface-primary p-3"
            >
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">{audit.subject as React.ReactNode}</span>
                <StatusBadge
                  status={
                    audit.gate_result === 'pass'
                      ? 'success'
                      : audit.gate_result === 'fail'
                        ? 'danger'
                        : 'warning'
                  }
                  label={audit.gate_result as string | undefined}
                />
              </div>
              <div className="mt-2 flex gap-4 text-xs text-text-secondary">
                <span>Type: {audit.subject_type as React.ReactNode}</span>
                <span>Vulnerabilities: {audit.vulnerabilities_found as React.ReactNode}</span>
                <span>Risk: {((audit.risk_score as number) * 100)?.toFixed(0) ?? 0}%</span>
              </div>
              <p className="mt-1 text-xs text-text-secondary">
                {new Date(audit.timestamp as string | number | Date).toLocaleString()}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
