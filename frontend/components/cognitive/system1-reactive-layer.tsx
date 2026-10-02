"use client";

import { type ReactNode, useState } from "react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { TerminalWidget } from "@/components/workspace/shared/terminal-widget";
import { useCognitiveStore } from "@/store/cognitive-store";
import { CognitiveLayer } from "@/types/cognitive";
import { cn } from "@/lib/utils";
import { QuickActions } from "./quick-actions";
import { ChatInputWithSuggestions } from "./chat-input-with-suggestions";

interface System1ReactiveLayerProps {
  className?: string;
}

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export function System1ReactiveLayer({ className }: System1ReactiveLayerProps) {
  const currentLayer = useCognitiveStore((s) => s.current_layer);
  const setLayer = useCognitiveStore((s) => s.setLayer);
  const activeCapability = useCognitiveStore((s) => s.active_capability);
  const metaFlags = useCognitiveStore((s) => s.meta_cognitive_flags);

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isSending, setIsSending] = useState(false);

  const handleSend = (message: string) => {
    if (!message.trim()) return;
    setMessages((prev) => [...prev, { role: "user", content: message }]);
    setIsSending(true);
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Understood. I'll process this in System 1." },
      ]);
      setIsSending(false);
    }, 500);
  };

  if (currentLayer !== CognitiveLayer.REACTIVE) {
    return (
      <div className={cn("flex items-center justify-center h-full", className)}>
        <div className="text-center">
          <p className="text-sm text-[var(--color-text-secondary)] mb-3">
            System 1 is inactive. Switch to L1 for reactive interactions.
          </p>
          <button
            onClick={() => setLayer(CognitiveLayer.REACTIVE)}
            className="px-4 py-2 rounded-lg bg-[var(--color-primary-500)] text-white text-sm font-medium hover:opacity-90 transition-opacity"
          >
            Activate System 1
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={cn("grid grid-cols-1 lg:grid-cols-2 gap-4 p-4 h-full overflow-y-auto", className)}>
      <div className="space-y-4">
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>System 1 shortcuts to capabilities</CardDescription>
          </CardHeader>
          <div className="p-4">
            <QuickActions />
          </div>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Live Terminal</CardTitle>
            <CardDescription>Real-time execution output</CardDescription>
          </CardHeader>
          <div className="p-4">
            <TerminalWidget
              title="Execution Output"
              lines={[
                { type: "info", text: activeCapability ? `Active capability: ${activeCapability}` : "System 1 ready. Waiting for input..." },
              ]}
            />
          </div>
        </Card>
      </div>

      <div className="space-y-4">
        <Card>
          <CardHeader>
            <CardTitle>AI Assistant</CardTitle>
            <CardDescription>Streaming chat interface</CardDescription>
          </CardHeader>
          <div className="flex h-[480px] flex-col">
            <div className="flex-1 overflow-y-auto p-4 space-y-3 min-h-0">
              {messages.length === 0 && (
                <span className="text-xs text-[var(--color-text-secondary)]">Start a conversation...</span>
              )}
              {messages.map((msg, i) => (
                <div
                  key={i}
                  className={cn(
                    "rounded-lg px-3 py-2 text-xs max-w-[80%]",
                    msg.role === "user"
                      ? "bg-[var(--color-accent)] text-white ml-auto"
                      : "bg-[var(--color-bg-tertiary)] text-[var(--color-text-primary)]"
                  )}
                >
                  {msg.content}
                </div>
              ))}
              {isSending && (
                <div className="flex items-center gap-1.5 text-xs text-[var(--color-text-secondary)]">
                  <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-[var(--color-text-secondary)] [animation-delay:-0.3s]"></span>
                  <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-[var(--color-text-secondary)] [animation-delay:-0.15s]"></span>
                  <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-[var(--color-text-secondary)]"></span>
                </div>
              )}
            </div>
            <div className="border-t border-[var(--color-border)] p-4">
              <ChatInputWithSuggestions
                onSend={handleSend}
                disabled={isSending}
                placeholder="Ask Enal AI OS to do something..."
              />
            </div>
          </div>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>System Status</CardTitle>
            <CardDescription>
              {metaFlags.uncertainty ? "High uncertainty detected" : "Normal operation"}
            </CardDescription>
          </CardHeader>
          <div className="p-4 grid grid-cols-2 gap-3">
            <StatusItem label="Layer" value="System 1" />
            <StatusItem label="Mode" value="Reactive" />
            <StatusItem label="Confidence" value={metaFlags.confidence_trend === "decreasing" ? "Declining" : metaFlags.confidence_trend === "increasing" ? "Improving" : "Stable"} />
            <StatusItem label="Status" value={activeCapability ? activeCapability : "Ready"} />
          </div>
        </Card>
      </div>
    </div>
  );
}

function StatusItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex flex-col">
      <span className="text-xs text-[var(--color-text-secondary)]">{label}</span>
      <span className="text-sm font-medium text-[var(--color-text-primary)] transition-colors duration-150">{value}</span>
    </div>
  );
}
