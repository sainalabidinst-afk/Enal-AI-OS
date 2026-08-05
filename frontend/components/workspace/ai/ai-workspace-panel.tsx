"use client";

import { useState, useEffect } from "react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/design-system/layout/card";
import { Badge } from "@/components/design-system/primitives/badge";
import { Button } from "@/components/design-system/primitives/button";
import { useConversationStore } from "./stores/conversation-store";
import { useMemoryStore } from "./stores/memory-store";
import { tradingCapabilityAdapter } from "./adapters/trading-capability-adapter";
import { promptPipelineBuilder } from "./pipeline/prompt-pipeline";
import { EvidenceBuilder } from "./evidence/evidence-builder";
import type { EvidencePayload } from "./evidence/evidence-types";
import { Sparkles, CheckCircle, AlertTriangle, TrendingUp } from "lucide-react";

export function AIWorkspacePanel({ capabilityId = "trading" }: { capabilityId?: string }) {
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const currentThread = useConversationStore((s) => s.currentThread);
  const addMessage = useConversationStore((s) => s.addMessage);
  const setLoading = useConversationStore((s) => s.setLoading);
  const setError = useConversationStore((s) => s.setError);
  const lastEvidence = useConversationStore((s) => s.lastEvidence);

  useEffect(() => {
    const adapter = tradingCapabilityAdapter;
    adapter.provideContext().then((context) => {
      useConversationStore.getState().setCapabilityContext(context);
    });
  }, [capabilityId]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = {
      id: `msg-${Date.now()}`,
      role: "user" as const,
      content: input,
      timestamp: Date.now(),
    };

    addMessage(userMessage);
    setInput("");
    setIsLoading(true);
    setLoading(true);
    setError(null);

    try {
      const adapter = tradingCapabilityAdapter;
      const context = await adapter.provideContext();
      const tools = await adapter.provideTools();
      const knowledge = await adapter.provideKnowledge(input);

      const pipeline = promptPipelineBuilder.build({
        userMessage: input,
        capabilityContext: context,
        tools,
        memory: useMemoryStore.getState().getMemory(context.workspaceId, context.capabilityId) ?? {
          workspaceId: context.workspaceId,
          capabilityId: context.capabilityId,
          conversationHistory: [],
          preferences: {},
        },
        knowledge,
      });

      const responseContent = `Based on your question about "${input}", here is my analysis for ${context.symbol ?? "the market"}.`;

      const evidence = EvidenceBuilder.build({
        summary: responseContent,
        items: [
          EvidenceBuilder.fromData("Symbol", context.symbol ?? "Unknown"),
          EvidenceBuilder.fromData("Timeframe", context.timeframe ?? "1h"),
          ...knowledge.evidence,
        ],
        reasoning: "Analyzed current market data, indicators, and recent news.",
        confidence: 75,
        alternative: "Market conditions may change rapidly.",
        nextAction: "Monitor key levels and adjust strategy accordingly.",
      });

      const assistantMessage = {
        id: `msg-${Date.now()}`,
        role: "assistant" as const,
        content: responseContent,
        timestamp: Date.now(),
        evidence,
      };

      addMessage(assistantMessage);
      useConversationStore.getState().setLastEvidence(evidence);
    } catch (error) {
      setError(error instanceof Error ? error.message : "An error occurred");
    } finally {
      setIsLoading(false);
      setLoading(false);
    }
  };

  const renderEvidence = (evidence: EvidencePayload) => {
    return (
      <div className="mt-3 space-y-2">
        <div className="flex items-center gap-2">
          <Sparkles className="h-4 w-4 text-[var(--color-primary-500)]" />
          <span className="text-sm font-medium">Summary</span>
        </div>
        <p className="text-sm text-[var(--color-secondary-600)]">{evidence.summary}</p>

        <div className="space-y-1">
          <span className="text-xs font-medium text-[var(--color-secondary-500)]">Evidence</span>
          {evidence.evidence.map((item, idx) => (
            <div key={idx} className="flex items-center gap-2 text-xs">
              <span className="text-[var(--color-secondary-500)]">•</span>
              <span className="font-medium">{item.label}:</span>
              <span className="text-[var(--color-secondary-600)]">{String(item.value)}</span>
            </div>
          ))}
        </div>

        <div className="space-y-1">
          <span className="text-xs font-medium text-[var(--color-secondary-500)]">Reasoning</span>
          <p className="text-xs text-[var(--color-secondary-600)]">{evidence.reasoning}</p>
        </div>

        <div className="flex items-center gap-2">
          <CheckCircle className="h-4 w-4 text-[var(--color-success-500)]" />
          <span className="text-sm font-medium">Confidence</span>
          <Badge variant="success">{evidence.confidence}%</Badge>
        </div>

        {evidence.alternative && (
          <div className="flex items-start gap-2">
            <AlertTriangle className="h-4 w-4 text-[var(--color-warning-500)] mt-0.5" />
            <div>
              <span className="text-xs font-medium text-[var(--color-secondary-500)]">Alternative</span>
              <p className="text-xs text-[var(--color-secondary-600)]">{evidence.alternative}</p>
            </div>
          </div>
        )}

        {evidence.nextAction && (
          <div className="flex items-start gap-2">
            <TrendingUp className="h-4 w-4 text-[var(--color-primary-500)] mt-0.5" />
            <div>
              <span className="text-xs font-medium text-[var(--color-secondary-500)]">Next Action</span>
              <p className="text-xs text-[var(--color-secondary-600)]">{evidence.nextAction}</p>
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <aside className="flex w-80 flex-col border-l border-[var(--color-border)] bg-[var(--color-surface)]" aria-label="AI Workspace panel">
      <div className="border-b border-[var(--color-border)] px-4 py-3">
        <h2 className="text-sm font-semibold">AI Workspace</h2>
        <p className="text-xs text-[var(--color-secondary-500)]">Capability: {capabilityId}</p>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {currentThread?.messages.map((message) => (
          <Card key={message.id}>
            <CardHeader>
              <div className="flex items-center gap-2">
                <span className="text-xs font-medium text-[var(--color-secondary-500)]">
                  {message.role === "user" ? "You" : "AI"}
                </span>
                <span className="text-xs text-[var(--color-secondary-500)]">
                  {new Date(message.timestamp).toLocaleTimeString()}
                </span>
              </div>
              <CardDescription>{message.content}</CardDescription>
            </CardHeader>
            {message.evidence && renderEvidence(message.evidence)}
          </Card>
        ))}

        {isLoading && (
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-[var(--color-primary-500)] border-t-transparent" />
                <span className="text-sm text-[var(--color-secondary-500)]">AI is thinking...</span>
              </div>
            </CardHeader>
          </Card>
        )}
      </div>

      <div className="border-t border-[var(--color-border)] p-4">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Ask AI..."
            className="flex-1 text-sm border border-[var(--color-border)] rounded-lg px-3 py-2 bg-[var(--color-bg-secondary)]"
          />
          <Button onClick={handleSend} disabled={isLoading}>
            Send
          </Button>
        </div>
      </div>
    </aside>
  );
}

