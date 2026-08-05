"use client";

import { type ReactNode, useState } from "react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Send } from "lucide-react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

interface AIChatPanelProps {
  title?: string;
  messages?: Message[];
  onSend?: (message: string) => void;
  className?: string;
}

export function AIChatPanel({ title = "AI Assistant", messages = [], onSend, className }: AIChatPanelProps) {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;
    onSend?.(input.trim());
    setInput("");
  };

  return (
    <div className={className}>
      <Card>
        <CardHeader>
          <CardTitle>{title}</CardTitle>
          <CardDescription>AI-powered assistant</CardDescription>
        </CardHeader>
        <div className="p-4 space-y-3 max-h-[400px] overflow-y-auto">
          {messages.length === 0 && (
            <span className="text-xs text-[var(--color-text-secondary)]">Start a conversation...</span>
          )}
          {messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
              <div
                className={`rounded-lg px-3 py-2 text-xs max-w-[80%] ${
                  msg.role === "user"
                    ? "bg-[var(--color-accent)] text-white"
                    : "bg-[var(--color-bg-tertiary)] text-[var(--color-text-primary)]"
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}
        </div>
        <div className="p-4 border-t border-[var(--color-border)]">
          <div className="flex gap-2">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              placeholder="Ask anything..."
              className="flex-1 rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] px-4 py-2 text-sm"
            />
            <Button size="icon" onClick={handleSend}>
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
}
