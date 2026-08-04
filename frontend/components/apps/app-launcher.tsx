"use client";

import { useState } from "react";
import Link from "next/link";
import { Search, Settings } from "lucide-react";
import {
  CAPABILITY_APPS,
  searchCapabilityApps,
  type CapabilityApp,
} from "./capability-registry";
import { CapabilityCard } from "./capability-card";
import { useLauncherStore } from "@/store/launcher-store";
import { useAuthStore } from "@/store/auth-store";

interface AppLauncherProps {
  title?: string;
  subtitle?: string;
  apps?: CapabilityApp[];
  showSearch?: boolean;
  showFavorites?: boolean;
  showRecent?: boolean;
  showHeader?: boolean;
}

export function AppLauncher({
  title = "AI Capabilities",
  subtitle = "Select a capability to launch its workspace",
  apps = CAPABILITY_APPS,
  showSearch = true,
  showFavorites = true,
  showRecent = true,
  showHeader = true,
}: AppLauncherProps) {
  const [query, setQuery] = useState("");
  const favorites = useLauncherStore((s) => s.favorites);
  const recent = useLauncherStore((s) => s.recent);
  const user = useAuthStore((s) => s.user);

  const filtered = searchCapabilityApps(query).filter((app) =>
    apps.some((a) => a.id === app.id)
  );

  const favoriteApps = apps.filter((app) => favorites.includes(app.id));
  const recentApps = recent
    .map((id) => apps.find((a) => a.id === id))
    .filter((a): a is CapabilityApp => Boolean(a));

  return (
    <div className="mx-auto max-w-6xl p-6 space-y-8">
      {/* Header */}
      {showHeader && (
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-[var(--color-text-primary)]">
              {title}
            </h1>
            <p className="text-xs text-[var(--color-text-secondary)]">
              Version 1.0.0
            </p>
          </div>
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <div className="h-8 w-8 rounded-full bg-[var(--color-accent)] flex items-center justify-center text-sm text-white font-medium">
                {user?.username?.charAt(0).toUpperCase() || "U"}
              </div>
              <span className="hidden sm:block text-sm text-[var(--color-text-secondary)]">
                {user?.username || "User"}
              </span>
            </div>
            <Link
              href="/settings"
              className="rounded-lg p-2 text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)] hover:text-[var(--color-text-primary)] transition-colors"
              aria-label="Settings"
            >
              <Settings className="h-5 w-5" />
            </Link>
          </div>
        </div>
      )}

      {/* Search */}
      {showSearch && (
        <div className="relative mx-auto max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[var(--color-text-secondary)]" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search Capability..."
            className="w-full rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] py-2.5 pl-10 pr-4 text-sm text-[var(--color-text-primary)] placeholder:text-[var(--color-text-secondary)] focus:border-[var(--color-accent)] focus:outline-none focus:ring-1 focus:ring-[var(--color-accent)]"
          />
        </div>
      )}

      {/* Favorites */}
      {showFavorites && favoriteApps.length > 0 && (
        <section className="space-y-3">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-[var(--color-text-secondary)]">
            ⭐ Favorites
          </h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
            {favoriteApps.map((app) => (
              <CapabilityCard key={app.id} app={app} />
            ))}
          </div>
        </section>
      )}

      {/* Recent */}
      {showRecent && recentApps.length > 0 && (
        <section className="space-y-3">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-[var(--color-text-secondary)]">
            🕒 Recent
          </h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
            {recentApps.map((app) => (
              <CapabilityCard key={app.id} app={app} />
            ))}
          </div>
        </section>
      )}

      {/* All capabilities */}
      <section className="space-y-3">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-[var(--color-text-secondary)]">
          🧩 Capabilities
        </h2>
        {filtered.length > 0 ? (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
            {filtered.map((app) => (
              <CapabilityCard key={app.id} app={app} />
            ))}
          </div>
        ) : (
          <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-10 text-center">
            <p className="text-lg mb-2">🔍</p>
            <p className="text-sm text-[var(--color-text-secondary)]">
              No capability found for "{query}"
            </p>
          </div>
        )}
      </section>
    </div>
  );
}
