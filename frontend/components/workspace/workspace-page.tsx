"use client";

import { useWorkspaceStore } from "@/store/workspace-store";
import { useState } from "react";
import { AttachmentPanel } from "@/components/attachments/attachment-panel";

type Tab = "conversation" | "attachments" | "files" | "memory" | "history";

export function WorkspacePage() {
  const [tab, setTab] = useState<Tab>("attachments");
  const workspaces = useWorkspaceStore((s) => s.workspaces);
  const activeWorkspaceId = useWorkspaceStore((s) => s.activeWorkspaceId);
  const setActiveWorkspace = useWorkspaceStore((s) => s.setActiveWorkspace);
  const loadFiles = useWorkspaceStore((s) => s.loadFiles);
  const createFile = useWorkspaceStore((s) => s.createFile);
  const removeFile = useWorkspaceStore((s) => s.removeFile);
  const memory = useWorkspaceStore((s) => s.memory);

  const activeWorkspace = workspaces.find((w) => w.id === activeWorkspaceId) || workspaces[0];

  return (
    <div className="max-w-5xl mx-auto p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold">Workspace</h1>
          <p className="text-sm text-[var(--color-text-secondary)]">{activeWorkspace?.name}</p>
        </div>
        <select
          value={activeWorkspaceId || ""}
          onChange={(e) => e.target.value && setActiveWorkspace(e.target.value)}
          className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] px-3 py-1 text-sm"
        >
          <option value="">Select workspace</option>
          {workspaces.map((ws) => (
            <option key={ws.id} value={ws.id}>{ws.name}</option>
          ))}
        </select>
      </div>

      <div className="flex gap-2 border-b border-[var(--color-border)]">
        {(["attachments", "files", "memory", "history"] as Tab[]).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`rounded-t-lg px-4 py-2 text-sm capitalize ${
              tab === t ? "border-b-2 border-[var(--color-accent)] text-[var(--color-text-primary)]" : "text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)]"
            }`}
          >
            {t}
          </button>
        ))}
      </div>

      <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4">
        {!activeWorkspace ? (
          <p className="text-sm text-[var(--color-text-secondary)]">Select or create a workspace.</p>
        ) : (
          <>
            {tab === "attachments" && <AttachmentPanel conversationId={activeWorkspace.id} workspaceId={activeWorkspace.id} />}
            {tab === "files" && <WorkspaceFilesTab workspaceId={activeWorkspace.id} files={activeWorkspace.files} onLoad={loadFiles} onCreate={createFile} onRemove={removeFile} />}
            {tab === "memory" && <WorkspaceMemoryTab memory={memory} />}
            {tab === "history" && <WorkspaceHistoryTab workspace={activeWorkspace} />}
          </>
        )}
      </div>
    </div>
  );
}

function WorkspaceConversationTab({ workspace }: { workspace: ReturnType<typeof useWorkspaceStore.getState>["workspaces"][number] }) {
  return (
    <div className="space-y-2">
      <p className="text-sm font-medium">Conversation</p>
      <p className="text-xs text-[var(--color-text-secondary)]"> Conversations are isolated per workspace. Open the chat to continue.</p>
      <div className="rounded-md border border-[var(--color-border)] bg-[var(--color-bg-primary)] p-3">
        <p className="text-xs text-[var(--color-text-secondary)]">Workspace ID: {workspace.id}</p>
        <p className="text-xs text-[var(--color-text-secondary)]">Conversations: {workspace.conversation_ids.length}</p>
        <p className="text-xs text-[var(--color-text-secondary)]">Executions: {workspace.execution_ids.length}</p>
        <p className="text-xs text-[var(--color-text-secondary)]">Artifacts: {workspace.artifact_ids.length}</p>
      </div>
    </div>
  );
}

function WorkspaceFilesTab({
  workspaceId,
  files,
  onLoad,
  onCreate,
  onRemove,
}: {
  workspaceId: string;
  files: ReturnType<typeof useWorkspaceStore.getState>["files"];
  onLoad: (id: string) => Promise<void>;
  onCreate: (id: string, file: { filename: string; path: string; size: number; metadata?: Record<string, any> }) => Promise<void>;
  onRemove: (id: string, filename: string) => Promise<void>;
}) {
  const [name, setName] = useState("");
  const [path, setPath] = useState("");

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="filename" className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-3 py-1 text-sm" />
        <input value={path} onChange={(e) => setPath(e.target.value)} placeholder="path" className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-3 py-1 text-sm" />
        <button
          onClick={async () => {
            if (!name.trim()) return;
            await onCreate(workspaceId, { filename: name.trim(), path: path.trim(), size: 0 });
            setName("");
            setPath("");
            await onLoad(workspaceId);
          }}
          className="rounded-lg bg-[var(--color-accent)] px-3 py-1 text-sm text-white hover:opacity-90"
        >
          Add
        </button>
      </div>
      <div className="space-y-1">
        {files.map((f) => (
          <div key={f.filename} className="flex items-center justify-between rounded-md border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-3 py-2">
            <div>
              <p className="text-sm">{f.filename}</p>
              <p className="text-xs text-[var(--color-text-secondary)]">{f.path}</p>
            </div>
            <button onClick={() => onRemove(workspaceId, f.filename)} className="text-xs text-[var(--color-danger)] hover:underline">
              Delete
            </button>
          </div>
        ))}
        {files.length === 0 && <p className="text-sm text-[var(--color-text-secondary)]">No files.</p>}
      </div>
    </div>
  );
}

function WorkspaceMemoryTab({ memory }: { memory: Record<string, any> }) {
  return (
    <div className="space-y-2">
      <p className="text-sm font-medium">Memory</p>
      <pre className="rounded-md border border-[var(--color-border)] bg-[var(--color-bg-primary)] p-4 text-xs whitespace-pre-wrap">{JSON.stringify(memory, null, 2)}</pre>
    </div>
  );
}

function WorkspaceHistoryTab({ workspace }: { workspace: ReturnType<typeof useWorkspaceStore.getState>["workspaces"][number] }) {
  return (
    <div className="space-y-2">
      <p className="text-sm font-medium">Execution & Artifact History</p>
      <p className="text-xs text-[var(--color-text-secondary)]">Executions: {workspace.execution_ids.length}</p>
      <p className="text-xs text-[var(--color-text-secondary)]">Artifacts: {workspace.artifact_ids.length}</p>
    </div>
  );
}
