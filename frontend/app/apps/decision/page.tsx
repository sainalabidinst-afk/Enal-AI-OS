import { AppShell } from "@/components/apps/app-shell";
import { AppComingSoon } from "@/components/apps/app-coming-soon";
import { findCapabilityApp } from "@/components/apps/capability-registry";

export default function DecisionAppPage() {
  const app = findCapabilityApp("decision")!;
  return (
    <AppShell app={app}>
      <AppComingSoon app={app} />
    </AppShell>
  );
}
