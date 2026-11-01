'use client';

import Link from 'next/link';
import { Activity, ArrowUpRight, Hammer, Package } from 'lucide-react';
import { GovernanceCards } from '@/components/dashboard/governance-cards';
import { MarketFeedWidget } from '@/components/dashboard/market-feed-widget';
import { SystemHealthPanel } from '@/components/dashboard/system-health-panel';
import { AuditTrailPreview } from '@/components/dashboard/audit-trail-preview';

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div className="page-intro">
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-primary">
          Operations workspace
        </p>
        <h2 className="mt-2 text-3xl font-semibold">Command center</h2>
        <p className="mt-2 max-w-2xl text-sm text-text-secondary">
          Monitor platform activity, inspect capability packs, and move from
          signals to action.
        </p>
      </div>

      <GovernanceCards />

      <section className="grid gap-3 md:grid-cols-3" aria-label="Quick actions">
        <Link href="/capability-packs" className="workspace-action">
          <Package size={18} />
          <span>
            <strong>Explore capabilities</strong>
            <small>Inspect available domain packs</small>
          </span>
          <ArrowUpRight size={16} className="ml-auto" />
        </Link>
        <Link href="/builder" className="workspace-action">
          <Hammer size={18} />
          <span>
            <strong>Build a capability</strong>
            <small>Create or register a pack</small>
          </span>
          <ArrowUpRight size={16} className="ml-auto" />
        </Link>
        <Link href="/observability" className="workspace-action">
          <Activity size={18} />
          <span>
            <strong>Open observability</strong>
            <small>Review telemetry and alerts</small>
          </span>
          <ArrowUpRight size={16} className="ml-auto" />
        </Link>
      </section>

      <section className="grid gap-4 lg:grid-cols-3">
        <div className="rounded-lg border border-border bg-surface-secondary p-4 lg:col-span-2">
          <h3 className="text-sm font-semibold">Market Feed - BTCUSDT</h3>
          <p className="mt-1 text-xs text-text-secondary">
            Confidence trend streamed from the trading module.
          </p>
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
