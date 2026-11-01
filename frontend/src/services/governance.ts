import { apiClient } from '@/lib/api-client';
import type { GovernanceStatus } from '@/types/adr';
import type { AuditEntry } from '@/types/audit';

interface GovernancePackRecord {
  status: string;
}

interface GovernanceAuditRecord {
  entry_id: string;
  actor: string;
  action: string;
  pack_id: string | null;
  metadata: Record<string, unknown>;
  created_at: string;
}

export async function getPacks(status?: string) {
  return apiClient.get('/api/v1/packs', { params: status ? { status } : undefined });
}

export async function getPack(packId: string) {
  return apiClient.get(`/api/v1/packs/${packId}`);
}

export async function registerPack(payload: Record<string, unknown>) {
  return apiClient.post('/api/v1/packs', payload);
}

export async function getAuditTrail(
  packId?: string,
): Promise<{ entries: AuditEntry[]; count: number }> {
  const response = await apiClient.get<{
    entries: GovernanceAuditRecord[];
    count: number;
  }>('/api/v1/audit', { params: packId ? { pack_id: packId } : undefined });

  return {
    entries: response.entries.map((entry) => ({
      id: entry.entry_id,
      action: entry.action,
      user: entry.actor,
      pack_id: entry.pack_id ?? undefined,
      timestamp: entry.created_at,
      metadata: entry.metadata,
    })),
    count: response.count,
  };
}

export async function getGovernanceStatus(): Promise<GovernanceStatus> {
  const response = await apiClient.get<{ packs: GovernancePackRecord[] }>('/api/v1/packs');

  return {
    total_packs: response.packs.length,
    registered_packs: response.packs.filter((pack) => pack.status === 'registered').length,
    approved_packs: response.packs.filter((pack) => pack.status === 'approved').length,
    deprecated_packs: response.packs.filter((pack) => pack.status === 'deprecated').length,
  };
}
