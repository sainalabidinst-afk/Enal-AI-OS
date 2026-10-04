"use client";

import { Field, Toggle, inputClass } from "@/components/console/ui/controls";
import { EmptyBlock, Pill } from "@/components/console/ui/states";
import { useConsoleStore } from "@/store/console-store";
import { useConsolePreferences } from "@/store/console-settings-store";
import { titleCase } from "@/lib/format";

export function SecurityTab() {
  const guardrails = useConsoleStore((s) => s.guardrails);
  const policies = useConsoleStore((s) => s.policies);
  const prefs = useConsolePreferences();
  const setPref = useConsolePreferences((s) => s.set);
  const toggleGuardrail = useConsolePreferences((s) => s.toggleGuardrail);

  const rails = guardrails.data ?? [];
  const policyList = policies.data ?? [];

  return (
    <div className="grid gap-4 lg:grid-cols-2">
      <div className="space-y-3">
        <h3 className="text-[11px] font-semibold uppercase tracking-wide text-[var(--ecp-text-dim)]">
          Guardrails
        </h3>
        {guardrails.error ? (
          <p className="text-[11px] text-[var(--ecp-danger)]">{guardrails.error}</p>
        ) : rails.length === 0 ? (
          <EmptyBlock title="No guardrails reported" />
        ) : (
          rails.map((rail) => (
            <Toggle
              key={rail.name}
              checked={Boolean(prefs.guardrails[rail.name])}
              onChange={() => toggleGuardrail(rail.name)}
              label={titleCase(rail.name)}
              description={rail.description}
            />
          ))
        )}
      </div>

      <div className="space-y-3">
        <h3 className="text-[11px] font-semibold uppercase tracking-wide text-[var(--ecp-text-dim)]">
          Policy controls
        </h3>
        <Field label="Rate limit (requests / minute)">
          <input
            type="number"
            value={prefs.rateLimitPerMinute}
            onChange={(event) => setPref("rateLimitPerMinute", Number(event.target.value))}
            className={inputClass()}
          />
        </Field>
        <Toggle
          checked={prefs.sandboxIsolation}
          onChange={(next) => setPref("sandboxIsolation", next)}
          label="Sandbox isolation for packs"
          description="Packs run in a governance sandbox with blocked write and network operations"
        />
        <div className="rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] p-3">
          <h4 className="mb-2 text-[11px] font-medium text-[var(--ecp-text)]">
            Backend policy ids
          </h4>
          {policyList.length === 0 ? (
            <p className="text-[11px] text-[var(--ecp-text-dim)]">
              {policies.error ?? "No policies reported."}
            </p>
          ) : (
            <div className="flex flex-wrap gap-1.5">
              {policyList.map((policy) => (
                <Pill key={policy} tone="info">
                  {policy}
                </Pill>
              ))}
            </div>
          )}
        </div>
        <p className="text-[11px] text-[var(--ecp-text-dim)]">
          API keys are issued by the backend auth service and are never stored in the
          browser.
        </p>
      </div>
    </div>
  );
}