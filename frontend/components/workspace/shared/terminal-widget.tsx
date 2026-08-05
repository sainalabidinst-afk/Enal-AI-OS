"use client";

import { type ReactNode } from "react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

interface TerminalWidgetProps {
  title?: string;
  lines?: Array<{ type: "info" | "error" | "warning" | "success"; text: string }>;
  className?: string;
}

const TYPE_STYLES = {
  info: "text-[var(--color-text-secondary)]",
  error: "text-[var(--color-danger)]",
  warning: "text-yellow-400",
  success: "text-green-400",
};

export function TerminalWidget({ title = "Terminal", lines = [], className }: TerminalWidgetProps) {
  return (
    <div className={className}>
      <Card>
        <CardHeader>
          <CardTitle>{title}</CardTitle>
          <CardDescription>Command output and logs</CardDescription>
        </CardHeader>
        <div className="bg-[var(--color-bg-primary)] p-4 rounded-b-xl min-h-[120px] font-mono text-xs space-y-1">
          {lines.length === 0 && (
            <span className="text-[var(--color-text-secondary)]">Terminal ready. Type a command...</span>
          )}
          {lines.map((line, i) => (
            <div key={i} className={TYPE_STYLES[line.type]}>
              <span className="text-[var(--color-text-secondary)] mr-2">$</span>
              {line.text}
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
