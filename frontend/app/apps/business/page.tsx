import { AppShell } from "@/components/apps/app-shell";
import { AppComingSoon } from "@/components/apps/app-coming-soon";
import { findCapabilityApp } from "@/components/apps/capability-registry";

export default function BusinessAppPage() {
  const app = findCapabilityApp("business")!;
  return (
    <AppShell app={app}>
      <AppComingSoon app={app} />
    </AppShell>
  );
}
