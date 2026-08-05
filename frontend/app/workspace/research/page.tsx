"use client";

import dynamic from "next/dynamic";
import { PageSkeleton } from "@/components/ui/loading-skeleton";

const ResearchWorkspace = dynamic(
  () =>
    import("@/components/workspace/apps/research-workspace").then((m) => ({
      default: m.ResearchWorkspace,
    })),
  {
    loading: () => <PageSkeleton />,
    ssr: false,
  }
);

export default function ResearchWorkspacePage() {
  return <ResearchWorkspace />;
}
