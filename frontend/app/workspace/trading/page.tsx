"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function TradingWorkspacePage() {
  const router = useRouter();

  useEffect(() => {
    router.replace("/console/trading");
  }, [router]);

  return (
    <div className="flex h-screen items-center justify-center">
      <div className="text-center">
        <p className="text-sm text-[var(--color-text-secondary)]">
          Redirecting to <a href="/console/trading" className="text-[var(--color-accent)] underline">/console/trading</a>…
        </p>
      </div>
    </div>
  );
}
