"use client";

import { type ReactNode } from "react";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";

interface CodeViewerProps {
  code?: string;
  language?: string;
  filename?: string;
  lineNumbers?: boolean;
  className?: string;
}

export function CodeViewer({
  code = "// Code will appear here",
  language = "plaintext",
  filename,
  lineNumbers = true,
  className,
}: CodeViewerProps) {
  const lines = code.split("\n");

  return (
    <div className={className}>
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>{filename || "Code"}</CardTitle>
            <span className="text-xs text-[var(--color-text-secondary)]">{language}</span>
          </div>
        </CardHeader>
        <div className="overflow-x-auto">
          <pre className="text-xs text-[var(--color-text-secondary)] bg-[var(--color-bg-primary)] p-4 rounded-b-xl">
            {lines.map((line, i) => (
              <div key={i} className="flex">
                {lineNumbers && (
                    <span className="w-8 shrink-0 text-right pr-3 text-[var(--color-text-secondary)] select-none border-r border-[var(--color-border)] mr-3 opacity-60">
                    {i + 1}
                  </span>
                )}
                <span>{line || "\u00A0"}</span>
              </div>
            ))}
          </pre>
        </div>
      </Card>
    </div>
  );
}
