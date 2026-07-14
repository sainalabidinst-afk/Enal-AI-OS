export interface AttachmentMeta {
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

export async function uploadAttachment(
  file: File,
  workspaceId?: string,
  conversationId?: string,
): Promise<AttachmentMeta> {
  const form = new FormData();
  form.append("file", file, file.name);
  if (workspaceId) form.append("workspace_id", workspaceId);
  if (conversationId) form.append("conversation_id", conversationId);

  const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const response = await fetch(`${base}/api/v1/attachments/upload`, {
    method: "POST",
    body: form,
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || response.statusText);
  }
  return (await response.json()) as Promise<AttachmentMeta>;
}

export async function analyzeAttachments(files: File[]): Promise<{ count: number; results: AttachmentMeta[] }> {
  const form = new FormData();
  for (const file of files) {
    form.append("files", file, file.name);
  }

  const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const response = await fetch(`${base}/api/v1/attachments/analyze`, {
    method: "POST",
    body: form,
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || response.statusText);
  }
  return (await response.json()) as Promise<{ count: number; results: AttachmentMeta[] }>;
}
