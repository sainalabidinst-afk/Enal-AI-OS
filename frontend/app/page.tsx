"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/store/auth-store";
import { useEulaStore } from "@/store/eula-store";

type BootStep = {
  label: string;
  status: "pending" | "running" | "done";
};

export default function HomePage() {
  const router = useRouter();
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const initialize = useAuthStore((s) => s.initialize);
  const hasAccepted = useEulaStore((s) => s.hasAccepted);

  const [steps, setSteps] = useState<BootStep[]>([
    { label: "Initializing...", status: "running" },
    { label: "Checking Authentication...", status: "pending" },
    { label: "Loading Workspace...", status: "pending" },
    { label: "Capability Registry", status: "pending" },
  ]);

  useEffect(() => {
    initialize();
  }, [initialize]);

  // Drive boot sequence progress
  useEffect(() => {
    const timers: ReturnType<typeof setTimeout>[] = [];
    steps.forEach((_, i) => {
      timers.push(
        setTimeout(() => {
          setSteps((prev) =>
            prev.map((s, j) =>
              j === i ? { ...s, status: "done" } : j === i + 1 ? { ...s, status: "running" } : s
            )
          );
        }, 400 * (i + 1))
      );
    });
    return () => timers.forEach(clearTimeout);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Route once boot sequence done
  useEffect(() => {
    const t = setTimeout(() => {
      if (!isAuthenticated) {
        router.push("/login");
      } else if (!hasAccepted()) {
        router.push("/eula");
      } else {
        router.push("/dashboard");
      }
    }, 400 * steps.length + 400);
    return () => clearTimeout(t);
  }, [isAuthenticated, hasAccepted, router, steps.length]);

  const doneCount = steps.filter((s) => s.status === "done").length;

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-[var(--color-bg-primary)]">
      <div className="w-full max-w-sm text-center space-y-8">
        {/* Logo */}
        <div className="space-y-2">
          <div className="text-5xl mb-2">🧠</div>
          <h1 className="text-2xl font-bold text-[var(--color-text-primary)]">
            Enal AI OS
          </h1>
          <p className="text-sm text-[var(--color-text-secondary)]">
            Artificial Intelligence Operating System
          </p>
        </div>

        {/* Progress bar */}
        <div className="w-full bg-[var(--color-bg-tertiary)] rounded-full h-1.5 overflow-hidden">
          <div
            className="h-full bg-[var(--color-accent)] rounded-full transition-all duration-500"
            style={{ width: `${(doneCount / steps.length) * 100}%` }}
          />
        </div>

        {/* Boot steps */}
        <div className="space-y-2 text-left">
          {steps.map((step) => (
            <div key={step.label} className="flex items-center gap-2 text-sm">
              {step.status === "done" ? (
                <span className="text-[var(--color-success)]">✓</span>
              ) : step.status === "running" ? (
                <span className="inline-block h-3 w-3 border-2 border-[var(--color-accent)] border-t-transparent rounded-full animate-spin" />
              ) : (
                <span className="inline-block h-3 w-3 rounded-full border border-[var(--color-border)]" />
              )}
              <span
                className={
                  step.status === "done"
                    ? "text-[var(--color-text-primary)]"
                    : step.status === "running"
                    ? "text-[var(--color-text-secondary)]"
                    : "text-[var(--color-text-secondary)]/50"
                }
              >
                {step.label}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
