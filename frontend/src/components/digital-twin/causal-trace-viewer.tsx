'use client';

import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';

export function CausalTraceViewer() {
  const [treatment, setTreatment] = useState('');
  const [outcome, setOutcome] = useState('');
  const [conditions, setConditions] = useState('{}');
  const queryClient = useQueryClient();

  const mutation = useMutation<{ causal_effect?: number; confidence?: number; counterfactual?: string }>({
    mutationFn: () =>
      apiClient.post('/api/v1/twin/causal-trace', {
        treatment,
        outcome,
        conditions: JSON.parse(conditions || '{}'),
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
      <h3 className="text-sm font-semibold">Causal Trace Viewer</h3>
      <p className="mt-1 text-xs text-text-secondary">
        Analyze treatment → outcome causal relationships with counterfactuals.
      </p>
      <form onSubmit={handleSubmit} className="mt-4 space-y-3">
        <div className="grid gap-3 md:grid-cols-2">
          <div>
            <label className="block text-xs text-text-secondary">Treatment (Cause)</label>
            <input
              type="text"
              value={treatment}
              onChange={(e) => setTreatment(e.target.value)}
              placeholder="e.g. interest_rate"
              className="mt-1 w-full rounded-md border border-border bg-surface-primary p-2 text-sm"
            />
          </div>
          <div>
            <label className="block text-xs text-text-secondary">Outcome (Effect)</label>
            <input
              type="text"
              value={outcome}
              onChange={(e) => setOutcome(e.target.value)}
              placeholder="e.g. inflation"
              className="mt-1 w-full rounded-md border border-border bg-surface-primary p-2 text-sm"
            />
          </div>
        </div>
        <div>
          <label className="block text-xs text-text-secondary">Conditions (JSON)</label>
          <textarea
            value={conditions}
            onChange={(e) => setConditions(e.target.value)}
            placeholder='{"control": "value"}'
            className="mt-1 w-full rounded-md border border-border bg-surface-primary p-2 text-sm font-mono"
            rows={2}
          />
        </div>
        <button
          type="submit"
          disabled={mutation.isPending || !treatment || !outcome}
          className="rounded-md bg-primary px-4 py-2 text-sm text-white disabled:opacity-50"
        >
          {mutation.isPending ? 'Tracing...' : 'Run Causal Trace'}
        </button>
        {mutation.isError && (
          <p className="text-xs text-danger">{(mutation.error as Error).message}</p>
        )}
        {mutation.isSuccess && (
          <div className="mt-3 space-y-2 rounded-md border border-border bg-surface-primary p-3">
            <div className="flex items-center gap-3">
              <span className="text-xs text-text-secondary">Causal Effect:</span>
              <span className="text-sm font-semibold">
                {mutation.data?.causal_effect?.toFixed(4) ?? '—'}
              </span>
              <span className="text-xs text-text-secondary">
                Confidence: {((mutation.data?.confidence ?? 0) * 100)?.toFixed(1)}%
              </span>
            </div>
            {mutation.data?.counterfactual && (
              <div>
                <p className="text-xs text-text-secondary">Counterfactual:</p>
                <p className="mt-1 text-sm">{mutation.data.counterfactual}</p>
              </div>
            )}
            <pre className="overflow-auto rounded-md bg-surface-tertiary p-2 font-mono text-xs text-text-secondary">
              {JSON.stringify(mutation.data, null, 2)}
            </pre>
          </div>
        )}
      </form>
    </div>
  );
}
