"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { Mic, Send, Square, Volume2 } from "lucide-react";
import { api } from "@/services/api";
import { getConversation } from "@/services/chat";
import type { ChatResponse, Message } from "@/types/chat";

export interface VoiceSession {
  conversationId: string | null;
  messages: Message[];
  sending: boolean;
  error: string | null;
  lastLatencyMs: number | null;
  send: (text: string) => Promise<void>;
  clear: () => void;
  hydrate: (conversationId: string) => Promise<void>;
}

export function useVoiceSession(): VoiceSession {
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastLatencyMs, setLastLatencyMs] = useState<number | null>(null);
  const startedAt = useRef<number>(0);

  const send = useCallback(
    async (text: string) => {
      const trimmed = text.trim();
      if (!trimmed) return;
      setSending(true);
      setError(null);
      setMessages((current) => [
        ...current,
        { role: "user", content: trimmed, timestamp: new Date().toISOString() },
      ]);
      startedAt.current = Date.now();
      try {
        const response = await api.post<ChatResponse>("/api/v1/chat", {
          message: trimmed,
          conversation_id: conversationId ?? undefined,
        });
        setConversationId(response.conversation_id);
        setLastLatencyMs(Date.now() - startedAt.current);
        setMessages((current) => [
          ...current,
          {
            role: "assistant",
            content: response.message,
            timestamp: new Date().toISOString(),
            agent: response.agent,
          },
        ]);
      } catch (caught) {
        setError(caught instanceof Error ? caught.message : "Chat request failed");
      } finally {
        setSending(false);
      }
    },
    [conversationId]
  );

  const hydrate = useCallback(async (id: string) => {
    try {
      const conversation = await getConversation(id);
      setConversationId(conversation.conversation_id);
      setMessages(
        (conversation.messages ?? []).map((message) => ({
          role: message.role,
          content: message.content,
          timestamp: message.timestamp ?? new Date().toISOString(),
          agent: message.agent,
        }))
      );
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Failed to load conversation");
    }
  }, []);

  const clear = useCallback(() => {
    setMessages([]);
    setConversationId(null);
    setLastLatencyMs(null);
    setError(null);
  }, []);

  return { conversationId, messages, sending, error, lastLatencyMs, send, clear, hydrate };
}

export interface SpeechOptions {
  speed: number;
  voice: string;
}

export function useSpeechPlayback() {
  const [playingId, setPlayingId] = useState<string | null>(null);

  useEffect(() => {
    return () => {
      if (typeof window !== "undefined") window.speechSynthesis?.cancel();
    };
  }, []);

  const speak = useCallback(
    async (text: string, id: string, options: SpeechOptions) => {
      if (typeof window === "undefined") return;
      setPlayingId(id);
      const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const token = localStorage.getItem("enal-auth-token");
      const url = `${base}/api/v1/voice/speak?text=${encodeURIComponent(
        text.slice(0, 5000)
      )}&voice=${encodeURIComponent(options.voice)}&speed=${options.speed}`;
      try {
        const audio = new Audio(url);
        if (token) audio.crossOrigin = "use-credentials";
        audio.onended = () => setPlayingId(null);
        audio.onerror = () => setPlayingId(null);
        await audio.play();
      } catch {
        setPlayingId(null);
        if (window.speechSynthesis) {
          const utterance = new SpeechSynthesisUtterance(text);
          utterance.rate = options.speed;
          window.speechSynthesis.speak(utterance);
          utterance.onend = () => setPlayingId(null);
        }
      }
    },
    []
  );

  const stop = useCallback(() => {
    if (typeof window !== "undefined") window.speechSynthesis?.cancel();
    setPlayingId(null);
  }, []);

  return { speak, stop, playingId };
}

export interface RecorderHandle {
  supported: boolean;
  recording: boolean;
  start: () => Promise<void>;
  stop: () => Promise<Blob | null>;
}

export function useRecorder(): RecorderHandle {
  const [recording, setRecording] = useState(false);
  const mediaRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const supported =
    typeof window !== "undefined" &&
    typeof window.MediaRecorder !== "undefined" &&
    !!navigator.mediaDevices?.getUserMedia;

  const start = useCallback(async () => {
    if (!supported) return;
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const recorder = new MediaRecorder(stream);
    chunksRef.current = [];
    recorder.ondataavailable = (event) => {
      if (event.data.size > 0) chunksRef.current.push(event.data);
    };
    recorder.start();
    mediaRef.current = recorder;
    setRecording(true);
  }, [supported]);

  const stop = useCallback(async () => {
    const recorder = mediaRef.current;
    if (!recorder) return null;
    const blob = await new Promise<Blob>((resolve) => {
      recorder.onstop = () => resolve(new Blob(chunksRef.current, { type: "audio/webm" }));
      recorder.stop();
    });
    recorder.stream.getTracks().forEach((track) => track.stop());
    mediaRef.current = null;
    setRecording(false);
    return blob;
  }, []);

  return { supported, recording, start, stop };
}

export function speakWithBrowser(text: string, rate = 1): void {
  if (typeof window === "undefined" || !window.speechSynthesis) return;
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.rate = rate;
  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(utterance);
}

export const VOICE_ICONS = { Mic, Send, Square, Volume2 };