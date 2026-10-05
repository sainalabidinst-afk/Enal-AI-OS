import { api } from "@/services/api";
import type {
  ModelProviderStatus,
  ServiceHealth,
  VoiceProviderInfo,
  VoiceTranscription,
} from "@/types/console";

export function getServiceHealth() {
  return api.get<ServiceHealth>("/health");
}

export function getModelProviders() {
  return api.get<ModelProviderStatus[] | Record<string, ModelProviderStatus>>(
    "/api/v1/providers"
  );
}

export function getModelHealth(provider?: string) {
  const query = provider ? `?provider=${encodeURIComponent(provider)}` : "";
  return api.get<Record<string, ModelProviderStatus>>(
    `/api/v1/health${query}`
  );
}

export function getVoiceProviders() {
  return api.get<VoiceProviderInfo>("/api/v1/voice/providers");
}

export function getSupportedLanguages() {
  return api.get<{ languages: string[] }>("/api/v1/voice/languages");
}

export async function transcribeAudio(
  blob: Blob,
  language = "id"
): Promise<VoiceTranscription> {
  const form = new FormData();
  form.append("file", blob, "audio.wav");
  const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const token =
    typeof window === "undefined" ? "" : localStorage.getItem("enal-auth-token") || "";
  const response = await fetch(
    `${base}/api/v1/voice/transcribe?language=${encodeURIComponent(language)}`,
    {
      method: "POST",
      headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      body: form,
    }
  );
  if (!response.ok) {
    const detail = await response.json().catch(() => null);
    throw new Error(detail?.detail || "Transcription failed");
  }
  return response.json() as Promise<VoiceTranscription>;
}