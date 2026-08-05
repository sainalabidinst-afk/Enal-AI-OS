import { type ReactNode } from "react";
import { cn } from "@/lib/utils";
import { Card, CardHeader, CardTitle } from "@/components/design-system/layout/card";

interface CodeBlockProps {
  code: string;
  language?: string;
  filename?: string;
  lineNumbers?: boolean;
  className?: string;
}

export function CodeBlock({ code, language = "plaintext", filename, lineNumbers = true, className }: CodeBlockProps) {
  const lines = code.split("\n");

  return (
    <Card className={className}>
      {(filename || language) && (
        <CardHeader>
          <div className="flex items-center justify-between">
            {filename && <CardTitle>{filename}</CardTitle>}
            <span className="text-xs text-[var(--color-secondary-500)]">{language}</span>
          </div>
        </CardHeader>
      )}
      <div className="overflow-x-auto">
        <pre className="text-xs text-[var(--color-foreground)] bg-[var(--color-secondary-50)] p-4 rounded-b-xl">
          {lines.map((line, i) => (
            <div key={i} className="flex">
              {lineNumbers && (
                <span className="w-8 shrink-0 text-right pr-3 text-[var(--color-secondary-400)] select-none border-r border-[var(--color-border)] mr-3 opacity-60">
                  {i + 1}
                </span>
              )}
              <span>{line || "\u00A0"}</span>
            </div>
          ))}
        </pre>
      </div>
    </Card>
  );
}
