'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { executeCapability } from '@/services/capabilities';
import { useExecutionStore } from '@/features/execution/execution-store';

export function useExecution(capabilityId: string) {
  const queryClient = useQueryClient();
  const addExecution = useExecutionStore((state) => state.addExecution);

  const executeMutation = useMutation({
    mutationFn: (payload: { message: string; workspace_id?: string }) => executeCapability(capabilityId, payload),
    onSuccess: (data) => {
      addExecution({
        executionId: data.executionId ?? Date.now().toString(),
        goal: 'Manual execution',
        status: 'completed',
        progress: 100,
        conversationId: data.conversationId,
        workspaceId: data.workspaceId,
        phases: [{ phaseId: '1', name: 'execute', status: 'completed' }],
        artifacts: [],
        logs: [],
      });
      queryClient.invalidateQueries({ queryKey: ['execution'] });
    },
  });

  return {
    execute: executeMutation.mutate,
    isExecuting: executeMutation.isPending,
  };
}
