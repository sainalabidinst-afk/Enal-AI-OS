"use client";

import dynamic from "next/dynamic";
import { PageSkeleton } from "@/components/ui/loading-skeleton";

const DatabaseWorkspace = dynamic(
  () =>
    import("@/components/workspace/apps/database-workspace").then((m) => ({
      default: m.DatabaseWorkspace,
    })),
  {
    loading: () => <PageSkeleton />,
    ssr: false,
  }
);

export default function DatabaseWorkspacePage() {
  return <DatabaseWorkspace />;
}
