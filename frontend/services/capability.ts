import { api } from "./api";
import type { Capability, CapabilityListResponse } from "@/types/capability";

export async function listCapabilities(): Promise<CapabilityListResponse> {
  return api.get<CapabilityListResponse>("/api/v1/capabilities");
}

export async function getCapability(capabilityId: string): Promise<Capability> {
  return api.get<Capability>(`/api/v1/capabilities/${encodeURIComponent(capabilityId)}`);
}
