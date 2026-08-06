"use client";

import { type ReactNode } from "react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { TerminalWidget } from "@/components/workspace/shared/terminal-widget";
import { AIChatPanel } from "@/components/workspace/shared/ai-chat-panel";
import { useCognitiveStore } from "@/store/cognitive-store";
import { CognitiveLayer } from "@/types/cognitive";
import { cn } from "@/lib/utils";

interface System1ReactiveLayerProps {
  className?: string;
}

export function System1ReactiveLayer({ className }: System1ReactiveLayerProps) {
  const currentLayer = useCognitiveStore((s) => s.current_layer);
  const setLayer = useCognitiveStore((s) => s.setLayer);
  const metaFlags = useCognitiveStore((s) => s.meta_cognitive_flags);

  if (currentLayer !== CognitiveLayer.REACTIVE) {
    return (
      <div className={cn("flex items-center justify-center h-full", className)}>
        <div className="text-center">
          <p className="text-sm text-[var(--color-text-secondary)] mb-3">
            System 1 is inactive. Switch to L1 for reactive interactions.
          </p>
          <button
            onClick={() => setLayer(CognitiveLayer.REACTIVE)}
            className="px-4 py-2 rounded-lg bg-[var(--color-primary-500)] text-white text-sm font-medium hover:bg-[var(--color-primary-600)] transition-colors"
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
            <CardDescription>System 1 shortcuts</CardDescription>
          </CardHeader>
          <div className="p-4 flex flex-wrap gap-2">
            {["Analyze", "Generate", "Review", "Optimize"].map((action) => (
              <button
                key={action}
                className="px-3 py-1.5 rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] text-xs font-medium text-[var(--color-text-primary)] hover:bg-[var(--color-bg-tertiary)] transition-colors"
              >
                {action}
              </button>
            ))}
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
                { type: "info", text: "System 1 ready. Waiting for input..." },
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
          <div className="p-4">
            <AIChatPanel
              title="System 1 Assistant"
              messages={[]}
              onSend={(message) => {
                console.log("System 1 chat:", message);
              }}
            />
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
            <StatusItem label="Confidence" value="High" />
            <StatusItem label="Status" value="Ready" />
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
      <span className="text-sm font-medium text-[var(--color-text-primary)]">{value}</span>
    </div>
  );
}
