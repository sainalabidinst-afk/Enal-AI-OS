'use client';

import { create } from 'zustand';
import type { AuditEntry } from '@/types/audit';
import type { GovernanceStatus } from '@/types/adr';

interface GovernanceState {
  packs: GovernanceStatus | null;
  auditTrail: AuditEntry[];
  setPacks: (packs: GovernanceStatus) => void;
  setAuditTrail: (trail: AuditEntry[]) => void;
  registerPack: (pack: Record<string, unknown>) => void;
}

export const useGovernanceStore = create<GovernanceState>((set) => ({
  packs: null,
  auditTrail: [],
  setPacks: (packs) => set({ packs }),
  setAuditTrail: (auditTrail) => set({ auditTrail }),
  registerPack: (pack) => {
    // optimistic update could go here
    console.log('Register pack', pack);
  },
}));
