'use client';

import { useEffect } from 'react';
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

  const { data: statusData } = useQuery({
    queryKey: ['governance', 'status'],
    queryFn: getGovernanceStatus,
  });

  useEffect(() => {
    if (data) setAuditTrail(data.entries);
  }, [data, setAuditTrail]);

  useEffect(() => {
    if (statusData) setPacks(statusData);
  }, [statusData, setPacks]);

  return {
    auditTrail: data?.entries ?? [],
    isLoading,
    refetch,
  };
}
