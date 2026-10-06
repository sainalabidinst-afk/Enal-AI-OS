'use client';

import { useState } from 'react';

export function CapabilityEditor() {
  const [skills, setSkills] = useState('parse, reason, execute');
  const [complexity, setComplexity] = useState(50);

  return (
    <div className="space-y-4 rounded-lg border border-border bg-surface-secondary p-4">
      <h3 className="text-sm font-semibold">Capability Editor</h3>
      <div>
        <label className="block text-sm font-medium">Skills (comma separated)</label>
        <input
          className="mt-1 w-full rounded-md border border-border bg-surface-primary px-3 py-2 text-sm outline-none focus:border-primary"
          value={skills}
          onChange={(e) => setSkills(e.target.value)}
        />
      </div>
      <div>
        <label className="block text-sm font-medium">Complexity</label>
        <input
          type="range"
          min="0"
          max="100"
          value={complexity}
          onChange={(e) => setComplexity(Number(e.target.value))}
          className="mt-1 w-full"
        />
        <span className="text-xs text-text-secondary">{complexity}%</span>
      </div>
    </div>
  );
}
