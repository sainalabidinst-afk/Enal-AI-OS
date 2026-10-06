'use client';

import { AuditTimeline } from '@/components/audit-trail/audit-timeline';
import { AuditFilter } from '@/components/audit-trail/audit-filter';
import { PackProgressionPanel } from '@/components/audit-trail/pack-progression-panel';
import { useState } from 'react';

export default function AuditTrailPage() {
  const [packId, setPackId] = useState('');

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Audit Trail</h2>
        <p className="text-sm text-text-secondary">Governance activity log and pack progression.</p>
      </div>

      <AuditFilter />

      <section className="rounded-lg border border-border bg-surface-secondary p-4">
        <h3 className="text-sm font-semibold">Activity Log</h3>
        <AuditTimeline />
      </section>

      {packId && (
        <section className="rounded-lg border border-border bg-surface-secondary p-4">
          <h3 className="text-sm font-semibold">Pack Progression</h3>
          <PackProgressionPanel packId={packId} />
        </section>
      )}
    </div>
  );
}
