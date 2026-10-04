"use client";

import { Loader2, Mic, Square, Volume2 } from "lucide-react";
import type { Message } from "@/types/chat";

function Waveform({ active }: { active: boolean }) {
  const bars = Array.from({ length: 28 });
  return (
    <div className="flex h-8 items-end gap-[3px]" aria-hidden>
      {bars.map((_, index) => (
        <span
          key={index}
          className={`w-[3px] rounded-full ${
            active ? "bg-[var(--ecp-gov)] ecp-pulse" : "bg-[var(--ecp-border-strong)]"
          }`}
          style={{
            height: active ? `${18 + ((index * 7) % 14)}px` : "6px",
            animationDelay: active ? `${index * 45}ms` : undefined,
          }}
        />
      ))}
    </div>
  );
}

export function ChatStream({
  messages,
  sending,
  playingId,
  onReplay,
}: {
  messages: Message[];
  sending: boolean;
  playingId: string | null;
  onReplay: (message: Message, index: number) => void;
}) {
  if (messages.length === 0) {
    return (
      <div className="grid h-full place-items-center px-6 text-center">
        <div>
          <p className="text-sm text-[var(--ecp-text-muted)]">
            Start a conversation with the voice persona
          </p>
          <p className="mt-1 text-[11px] text-[var(--ecp-text-dim)]">
            Messages are routed to the backend cognitive pipeline; replies can be spoken
            back with the active TTS provider.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4 p-4">
      {messages.map((message, index) => {
        const id = `${index}-${message.timestamp}`;
        const user = message.role === "user";
        const speaking = playingId === id;
        return (
          <div key={id} className={`flex gap-2 ${user ? "justify-end" : ""}`}>
            {!user && (
              <span className="mt-0.5 grid h-7 w-7 shrink-0 place-items-center rounded-lg bg-[var(--ecp-surface-3)] text-[10px] font-bold text-[var(--ecp-gov)]">
                {message.agent ? message.agent.slice(0, 2).toUpperCase() : "AI"}
              </span>
            )}
            <div
              className={`max-w-[78%] rounded-xl border px-3.5 py-2.5 text-xs leading-relaxed ${
                user
                  ? "border-[var(--ecp-blue)]/40 bg-[var(--ecp-blue-soft)] text-[var(--ecp-text)]"
                  : "border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] text-[var(--ecp-text-muted)]"
              }`}
            >
              <p className="whitespace-pre-wrap">{message.content}</p>
              {!user && (
                <div className="mt-2 flex items-center justify-between gap-2 border-t border-[var(--ecp-border)] pt-2">
                  <Waveform active={speaking} />
                  <button
                    type="button"
                    onClick={() => onReplay(message, index)}
                    className="flex items-center gap-1 rounded-md border border-[var(--ecp-border)] px-2 py-1 text-[10px] text-[var(--ecp-text-dim)] transition-colors hover:border-[var(--ecp-gov)] hover:text-[var(--ecp-text)]"
                  >
                    <Volume2 className="h-3 w-3" />
                    Speak
                  </button>
                </div>
              )}
            </div>
          </div>
        );
      })}
      {sending && (
        <div className="flex items-center gap-2 text-[11px] text-[var(--ecp-text-dim)]">
          <Loader2 className="h-3 w-3 animate-spin" />
          Thinking…
        </div>
      )}
    </div>
  );
}

export function Composer({
  onSend,
  onRecord,
  onStopRecording,
  recording,
  supported,
  disabled,
}: {
  onSend: (text: string) => void;
  onRecord: () => void;
  onStopRecording: () => void;
  recording: boolean;
  supported: boolean;
  disabled: boolean;
}) {
  return (
    <div className="flex items-center gap-2 border-t border-[var(--ecp-border)] p-3">
      <button
        type="button"
        onClick={recording ? onStopRecording : onRecord}
        disabled={!supported}
        title={
          supported ? (recording ? "Stop recording" : "Record voice input") : "Recording unsupported"
        }
        className={`grid h-9 w-9 place-items-center rounded-lg border transition-colors ${
          recording
            ? "border-[var(--ecp-alert)] bg-[var(--ecp-alert-soft)] text-[var(--ecp-alert)]"
            : "border-[var(--ecp-border)] text-[var(--ecp-text-muted)] hover:border-[var(--ecp-gov)] hover:text-[var(--ecp-text)]"
        } disabled:opacity-40`}
      >
        {recording ? <Square className="h-3.5 w-3.5" /> : <Mic className="h-3.5 w-3.5" />}
      </button>

      <input
        onKeyDown={(event) => {
          if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            const input = event.currentTarget;
            if (input.value.trim()) {
              onSend(input.value);
              input.value = "";
            }
          }
        }}
        disabled={disabled}
        placeholder={recording ? "Listening…" : "Ask the voice agent…"}
        className="flex-1 rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-bg-raised)] px-3 py-2 text-xs outline-none transition-colors placeholder:text-[var(--ecp-text-dim)] focus:border-[var(--ecp-gov)] disabled:opacity-50"
      />

      <span className="rounded-md border border-[var(--ecp-border)] px-2 py-1 text-[10px] text-[var(--ecp-text-dim)]">
        Enter to send
      </span>
    </div>
  );
}