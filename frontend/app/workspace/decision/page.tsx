"use client";

import dynamic from "next/dynamic";
import { PageSkeleton } from "@/components/ui/loading-skeleton";

const DecisionWorkspace = dynamic(
  () =>
    import("@/components/workspace/apps/decision-workspace").then((m) => ({
      default: m.DecisionWorkspace,
    })),
  {
    loading: () => <PageSkeleton />,
    ssr: false,
  }
);

export default function DecisionWorkspacePage() {
  return <DecisionWorkspace />;
}
