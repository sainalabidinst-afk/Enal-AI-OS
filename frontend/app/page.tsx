"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { useChatStore } from "@/store/chat-store";
import { useWorkspaceStore } from "@/store/workspace-store";
import { createChatStream } from "@/services/stream";
import { createWorkspace } from "@/services/workspace";
import type { Message, StreamEvent } from "@/types";
import { ChatWindow } from "@/components/chat/chat-window";
import { PromptBox } from "@/components/chat/prompt-box";

export default function ChatPage() {
  const [input, setInput] = useState("");
  const [streamSource, setStreamSource] = useState<EventSource | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const chat = useChatStore();
  const workspace = useWorkspaceStore();

  const activeConversationId = chat.activeConversationId;
  const conversations = chat.conversations;
  const messages = activeConversationId ? conversations[activeConversationId]?.messages || [] : [];
  const isLoading = chat.isStreaming;

  const workspaceId = workspace.activeWorkspaceId;
  const workspaces = workspace.workspaces;

  useEffect(() => {
    if (!streamSource) return;
    return () => {
      streamSource.close();
      setStreamSource(null);
    };
  }, [streamSource]);

  const ensureWorkspace = async (): Promise<string | null> => {
    if (workspaceId) return workspaceId;
    let ws = workspaces[0];
    if (!ws) {
      ws = await createWorkspace({ name: "Default Workspace" });
      await workspace.loadWorkspaces();
    }
    await workspace.setActiveWorkspace(ws.id);
    return ws.id;
  };

  const sendMessage = useCallback(
    async (text: string) => {
      const trimmed = text.trim();
      if (!trimmed || isLoading) return;

      const userMessage: Message = {
        id: `msg-${Date.now()}`,
        role: "user",
        content: trimmed,
        timestamp: new Date().toISOString(),
      };

      const currentConversationId = activeConversationId || `conv-${Date.now()}`;
      if (!activeConversationId) {
        chat.setActiveConversation(currentConversationId);
      }

      chat.appendMessage(currentConversationId, userMessage);
      chat.setStreaming(true);
      chat.setError(null);

      try {
        const wsId = await ensureWorkspace();
        const source = createChatStream(
          {
            message: trimmed,
            conversation_id: currentConversationId,
            workspace_id: wsId || undefined,
            stream: true,
          },
          {
            onEvent: (event: StreamEvent) => {
              chat.appendStreamEvent(currentConversationId, event);
              if (["execution_started", "phase", "artifact"].includes(event.type)) {
                workspace.refreshWorkspace(wsId || "").catch(() => {});
              }
            },
            onError: (error) => {
              chat.setError(error.message);
            },
            onComplete: () => {
              chat.setStreaming(false);
              setStreamSource(null);
            },
          }
        );
        setStreamSource(source);
      } catch (error) {
        chat.setError(error instanceof Error ? error.message : "Failed to send message");
        chat.setStreaming(false);
      }
    },
    [isLoading, activeConversationId, workspaceId, workspaces, chat, workspace]
  );

  const handleCreateWorkspace = async (name: string) => {
    if (!name.trim()) return;
    await createWorkspace({ name: name.trim() });
    await workspace.loadWorkspaces();
  };

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto p-4 gap-4">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold">Enal AI OS</h1>
          <p className="text-sm text-[var(--color-text-secondary)]">AI Execution Platform</p>
        </div>
        <div className="flex items-center gap-2">
          <select
            value={workspaceId ?? ""}
            onChange={(e) => { const v = e.target.value; if (v) workspace.setActiveWorkspace(v); }}
            className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] px-3 py-1 text-sm"
          >
            <option value="">Select workspace</option>
            {workspaces.map((ws) => (
              <option key={ws.id} value={ws.id}>{ws.name}</option>
            ))}
          </select>
          <WorkspaceCreateInline onCreate={handleCreateWorkspace} />
        </div>
      </header>

      <ChatWindow
        messages={messages}
        isLoading={isLoading}
        emptyState={
          <div className="text-[var(--color-text-secondary)] text-center mt-20">
            <p className="text-lg">Start a conversation with Enal AI OS.</p>
            <p className="text-sm mt-2">Try: &ldquo;Audit this MikroTik configuration&rdquo;</p>
          </div>
        }
      />

      {chat.error && (
        <div className="rounded-lg border border-[var(--color-danger)] bg-[var(--color-bg-secondary)] px-4 py-2 text-sm text-[var(--color-danger)]">
          {chat.error}
          <button onClick={() => chat.clearError()} className="ml-2 underline">
            Dismiss
          </button>
        </div>
      )}

      <PromptBox onSend={sendMessage} disabled={isLoading} />
    </div>
  );
}

function WorkspaceCreateInline({ onCreate }: { onCreate: (name: string) => void }) {
  const [name, setName] = useState("");
  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onCreate(name);
        setName("");
      }}
      className="flex gap-1"
    >
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="New workspace"
        className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] px-3 py-1 text-sm"
      />
      <button
        type="submit"
        className="rounded-lg bg-[var(--color-accent)] px-3 py-1 text-sm text-white hover:opacity-90"
      >
        Create
      </button>
    </form>
  );
}
