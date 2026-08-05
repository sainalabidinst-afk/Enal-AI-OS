"use client";

import { type ReactNode } from "react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

interface MarkdownViewerProps {
  title?: string;
  content?: string;
  className?: string;
}

export function MarkdownViewer({ title = "Document", content = "", className }: MarkdownViewerProps) {
  return (
    <div className={className}>
      <Card>
        <CardHeader>
          <CardTitle>{title}</CardTitle>
          <CardDescription>Markdown content</CardDescription>
        </CardHeader>
        <div className="p-4 prose prose-sm max-w-none rounded-b-xl border-t border-[var(--color-border)]">
          {content ? (
            <div className="whitespace-pre-wrap text-sm text-[var(--color-text-primary)]">{content}</div>
          ) : (
            <span className="text-sm text-[var(--color-text-secondary)]">No content yet.</span>
          )}
        </div>
      </Card>
    </div>
  );
}
