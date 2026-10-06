'use client';

import { useState } from 'react';

export function PolicyEditor() {
  const [policy, setPolicy] = useState('allow model:read\nallow capabilities:execute');

  return (
    <div className="space-y-4 rounded-lg border border-border bg-surface-secondary p-4">
      <h3 className="text-sm font-semibold">Policy Editor</h3>
      <div>
        <label className="block text-sm font-medium">Policy Rails</label>
        <textarea
          className="mt-1 w-full rounded-md border border-border bg-surface-primary px-3 py-2 text-sm outline-none focus:border-primary font-mono"
          value={policy}
          onChange={(e) => setPolicy(e.target.value)}
          rows={5}
        />
      </div>
    </div>
  );
}
