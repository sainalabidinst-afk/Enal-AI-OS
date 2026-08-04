"use client";

import Link from "next/link";
import { Star } from "lucide-react";
import type { CapabilityApp, CapabilityStatus } from "./capability-registry";
import { useLauncherStore } from "@/store/launcher-store";

interface CapabilityCardProps {
  app: CapabilityApp;
  onToggleFavorite?: (appId: string) => void;
}

const STATUS_STYLES: Record<CapabilityStatus, string> = {
  Ready: "bg-[var(--color-success)]/15 text-[var(--color-success)]",
  Beta: "bg-[var(--color-warning)]/15 text-[var(--color-warning)]",
  "Coming Soon": "bg-[var(--color-bg-tertiary)] text-[var(--color-text-secondary)]",
  Installed: "bg-[var(--color-accent)]/15 text-[var(--color-accent)]",
};

export function CapabilityCard({ app, onToggleFavorite }: CapabilityCardProps) {
  const isFavorite = useLauncherStore((s) => s.isFavorite(app.id));
  const toggleFavorite = useLauncherStore((s) => s.toggleFavorite);

  const handleFavorite = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    toggleFavorite(app.id);
    onToggleFavorite?.(app.id);
  };

  const statusClass = STATUS_STYLES[app.status] || STATUS_STYLES["Coming Soon"];

  return (
    <Link
      href={app.route}
      className="group relative flex flex-col items-center justify-center gap-3 rounded-2xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-6 text-center transition-all hover:border-[var(--color-accent)] hover:shadow-lg hover:-translate-y-0.5"
    >
      {/* Favorite star */}
      <button
        onClick={handleFavorite}
        aria-label="Toggle favorite"
        className={`absolute top-2 right-2 rounded-md p-1 transition-colors ${
          isFavorite
            ? "text-[var(--color-warning)]"
            : "text-[var(--color-text-secondary)] opacity-0 group-hover:opacity-100 hover:text-[var(--color-warning)]"
        }`}
      >
        <Star className="h-4 w-4" fill={isFavorite ? "currentColor" : "none"} />
      </button>

      {/* Status badge */}
      <span
        className={`absolute top-2 left-2 rounded-full px-2 py-0.5 text-[9px] font-semibold uppercase tracking-wide ${statusClass}`}
      >
        {app.status}
      </span>

      {/* Icon */}
      <div
        className="flex h-16 w-16 items-center justify-center rounded-2xl text-3xl"
        style={{ backgroundColor: `${app.color}1a` }}
      >
        <span>{app.icon}</span>
      </div>

      {/* Name */}
      <p className="text-sm font-semibold text-[var(--color-text-primary)]">
        {app.name}
      </p>

      {/* Category + version */}
      <p className="text-[10px] text-[var(--color-text-secondary)]">
        {app.category} · v{app.version}
      </p>

      {/* Description */}
      <p className="text-xs text-[var(--color-text-secondary)] line-clamp-2">
        {app.description}
      </p>
    </Link>
  );
}
