"use client";

import type { CapabilityApp } from "./capability-registry";

export function AppComingSoon({ app }: { app: CapabilityApp }) {
  return (
    <div className="flex h-[calc(100vh-64px)]">
      {/* Sidebar (empty scaffold) */}
      <aside className="hidden md:flex w-56 flex-col border-r border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-3 gap-1">
        <p className="px-2 py-1 text-[10px] uppercase tracking-wide text-[var(--color-text-secondary)]">
          Workspace
        </p>
        {Array.from({ length: 6 }).map((_, i) => (
          <div
            key={i}
            className="h-8 rounded-lg bg-[var(--color-bg-tertiary)]/50 animate-pulse"
          />
        ))}
      </aside>

      {/* Main area: workspace + right panel */}
      <div className="flex flex-1 flex-col">
        <div className="flex flex-1">
          {/* Workspace area */}
          <main className="flex-1 flex flex-col items-center justify-center p-8">
            <div
              className="flex h-20 w-20 items-center justify-center rounded-3xl text-4xl mb-6"
              style={{ backgroundColor: `${app.color}1a` }}
            >
              <span>{app.icon}</span>
            </div>
            <h2 className="text-2xl font-bold text-[var(--color-text-primary)] mb-2">
              {app.name}
            </h2>
            <p className="text-sm text-[var(--color-text-secondary)] max-w-md mb-6 text-center">
              {app.description}
            </p>
            <div className="rounded-xl border border-dashed border-[var(--color-border)] px-6 py-3">
              <p className="text-xs text-[var(--color-text-secondary)]">
                Workspace is coming soon
              </p>
            </div>
          </main>

          {/* Right panel (empty scaffold) */}
          <aside className="hidden lg:flex w-72 flex-col border-l border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-3 gap-1">
            <p className="px-2 py-1 text-[10px] uppercase tracking-wide text-[var(--color-text-secondary)]">
              AI Panel
            </p>
            {Array.from({ length: 8 }).map((_, i) => (
              <div
                key={i}
                className="h-10 rounded-lg bg-[var(--color-bg-tertiary)]/50 animate-pulse"
              />
            ))}
          </aside>
        </div>
      </div>
    </div>
  );
}
