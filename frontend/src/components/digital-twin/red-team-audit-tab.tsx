'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { StatusBadge } from '@/components/shared/status-badge';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';

export function RedTeamAuditTab() {
  const { data, isLoading } = useQuery<{ audits?: Array<Record<string, unknown>> }>({
    queryKey: ['twin', 'audit'],
    queryFn: () => apiClient.get('/api/v1/twin/audit'),
    refetchInterval: 10000,
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
      <h3 className="text-sm font-semibold">Red Team Audit</h3>
      <p className="mt-1 text-xs text-text-secondary">
        Recent adversarial test results against plans, strategies, and decisions.
      </p>
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
