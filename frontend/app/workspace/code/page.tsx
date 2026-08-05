"use client";

import dynamic from "next/dynamic";
import { PageSkeleton } from "@/components/ui/loading-skeleton";

const CodeWorkspace = dynamic(
  () =>
    import("@/components/workspace/apps/code-workspace").then((m) => ({
      default: m.CodeWorkspace,
    })),
  {
    loading: () => <PageSkeleton />,
    ssr: false,
  }
);

export default function CodeWorkspacePage() {
  return <CodeWorkspace />;
}
