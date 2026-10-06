'use client';

import ReactMarkdown from 'react-markdown';

interface MarkdownRendererProps {
  content: string;
  className?: string;
}

export function MarkdownRenderer({ content, className }: MarkdownRendererProps) {
  return (
    <div className={className}>
      <ReactMarkdown
        components={{
          h1: ({ children }) => <h1 className="text-xl font-semibold">{children}</h1>,
          h2: ({ children }) => <h2 className="text-lg font-semibold">{children}</h2>,
          h3: ({ children }) => <h3 className="text-base font-semibold">{children}</h3>,
          p: ({ children }) => <p className="mb-2 text-sm text-text-secondary">{children}</p>,
          ul: ({ children }) => <ul className="mb-2 list-inside list-disc text-sm text-text-secondary">{children}</ul>,
          ol: ({ children }) => <ol className="mb-2 list-inside list-decimal text-sm text-text-secondary">{children}</ol>,
          code: ({ children }) => (
            <code className="rounded bg-surface-tertiary px-1.5 py-0.5 font-mono text-xs text-text-primary">
              {children}
            </code>
          ),
          pre: ({ children }) => (
            <pre className="overflow-auto rounded-md border border-border bg-surface-primary p-4 font-mono text-xs text-text-secondary">
              {children}
            </pre>
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
