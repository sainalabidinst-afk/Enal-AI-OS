'use client';

import React from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select } from '@/components/ui/select';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import {
  Settings,
  Save,
  Play,
  Trash2,
  Plus,
} from 'lucide-react';

interface StepConfigPanelProps {
  step: {
    id?: string;
    type: string;
    label: string;
    config: Record<string, unknown>;
  } | null;
  onChange: (step: StepConfigPanelProps['step']) => void;
  onSave?: () => void;
  onRun?: () => void;
  stepTypes: Array<{ value: string; label: string }>;
}

const StepConfigPanel: React.FC<StepConfigPanelProps> = ({
  step,
  onChange,
  onSave,
  onRun,
  stepTypes,
}) => {
  const update = (patch: Partial<StepConfigPanelProps['step']>) => {
    if (!step) return;
    onChange({ ...step, ...patch });
  };

  return (
    <div className="flex h-full w-96 flex-col border-l bg-white">
      <div className="flex items-center justify-between border-b px-4 py-3">
        <div className="flex items-center gap-2">
          <Settings className="h-5 w-5 text-green-600" />
          <span className="font-semibold text-gray-800">Step Configuration</span>
        </div>
        <div className="flex items-center gap-1">
          <Button variant="ghost" size="sm" onClick={() => onChange(null)}>
            <Trash2 className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="sm" onClick={onSave}>
            <Save className="h-4 w-4" />
          </Button>
          <Button size="sm" onClick={onRun}>
            <Play className="mr-1 h-4 w-4" />
            Run
          </Button>
        </div>
      </div>

      <ScrollArea className="flex-1 px-4 py-4">
        {!step ? (
          <div className="flex h-full flex-col items-center justify-center text-center text-sm text-gray-500">
            <Settings className="mb-2 h-8 w-8 text-gray-300" />
            <p>Select a step on the canvas to configure it.</p>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700">Step ID</label>
              <Input value={step.id || ''} onChange={(e) => update({ id: e.target.value })} placeholder="step-1" />
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700">Label</label>
              <Input value={step.label} onChange={(e) => update({ label: e.target.value })} placeholder="My Step" />
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700">Type</label>
              <Select
                id="step-type"
                label=""
                value={step.type}
                onChange={(e) => update({ type: e.target.value })}
                options={stepTypes}
              />
            </div>

            <Separator />

            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700">Configuration (JSON)</label>
              <textarea
                value={JSON.stringify(step.config, null, 2)}
                onChange={(e) => {
                  try {
                    const config = JSON.parse(e.target.value);
                    update({ config });
                  } catch {
                    // ignore invalid JSON while typing
                  }
                }}
                rows={12}
                className="flex min-h-[120px] w-full rounded-md border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-3 py-2 text-sm text-[var(--color-text-primary)] placeholder:text-[var(--color-text-secondary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)] focus:ring-offset-2 font-mono"
              />
            </div>
          </div>
        )}
      </ScrollArea>
    </div>
  );
};

export default StepConfigPanel;
