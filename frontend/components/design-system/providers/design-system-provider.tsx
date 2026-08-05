"use client";

import { type ReactNode } from "react";
import { ThemeProvider } from "@/components/design-system/theme/theme-provider";

export function DesignSystemProvider({ children }: { children: ReactNode }) {
  return (
    <ThemeProvider>
      {children}
    </ThemeProvider>
  );
}
