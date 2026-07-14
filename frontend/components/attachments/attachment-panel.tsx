"use client";

import { useCallback, useState } from "react";

interface AttachmentMeta {
  filename: string;
  attachment_type: string;
  vendor: string;
  device_role: string;
  format: string;
  version: string;
  confidence: number;
  summary: string;
  risk_score: number;
  recommendations: string[];
  ast: Record<string, any>;
  analysis_error?: string;
}

interface AttachmentResult extends AttachmentMeta {
  id: string;
  status: "uploading" | "done" | "error";
  error?: string;
}

interface AttachmentPanelProps {
  conversationId: string;
  workspaceId?: string;
  onAnalyzed?: (result: AttachmentResult) => void;
}

export function AttachmentPanel({ conversationId, workspaceId, onAnalyzed }: AttachmentPanelProps) {
  const [results, setResults] = useState<AttachmentResult[]>([]);
  const [dragOver, setDragOver] = useState(false);
  const [uploading, setUploading] = useState(false);

  const uploadFiles = useCallback(
    async (files: FileList | File[]) => {
      if (!files.length) return;
      setUploading(true);
      const form = new FormData();
      for (const file of Array.from(files)) {
        form.append("file", file, file.name);
      }
      if (workspaceId) {
        form.append("workspace_id", workspaceId);
      }
      if (conversationId) {
        form.append("conversation_id", conversationId);
      }

      try {
        const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        const response = await fetch(`${base}/api/v1/attachments/upload`, {
          method: "POST",
          body: form,
        });
        if (!response.ok) {
          const text = await response.text();
          throw new Error(text || response.statusText);
        }
        const data = (await response.json()) as AttachmentMeta;
        const result: AttachmentResult = {
          id: `${conversationId}-${data.filename}-${Date.now()}`,
          status: "done",
          ...data,
        };
        setResults((prev) => [result, ...prev]);
        onAnalyzed?.(result);
      } catch (error) {
        const result: AttachmentResult = {
          id: `${conversationId}-error-${Date.now()}`,
          status: "error",
          filename: Array.from(files)[0]?.name || "unknown",
          attachment_type: "unknown",
          vendor: "unknown",
          device_role: "unknown",
          format: "",
          version: "",
          confidence: 0,
          summary: "Upload failed",
          risk_score: 0,
          recommendations: [],
          ast: {},
          error: error instanceof Error ? error.message : "Unknown error",
        };
        setResults((prev) => [result, ...prev]);
      } finally {
        setUploading(false);
      }
    },
    [conversationId, workspaceId, onAnalyzed]
  );

  const handleDrop = useCallback(
    (event: React.DragEvent<HTMLDivElement>) => {
      event.preventDefault();
      setDragOver(false);
      uploadFiles(event.dataTransfer.files);
    },
    [uploadFiles]
  );

  return (
    <div className="space-y-4">
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setDragOver(true);
        }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        className={`rounded-lg border-2 border-dashed p-4 text-center text-sm ${
          dragOver ? "border-[var(--color-accent)] bg-[var(--color-bg-secondary)]" : "border-[var(--color-border)]"
        }`}
      >
        <p className="text-[var(--color-text-secondary)]">
          Drag and drop config, screenshot, archive, or document here
        </p>
        <p className="mt-1 text-xs text-[var(--color-text-secondary)]">
          Supported: .rsc, .conf, .cfg, .txt, .pdf, .png, .zip, .tar.gz and more
        </p>
        <input
          type="file"
          multiple
          className="mt-2 text-xs"
          onChange={(e) => uploadFiles(e.target.files || [])}
        />
        {uploading && <p className="mt-2 text-xs text-[var(--color-accent)]">Analyzing...</p>}
      </div>

      <div className="space-y-3">
        {results.map((result) => (
          <AttachmentCard key={result.id} result={result} />
        ))}
      </div>
    </div>
  );
}

function AttachmentCard({ result }: { result: AttachmentResult }) {
  if (result.status === "error") {
    return (
      <div className="rounded-lg border border-[var(--color-danger)] bg-[var(--color-bg-secondary)] p-4">
        <p className="text-sm font-medium text-[var(--color-danger)]">{result.filename}</p>
        <p className="text-xs text-[var(--color-danger)]">{result.error || "Upload failed"}</p>
      </div>
    );
  }

  return (
    <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium">{result.filename}</p>
          <p className="text-xs text-[var(--color-text-secondary)]">
            {result.attachment_type} • {result.vendor} • {result.device_role} • confidence {Math.round((result.confidence || 0) * 100)}%
          </p>
        </div>
        <span className="text-xs text-[var(--color-text-secondary)]">Risk {Math.round((result.risk_score || 0) * 100)}%</span>
      </div>
      <p className="mt-2 text-xs text-[var(--color-text-secondary)]">{result.summary}</p>
      {result.analysis_error && (
        <p className="mt-2 text-xs text-[var(--color-danger)]">{result.analysis_error}</p>
      )}
      {result.recommendations?.length > 0 && (
        <ul className="mt-2 list-disc pl-5 text-xs text-[var(--color-text-secondary)]">
          {result.recommendations.slice(0, 5).map((rec, index) => (
            <li key={index}>{rec}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
