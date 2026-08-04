import { AppShell } from "@/components/apps/app-shell";
import { AppComingSoon } from "@/components/apps/app-coming-soon";
import { findCapabilityApp } from "@/components/apps/capability-registry";

export default function SecurityAppPage() {
  const app = findCapabilityApp("security")!;
  return (
    <AppShell app={app}>
      <AppComingSoon app={app} />
    </AppShell>
  );
}
