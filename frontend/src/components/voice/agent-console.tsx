'use client';

import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { cn } from '@/lib/cn';
import { useToast } from '@/components/shared/toast';
import { Loader2, Mic, Square } from 'lucide-react';

export function AgentConsole() {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const addToast = useToast((state) => state.addToast);
  const queryClient = useQueryClient();

  const startMutation = useMutation({
    mutationFn: () => apiClient.post('/api/v1/voice/stt/start'),
    onSuccess: () => {
      setIsRecording(true);
      addToast('success', 'Voice recording started');
    },
    onError: () => addToast('error', 'Failed to start voice'),
  });

  const stopMutation = useMutation({
    mutationFn: () => apiClient.post('/api/v1/voice/stt/stop'),
    onSuccess: () => {
      setIsRecording(false);
      addToast('success', 'Voice recording stopped');
      queryClient.invalidateQueries({ queryKey: ['voice'] });
    },
    onError: () => addToast('error', 'Failed to stop voice'),
  });

  const sendMutation = useMutation({
    mutationFn: (text: string) => apiClient.post('/api/v1/voice/transcript', { text }),
    onSuccess: () => {
      setTranscript('');
      addToast('success', 'Transcript sent');
    },
    onError: () => addToast('error', 'Failed to send transcript'),
  });

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <button
          onClick={() => (isRecording ? stopMutation.mutate() : startMutation.mutate())}
          disabled={startMutation.isPending || stopMutation.isPending}
          className={cn(
            'flex items-center gap-2 rounded-md border border-border px-4 py-2 text-sm hover:bg-surface-hover disabled:opacity-70',
            isRecording && 'border-danger text-danger'
          )}
        >
          {isRecording ? <Square size={16} /> : <Mic size={16} />}
          {isRecording ? 'Stop' : 'Start Recording'}
        </button>
        {isRecording && (
          <span className="flex items-center gap-2 text-xs text-danger">
            <span className="h-2 w-2 animate-pulse rounded-full bg-danger" />
            Recording...
          </span>
        )}
      </div>
      <div>
        <label className="block text-sm font-medium">Transcript</label>
        <textarea
          className="mt-1 w-full rounded-md border border-border bg-surface-primary px-3 py-2 text-sm outline-none focus:border-primary font-mono"
          value={transcript}
          onChange={(e) => setTranscript(e.target.value)}
          rows={4}
        />
      </div>
      <button
        onClick={() => transcript && sendMutation.mutate(transcript)}
        disabled={!transcript || sendMutation.isPending}
        className="rounded-md bg-primary px-4 py-2 text-sm text-white hover:bg-primary-hover disabled:opacity-70"
      >
        {sendMutation.isPending ? 'Sending...' : 'Send Transcript'}
      </button>
    </div>
  );
}
