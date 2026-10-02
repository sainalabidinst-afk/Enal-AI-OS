"use client";

import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { useCognitiveStore } from "@/store/cognitive-store";
import { CognitiveLayer } from "@/types/cognitive";
import type { TranslationConfidenceMetric } from "@/types/cognitive";
import { cn } from "@/lib/utils";
import { MemoryVisualization } from "./memory-visualization";
import { LearningInsights } from "./learning-insights";
import { MetaCognitiveState } from "./meta-cognitive-state";
import { CrossCapabilityView } from "./cross-capability-view";
import { ReasoningChain } from "./reasoning-chain";
import { ConfidenceMeter } from "./confidence-meter";

interface System3StrategicLayerProps {
  className?: string;
}

export function System3StrategicLayer({ className }: System3StrategicLayerProps) {
  const currentLayer = useCognitiveStore((s) => s.current_layer);
  const setLayer = useCognitiveStore((s) => s.setLayer);
  const layerTransitionCount = useCognitiveStore((s) => s.layerTransitionCount);
  const thinkingHistory = useCognitiveStore((s) => s.thinkingHistory);

  if (currentLayer !== CognitiveLayer.META_COGNITIVE) {
    return (
      <div className={cn("flex items-center justify-center h-full", className)}>
        <div className="text-center">
          <p className="text-sm text-[var(--color-text-secondary)] mb-3">
            System 3 is inactive. Switch to L3 for meta-cognitive insights.
          </p>
          <button
            onClick={() => setLayer(CognitiveLayer.META_COGNITIVE)}
            className="px-4 py-2 rounded-lg bg-[var(--color-accent)] text-white text-sm font-medium hover:opacity-90 transition-opacity"
          >
            Activate System 3
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={cn("grid grid-cols-1 lg:grid-cols-3 gap-4 p-4 h-full overflow-y-auto", className)}>
      <div className="space-y-4">
        <Card>
          <CardHeader>
            <CardTitle>Cross-Capability Orchestration</CardTitle>
            <CardDescription>Capability status and coordination</CardDescription>
          </CardHeader>
          <div className="p-4">
            <CrossCapabilityView />
          </div>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Memory Layers</CardTitle>
            <CardDescription>7-layer memory visualization</CardDescription>
          </CardHeader>
          <div className="p-4">
            <MemoryVisualization />
          </div>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Meta-Cognitive State</CardTitle>
            <CardDescription>Confidence, uncertainty, and trend</CardDescription>
          </CardHeader>
          <div className="p-4">
            <MetaCognitiveState />
          </div>
        </Card>
      </div>

      <div className="lg:col-span-2 space-y-4">
        <Card>
          <CardHeader>
            <CardTitle>Executive Dashboard</CardTitle>
            <CardDescription>Cross-capability insights and trends</CardDescription>
          </CardHeader>
          <div className="p-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <MetricCard label="Total Executions" value={thinkingHistory.length.toString()} />
              <MetricCard label="L1 Transitions" value={layerTransitionCount[CognitiveLayer.REACTIVE].toString()} />
              <MetricCard label="L2 Transitions" value={layerTransitionCount[CognitiveLayer.ANALYTICAL].toString()} />
              <MetricCard label="L3 Transitions" value={layerTransitionCount[CognitiveLayer.META_COGNITIVE].toString()} />
            </div>

            <TranslationConfidenceSummary />
          </div>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Reasoning Chain</CardTitle>
            <CardDescription>Step-by-step meta-cognitive reasoning</CardDescription>
          </CardHeader>
          <div className="p-4">
            <ReasoningChain />
          </div>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Confidence Breakdown</CardTitle>
            <CardDescription>Meta-cognitive confidence score</CardDescription>
          </CardHeader>
          <div className="p-4">
            <ConfidenceMeter />
          </div>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Learning Insights</CardTitle>
            <CardDescription>Improvement suggestions from meta-cognition</CardDescription>
          </CardHeader>
          <div className="p-4">
            <LearningInsights />
          </div>
        </Card>
      </div>
    </div>
  );
}

function MetricCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-[var(--color-border)] p-3 bg-[var(--color-bg-primary)]">
      <div className="text-xs text-[var(--color-text-secondary)] mb-1">{label}</div>
      <div className="text-lg font-semibold text-[var(--color-text-primary)]">{value}</div>
    </div>
  );
}

function TranslationConfidenceSummary() {
  const translationConfidences = useCognitiveStore(
    (s) => s.orchestration.translation_confidences ?? [],
  );

  if (translationConfidences.length === 0) return null;

  const latest = translationConfidences[translationConfidences.length - 1];
  const avgConfidence =
    translationConfidences.reduce((sum, m) => sum + m.confidence, 0) /
    translationConfidences.length;
  const avgLatency =
    translationConfidences.reduce((sum, m) => sum + m.latency_ms, 0) /
    translationConfidences.length;
  const confidenceColor =
    avgConfidence >= 0.8
      ? "text-green-500"
      : avgConfidence >= 0.6
      ? "text-yellow-500"
      : avgConfidence >= 0.4
      ? "text-orange-500"
      : "text-red-500";

  return (
    <div className="mt-4 grid grid-cols-3 gap-4">
      <MetricCard
        label="Translation Confidence"
        value={`${Math.round(avgConfidence * 100)}%`}
      />
      <MetricCard label="Latest Pair" value={`${latest.source_lang}→${latest.target_lang}`} />
      <MetricCard label="Avg Latency" value={`${Math.round(avgLatency)}ms`} />
    </div>
  );
}
