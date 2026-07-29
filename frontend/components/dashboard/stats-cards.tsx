"use client";

interface StatsCardsProps {
  capabilities: number;
  workspaces: number;
  activeExecutions: number;
  completedExecutions: number;
  isLoading: boolean;
}

function StatCard({
  title,
  value,
  subtitle,
  icon,
  isLoading,
}: {
  title: string;
  value: number | string;
  subtitle?: string;
  icon: string;
  isLoading: boolean;
}) {
  if (isLoading) {
    return (
      <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4 animate-pulse">
        <div className="h-3 w-20 bg-[var(--color-bg-tertiary)] rounded mb-2" />
        <div className="h-8 w-12 bg-[var(--color-bg-tertiary)] rounded mb-1" />
        <div className="h-3 w-28 bg-[var(--color-bg-tertiary)] rounded" />
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4 transition-colors hover:border-[var(--color-text-secondary)]">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-[var(--color-text-secondary)]">
            {title}
          </p>
          <p className="text-2xl font-semibold mt-1 text-[var(--color-text-primary)]">
            {value}
          </p>
          {subtitle && (
            <p className="text-xs text-[var(--color-text-secondary)] mt-1">{subtitle}</p>
          )}
        </div>
        <span className="text-xl">{icon}</span>
      </div>
    </div>
  );
}

export function StatsCards({
  capabilities,
  workspaces,
  activeExecutions,
  completedExecutions,
  isLoading,
}: StatsCardsProps) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <StatCard
        title="Capabilities"
        value={capabilities}
        subtitle="Registered capability packs"
        icon="🧩"
        isLoading={isLoading}
      />
      <StatCard
        title="Workspaces"
        value={workspaces}
        subtitle="Active workspaces"
        icon="📁"
        isLoading={isLoading}
      />
      <StatCard
        title="Active Executions"
        value={activeExecutions}
        subtitle="Currently running"
        icon="⚡"
        isLoading={isLoading}
      />
      <StatCard
        title="Completed"
        value={completedExecutions}
        subtitle="Total completed"
        icon="✅"
        isLoading={isLoading}
      />
    </div>
  );
}

