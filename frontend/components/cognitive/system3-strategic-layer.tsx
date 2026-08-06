"use client";

import { type ReactNode } from "react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { useCognitiveStore } from "@/store/cognitive-store";
import { CognitiveLayer } from "@/types/cognitive";
import { cn } from "@/lib/utils";

interface System3StrategicLayerProps {
  className?: string;
}

export function System3StrategicLayer({ className }: System3StrategicLayerProps) {
  const currentLayer = useCognitiveStore((s) => s.current_layer);
  const setLayer = useCognitiveStore((s) => s.setLayer);
  const thinkingHistory = useCognitiveStore((s) => s.thinkingHistory);
  const layerTransitionCount = useCognitiveStore((s) => s.layerTransitionCount);
  const metaFlags = useCognitiveStore((s) => s.meta_cognitive_flags);

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
            <CardTitle>Capability Registry</CardTitle>
            <CardDescription>Cross-capability orchestration</CardDescription>
          </CardHeader>
          <div className="p-4">
            <div className="space-y-2">
              {["Network Engineer", "Code Engineer", "Trading Analyst", "System Architect"].map((cap) => (
                <div
                  key={cap}
                  className="flex items-center justify-between rounded-lg border border-[var(--color-border)] p-3 bg-[var(--color-bg-primary)]"
                >
                  <span className="text-sm text-[var(--color-text-primary)]">{cap}</span>
                  <span className="text-xs px-2 py-0.5 rounded-full bg-green-100 text-green-700">Ready</span>
                </div>
              ))}
            </div>
          </div>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Memory Layers</CardTitle>
            <CardDescription>7-layer memory visualization</CardDescription>
          </CardHeader>
          <div className="p-4">
            <MemoryLayersPlaceholder />
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
              <MetricCard label="Total Executions" value="1,234" />
              <MetricCard label="Success Rate" value="94%" />
              <MetricCard label="Avg Confidence" value="87%" />
              <MetricCard label="Active Capabilities" value="13" />
            </div>
          </div>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Learning Insights</CardTitle>
            <CardDescription>Improvement suggestions from meta-cognition</CardDescription>
          </CardHeader>
          <div className="p-4">
            <InsightsPlaceholder />
          </div>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Cognitive State</CardTitle>
            <CardDescription>
              Uncertainty: {metaFlags.uncertainty ? "Yes" : "No"} | Trend: {metaFlags.confidence_trend}
            </CardDescription>
          </CardHeader>
          <div className="p-4">
            <div className="grid grid-cols-2 gap-3">
              <StatusItem label="L1 Transitions" value={layerTransitionCount[CognitiveLayer.REACTIVE].toString()} />
              <StatusItem label="L2 Transitions" value={layerTransitionCount[CognitiveLayer.ANALYTICAL].toString()} />
              <StatusItem label="L3 Transitions" value={layerTransitionCount[CognitiveLayer.META_COGNITIVE].toString()} />
              <StatusItem label="Thinking Modes" value={thinkingHistory.length.toString()} />
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}

function MemoryLayersPlaceholder() {
  const layers = [
    { name: "Working", color: "bg-blue-500" },
    { name: "Conversation", color: "bg-green-500" },
    { name: "Knowledge", color: "bg-yellow-500" },
    { name: "Long-term", color: "bg-purple-500" },
    { name: "Episodic", color: "bg-pink-500" },
    { name: "Session", color: "bg-indigo-500" },
    { name: "Project", color: "bg-orange-500" },
  ];

  return (
    <div className="space-y-2">
      {layers.map((layer) => (
        <div key={layer.name} className="flex items-center gap-2">
          <div className={cn("w-3 h-3 rounded", layer.color)} />
          <span className="text-xs text-[var(--color-text-primary)]">{layer.name}</span>
          <span className="text-xs text-[var(--color-text-secondary)] ml-auto">Active</span>
        </div>
      ))}
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

function InsightsPlaceholder() {
  return (
    <div className="space-y-2">
      {[
        { text: "Consider using database partitioning for large tables", priority: "high" },
        { text: "Add integration tests for new API endpoints", priority: "medium" },
        { text: "Review memory consolidation frequency", priority: "low" },
      ].map((insight, i) => (
        <div
          key={i}
          className="flex items-start gap-2 rounded-lg border border-[var(--color-border)] p-3 bg-[var(--color-bg-primary)]"
        >
          <div
            className={cn(
              "w-2 h-2 rounded-full mt-1",
              insight.priority === "high" && "bg-red-500",
              insight.priority === "medium" && "bg-yellow-500",
              insight.priority === "low" && "bg-green-500"
            )}
          />
          <span className="text-xs text-[var(--color-text-primary)]">{insight.text}</span>
        </div>
      ))}
    </div>
  );
}

function StatusItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex flex-col">
      <span className="text-xs text-[var(--color-text-secondary)]">{label}</span>
      <span className="text-sm font-medium text-[var(--color-text-primary)]">{value}</span>
    </div>
  );
}
