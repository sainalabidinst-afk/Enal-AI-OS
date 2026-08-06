"use client";

import dynamic from "next/dynamic";
import { PageSkeleton } from "@/components/ui/loading-skeleton";

const DevOpsWorkspace = dynamic(
  () =>
    import("@/components/workspace/apps/devops-workspace").then((m) => ({
      default: m.DevOpsWorkspace,
    })),
  {
    loading: () => <PageSkeleton />,
    ssr: false,
  }
);

export default function DevOpsWorkspacePage() {
  return <DevOpsWorkspace />;
}
