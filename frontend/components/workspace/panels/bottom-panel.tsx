"use client";

import { useState } from "react";
import { Tabs, TabPanel } from "@/components/design-system/navigation/tabs";
import { Button } from "@/components/ui/button";
import { Send, Mic, Paperclip, Smile, Terminal } from "lucide-react";
import { useWorkspaceStore } from "@/components/workspace/stores/workspace-store";
import { cn } from "@/lib/utils";

const TABS = ["Logs", "Problems", "Output", "Debug Console"] as const;

const COMMAND_SHORTCUTS = [
  { key: "upload", label: "Upload File" },
  { key: "test", label: "Run Tests" },
  { key: "report", label: "Generate Report" },
  { key: "deploy", label: "Deploy" },
  { key: "analyze", label: "Analyze Code" },
  { key: "audit", label: "Security Audit" },
];

export function BottomPanel() {
  const [activeTab, setActiveTab] = useState<(typeof TABS)[number]>("Logs");
  const system = useWorkspaceStore((s) => s.system);
  const [input, setInput] = useState("");
  const [recording, setRecording] = useState(false);

  const handleSend = () => {
    if (!input.trim()) return;
    setInput("");
  };

  const toggleRecording = () => {
    setRecording((prev) => !prev);
  };

  return (
    <div
      className="flex shrink-0 flex-col border-t border-[var(--color-border)] bg-[var(--color-surface)]"
      aria-label="Bottom panel"
    >
      <Tabs
        tabs={TABS.map((tab) => ({ id: tab, label: tab }))}
        activeTab={activeTab}
        onChange={(id) => setActiveTab(id as (typeof TABS)[number])}
      />

      <TabPanel>
        <pre className="text-xs text-[var(--color-text-secondary)] whitespace-pre-wrap p-3">
          {activeTab === "Logs" && "[workspace] Workspace engine initialized.\n[workspace] Ready."}
          {activeTab === "Problems" && "No problems detected."}
          {activeTab === "Output" && "Workspace output will appear here."}
          {activeTab === "Debug Console" && "> _"}
        </pre>
      </TabPanel>

      <div className="border-t border-[var(--color-border)] p-2 bg-[var(--color-bg-secondary)]">
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1 text-[10px] text-[var(--color-text-secondary)]">
            <span>/commands:</span>
            {COMMAND_SHORTCUTS.slice(0, 3).map((cmd) => (
              <kbd
                key={cmd.key}
                className="px-1 py-0.5 rounded bg-[var(--color-bg-tertiary)] text-[var(--color-text-secondary)]"
              >
                /{cmd.key}
              </kbd>
            ))}
            <span className="opacity-50">...</span>
          </div>

          <Button variant="ghost" size="icon" className="h-6 w-6 shrink-0">
            <Paperclip className="h-3.5 w-3.5" />
          </Button>

          <div className="relative flex-1">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              placeholder="Type a command or message..."
              className="w-full rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-3 py-1.5 text-xs text-[var(--color-text-primary)] placeholder:text-[var(--color-text-secondary)] focus:border-[var(--color-accent)] focus:outline-none"
            />
            <span className="absolute right-2 top-1/2 -translate-y-1/2 text-[9px] text-[var(--color-text-secondary)]">
              ↵
            </span>
          </div>

          <Button
            variant="ghost"
            size="icon"
            className={cn("h-6 w-6 shrink-0", recording && "text-[var(--color-danger)] animate-pulse")}
            onClick={toggleRecording}
            aria-label={recording ? "Stop recording" : "Start recording"}
          >
            <Mic className="h-3.5 w-3.5" />
          </Button>

          <Button
            variant="ghost"
            size="icon"
            className="h-6 w-6 shrink-0"
            onClick={handleSend}
            aria-label="Send"
          >
            <Send className="h-3.5 w-3.5" />
          </Button>

          <div className="flex items-center gap-1 text-[10px] text-[var(--color-text-secondary)]">
            <Terminal className="h-3 w-3" />
            <span>{system.latencyMs}ms</span>
          </div>
        </div>
      </div>
    </div>
  );
}
