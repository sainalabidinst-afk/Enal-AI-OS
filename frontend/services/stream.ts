import type { ChatRequest, StreamEvent, StreamEventType, FinalEvent, ExecutionStartedEvent, PhaseEvent, TaskEvent, LogEvent, ArtifactEvent, ProgressEvent, ExecutionCompleteEvent, ErrorEvent } from "@/types";

export interface StreamOptions {
  onEvent: (event: StreamEvent) => void;
  onError?: (error: Error) => void;
  onComplete?: () => void;
  signal?: AbortSignal;
}

export function createChatStream(request: ChatRequest, options: StreamOptions): EventSource {
  const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const qs = new URLSearchParams();
  qs.set("message", request.message);
  if (request.conversation_id) qs.set("conversation_id", request.conversation_id);
  if (request.workspace_id) qs.set("workspace_id", request.workspace_id);
  const url = `${base}/api/v1/chat/stream?${qs.toString()}`;

  const source = new EventSource(url);

  source.addEventListener("message", (event) => {
    try {
      const data = JSON.parse((event as MessageEvent).data);
      options.onEvent(data);
      if (data.type === "execution_complete" || data.type === "error") {
        source.close();
        options.onComplete?.();
      }
    } catch (error) {
      options.onError?.(error instanceof Error ? error : new Error(String(error)));
    }
  });

  source.onerror = () => {
    options.onError?.(new Error("Stream connection failed"));
    source.close();
    options.onComplete?.();
  };

  options.signal?.addEventListener("abort", () => {
    source.close();
  });

  return source;
}
