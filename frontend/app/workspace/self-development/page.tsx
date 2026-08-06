"use client";

import dynamic from "next/dynamic";
import { PageSkeleton } from "@/components/ui/loading-skeleton";

const SelfDevelopmentWorkspace = dynamic(
  () =>
    import("@/components/workspace/apps/self-development-workspace").then((m) => ({
      default: m.SelfDevelopmentWorkspace,
    })),
  {
    loading: () => <PageSkeleton />,
    ssr: false,
  }
);

export default function SelfDevelopmentWorkspacePage() {
  return <SelfDevelopmentWorkspace />;
}
