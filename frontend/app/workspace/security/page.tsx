"use client";

import dynamic from "next/dynamic";
import { PageSkeleton } from "@/components/ui/loading-skeleton";

const SecurityWorkspace = dynamic(
  () =>
    import("@/components/workspace/apps/security-workspace").then((m) => ({
      default: m.SecurityWorkspace,
    })),
  {
    loading: () => <PageSkeleton />,
    ssr: false,
  }
);

export default function SecurityWorkspacePage() {
  return <SecurityWorkspace />;
}
