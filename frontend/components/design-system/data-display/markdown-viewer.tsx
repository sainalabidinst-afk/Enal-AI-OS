import { type ReactNode } from "react";
import { cn } from "@/lib/utils";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/design-system/layout/card";

interface MarkdownViewerProps {
  title?: string;
  description?: string;
  content: string;
  className?: string;
}

export function MarkdownViewer({ title, description, content, className }: MarkdownViewerProps) {
  return (
    <Card className={className}>
      {(title || description) && (
        <CardHeader>
          {title && <CardTitle>{title}</CardTitle>}
          {description && <CardDescription>{description}</CardDescription>}
        </CardHeader>
      )}
      <div className="p-4 prose prose-sm max-w-none border-t border-[var(--color-border)]">
        <div className="whitespace-pre-wrap text-sm text-[var(--color-foreground)]">{content}</div>
      </div>
    </Card>
  );
}
