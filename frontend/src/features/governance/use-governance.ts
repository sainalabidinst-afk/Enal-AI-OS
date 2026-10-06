'use client';

import { useQuery } from '@tanstack/react-query';
import { getAuditTrail, getGovernanceStatus } from '@/services/governance';
import { useGovernanceStore } from '@/features/governance/governance-store';
import type { AuditEntry } from '@/types/audit';

export function useGovernance(packId?: string) {
  const { data, isLoading, refetch } = useQuery<{ entries?: Array<{ id?: string; action?: string; timestamp?: string; user?: string }> }>({
    queryKey: ['governance', packId],
    queryFn: () => getAuditTrail(packId) as Promise<{ entries?: Array<{ id?: string; action?: string; timestamp?: string; user?: string }> }>,
  });

  const setAuditTrail = useGovernanceStore((state) => state.setAuditTrail);
  const setPacks = useGovernanceStore((state) => state.setPacks);

  if (data) {
    setAuditTrail(data.entries as AuditEntry[]);
  }

  useQuery({
    queryKey: ['governance', 'status'],
    queryFn: getGovernanceStatus,
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    onSuccess: (statusData: any) => {
      setPacks(statusData);
    },
  } as any);

  return {
    auditTrail: data?.entries ?? [],
    isLoading,
    refetch,
  };
}
