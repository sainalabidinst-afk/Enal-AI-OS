"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Activity } from "lucide-react";
import { useAuthStore } from "@/store/auth-store";
import { useEulaStore } from "@/store/eula-store";
import { AppLauncher } from "@/components/apps/app-launcher";

export function DashboardPage() {
  const router = useRouter();
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const hasAccepted = useEulaStore((s) => s.hasAccepted);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login");
      return;
    }
    if (!hasAccepted()) {
      router.push("/eula");
    }
  }, [isAuthenticated, hasAccepted, router]);

  if (!isAuthenticated || !hasAccepted()) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[var(--color-bg-primary)]">
        <div className="animate-spin h-8 w-8 border-2 border-[var(--color-accent)] border-t-transparent rounded-full" />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-6xl p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-[var(--color-text-primary)]">
            Enal AI OS
          </h1>
          <p className="text-xs text-[var(--color-text-secondary)]">
            AI Operating System — Select a capability to launch
          </p>
        </div>
        <Link
          href="/capabilities/lifecycle"
          className="inline-flex items-center gap-2 rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] px-3 py-2 text-sm text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)] hover:text-[var(--color-text-primary)] transition-colors"
        >
          <Activity className="h-4 w-4" />
          Capability Lifecycle
        </Link>
      </div>
      <AppLauncher
        title="Capabilities"
        subtitle="Select a capability to launch its workspace"
        showHeader={false}
      />
    </div>
  );
}
