"use client";

import dynamic from "next/dynamic";
import { PageSkeleton } from "@/components/ui/loading-skeleton";

const TradingWorkspace = dynamic(
  () =>
    import("@/components/workspace/apps/trading-workspace").then((m) => ({
      default: m.TradingWorkspace,
    })),
  {
    loading: () => <PageSkeleton />,
    ssr: false,
  }
);

export default function TradingWorkspacePage() {
  return <TradingWorkspace />;
}
