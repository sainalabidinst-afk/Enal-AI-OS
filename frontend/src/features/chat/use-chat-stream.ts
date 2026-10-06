'use client';

import { useEffect, useRef } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { createStreamReader } from '@/lib/stream-handler';
import { useChatStore } from '@/features/chat/chat-store';

export function useChatStream(message: string, conversationId?: string, workspaceId?: string) {
  const queryClient = useQueryClient();
  const addMessage = useChatStore((state) => state.addMessage);
  const setStreaming = useChatStore((state) => state.setStreaming);
  const urlRef = useRef<string | null>(null);

  useEffect(() => {
    if (!message) return;

    const url = `/api/v1/chat/stream?message=${encodeURIComponent(message)}${conversationId ? `&conversationId=${encodeURIComponent(conversationId)}` : ''}${workspaceId ? `&workspaceId=${encodeURIComponent(workspaceId)}` : ''}`;
    urlRef.current = url;
    setStreaming(true);

    const cleanup = createStreamReader(
      url,
      (event) => {
        const data = JSON.parse(event.data);
        addMessage({ role: 'assistant', content: data.message ?? '', timestamp: new Date().toISOString() });
      },
      () => {
        setStreaming(false);
      }
    );

    return cleanup;
  }, [message, conversationId, workspaceId, addMessage, setStreaming]);

  return { urlRef };
}
