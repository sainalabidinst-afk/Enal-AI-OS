"use client";

import { useState, useCallback } from "react";
import { useExecutionStore } from "@/store/execution-store";
import { useCognitiveStore } from "@/store/cognitive-store";
import { cn } from "@/lib/utils";

export type TranslationStyle = "formal" | "informal" | "technical" | "creative";
export type DomainGlossary = "finance" | "legal" | "medical" | "technical" | "general";

const SUPPORTED_LANGUAGES = [
  { code: "en", name: "English" },
  { code: "id", name: "Indonesian" },
  { code: "es", name: "Spanish" },
  { code: "zh", name: "Chinese (Simplified)" },
  { code: "fr", name: "French" },
  { code: "de", name: "German" },
  { code: "ja", name: "Japanese" },
  { code: "pt", name: "Portuguese" },
  { code: "ru", name: "Russian" },
  { code: "ar", name: "Arabic" },
  { code: "nl", name: "Dutch" },
  { code: "ko", name: "Korean" },
  { code: "vi", name: "Vietnamese" },
  { code: "th", name: "Thai" },
  { code: "tr", name: "Turkish" },
  { code: "pl", name: "Polish" },
  { code: "hi", name: "Hindi" },
  { code: "ms", name: "Malay" },
  { code: "sw", name: "Swahili" },
  { code: "ur", name: "Urdu" },
  { code: "bn", name: "Bengali" },
  { code: "it", name: "Italian" },
] as const;

const STYLE_OPTIONS: { value: TranslationStyle; label: string; desc: string }[] = [
  { value: "formal", label: "Formal", desc: "Professional, respectful register" },
  { value: "informal", label: "Informal", desc: "Conversational, casual tone" },
  { value: "technical", label: "Technical", desc: "Domain-specific terminology" },
  { value: "creative", label: "Creative", desc: "Expressive, narrative style" },
];

const DOMAIN_OPTIONS: { value: DomainGlossary; label: string; desc: string }[] = [
  { value: "finance", label: "Finance", desc: "Financial & investment terminology" },
  { value: "legal", label: "Legal", desc: "Contracts & legal documents" },
  { value: "medical", label: "Medical", desc: "Clinical & medical guidelines" },
  { value: "technical", label: "Technical", desc: "Engineering & technical docs" },
  { value: "general", label: "General", desc: "General purpose translation" },
];

export interface TranslationPipelineProps {
  executionId?: string;
  initialText?: string;
  initialSourceLang?: string;
  initialTargetLang?: string;
}

