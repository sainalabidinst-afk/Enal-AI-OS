e"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/store/auth-store";
import { useEulaStore } from "@/store/eula-store";

export default function HomePage() {
  const router = useRouter();
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const initialize = useAuthStore((s) => s.initialize);
  const hasAccepted = useEulaStore((s) => s.hasAccepted);

  useEffect(() => {
    initialize();
  }, [initialize]);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login");
    } else if (!hasAccepted()) {
      router.push("/eula");
    } else {
      router.push("/dashboard");
    }
  }, [isAuthenticated, hasAccepted, router]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-[var(--color-bg-primary)]">
      <div className="text-center">
        <div className="text-5xl mb-4">🧠</div>
        <h1 className="text-2xl font-bold text-[var(--color-text-primary)]">
          Enal AI OS
        </h1>
        <p className="text-sm text-[var(--color-text-secondary)] mt-1">
          Artificial Intelligence Operating System
        </p>
        <div className="mt-6 animate-spin h-8 w-8 border-2 border-[var(--color-accent)] border-t-transparent rounded-full mx-auto" />
      </div>
    </div>
  );
}
