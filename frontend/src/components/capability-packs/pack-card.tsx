'use client';

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { StatusBadge } from '@/components/shared/status-badge';
import { useToast } from '@/components/shared/toast';
import { Loader2, Play } from 'lucide-react';
import { apiClient } from '@/lib/api-client';

interface PackCardProps {
  id: string;
  name: string;
  description?: string;
  category?: string;
}

export function PackCard({ id, name, description, category }: PackCardProps) {
  const queryClient = useQueryClient();
  const { addToast } = useToast();

  const executeMutation = useMutation({
    mutationFn: () => apiClient.post(`/api/v1/capabilities/${id}/execute`, { message: 'Execute via UI', workspace_id: 'default' }),
    onSuccess: () => {
      addToast('success', 'Pack executed');
      queryClient.invalidateQueries({ queryKey: ['capabilities'] });
    },
    onError: () => addToast('error', 'Execution failed'),
  });

  return (
    <div className="rounded-lg border border-border bg-surface-secondary p-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold">{name}</h3>
        <StatusBadge status="success" label={category ?? 'pack'} />
      </div>
      <p className="mt-2 text-xs text-text-secondary">{description}</p>
      <p className="mt-3 text-xs font-mono text-text-muted">{id}</p>
      <button
        onClick={() => executeMutation.mutate()}
        disabled={executeMutation.isPending}
        className="mt-3 flex items-center gap-2 rounded-md bg-primary px-3 py-1.5 text-xs text-white hover:bg-primary-hover disabled:opacity-70"
      >
        {executeMutation.isPending && <Loader2 size={14} className="animate-spin" />}
        <Play size={14} />
        Execute Pack
      </button>
    </div>
  );
}
