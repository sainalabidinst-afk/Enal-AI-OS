'use client';

import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';

export function ScenarioSimulatorPanel() {
  const [scenario, setScenario] = useState('');
  const [iterations, setIterations] = useState(100);
  const [baseState, setBaseState] = useState('{}');
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: () =>
      apiClient.post('/api/v1/twin/simulate', {
        scenario,
        parameters: {
          base_state: JSON.parse(baseState || '{}'),
        },
        iterations,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['twin'] });
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutation.mutate();
  };

  return (
    <div className="rounded-lg border border-border bg-surface-secondary p-4">
      <h3 className="text-sm font-semibold">Scenario Simulator</h3>
      <form onSubmit={handleSubmit} className="mt-4 space-y-3">
        <div>
          <label className="block text-xs text-text-secondary">Scenario Description</label>
          <textarea
            value={scenario}
            onChange={(e) => setScenario(e.target.value)}
            placeholder="e.g. What if interest rate rises 1%?"
            className="mt-1 w-full rounded-md border border-border bg-surface-primary p-2 text-sm"
            rows={3}
          />
        </div>
        <div>
          <label className="block text-xs text-text-secondary">Iterations</label>
          <input
            type="number"
            value={iterations}
            onChange={(e) => setIterations(Number(e.target.value))}
            min={1}
            max={10000}
            className="mt-1 w-24 rounded-md border border-border bg-surface-primary p-2 text-sm"
          />
        </div>
        <div>
          <label className="block text-xs text-text-secondary">Base State (JSON)</label>
          <textarea
            value={baseState}
            onChange={(e) => setBaseState(e.target.value)}
            placeholder='{"key": "value"}'
            className="mt-1 w-full rounded-md border border-border bg-surface-primary p-2 text-sm font-mono"
            rows={2}
          />
        </div>
        <button
          type="submit"
          disabled={mutation.isPending || !scenario}
          className="rounded-md bg-primary px-4 py-2 text-sm text-white disabled:opacity-50"
        >
          {mutation.isPending ? 'Running...' : 'Run Simulation'}
        </button>
        {mutation.isError && (
          <p className="text-xs text-danger">{(mutation.error as Error).message}</p>
        )}
        {mutation.isSuccess && (
          <div className="mt-2 rounded-md border border-border bg-surface-primary p-3">
            <p className="text-xs font-semibold">Result</p>
            <pre className="mt-1 overflow-auto rounded-md bg-surface-tertiary p-2 font-mono text-xs text-text-secondary">
              {JSON.stringify(mutation.data, null, 2)}
            </pre>
          </div>
        )}
      </form>
    </div>
  );
}
