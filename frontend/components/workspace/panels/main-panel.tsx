"use client";

import { type ReactNode, useState } from "react";
import { cn } from "@/lib/utils";
import { AIChatPanel, type Message } from "@/components/workspace/shared/ai-chat-panel";
import { Button } from "@/components/ui/button";
import { Upload, Play, FileText, Sparkles, Send, Paperclip, Mic } from "lucide-react";

const QUICK_ACTION_BUTTONS = [
  { label: "Upload File", icon: Upload, action: "upload" as const },
  { label: "Run Test", icon: Play, action: "test" as const },
  { label: "Generate Report", icon: FileText, action: "report" as const },
  { label: "AI Insight", icon: Sparkles, action: "insight" as const },
];

interface MainPanelProps {
  app?: string;
  children?: ReactNode;
  className?: string;
}

export function MainPanel({ app, children, className }: MainPanelProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");

  const handleSend = (text: string) => {
    if (!text.trim()) return;
    const userMsg: Message = { role: "user", content: text };
    setMessages((prev) => [...prev, userMsg]);
    const timer = setTimeout(() => {
      const aiMsg: Message = {
        role: "assistant",
        content: `Processing in ${app || "workspace"} context...`,
      };
      setMessages((prev) => [...prev, aiMsg]);
    }, 500);
    setInput("");
    return () => clearTimeout(timer);
  };

  const handleQuickAction = (action: string) => {
    const labels = {
      upload: "Upload File",
      test: "Run Test",
      report: "Generate Report",
      insight: "AI Insight",
    };
    handleSend(`Quick action: ${labels[action as keyof typeof labels]}`);
  };

  return (
    <main className={cn("flex h-full min-w-0 flex-1 flex-col overflow-hidden bg-[var(--color-bg-primary)]", className)}>
      {children ? (
        <div className="min-h-0 min-w-0 flex-1 overflow-hidden">{children}</div>
      ) : (
        <div className="min-h-0 min-w-0 flex-1 overflow-hidden">
          <AIChatPanel
            title={app ? `${app.charAt(0).toUpperCase() + app.slice(1)} Assistant` : "AI Assistant"}
            messages={messages}
            onSend={handleSend}
            className="h-full"
          />
        </div>
      )}

      {!children && (
        <div className="border-t border-[var(--color-border)] bg-[var(--color-surface)] p-2">
          <div className="flex flex-wrap gap-1.5 mb-2">
            {QUICK_ACTION_BUTTONS.map((btn) => (
              <Button
                key={btn.action}
                variant="ghost"
                size="sm"
                className="text-xs"
                onClick={() => handleQuickAction(btn.action)}
              >
                <btn.icon className="h-3 w-3 mr-1" />
                {btn.label}
              </Button>
            ))}
          </div>

          <div className="flex items-center gap-2">
            <Button variant="ghost" size="icon" className="h-7 w-7 shrink-0">
              <Paperclip className="h-4 w-4" />
            </Button>
            <div className="relative flex-1">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSend(input)}
                placeholder="Type a message or /command..."
                className="w-full rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] px-3 py-1.5 text-sm text-[var(--color-text-primary)] placeholder:text-[var(--color-text-secondary)] focus:border-[var(--color-accent)] focus:outline-none"
              />
              <kbd className="absolute right-2 top-1/2 -translate-y-1/2 text-[10px] text-[var(--color-text-secondary)] bg-[var(--color-bg-tertiary)] px-1 rounded">
                ↵
              </kbd>
            </div>
            <Button variant="ghost" size="icon" className="h-7 w-7 shrink-0">
              <Mic className="h-4 w-4" />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              className="h-7 w-7 shrink-0"
              onClick={() => handleSend(input)}
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </div>
      )}
    </main>
  );
}
