'use client';

import React from 'react';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Tabs, TabPanel } from '@/components/ui/tabs';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import {
  Shield,
  Save,
  Play,
  User,
  AlertTriangle,
  Ban,
  Brain,
  GitBranch,
  FileText,
  Scale,
  Plus,
} from 'lucide-react';

interface GuardrailConfigProps {
  agent: {
    id?: string;
    name: string;
    guardrails: {
      pii: boolean;
      toxicLanguage: boolean;
      promptInjection: boolean;
      biasCheck: boolean;
      logicCheck: boolean;
      competitorCheck: boolean;
      gibberish: boolean;
      readingLevel: boolean;
    };
  };
  onChange: (agent: GuardrailConfigProps['agent']) => void;
  onSave?: () => void;
  onTest?: () => void;
}

const guardrailItems = [
  { key: 'pii', label: 'PII Detection', description: 'Detect emails, phones, SSNs, credit cards', icon: User },
  { key: 'toxicLanguage', label: 'Toxic Language', description: 'Detect profanity and harmful content', icon: AlertTriangle },
  { key: 'promptInjection', label: 'Prompt Injection', description: 'Detect injection attacks', icon: Ban },
  { key: 'biasCheck', label: 'Bias Check', description: 'Detect biased output', icon: Brain },
  { key: 'logicCheck', label: 'Logic Check', description: 'Validate logical consistency', icon: GitBranch },
  { key: 'competitorCheck', label: 'Competitor Check', description: 'Detect competitor mentions', icon: Ban },
  { key: 'gibberish', label: 'Gibberish Detection', description: 'Detect nonsense output', icon: FileText },
  { key: 'readingLevel', label: 'Reading Level', description: 'Validate reading complexity', icon: Scale },
];

const GuardrailConfig: React.FC<GuardrailConfigProps> = ({
  agent,
  onChange,
  onSave,
  onTest,
}) => {
  const update = (patch: Partial<GuardrailConfigProps['agent']>) => {
    onChange({ ...agent, ...patch });
  };

  const toggleGuardrail = (key: keyof GuardrailConfigProps['agent']['guardrails']) => {
    onChange({
      ...agent,
      guardrails: {
        ...agent.guardrails,
        [key]: !agent.guardrails[key],
      },
    });
  };

  const tabs = [
    { id: 'guardrails', label: 'Guardrails' },
    { id: 'policies', label: 'Policies' },
    { id: 'test', label: 'Test' },
  ];

  const [activeTab, setActiveTab] = React.useState('guardrails');

  const enabledCount = Object.values(agent.guardrails).filter(Boolean).length;

  return (
    <div className="flex h-full w-96 flex-col border-l bg-white">
      <div className="flex items-center justify-between border-b px-4 py-3">
        <div className="flex items-center gap-2">
          <Shield className="h-5 w-5 text-red-600" />
          <span className="font-semibold text-gray-800">Guardrails</span>
          <span className="rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-600">
            {enabledCount} active
          </span>
        </div>
        <div className="flex items-center gap-1">
          <Button variant="ghost" size="sm" onClick={onTest}>
            <Play className="mr-1 h-4 w-4" />
            Test
          </Button>
          <Button variant="ghost" size="sm" onClick={onSave}>
            <Save className="mr-1 h-4 w-4" />
            Save
          </Button>
        </div>
      </div>

      <ScrollArea className="flex-1 px-4 py-4">
        <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} className="w-full" />

        {activeTab === 'guardrails' && (
          <div className="mt-4 space-y-3">
            {guardrailItems.map((item) => {
              const Icon = item.icon;
              const isEnabled = agent.guardrails[item.key as keyof GuardrailConfigProps['agent']['guardrails']];
              return (
                <div
                  key={item.key}
                  className={`rounded-md border p-3 ${
                    isEnabled ? 'border-red-200 bg-red-50' : 'border-gray-200 bg-gray-50'
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <Checkbox
                      id={`guardrail-${item.key}`}
                      checked={isEnabled}
                      onChange={() => toggleGuardrail(item.key as keyof GuardrailConfigProps['agent']['guardrails'])}
                    />
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <Icon className="h-4 w-4 text-gray-600" />
                        <label htmlFor={`guardrail-${item.key}`} className="text-sm font-medium text-gray-800">
                          {item.label}
                        </label>
                      </div>
                      <p className="mt-1 text-xs text-gray-500">{item.description}</p>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {activeTab === 'policies' && (
          <div className="mt-4 space-y-4">
            <div className="rounded-md border border-dashed border-gray-300 p-4 text-center">
              <Shield className="mx-auto mb-2 h-8 w-8 text-gray-300" />
              <p className="text-sm text-gray-500">No policies configured yet.</p>
                <Button variant="secondary" size="sm" className="mt-2">
                <Plus className="mr-1 h-4 w-4" />
                Create Policy
              </Button>
            </div>
          </div>
        )}

        {activeTab === 'test' && (
          <div className="mt-4 space-y-4">
            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700">Test Input</label>
              <textarea
                placeholder="Enter text to test guardrails..."
                rows={4}
                className="flex min-h-[80px] w-full rounded-md border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-3 py-2 text-sm text-[var(--color-text-primary)] placeholder:text-[var(--color-text-secondary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)] focus:ring-offset-2"
              />
            </div>
            <Button className="w-full" onClick={onTest}>
              <Play className="mr-2 h-4 w-4" />
              Run Guardrail Test
            </Button>
            <div className="rounded-md border border-dashed border-gray-300 p-4 text-center">
              <p className="text-sm text-gray-500">Run a test to see guardrail results here.</p>
            </div>
          </div>
        )}
      </ScrollArea>
    </div>
  );
};

export default GuardrailConfig;
