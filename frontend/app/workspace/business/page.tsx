"use client";

import dynamic from "next/dynamic";
import { PageSkeleton } from "@/components/ui/loading-skeleton";

const BusinessWorkspace = dynamic(
  () =>
    import("@/components/workspace/apps/business-workspace").then((m) => ({
      default: m.BusinessWorkspace,
    })),
  {
    loading: () => <PageSkeleton />,
    ssr: false,
  }
);

export default function BusinessWorkspacePage() {
  return <BusinessWorkspace />;
}
