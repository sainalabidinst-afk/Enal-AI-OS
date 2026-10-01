"use client";

import { FormEvent, useEffect, useRef, useState } from "react";
import {
  ArrowUp,
  ChevronDown,
  Clock3,
  Copy,
  Menu,
  Mic,
  Paperclip,
  Plus,
  Search,
  Send,
  Sparkles,
  Square,
  Volume2,
  VolumeX,
  X,
} from "lucide-react";
import { sendChat } from "@/services/chat";
import type { Message } from "@/types/chat";

interface SpeechRecognitionEventLike extends Event {
  results: SpeechRecognitionResultList;
}

interface SpeechRecognitionLike {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  onend: (() => void) | null;
  onerror: (() => void) | null;
  onresult: ((event: SpeechRecognitionEventLike) => void) | null;
  start: () => void;
  stop: () => void;
}

type SpeechRecognitionConstructor = new () => SpeechRecognitionLike;

declare global {
  interface Window {
    SpeechRecognition?: SpeechRecognitionConstructor;
    webkitSpeechRecognition?: SpeechRecognitionConstructor;
  }
}

const starters = [
  "Summarize what I should focus on today",
  "Review this project architecture",
  "Help me make a safer deployment plan",
];

const initialMessage: Message = {
  id: "welcome",
  role: "assistant",
  content:
    "Good morning. I am ready to help you think, build, and execute. What should we work on?",
  timestamp: new Date().toISOString(),
  agent: "Enal AI",
};

function formatTime(timestamp: string) {
  return new Intl.DateTimeFormat("en", { hour: "numeric", minute: "2-digit" }).format(
    new Date(timestamp),
  );
}

