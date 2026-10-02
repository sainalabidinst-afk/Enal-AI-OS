"use client";

import { useState, useRef, useEffect, useMemo, KeyboardEvent, ChangeEvent } from "react";
import { CAPABILITY_APPS } from "@/components/apps/capability-registry";
import { cn } from "@/lib/utils";
import { Send, Sparkles } from "lucide-react";

const STARTER_PROMPTS = [
  { text: "Analyze this network configuration for vulnerabilities", category: "security" },
  { text: "Review this code for architecture violations", category: "code" },
  { text: "What are the key levels in Wyckoff analysis?", category: "trading" },
  { text: "Generate a CI/CD pipeline for this service", category: "devops" },
  { text: "Design a trading bot for crypto momentum strategy", category: "trading" },
  { text: "Create a database schema for user management", category: "database" },
];

export interface ChatInputWithSuggestionsProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

export function ChatInputWithSuggestions({ onSend, disabled, placeholder = "Ask Enal AI OS..." }: ChatInputWithSuggestionsProps) {
  const [value, setValue] = useState("");
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [highlightedIdx, setHighlightedIdx] = useState(-1);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const listRef = useRef<HTMLDivElement>(null);

  const keywordSuggestions = useMemo(() => {
    const keywords = new Set<string>();
    for (const app of CAPABILITY_APPS) {
      keywords.add(app.name);
      app.keywords.forEach((kw) => keywords.add(kw));
    }
    return Array.from(keywords);
  }, []);

  const suggestions = useMemo(() => {
    if (!value.trim()) {
      return STARTER_PROMPTS;
    }
    const lower = value.toLowerCase();
    return [
      ...STARTER_PROMPTS.filter((p) => p.text.toLowerCase().includes(lower)),
      ...keywordSuggestions
        .filter((k) => k.toLowerCase().includes(lower))
        .slice(0, 5)
        .map((k) => ({ text: k, category: "capability" })),
    ].slice(0, 8);
  }, [value, keywordSuggestions]);

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (listRef.current && !listRef.current.contains(e.target as Node) && inputRef.current && !inputRef.current.contains(e.target as Node)) {
        setShowSuggestions(false);
        setHighlightedIdx(-1);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  const filteredSuggestions = suggestions.slice(0, 8);

  const handleInputChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    setValue(e.target.value);
    setShowSuggestions(true);
    setHighlightedIdx(-1);
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (!showSuggestions) {
      if (e.key === "ArrowDown") {
        setShowSuggestions(true);
        setHighlightedIdx(0);
        e.preventDefault();
      }
      return;
    }

    switch (e.key) {
      case "ArrowDown":
        e.preventDefault();
        setHighlightedIdx((prev) => (prev + 1) % filteredSuggestions.length);
        break;
      case "ArrowUp":
        e.preventDefault();
        setHighlightedIdx((prev) => (prev - 1 + filteredSuggestions.length) % filteredSuggestions.length);
        break;
      case "Enter":
        if (!e.shiftKey && highlightedIdx >= 0) {
          e.preventDefault();
          selectSuggestion(filteredSuggestions[highlightedIdx]);
        }
        break;
      case "Escape":
        setShowSuggestions(false);
        setHighlightedIdx(-1);
        break;
    }
  };

  const selectSuggestion = (suggestion: { text: string }) => {
    setValue(suggestion.text);
    setShowSuggestions(false);
    setHighlightedIdx(-1);
    inputRef.current?.focus();
  };

  const handleSubmit = () => {
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    setShowSuggestions(false);
    onSend(trimmed);
    setValue("");
  };

  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.style.height = "auto";
      inputRef.current.style.height = `${inputRef.current.scrollHeight}px`;
    }
  }, [value]);

  return (
    <div className="relative">
      <div className="flex items-end gap-2">
        <div className="relative flex-1">
          <textarea
            ref={inputRef}
            value={value}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            onFocus={() => setShowSuggestions(true)}
            onBlur={() => setTimeout(() => setShowSuggestions(false), 150)}
            placeholder={placeholder}
            disabled={disabled}
            className="w-full resize-none rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-4 py-2.5 pr-10 text-sm text-[var(--color-text-primary)] placeholder-[var(--color-text-secondary)] focus:border-[var(--color-accent)] focus:outline-none disabled:cursor-not-allowed disabled:opacity-50"
            rows={1}
            style={{ maxHeight: "120px" }}
          />
          <Sparkles className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[var(--color-accent)]" />
        </div>

        <button
          onClick={handleSubmit}
          disabled={disabled || !value.trim()}
          className="shrink-0 rounded-lg bg-[var(--color-accent)] p-2.5 text-white transition-all hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
          aria-label="Send message"
        >
          <Send className="h-4 w-4" />
        </button>
      </div>

      {showSuggestions && (
        <div
          ref={listRef}
          className="absolute bottom-full mb-2 w-full space-y-1 overflow-y-auto rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] py-1 shadow-lg max-h-48"
        >
          {filteredSuggestions.length === 0 ? (
            <div className="px-3 py-2 text-xs text-[var(--color-text-secondary)]">
              No suggestions found
            </div>
          ) : (
            filteredSuggestions.map((suggestion, idx) => (
              <button
                key={`${suggestion.category}-${idx}`}
                onMouseEnter={() => setHighlightedIdx(idx)}
                onClick={() => selectSuggestion(suggestion)}
                className={cn(
                  "w-full px-3 py-2 text-left text-xs transition-colors",
                  idx === highlightedIdx
                    ? "bg-[var(--color-accent)]/10 text-[var(--color-text-primary)]"
                    : "text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)] hover:text-[var(--color-text-primary)]"
                )}
              >
                <span className="mr-1.5 text-xs opacity-60">
                  {suggestion.category === "trading" ? "📈" : suggestion.category === "code" ? "💻" : suggestion.category === "security" ? "🛡️" : suggestion.category === "devops" ? "⚙️" : suggestion.category === "database" ? "🗄️" : "⚡"}
                </span>
                {suggestion.text}
              </button>
            ))
          )}
        </div>
      )}
    </div>
  );
}
