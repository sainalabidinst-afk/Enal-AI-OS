"use client";

import { useEffect, useRef } from "react";
import type { Message } from "@/types";
import { ChatBubble } from "./chat-bubble";

interface ChatWindowProps {
  messages: Message[];
  isLoading?: boolean;
  emptyState?: React.ReactNode;
}

export function ChatWindow({ messages, isLoading, emptyState }: ChatWindowProps) {
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4 space-y-4">
      {messages.length === 0 && !isLoading && (
        <div className="text-[var(--color-text-secondary)] text-center mt-20">
          {emptyState || (
            <>
              <p className="text-lg">Start a conversation with Enal AI OS.</p>
              <p className="text-sm mt-2">Try: &ldquo;Audit this MikroTik configuration&rdquo;</p>
            </>
          )}
        </div>
      )}
      {messages.map((msg, idx) => (
        <ChatBubble key={msg.id || idx} message={msg} />
      ))}
      {isLoading && (
        <div className="flex justify-start">
          <div className="rounded-lg px-4 py-2 text-[var(--color-text-secondary)]">
            Processing with AI agents...
          </div>
        </div>
      )}
      <div ref={endRef} />
    </div>
  );
}
