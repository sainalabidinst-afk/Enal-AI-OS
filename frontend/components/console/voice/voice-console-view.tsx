"use client";

import { useState } from "react";
import { Cpu, Mic2, Trash2 } from "lucide-react";
import { PageHeader, Panel, PanelBody, PanelHeader } from "@/components/console/ui/panel";
import { ChatStream, Composer } from "@/components/console/voice/chat-stream";
import {
  ConversationContextPanel,
  VoiceSettingsPanel,
  type VoiceSettingsModel,
} from "@/components/console/voice/voice-panels";
import {
  useRecorder,
  useSpeechPlayback,
  useVoiceSession,
} from "@/features/console/use-voice-session";
import { useConsoleStore } from "@/store/console-store";
import { useConsoleHydration } from "@/features/console/use-console";
import { getSupportedLanguages, transcribeAudio } from "@/services/console/environment";
import { formatDurationMs } from "@/lib/format";
import type { Message } from "@/types/chat";

const DEFAULT_SETTINGS: VoiceSettingsModel = {
  pitch: 1,
  speed: 1,
  emphasis: 1,
  stability: 0.5,
  voice: "",
  autoTranscribe: true,
};

export function VoiceConsoleView() {
  useConsoleHydration("environment");
  const session = useVoiceSession();
  const playback = useSpeechPlayback();
  const recorder = useRecorder();
  const providers = useConsoleStore((s) => s.voiceProviders);
  const [settings, setSettings] = useState<VoiceSettingsModel>(DEFAULT_SETTINGS);
  const [languages, setLanguages] = useState<string[]>([]);
  const [transcribing, setTranscribing] = useState(false);

  async function handleStopRecording() {
    const blob = await recorder.stop();
    if (!blob) return;
    setTranscribing(true);
    try {
      const result = await transcribeAudio(blob, settings.voice || "id");
      await session.send(result.text);
    } finally {
      setTranscribing(false);
    }
  }

  return (
    <div className="space-y-4">
      <PageHeader
        title="Voice Agent"
        description="Conversational persona backed by the backend chat pipeline and voice providers"
        actions={
          <>
            <span className="flex items-center gap-1.5 rounded-full border border-[var(--ecp-border)] bg-[var(--ecp-surface)] px-2.5 py-1 text-[11px] text-[var(--ecp-text-muted)]">
              <Mic2 className="h-3.5 w-3.5 text-[var(--ecp-gov)]" />
              {providers.data?.tts_voice_name || providers.data?.tts_voice || "voice profile"}
            </span>
            <span className="flex items-center gap-1.5 rounded-full border border-[var(--ecp-border)] bg-[var(--ecp-surface)] px-2.5 py-1 text-[11px] text-[var(--ecp-text-muted)]">
              <Cpu className="h-3.5 w-3.5 text-[var(--ecp-sky)]" />
              {providers.status === "error"
                ? "providers offline"
                : providers.data?.tts_provider || "loading model…"}
            </span>
            <button
              type="button"
              onClick={() => {
                getSupportedLanguages()
                  .then((response) => setLanguages(response.languages ?? []))
                  .catch(() => setLanguages([]));
              }}
              className="rounded-md border border-[var(--ecp-border)] px-2.5 py-1 text-[11px] text-[var(--ecp-text-muted)] transition-colors hover:border-[var(--ecp-gov)] hover:text-[var(--ecp-text)]"
            >
              Load languages
            </button>
          </>
        }
      />

      {session.error && (
        <p className="rounded-lg border border-[var(--ecp-danger)]/40 bg-[var(--ecp-danger-soft)] px-3 py-2 text-[11px] text-[var(--ecp-danger)]">
          {session.error}
        </p>
      )}

      <div className="grid gap-4 xl:grid-cols-[minmax(0,1fr)_320px]">
        <Panel className="flex min-h-[520px] flex-col">
          <PanelHeader
            title={providers.data?.tts_voice_name || "Voice persona"}
            subtitle={`${providers.data?.tts_provider ?? "provider"} · ${
              providers.data?.tts_voice_tone ?? "tone"
            } · ${providers.data?.tts_voice_attitude ?? "attitude"}`}
            actions={
              <button
                type="button"
                onClick={session.clear}
                className="flex items-center gap-1 text-[11px] text-[var(--ecp-text-dim)] transition-colors hover:text-[var(--ecp-danger)]"
              >
                <Trash2 className="h-3.5 w-3.5" />
                Reset
              </button>
            }
          />
          <PanelBody className="flex-1 overflow-y-auto p-0">
            <ChatStream
              messages={session.messages}
              sending={session.sending}
              playingId={playback.playingId}
              onReplay={(message: Message, index: number) =>
                playback.speak(message.content, `${index}-${message.timestamp}`, {
                  speed: settings.speed,
                  voice: settings.voice,
                })
              }
            />
          </PanelBody>
          <div className="flex items-center justify-between border-t border-[var(--ecp-border)] px-4 py-2 text-[11px] text-[var(--ecp-text-dim)]">
            <span>
              Latency {formatDurationMs(session.lastLatencyMs)} ·{" "}
              {recorder.supported ? "microphone ready" : "microphone unavailable"}
            </span>
            <span className="flex items-center gap-2">
              {settings.autoTranscribe && (
                <span className="rounded-md border border-[var(--ecp-border)] px-2 py-0.5">
                  auto-transcribe on
                </span>
              )}
              {transcribing && <span className="text-[var(--ecp-alert)]">transcribing…</span>}
              {playback.playingId && (
                <button
                  type="button"
                  onClick={playback.stop}
                  className="rounded-md border border-[var(--ecp-border)] px-2 py-0.5 text-[var(--ecp-text-muted)] hover:text-[var(--ecp-text)]"
                >
                  stop playback
                </button>
              )}
            </span>
          </div>
          <Composer
            onSend={session.send}
            onRecord={recorder.start}
            onStopRecording={handleStopRecording}
            recording={recorder.recording}
            supported={recorder.supported}
            disabled={session.sending || transcribing}
          />
        </Panel>

        <aside className="space-y-4">
          <VoiceSettingsPanel
            settings={settings}
            onChange={setSettings}
            languages={languages}
          />
          <ConversationContextPanel
            conversationId={session.conversationId}
            latencyMs={session.lastLatencyMs}
            messageCount={session.messages.length}
            onClear={session.clear}
          />
        </aside>
      </div>
    </div>
  );
}