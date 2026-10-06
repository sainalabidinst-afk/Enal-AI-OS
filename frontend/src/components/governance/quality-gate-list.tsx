'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { StatusBadge } from '@/components/shared/status-badge';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';

export function QualityGateList() {
  const { data, isLoading } = useQuery<Array<{ gate_id: string; pack_id: string; passed: boolean }>>({
    queryKey: ['governance', 'quality-gates'],
    queryFn: () => apiClient.get('/api/v1/governance/quality-gates'),
  });

  if (isLoading) return <LoadingSkeleton className="mt-4 h-64 w-full" />;

  const gates = data ?? [];

  return (
    <div className="mt-4 space-y-2">
      {gates.map((gate: { gate_id: string; pack_id: string; passed: boolean }) => (
        <div key={gate.gate_id} className="flex items-center justify-between rounded-md border border-border px-3 py-2">
          <div>
            <p className="text-sm font-medium">{gate.gate_id}</p>
            <p className="text-xs text-text-muted">Pack: {gate.pack_id}</p>
          </div>
          <StatusBadge status={gate.passed ? 'success' : 'danger'} label={gate.passed ? 'Pass' : 'Fail'} />
        </div>
      ))}
    </div>
  );
}
