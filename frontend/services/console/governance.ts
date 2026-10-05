import { api } from "@/services/api";
import type {
  AuditTrail,
  CapabilityDependencies,
  CapabilityCompatibility,
  CapabilityLifecycleResponse,
  GovernancePackList,
  GovernancePack,
  QualityGateResult,
  SandboxRecord,
} from "@/types/console";

export function listGovernancePacks(status?: string) {
  const query = status ? `?status=${encodeURIComponent(status)}` : "";
  return api.get<GovernancePackList>(`/api/v1/packs${query}`);
}

export function getGovernancePack(packId: string) {
  return api.get<GovernancePack>(
    `/api/v1/packs/${encodeURIComponent(packId)}`
  );
}

export function registerGovernancePack(payload: {
  pack_id?: string;
  name: string;
  domain: string;
  status?: string;
  metadata?: Record<string, unknown>;
}) {
  return api.post<GovernancePack>("/api/v1/packs", payload);
}

export function evaluateQualityGate(
  packId: string,
  thresholds?: {
    min_benchmark_score?: number;
    min_coverage?: number;
    min_test_pass_rate?: number;
  }
) {
  return api.post<QualityGateResult>(
    `/api/v1/packs/${encodeURIComponent(packId)}/evaluate`,
    thresholds ?? {}
  );
}

export function createPackSandbox(packId: string) {
  return api.post<SandboxRecord>(
    `/api/v1/packs/${encodeURIComponent(packId)}/sandbox`
  );
}

export function getAuditTrail(packId?: string) {
  const query = packId ? `?pack_id=${encodeURIComponent(packId)}` : "";
  return api.get<AuditTrail>(`/api/v1/audit${query}`);
}

export function listCapabilityLifecycle() {
  return api.get<CapabilityLifecycleResponse>("/api/v1/capabilities/lifecycle");
}

export function getCapabilityLifecycle(capabilityId: string) {
  return api.get<CapabilityLifecycleResponse["capabilities"][number]>(
    `/api/v1/capabilities/${encodeURIComponent(capabilityId)}/lifecycle`
  );
}

export function getCapabilityDependencies(capabilityId: string) {
  return api.get<CapabilityDependencies>(
    `/api/v1/capabilities/${encodeURIComponent(capabilityId)}/dependencies`
  );
}

export function getCapabilityCompatibility(
  capabilityId: string,
  contractVersion = "1"
) {
  return api.get<CapabilityCompatibility>(
    `/api/v1/capabilities/${encodeURIComponent(capabilityId)}/compatibility?contract_version=${encodeURIComponent(
      contractVersion
    )}`
  );
}

export function setCapabilityState(
  capabilityId: string,
  action: "load" | "unload" | "suspend" | "resume"
) {
  return api.post<CapabilityLifecycleResponse["capabilities"][number]>(
    `/api/v1/capabilities/${encodeURIComponent(capabilityId)}/${action}`
  );
}