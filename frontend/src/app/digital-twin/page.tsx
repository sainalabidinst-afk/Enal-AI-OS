'use client';

import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { TwinStatusWidget } from '@/components/digital-twin/twin-status-widget';
import { ScenarioSimulatorPanel } from '@/components/digital-twin/scenario-simulator-panel';
import { CausalTraceViewer } from '@/components/digital-twin/causal-trace-viewer';
import { RedTeamAuditTab } from '@/components/digital-twin/red-team-audit-tab';

type Tab = 'status' | 'scenario' | 'causal' | 'redteam';

export default function DigitalTwinPage() {
  const [activeTab, setActiveTab] = useState<Tab>('status');

  const tabs: { id: Tab; label: string }[] = [
    { id: 'status', label: 'Decision Twin Status' },
    { id: 'scenario', label: 'Scenario Simulator' },
    { id: 'causal', label: 'Causal Trace Viewer' },
    { id: 'redteam', label: 'Red Team Audit' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Digital Twin</h2>
        <p className="text-sm text-text-secondary">
          Decision Intelligence simulation brain — scenario, adversarial, and causal analysis.
        </p>
      </div>

      <div className="flex gap-1 rounded-lg border border-border bg-surface-secondary p-1">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`rounded-md px-3 py-1.5 text-sm font-medium transition-colors ${
              activeTab === tab.id
                ? 'bg-surface-primary text-text-primary shadow-sm'
                : 'text-text-secondary hover:text-text-primary'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {activeTab === 'status' && <TwinStatusWidget />}
      {activeTab === 'scenario' && <ScenarioSimulatorPanel />}
      {activeTab === 'causal' && <CausalTraceViewer />}
      {activeTab === 'redteam' && <RedTeamAuditTab />}
    </div>
  );
}
