'use client';

import { GovernanceCards } from '@/components/dashboard/governance-cards';
import { MarketFeedWidget } from '@/components/dashboard/market-feed-widget';
import { SystemHealthPanel } from '@/components/dashboard/system-health-panel';
import { AuditTrailPreview } from '@/components/dashboard/audit-trail-preview';

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Dashboard</h2>
        <p className="text-sm text-text-secondary">Governance, observability, and system status.</p>
      </div>

      <GovernanceCards />

      <section className="grid gap-4 lg:grid-cols-3">
        <div className="lg:col-span-2 rounded-lg border border-border bg-surface-secondary p-4">
          <h3 className="text-sm font-semibold">Market Feed - BTCUSDT</h3>
          <p className="text-xs text-text-secondary">Confidence trend streamed from trading module.</p>
          <MarketFeedWidget symbol="BTCUSDT" />
        </div>
        <div className="rounded-lg border border-border bg-surface-secondary p-4">
          <h3 className="text-sm font-semibold">System Health</h3>
          <SystemHealthPanel />
        </div>
      </section>

      <section className="rounded-lg border border-border bg-surface-secondary p-4">
        <h3 className="text-sm font-semibold">Audit Trail Preview</h3>
        <AuditTrailPreview limit={5} />
      </section>
    </div>
  );
}
