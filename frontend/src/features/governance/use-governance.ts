'use client';

import { useQuery } from '@tanstack/react-query';
import { getAuditTrail, getGovernanceStatus } from '@/services/governance';
import { useGovernanceStore } from '@/features/governance/governance-store';

export function useGovernance(packId?: string) {
  const { data, isLoading, refetch } = useQuery({
    queryKey: ['governance', packId],
    queryFn: () => getAuditTrail(packId),
  });

  const setAuditTrail = useGovernanceStore((state) => state.setAuditTrail);
  const setPacks = useGovernanceStore((state) => state.setPacks);

  if (data) {
    setAuditTrail(data.entries ?? []);
  }

  useQuery({
    queryKey: ['governance', 'status'],
    queryFn: getGovernanceStatus,
    onSuccess: (statusData) => {
      setPacks(statusData);
    },
  });

  return {
    auditTrail: data?.entries ?? [],
    isLoading,
    refetch,
  };
}
