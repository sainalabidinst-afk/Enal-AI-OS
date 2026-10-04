import { api } from "./api";
import type {
  FeedStatusResponse,
  FeedTick,
  FeedTickEnvelope,
  MarketRegimeLive,
  TradingAnalyzeResponse,
} from "../types/trading";

export async function analyzeMarket(
  symbol: string,
  timeframes?: string[]
): Promise<TradingAnalyzeResponse> {
  return api.post<TradingAnalyzeResponse>("/api/v1/trading/analyze", {
    symbol: symbol.toUpperCase().trim(),
    timeframes: timeframes,
  });
}

export interface StartFeedOptions {
  symbol: string;
  timeframes?: string[];
  pollInterval?: number;
}

export async function startLiveFeed(options: StartFeedOptions) {
  return api.post<{ success: boolean; data: Record<string, unknown> }>(
    "/api/v1/trading/feed/start",
    {
      symbol: options.symbol.toUpperCase().trim(),
      timeframes: options.timeframes,
      poll_interval: options.pollInterval ?? 5,
    }
  );
}

export async function stopLiveFeed() {
  return api.post<{ success: boolean; data: { message: string } }>(
    "/api/v1/trading/feed/stop"
  );
}

export async function getFeedStatus(): Promise<FeedStatusResponse> {
  const response = await api.get<{ success: boolean; data: FeedStatusResponse }>(
    "/api/v1/trading/feed/status"
  );
  return response.data;
}

export async function getLiveRegime(
  symbol: string,
  lookback = 20
): Promise<MarketRegimeLive> {
  const response = await api.get<{ success: boolean; data: MarketRegimeLive }>(
    `/api/v1/trading/regime/live?symbol=${encodeURIComponent(
      symbol.toUpperCase().trim()
    )}&lookback=${lookback}`
  );
  return response.data;
}

export interface StreamFeedOptions {
  symbol: string;
  interval?: number;
  lookback?: number;
  onTick: (tick: FeedTick, isSnapshot: boolean) => void;
  onError?: (error: Error) => void;
  signal?: AbortSignal;
}

function parseFrame(frame: string): { event: string; payload: FeedTickEnvelope } | null {
  const lines = frame.split("\n");
  let event = "message";
  const dataLines: string[] = [];
  for (const line of lines) {
    if (line.startsWith("event:")) event = line.slice(6).trim();
    if (line.startsWith("data:")) dataLines.push(line.slice(5).trim());
  }
  if (dataLines.length === 0) return null;
  try {
    return { event, payload: JSON.parse(dataLines.join("\n")) as FeedTickEnvelope };
  } catch {
    return null;
  }
}

/**
 * Subscribes to the trading feed SSE endpoint.
 * Uses fetch + ReadableStream so the auth header can be attached.
 */
export async function streamFeed(options: StreamFeedOptions): Promise<void> {
  const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const token =
    typeof window === "undefined" ? "" : localStorage.getItem("enal-auth-token") || "";
  const params = new URLSearchParams({
    symbol: options.symbol.toUpperCase().trim(),
    interval: String(options.interval ?? 5),
    lookback: String(options.lookback ?? 20),
  });

  const response = await fetch(`${base}/api/v1/trading/feed/stream?${params.toString()}`, {
    headers: {
      Accept: "text/event-stream",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    signal: options.signal,
  });

  if (!response.ok || !response.body) {
    throw new Error(`Feed stream failed with ${response.status}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  try {
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const frames = buffer.split("\n\n");
      buffer = frames.pop() ?? "";
      for (const frame of frames) {
        const parsed = parseFrame(frame);
        if (!parsed) continue;
        options.onTick(parsed.payload.data, parsed.event === "snapshot");
      }
    }
  } catch (error) {
    if ((error as Error)?.name === "AbortError") return;
    options.onError?.(error instanceof Error ? error : new Error("Feed stream error"));
  }
}