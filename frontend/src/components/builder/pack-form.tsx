'use client';

import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { cn } from '@/lib/cn';
import { useToast } from '@/components/shared/toast';
import { StatusBadge } from '@/components/shared/status-badge';
import { Loader2 } from 'lucide-react';

export function PackForm() {
  const [form, setForm] = useState({ name: '', domain: '', capabilities: '', policy: '' });
  const addToast = useToast((state) => state.addToast);

  const mutation = useMutation({
    mutationFn: (payload: Record<string, unknown>) => apiClient.post('/api/v1/governance/packs', payload),
    onSuccess: () => addToast('success', 'Pack registered successfully'),
    onError: () => addToast('error', 'Failed to register pack'),
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutation.mutate({
      name: form.name,
      domain: form.domain,
      metadata: {
        capabilities: form.capabilities.split(',').map((s) => s.trim()).filter(Boolean),
        policy: form.policy,
      },
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 rounded-lg border border-border bg-surface-secondary p-4">
      <h3 className="text-sm font-semibold">Pack Details</h3>
      <div className="grid gap-4 md:grid-cols-2">
        <div>
          <label className="block text-sm font-medium">Name</label>
          <input
            className="mt-1 w-full rounded-md border border-border bg-surface-primary px-3 py-2 text-sm outline-none focus:border-primary"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium">Domain</label>
          <input
            className="mt-1 w-full rounded-md border border-border bg-surface-primary px-3 py-2 text-sm outline-none focus:border-primary"
            value={form.domain}
            onChange={(e) => setForm({ ...form, domain: e.target.value })}
            required
          />
        </div>
      </div>
      <div>
        <label className="block text-sm font-medium">Capabilities (comma separated)</label>
        <input
          className="mt-1 w-full rounded-md border border-border bg-surface-primary px-3 py-2 text-sm outline-none focus:border-primary"
          value={form.capabilities}
          onChange={(e) => setForm({ ...form, capabilities: e.target.value })}
        />
      </div>
      <div>
        <label className="block text-sm font-medium">Policy Rails</label>
        <textarea
          className="mt-1 w-full rounded-md border border-border bg-surface-primary px-3 py-2 text-sm outline-none focus:border-primary"
          value={form.policy}
          onChange={(e) => setForm({ ...form, policy: e.target.value })}
          rows={3}
        />
      </div>
      <button
        type="submit"
        disabled={mutation.isPending}
        className={cn('flex items-center gap-2 rounded-md bg-primary px-4 py-2 text-sm text-white hover:bg-primary-hover disabled:opacity-70')}
      >
        {mutation.isPending && <Loader2 size={14} className="animate-spin" />}
        {mutation.isPending ? 'Registering...' : 'Register Pack'}
      </button>
    </form>
  );
}
