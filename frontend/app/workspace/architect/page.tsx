"use client";

import dynamic from "next/dynamic";
import { PageSkeleton } from "@/components/ui/loading-skeleton";

const ArchitectWorkspace = dynamic(
  () =>
    import("@/components/workspace/apps/architect-workspace").then((m) => ({
      default: m.ArchitectWorkspace,
    })),
  {
    loading: () => <PageSkeleton />,
    ssr: false,
  }
);

export default function ArchitectWorkspacePage() {
  return <ArchitectWorkspace />;
}