export function TranslationPipeline({
  executionId,
  initialText = "",
  initialSourceLang = "en",
  initialTargetLang = "id",
}: TranslationPipelineProps) {
  const [sourceText, setSourceText] = useState(initialText);
  const [translatedText, setTranslatedText] = useState("");
  const [sourceLang, setSourceLang] = useState(initialSourceLang);
  const [targetLang, setTargetLang] = useState(initialTargetLang);
  const [style, setStyle] = useState<TranslationStyle>("formal");
  const [domain, setDomain] = useState<DomainGlossary>("general");
  const [isTranslating, setIsTranslating] = useState(false);
  const [confidence, setConfidence] = useState<number | null>(null);
  const [detectedLang, setDetectedLang] = useState<string | null>(null);
  const [glossaryTerms, setGlossaryTerms] = useState<string[]>([]);

  const appendLog = useExecutionStore((s) => s.appendLog);
  const updateProgress = useExecutionStore((s) => s.updateProgress);
  const addTranslationConfidence = useCognitiveStore((s) => s.addTranslationConfidence);
  const setCapabilityStatus = useCognitiveStore((s) => s.setCapabilityStatus);

  const handleTranslate = useCallback(async () => {
    if (!sourceText.trim()) return;

    const execId = executionId;
    if (!execId) return;

    setIsTranslating(true);
    setConfidence(null);
    setDetectedLang(null);
    setTranslatedText("");

    const startTime = Date.now();
    setCapabilityStatus("translator", "running");

    try {
      await updateProgress(execId, 10);
      await appendLog(execId, {
        message: `Starting translation: ${sourceLang} → ${targetLang} (${style}, ${domain})`,
        level: "info",
        metadata: { source_lang: sourceLang, target_lang: targetLang, style, domain },
      });

      await updateProgress(execId, 30);

      // Simulate translation pipeline:
      // 1. Language detection (auto-detect if source is "auto")
      if (sourceLang === "auto") {
        await appendLog(execId, {
          message: "Auto-detecting source language...",
          level: "info",
        });
        setDetectedLang("en");
        await updateProgress(execId, 40);
      }

      await updateProgress(execId, 60);

      // 2. Glossary preprocessing
      await appendLog(execId, {
        message: `Applying ${domain} glossary and ${style} style`,
        level: "info",
        metadata: { domain, style },
      });

      // 3. Translation (lazy-loaded MarianMT/M2M-100 via backend)
      await updateProgress(execId, 80);

      const simulatedResult = await simulateTranslation(
        sourceText,
        sourceLang,
        targetLang,
        style,
        domain,
      );
      const latencyMs = Date.now() - startTime;

      setTranslatedText(simulatedResult.text);
      setConfidence(simulatedResult.confidence);
      setGlossaryTerms(simulatedResult.glossaryTerms);

      addTranslationConfidence({
        source_lang: sourceLang === "auto" ? (detectedLang ?? "en") : sourceLang,
        target_lang: targetLang,
        confidence: simulatedResult.confidence,
        quality_score: simulatedResult.quality_score,
        latency_ms: latencyMs,
        glossary_terms_used: simulatedResult.glossaryTerms.length,
        throughput_cps: latencyMs > 0 ? simulatedResult.text.length / (latencyMs / 1000) : 0,
        model_used: simulatedResult.model_used,
        domain: domain,
      });

      await updateProgress(execId, 100);
      await appendLog(execId, {
        message: `Translation complete. Confidence: ${simulatedResult.confidence}`,
        level: "info",
        metadata: {
          confidence: simulatedResult.confidence,
          glossaryTermsUsed: simulatedResult.glossaryTerms.length,
          latency_ms: latencyMs,
        },
      });
    } catch (error) {
      setCapabilityStatus("translator", "failed");
      await appendLog(
        execId,
        {
          message: `Translation failed: ${error instanceof Error ? error.message : "Unknown error"}`,
          level: "error",
        },
      );
    } finally {
      setIsTranslating(false);
      setCapabilityStatus("translator", "idle");
    }
  }, [
    sourceText,
    sourceLang,
    targetLang,
    style,
    domain,
    executionId,
    appendLog,
    updateProgress,
    addTranslationConfidence,
    setCapabilityStatus,
    detectedLang,
  ]);

  const handleSwapLanguages = useCallback(() => {
    setSourceLang(targetLang);
    setTargetLang(sourceLang);
  }, [sourceLang, targetLang]);

  if (!executionId) {
    return (
      <div className="flex items-center justify-center p-8 text-sm text-[var(--color-text-secondary)]">
        <p>Pass an <code>executionId</code> prop to use the Translation Pipeline.</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-4 max-w-4xl">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <select
          value={sourceLang}
          onChange={(e) => setSourceLang(e.target.value)}
          className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)]"
        >
          <option value="auto">Auto-detect</option>
          {SUPPORTED_LANGUAGES.map((lang) => (
            <option key={lang.code} value={lang.code}>{lang.name}</option>
          ))}
        </select>

        <div className="flex items-center justify-center">
          <button
            onClick={handleSwapLanguages}
            disabled={!sourceLang || !targetLang || sourceLang === "auto"}
            className={cn(
              "rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-2 transition-all",
              "hover:bg-[var(--color-bg-tertiary)] disabled:opacity-50",
            )}
            aria-label="Swap languages"
          >
            ⇅
          </button>
        </div>

        <select
          value={targetLang}
          onChange={(e) => setTargetLang(e.target.value)}
          className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)]"
        >
          {SUPPORTED_LANGUAGES.map((lang) => (
            <option key={lang.code} value={lang.code}>{lang.name}</option>
          ))}
        </select>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="text-xs font-medium text-[var(--color-text-secondary)]">Style</label>
          <div className="mt-1 flex flex-wrap gap-2">
            {STYLE_OPTIONS.map((opt) => (
              <button
                key={opt.value}
                onClick={() => setStyle(opt.value)}
                className={cn(
                  "rounded-lg border px-3 py-1.5 text-xs font-medium transition-all",
                  style === opt.value
                    ? "border-[var(--color-accent)] bg-[var(--color-accent)]/10 text-[var(--color-accent)]"
                    : "border-[var(--color-border)] text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)]",
                )}
                title={opt.desc}
              >
                {opt.label}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="text-xs font-medium text-[var(--color-text-secondary)]">Domain Glossary</label>
          <div className="mt-1 flex flex-wrap gap-2">
            {DOMAIN_OPTIONS.map((opt) => (
              <button
                key={opt.value}
                onClick={() => setDomain(opt.value)}
                className={cn(
                  "rounded-lg border px-3 py-1.5 text-xs font-medium transition-all",
                  domain === opt.value
                    ? "border-[var(--color-accent)] bg-[var(--color-accent)]/10 text-[var(--color-accent)]"
                    : "border-[var(--color-border)] text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)]",
                )}
                title={opt.desc}
              >
                {opt.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="text-xs font-medium text-[var(--color-text-secondary)]">Source Text</label>
          <textarea
            value={sourceText}
            onChange={(e) => setSourceText(e.target.value)}
            placeholder="Enter text to translate..."
            className="w-full h-40 rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-3 py-2 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)]"
          />
        </div>
        <div>
          <label className="text-xs font-medium text-[var(--color-text-secondary)]">Translation</label>
          <div className="relative">
            {isTranslating && (
              <div className="absolute inset-0 flex items-center justify-center bg-[var(--color-bg-secondary)]/50 rounded-lg">
                <span className="text-sm text-[var(--color-text-secondary)]">Translating…</span>
              </div>
            )}
            <textarea
              value={translatedText}
              readOnly
              placeholder="Translation will appear here..."
              className="w-full h-40 rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] px-3 py-2 text-sm resize-none"
            />
          </div>
          {confidence !== null && (
            <div className="mt-2 flex items-center gap-2 text-xs text-[var(--color-text-secondary)]">
              <span>Confidence: <strong>{Math.round(confidence * 100)}%</strong></span>
              {detectedLang && <span>Detected: {detectedLang}</span>}
              {glossaryTerms.length > 0 && (
                <span>Glossary terms: {glossaryTerms.join(", ")}</span>
              )}
            </div>
          )}
        </div>
      </div>

      <button
        onClick={handleTranslate}
        disabled={isTranslating || !sourceText.trim()}
        className={cn(
          "self-start rounded-lg px-4 py-2 text-sm font-medium transition-all",
          "bg-[var(--color-accent)] text-white hover:bg-[var(--color-accent)]/90",
          "disabled:opacity-50 disabled:cursor-not-allowed",
        )}
      >
        {isTranslating ? "Translating…" : "Translate"}
      </button>
    </div>
  );
}

async function simulateTranslation(
  text: string,
  sourceLang: string,
  targetLang: string,
  style: TranslationStyle,
  domain: DomainGlossary,
): Promise<{
  text: string;
  confidence: number;
  quality_score: number;
  glossaryTerms: string[];
  model_used: string;
}> {
  await new Promise((r) => setTimeout(r, 200));

  const glossaryTerms =
    domain !== "general"
      ? [`term_${Math.floor(Math.random() * 3)}`, `term_${Math.floor(Math.random() * 3)}`]
      : [];

  const confidence = 0.85 + (style === "technical" ? 0.08 : 0) + (domain !== "general" ? 0.05 : 0);
  const modelUsed = sourceLang !== "auto" && sourceLang !== targetLang ? "m2m100" : "heuristic";

  return {
    text: `[${targetLang.toUpperCase()}] ${text.slice(0, 100)}${text.length > 100 ? "…" : ""}`,
    confidence: Math.min(confidence, 0.98),
    quality_score: Math.min(confidence + 0.02, 1.0),
    glossaryTerms,
    model_used: modelUsed,
  };
}
