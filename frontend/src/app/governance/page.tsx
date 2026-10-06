'use client';

import { GovernanceStatusPanel } from '@/components/governance/governance-status-panel';
import { ADRList } from '@/components/governance/adr-list';
import { QualityGateList } from '@/components/governance/quality-gate-list';

export default function GovernancePage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Governance Explorer</h2>
        <p className="text-sm text-text-secondary">ADR, Quality Gates, and governance status.</p>
      </div>

      <GovernanceStatusPanel />

      <section className="grid gap-4 lg:grid-cols-2">
        <div className="rounded-lg border border-border bg-surface-secondary p-4">
          <h3 className="text-sm font-semibold">ADR List</h3>
          <ADRList />
        </div>
        <div className="rounded-lg border border-border bg-surface-secondary p-4">
          <h3 className="text-sm font-semibold">Quality Gates</h3>
          <QualityGateList />
        </div>
      </section>
    </div>
  );
}
