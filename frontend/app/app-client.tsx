"use client";

import { Providers } from "./providers";
import { MainLayout } from "@/components/layouts/main-layout";

export default function AppClient({ children }: { children: React.ReactNode }) {
  return (
    <Providers>
      <MainLayout>{children}</MainLayout>
    </Providers>
  );
}
