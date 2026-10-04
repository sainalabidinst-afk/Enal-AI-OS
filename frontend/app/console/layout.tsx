import type { Metadata } from "next";
import { ConsoleShell } from "@/components/console/layout/console-shell";

export const metadata: Metadata = {
  title: "ECP Console",
  description: "Governance, benchmark, builder and marketplace console for ECP",
};

export default function ConsoleLayout({ children }: { children: React.ReactNode }) {
  return <ConsoleShell>{children}</ConsoleShell>;
}