export function ChatGPTPage() {
  const [messages, setMessages] = useState<Message[]>([initialMessage]);
  const [draft, setDraft] = useState("");
  const [conversationId, setConversationId] = useState<string>();
  const [isSending, setIsSending] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [speakingId, setSpeakingId] = useState<string>();
  const [showRail, setShowRail] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const recognitionRef = useRef<SpeechRecognitionLike | null>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isSending]);

  useEffect(() => {
    return () => {
      recognitionRef.current?.stop();
      window.speechSynthesis?.cancel();
    };
  }, []);

  async function submitMessage(event?: FormEvent) {
    event?.preventDefault();
    const message = draft.trim();
    if (!message || isSending) return;

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: "user",
      content: message,
      timestamp: new Date().toISOString(),
    };
    setMessages((current) => [...current, userMessage]);
    setDraft("");
    setIsSending(true);

    try {
      const response = await sendChat({
        message,
        conversation_id: conversationId,
        stream: false,
      });
      setConversationId(response.conversation_id);
      setMessages((current) => [
        ...current,
        {
          id: `assistant-${Date.now()}`,
          role: "assistant",
          content: response.message || "I completed the request, but no text response was returned.",
          timestamp: new Date().toISOString(),
          agent: response.agent || "Enal AI",
          metadata: response.metadata,
        },
      ]);
    } catch (error) {
      setMessages((current) => [
        ...current,
        {
          id: `error-${Date.now()}`,
          role: "assistant",
          content: error instanceof Error ? error.message : "The assistant could not respond.",
          timestamp: new Date().toISOString(),
          agent: "System",
        },
      ]);
    } finally {
      setIsSending(false);
    }
  }

  function toggleListening() {
    if (isListening) {
      recognitionRef.current?.stop();
      setIsListening(false);
      return;
    }

    const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!Recognition) {
      setMessages((current) => [
        ...current,
        {
          id: `voice-${Date.now()}`,
          role: "assistant",
          content: "Voice input is not available in this browser. Try Chrome or Edge.",
          timestamp: new Date().toISOString(),
          agent: "System",
        },
      ]);
      return;
    }

    const recognition = new Recognition();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.onresult = (event) => {
      const transcript = Array.from(event.results)
        .map((result) => result[0]?.transcript || "")
        .join("");
      setDraft(transcript);
    };
    recognition.onend = () => setIsListening(false);
    recognition.onerror = () => setIsListening(false);
    recognitionRef.current = recognition;
    setIsListening(true);
    recognition.start();
  }

  function speakMessage(message: Message) {
    if (!window.speechSynthesis) return;
    if (speakingId === message.id) {
      window.speechSynthesis.cancel();
      setSpeakingId(undefined);
      return;
    }
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(message.content);
    utterance.onend = () => setSpeakingId(undefined);
    setSpeakingId(message.id);
    window.speechSynthesis.speak(utterance);
  }

  function copyMessage(content: string) {
    void navigator.clipboard?.writeText(content);
  }

  return (
    <div className="chat-shell">
      <aside className={`chat-rail ${showRail ? "chat-rail-open" : ""}`}>
        <div className="chat-rail-top">
          <div className="brand-mark"><Sparkles size={16} /></div>
          <div>
            <p className="brand-name">Enal</p>
            <p className="brand-caption">Cognitive workspace</p>
          </div>
          <button className="icon-button rail-close" onClick={() => setShowRail(false)} aria-label="Close conversation list">
            <X size={17} />
          </button>
        </div>
        <button className="new-chat-button" onClick={() => { setMessages([initialMessage]); setConversationId(undefined); setShowRail(false); }}>
          <Plus size={17} /> New conversation
          <span className="shortcut">N</span>
        </button>
        <label className="search-field">
          <Search size={15} />
          <input placeholder="Search conversations" aria-label="Search conversations" />
          <span className="shortcut">⌘ K</span>
        </label>
        <p className="rail-label">Recent</p>
        <div className="conversation-list">
          <button className="conversation-item active"><span>Untitled conversation</span><span className="conversation-dot" /></button>
          <button className="conversation-item"><span>Deployment planning</span><span>Yesterday</span></button>
          <button className="conversation-item"><span>Network architecture review</span><span>Sep 30</span></button>
        </div>
        <div className="rail-footer">
          <div className="privacy-note"><span className="status-dot" /> Local AI connected</div>
          <p>Gemma 4 E4B · LM Studio</p>
        </div>
      </aside>

      <section className="chat-main">
        <header className="chat-header">
          <div className="header-left">
            <button className="icon-button mobile-menu" onClick={() => setShowRail(true)} aria-label="Open conversation list"><Menu size={19} /></button>
            <div className="model-selector"><span className="model-pulse" /><span>Enal Local</span><ChevronDown size={15} /></div>
          </div>
          <div className="header-actions">
            <span className="connection-label"><span className="status-dot" /> Local</span>
            <button className="icon-button" aria-label="Conversation history"><Clock3 size={18} /></button>
          </div>
        </header>

        <div className="message-scroll">
          <div className="message-column">
            <div className="conversation-intro">
              <div className="intro-orbit"><Sparkles size={22} /></div>
              <p className="eyebrow">Private intelligence</p>
              <h1>What are we<br /><em>making</em> today?</h1>
              <p className="intro-copy">Your local AI workspace for clear thinking, thoughtful decisions, and work that moves forward.</p>
            </div>

            {messages.length === 1 && (
              <div className="starter-grid">
                {starters.map((starter) => <button key={starter} onClick={() => setDraft(starter)}>{starter}<ArrowUp size={14} /></button>)}
              </div>
            )}

            <div className="messages">
              {messages.map((message) => (
                <article key={message.id} className={`message-row ${message.role}`}>
                  {message.role === "assistant" && <div className="assistant-avatar"><Sparkles size={14} /></div>}
                  <div className="message-content">
                    <div className="message-meta"><span>{message.role === "user" ? "You" : message.agent || "Enal AI"}</span><time>{formatTime(message.timestamp)}</time></div>
                    <p>{message.content}</p>
                    {message.role === "assistant" && (
                      <div className="message-tools">
                        <button onClick={() => speakMessage(message)} aria-label={speakingId === message.id ? "Stop speaking" : "Read aloud"}>{speakingId === message.id ? <VolumeX size={14} /> : <Volume2 size={14} />} {speakingId === message.id ? "Stop" : "Listen"}</button>
                        <button onClick={() => copyMessage(message.content)} aria-label="Copy response"><Copy size={14} /> Copy</button>
                      </div>
                    )}
                  </div>
                </article>
              ))}
              {isSending && <div className="message-row assistant"><div className="assistant-avatar"><Sparkles size={14} /></div><div className="thinking"><span /><span /><span /></div></div>}
              <div ref={bottomRef} />
            </div>
          </div>
        </div>

        <div className="composer-wrap">
          <form className="composer" onSubmit={submitMessage}>
            <button type="button" className="composer-tool" aria-label="Attach file"><Paperclip size={19} /></button>
            <textarea value={draft} onChange={(event) => setDraft(event.target.value)} onKeyDown={(event) => { if (event.key === "Enter" && !event.shiftKey) { event.preventDefault(); void submitMessage(); } }} placeholder="Message Enal..." rows={1} aria-label="Message Enal" />
            <button type="button" className={`composer-tool ${isListening ? "recording" : ""}`} onClick={toggleListening} aria-label={isListening ? "Stop voice input" : "Start voice input"}>{isListening ? <Square size={17} /> : <Mic size={19} />}</button>
            <button type="submit" className="send-button" disabled={!draft.trim() || isSending} aria-label="Send message">{isSending ? <span className="send-spinner" /> : <Send size={17} />}</button>
          </form>
          <p className="composer-note">Enal can make mistakes. Check important information.</p>
        </div>
      </section>
    </div>
  );
}
