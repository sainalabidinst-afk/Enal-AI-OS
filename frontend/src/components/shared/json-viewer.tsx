'use client';

import { cn } from '@/lib/cn';

interface JsonViewerProps {
  data: unknown;
  className?: string;
}

export function JsonViewer({ data, className }: JsonViewerProps) {
  const jsonString = JSON.stringify(data, null, 2);

  return (
    <pre
      className={cn(
        'overflow-auto rounded-md border border-border bg-surface-primary p-4 font-mono text-xs text-text-secondary',
        className
      )}
    >
      {jsonString}
    </pre>
  );
}
