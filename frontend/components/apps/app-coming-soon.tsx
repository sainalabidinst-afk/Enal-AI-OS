"use client";

import type { CapabilityApp } from "./capability-registry";

export function AppComingSoon({ app }: { app: CapabilityApp }) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] p-10 text-center">
      <div
        className="flex h-20 w-20 items-center justify-center rounded-3xl text-4xl mb-6"
        style={{ backgroundColor: `${app.color}1a` }}
      >
        <span>{app.icon}</span>
      </div>
      <h2 className="text-2xl font-bold text-[var(--color-text-primary)] mb-2">
        {app.name}
      </h2>
      <p className="text-sm text-[var(--color-text-secondary)] max-w-md mb-6">
        {app.description}
      </p>
      <div className="rounded-xl border border-dashed border-[var(--color-border)] px-6 py-3">
        <p className="text-xs text-[var(--color-text-secondary)]">
          Workspace is coming soon
        </p>
      </div>
    </div>
  );
}
