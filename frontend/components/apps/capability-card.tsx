"use client";

import Link from "next/link";
import { Star } from "lucide-react";
import type { CapabilityApp } from "./capability-registry";
import { useLauncherStore } from "@/store/launcher-store";

interface CapabilityCardProps {
  app: CapabilityApp;
  onToggleFavorite?: (appId: string) => void;
}

export function CapabilityCard({ app, onToggleFavorite }: CapabilityCardProps) {
  const isFavorite = useLauncherStore((s) => s.isFavorite(app.id));
  const toggleFavorite = useLauncherStore((s) => s.toggleFavorite);

  const handleFavorite = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    toggleFavorite(app.id);
    onToggleFavorite?.(app.id);
  };

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

      {/* Description */}
      <p className="text-xs text-[var(--color-text-secondary)] line-clamp-2">
        {app.description}
      </p>
    </Link>
  );
}
