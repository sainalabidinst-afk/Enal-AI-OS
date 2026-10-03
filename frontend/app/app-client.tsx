"use client";

import { useEffect } from "react";
import { Providers } from "./providers";
import { MainLayout } from "@/components/layouts/main-layout";

export default function AppClient({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    if (typeof window !== "undefined" && "serviceWorker" in navigator) {
      navigator.serviceWorker
        .register("/sw.js")
        .then((registration) => {
          console.log("Service Worker registered:", registration.scope);
        })
        .catch((error) => {
          console.error("Service Worker registration failed:", error);
        });
    }
  }, []);

  return (
    <Providers>
      <MainLayout>{children}</MainLayout>
    </Providers>
  );
}
