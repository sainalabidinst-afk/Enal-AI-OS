export interface AuditEntry {
  id: string;
  action: string;
  user?: string;
  pack_id?: string;
  timestamp: string;
  metadata?: Record<string, unknown>;
}

export interface PackProgression {
  pack_id: string;
  stages: Array<{
    stage: string;
    status: string;
    timestamp: string;
    note?: string;
  }>;
}
