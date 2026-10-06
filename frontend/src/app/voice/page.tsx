'use client';

import { AgentConsole } from '@/components/voice/agent-console';
import { TranscriptViewer } from '@/components/voice/transcript-viewer';
import { ContextMemoryPanel } from '@/components/voice/context-memory-panel';

export default function VoicePage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Voice Agent</h2>
        <p className="text-sm text-text-secondary">Speech-to-text agent console and transcript.</p>
      </div>

      <section className="grid gap-4 lg:grid-cols-2">
        <div className="rounded-lg border border-border bg-surface-secondary p-4">
          <h3 className="text-sm font-semibold">Agent Console</h3>
          <AgentConsole />
        </div>
        <div className="rounded-lg border border-border bg-surface-secondary p-4">
          <h3 className="text-sm font-semibold">Transcript</h3>
          <TranscriptViewer />
        </div>
      </section>

      <section className="rounded-lg border border-border bg-surface-secondary p-4">
        <h3 className="text-sm font-semibold">Context Memory</h3>
        <ContextMemoryPanel />
      </section>
    </div>
  );
}
