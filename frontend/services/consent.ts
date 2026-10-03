import { api } from "./api";

export type RiskLevel = "low" | "medium" | "high";

export type ConsentStatus = "pending" | "approved" | "denied" | "expired";

export interface ConsentRequest {
  request_id: string;
  session_id: string;
  action_type: string;
  description: string;
  risk_level: RiskLevel;
  params: Record<string, unknown>;
  connector_type: string;
  created_at: string;
  expires_at: string;
  timeout_seconds: number;
  status: ConsentStatus;
}

export interface ConsentResponse {
  request_id: string;
  status: string;
  risk_level: RiskLevel;
  description: string;
  timeout_seconds: number;
  expires_at: string;
}

export interface ConsentHistoryItem {
  request_id: string;
  session_id: string;
  action_type: string;
  description: string;
  risk_level: RiskLevel;
  status: string;
  connector_type: string;
  created_at: string;
  response_at: string | null;
  responder: string;
}

export interface ClassificationResult {
  action_type: string;
  risk_level: RiskLevel;
  requires_consent: boolean;
}

export async function getPendingConsents(): Promise<ConsentRequest[]> {
  return api.get<ConsentRequest[]>("/api/v1/consent/pending");
}

export async function requestConsent(payload: {
  action_type: string;
  description?: string;
  params?: Record<string, unknown>;
  session_id?: string;
  connector_type?: string;
  timeout_seconds?: number;
}): Promise<ConsentResponse> {
  return api.post<ConsentResponse>("/api/v1/consent/request", payload);
}

export async function respondToConsent(
  request_id: string,
  decision: "approve" | "deny",
  responder: string = "user",
): Promise<{ request_id: string; status: string; responder: string; response_at: string | null }> {
  return api.post<{ request_id: string; status: string; responder: string; response_at: string | null }>(
    "/api/v1/consent/respond",
    { request_id, decision, responder },
  );
}

export async function getConsentHistory(
  status?: ConsentStatus,
  limit: number = 100,
): Promise<ConsentHistoryItem[]> {
  const params = new URLSearchParams();
  if (status) params.set("status", status);
  params.set("limit", limit.toString());
  return api.get<ConsentHistoryItem[]>(`/api/v1/consent/history?${params.toString()}`);
}

export async function classifyAction(
  action_type: string,
  connector_type?: string,
): Promise<ClassificationResult> {
  const params = new URLSearchParams();
  params.set("action_type", action_type);
  if (connector_type) params.set("connector_type", connector_type);
  return api.get<ClassificationResult>(`/api/v1/consent/classify?${params.toString()}`);
}
