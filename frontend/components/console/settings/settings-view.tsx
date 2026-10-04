"use client";

import { useState } from "react";
import { CheckCircle2, Cpu, Plug, Save, ShieldCheck, Sliders } from "lucide-react";
import { PageHeader, Panel, PanelBody } from "@/components/console/ui/panel";
import { ConsoleTabs, type TabItem } from "@/components/console/ui/console-tabs";
import { useConsoleStore } from "@/store/console-store";
import { useConsolePreferences } from "@/store/console-settings-store";
import { useConsoleHydration } from "@/features/console/use-console";
import { relativeTime } from "@/lib/format";
import { ModelSettingsTab } from "./settings-model-tab";
import { IntegrationsTab } from "./settings-integrations-tab";
import { ObservabilityTab } from "./settings-observability-tab";
import { SecurityTab } from "./settings-security-tab";

const TABS: TabItem[] = [
  { id: "model", label: "Model Settings", icon: <Cpu className="h-3.5 w-3.5" /> },
  { id: "integrations", label: "Integrations", icon: <Plug className="h-3.5 w-3.5" /> },
  { id: "observability", label: "Observability", icon: <Sliders className="h-3.5 w-3.5" /> },
  { id: "security", label: "Security", icon: <ShieldCheck className="h-3.5 w-3.5" /> },
];

export function SettingsView() {
  useConsoleHydration("settings", "environment");
  const [tab, setTab] = useState("model");
  const [saving, setSaving] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);
  const updatedAt = useConsolePreferences((s) => s.updatedAt);
  const loadEnvironment = useConsoleStore((s) => s.loadEnvironment);
  const loadSettings = useConsoleStore((s) => s.loadSettings);
  const loadGovernance = useConsoleStore((s) => s.loadGovernance);
  const loadBenchmark = useConsoleStore((s) => s.loadBenchmark);

  function handleSave() {
    setSaving(true);
    setNotice(null);
    Promise.all([loadEnvironment(), loadSettings(), loadGovernance(), loadBenchmark()]).finally(
      () => {
        setSaving(false);
        setNotice(
          "Preferences saved in this browser. Service containers restart through docker compose, not from the browser."
        );
      }
    );
  }

  return (
    <div className="space-y-4">
      <PageHeader
        title="Settings"
        description="Model routing, integrations, observability thresholds and security policy"
        actions={
          <button
            type="button"
            onClick={handleSave}
            disabled={saving}
            className="flex items-center gap-1.5 rounded-lg bg-[var(--ecp-blue)] px-3 py-2 text-xs font-semibold text-white transition-opacity hover:opacity-90 disabled:opacity-50"
          >
            <Save className="h-3.5 w-3.5" />
            {saving ? "Applying…" : "Save & restart services"}
          </button>
        }
      />

      {notice && (
        <p className="flex items-center gap-2 rounded-lg border border-[var(--ecp-success)]/40 bg-[var(--ecp-success-soft)] px-3 py-2 text-[11px] text-[var(--ecp-success)]">
          <CheckCircle2 className="h-3.5 w-3.5" />
          {notice}
        </p>
      )}

      <Panel>
        <ConsoleTabs tabs={TABS} active={tab} onChange={setTab} className="px-3" />
        <PanelBody>
          {tab === "model" && <ModelSettingsTab />}
          {tab === "integrations" && <IntegrationsTab />}
          {tab === "observability" && <ObservabilityTab />}
          {tab === "security" && <SecurityTab />}
        </PanelBody>
      </Panel>

      <p className="text-[11px] text-[var(--ecp-text-dim)]">
        Preferences last written {relativeTime(updatedAt)}.
      </p>
    </div>
  );
}