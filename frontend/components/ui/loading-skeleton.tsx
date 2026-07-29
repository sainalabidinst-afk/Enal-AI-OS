"use client";

export function CardSkeleton() {
  return (
    <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4 animate-pulse">
      <div className="h-3 w-24 bg-[var(--color-bg-tertiary)] rounded mb-2" />
      <div className="h-8 w-16 bg-[var(--color-bg-tertiary)] rounded mb-1" />
      <div className="h-3 w-32 bg-[var(--color-bg-tertiary)] rounded" />
    </div>
  );
}

export function ListSkeleton({ rows = 5 }: { rows?: number }) {
  return (
    <div className="space-y-3 animate-pulse">
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="flex items-center gap-3 rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-3">
          <div className="h-4 w-4 bg-[var(--color-bg-tertiary)] rounded" />
          <div className="flex-1 space-y-2">
            <div className="h-3 w-3/4 bg-[var(--color-bg-tertiary)] rounded" />
            <div className="h-3 w-1/2 bg-[var(--color-bg-tertiary)] rounded" />
          </div>
        </div>
      ))}
    </div>
  );
}

export function PageSkeleton() {
  return (
    <div className="max-w-5xl mx-auto p-6 space-y-6 animate-pulse">
      <div className="h-8 w-48 bg-[var(--color-bg-tertiary)] rounded" />
      <div className="h-4 w-72 bg-[var(--color-bg-tertiary)] rounded" />
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <CardSkeleton />
        <CardSkeleton />
        <CardSkeleton />
      </div>
      <div className="h-48 bg-[var(--color-bg-secondary)] rounded-xl border border-[var(--color-border)]" />
    </div>
  );
}

export function TableSkeleton({ rows = 5, cols = 4 }: { rows?: number; cols?: number }) {
  return (
    <div className="animate-pulse space-y-2">
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="flex gap-4">
          {Array.from({ length: cols }).map((_, j) => (
            <div
              key={j}
              className="h-4 bg-[var(--color-bg-tertiary)] rounded"
              style={{ width: `${60 + Math.random() * 40}%` }}
            />
          ))}
        </div>
      ))}
    </div>
  );
}

