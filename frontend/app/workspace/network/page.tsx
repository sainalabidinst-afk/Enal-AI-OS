"use client";

import dynamic from "next/dynamic";
import { PageSkeleton } from "@/components/ui/loading-skeleton";

const NetworkWorkspace = dynamic(
  () =>
    import("@/components/workspace/apps/network-workspace").then((m) => ({
      default: m.NetworkWorkspace,
    })),
  {
    loading: () => <PageSkeleton />,
    ssr: false,
  }
);

export default function NetworkWorkspacePage() {
  return <NetworkWorkspace />;
}
