import { api } from "./api";

export interface VoiceTranscription {
  text: string;
  confidence: number;
  language: string;
  duration_ms: number;
  alternatives?: string[] | null;
}

export interface VoiceProviderInfo {
  stt_provider: string;
  tts_provider: string;
  tts_voice: string;
  stt_language: string;
  supported_languages: string[];
}

export async function getSupportedLanguages(): Promise<{ languages: string[] }> {
  return api.get<{ languages: string[]}>("/api/v1/voice/languages");
}

export async function getVoiceProviders(): Promise<VoiceProviderInfo> {
  return api.get<VoiceProviderInfo>("/api/v1/voice/providers");
}

export async function transcribeAudio(
  audioBlob: Blob,
  language: string = "id",
): Promise<VoiceTranscription> {
  const formData = new FormData();
  formData.append("file", audioBlob, "audio.wav");

  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/voice/transcribe?language=${language}`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("enal-auth-token") || ""}`,
      },
      body: formData,
    },
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error?.detail || "Transcription failed");
  }

  return response.json();
}

export function speakText(
  text: string,
  voice: string = "en",
  speed: number = 1.0,
): Promise<Blob> {
  return new Promise((resolve, reject) => {
    const audio = new Audio(
      `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/voice/speak?text=${encodeURIComponent(text)}&voice=${voice}&speed=${speed}`,
    );
    audio.onload = () => resolve(audio as unknown as Blob);
    audio.onerror = () => reject(new Error("TTS failed"));
    audio.play().catch(reject);
  });
}

export function speakTextBrowser(text: string, lang: string = "en"): void {
  if (!window.speechSynthesis) return;
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = lang;
  utterance.rate = 1.0;
  window.speechSynthesis.speak(utterance);
}
