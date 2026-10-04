"use client";

import { Panel, PanelBody, PanelHeader } from "@/components/console/ui/panel";
import { Pill } from "@/components/console/ui/states";
import { Field, selectClass } from "@/components/console/ui/controls";
import { useConsoleStore } from "@/store/console-store";
import { formatDurationMs, titleCase } from "@/lib/format";

export interface VoiceSettingsModel {
  pitch: number;
  speed: number;
  emphasis: number;
  stability: number;
  voice: string;
  autoTranscribe: boolean;
}

export function VoiceSettingsPanel({
  settings,
  onChange,
  languages,
}: {
  settings: VoiceSettingsModel;
  onChange: (next: VoiceSettingsModel) => void;
  languages: string[];
}) {
  const sliders: {
    key: "pitch" | "speed" | "emphasis" | "stability";
    label: string;
    min: number;
    max: number;
    step: number;
  }[] = [
    { key: "pitch", label: "Pitch", min: 0.5, max: 2, step: 0.05 },
    { key: "speed", label: "Speed", min: 0.5, max: 2, step: 0.05 },
    { key: "emphasis", label: "Emphasis", min: 0, max: 2, step: 0.05 },
    { key: "stability", label: "Stability", min: 0, max: 1, step: 0.05 },
  ];

  return (
    <Panel>
      <PanelHeader title="Voice Settings" subtitle="Applied to TTS synthesis requests" />
      <PanelBody className="space-y-3">
        <Field label="Voice / language">
          <select
            value={settings.voice}
            onChange={(event) => onChange({ ...settings, voice: event.target.value })}
            className={selectClass()}
          >
            <option value="">provider default</option>
            {languages.map((language) => (
              <option key={language} value={language}>
                {language}
              </option>
            ))}
          </select>
        </Field>

        {sliders.map((slider) => (
          <div key={slider.key}>
            <div className="mb-1 flex items-center justify-between text-[11px]">
              <span className="text-[var(--ecp-text-dim)]">{slider.label}</span>
              <span className="font-mono text-[var(--ecp-text)]">
                {settings[slider.key].toFixed(2)}
              </span>
            </div>
            <input
              type="range"
              min={slider.min}
              max={slider.max}
              step={slider.step}
              value={settings[slider.key]}
              onChange={(event) =>
                onChange({ ...settings, [slider.key]: Number(event.target.value) })
              }
              className="w-full accent-[var(--ecp-gov)]"
            />
          </div>
        ))}

        <label className="flex items-center justify-between rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] px-3 py-2 text-[11px]">
          <span className="text-[var(--ecp-text-muted)]">Auto-transcribe</span>
          <input
            type="checkbox"
            checked={settings.autoTranscribe}
            onChange={(event) =>
              onChange({ ...settings, autoTranscribe: event.target.checked })
            }
            className="accent-[var(--ecp-gov)]"
          />
        </label>
      </PanelBody>
    </Panel>
  );
}

export function ConversationContextPanel({
  conversationId,
  latencyMs,
  messageCount,
  onClear,
}: {
  conversationId: string | null;
  latencyMs: number | null;
  messageCount: number;
  onClear: () => void;
}) {
  const telemetry = useConsoleStore((s) => s.telemetry.data);
  const providers = useConsoleStore((s) => s.voiceProviders.data);
  const models = useConsoleStore((s) => s.modelProviders.data);

  const model = models?.find((item) => item.healthy || item.available) ?? models?.[0];

  return (
    <Panel>
      <PanelHeader title="Conversation Context" subtitle="Runtime session state" />
      <PanelBody className="space-y-2 text-[11px]">
        <Row label="Conversation" value={conversationId ? conversationId.slice(0, 18) : "new"} />
        <Row label="Messages" value={String(messageCount)} />
        <Row label="Last latency" value={formatDurationMs(latencyMs)} />
        <Row
          label="Chat runs"
          value={telemetry ? String(telemetry.chat.count) : "—"}
        />
        <Row label="STT" value={providers?.stt_provider ?? "—"} />
        <Row label="TTS" value={providers?.tts_provider ?? "—"} />
        <Row
          label="Voice"
          value={
            providers
              ? `${providers.tts_voice_name || providers.tts_voice} · ${providers.tts_voice_tone}`
              : "—"
          }
        />
        <Row label="Model gateway" value={model?.name ?? model?.provider ?? "—"} />
        {providers && (
          <div className="flex flex-wrap gap-1.5 pt-1">
            {[
              providers.tts_voice_gender,
              providers.tts_voice_attitude,
              providers.stt_language,
            ]
              .filter(Boolean)
              .map((tag) => (
                <Pill key={tag}>{titleCase(tag)}</Pill>
              ))}
          </div>
        )}
        <button
          type="button"
          onClick={onClear}
          className="mt-2 w-full rounded-lg border border-[var(--ecp-border)] px-3 py-1.5 text-[11px] text-[var(--ecp-text-muted)] transition-colors hover:border-[var(--ecp-danger)] hover:text-[var(--ecp-danger)]"
        >
          Reset session
        </button>
      </PanelBody>
    </Panel>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-baseline justify-between gap-3 border-b border-[var(--ecp-border)]/60 pb-1.5">
      <span className="text-[var(--ecp-text-dim)]">{label}</span>
      <span className="truncate font-medium text-[var(--ecp-text)]">{value}</span>
    </div>
  );
}