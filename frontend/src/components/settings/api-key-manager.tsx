'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { cn } from '@/lib/cn';
import { useToast } from '@/components/shared/toast';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';
import { Loader2, Plus, Trash2 } from 'lucide-react';

export function ApiKeyManager() {
  const [name, setName] = useState('');
  const [scope, setScope] = useState('read');
  const { addToast } = useToast();
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery<{ keys: Array<{ id: string; name: string; scope: string; key?: string }> }>({
    queryKey: ['settings', 'api-keys'],
    queryFn: () => apiClient.get('/api/v1/settings/api-keys'),
  });

  const createMutation = useMutation({
    mutationFn: (payload: { name: string; scope: string }) => apiClient.post('/api/v1/settings/api-keys', payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['settings', 'api-keys'] });
      addToast('success', 'API key created');
      setName('');
      setScope('read');
    },
    onError: () => addToast('error', 'Failed to create API key'),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => apiClient.delete(`/api/v1/settings/api-keys/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['settings', 'api-keys'] });
      addToast('success', 'API key deleted');
    },
    onError: () => addToast('error', 'Failed to delete API key'),
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createMutation.mutate({ name, scope });
  };

  if (isLoading) return <LoadingSkeleton className="mt-4 h-64 w-full" />;

  const keys = data?.keys ?? [];

  return (
    <div className="mt-4 space-y-4">
      <form onSubmit={handleSubmit} className="flex items-end gap-3">
        <div className="flex-1">
          <label className="block text-sm font-medium">Name</label>
          <input
            className="mt-1 w-full rounded-md border border-border bg-surface-primary px-3 py-2 text-sm outline-none focus:border-primary"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium">Scope</label>
          <select
            className="mt-1 rounded-md border border-border bg-surface-primary px-3 py-2 text-sm outline-none focus:border-primary"
            value={scope}
            onChange={(e) => setScope(e.target.value)}
          >
            <option value="read">read</option>
            <option value="trade">trade</option>
            <option value="admin">admin</option>
          </select>
        </div>
        <button type="submit" disabled={createMutation.isPending} className={cn('flex items-center gap-2 rounded-md bg-primary px-4 py-2 text-sm text-white hover:bg-primary-hover disabled:opacity-70')}>
          {createMutation.isPending && <Loader2 size={14} className="animate-spin" />}
          <Plus size={14} />
          Add
        </button>
      </form>
      <div className="space-y-2">
        {keys.map((key: { id: string; name: string; scope: string; key?: string }) => (
          <div key={key.id} className="flex items-center justify-between rounded-md border border-border px-3 py-2">
            <div>
              <p className="text-sm font-medium">{key.name}</p>
              <p className="text-xs font-mono text-text-muted">{key.key ? `${key.key.slice(0, 8)}...` : '••••'}</p>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-xs text-text-secondary">{key.scope}</span>
              <button onClick={() => deleteMutation.mutate(key.id)} className="rounded-md p-1 hover:bg-surface-hover text-danger">
                <Trash2 size={14} />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
