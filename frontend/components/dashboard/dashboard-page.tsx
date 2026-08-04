"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
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

  // If not authenticated or EULA not accepted, render nothing (redirecting)
  if (!isAuthenticated || !hasAccepted()) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[var(--color-bg-primary)]">
        <div className="animate-spin h-8 w-8 border-2 border-[var(--color-accent)] border-t-transparent rounded-full" />
      </div>
    );
  }

  return (
    <AppLauncher
      title="Enal AI OS"
      subtitle="AI Operating System — Select a capability to launch"
    />
  );
}
