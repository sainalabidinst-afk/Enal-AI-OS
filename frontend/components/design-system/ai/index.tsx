"use client";

import { type ReactNode, useState } from "react";
import { cn } from "@/lib/utils";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/design-system/layout/card";
import { Badge } from "@/components/design-system/primitives/badge";

interface AIResponseProps {
  children: ReactNode;
  className?: string;
}

export function AIResponse({ children, className }: AIResponseProps) {
  return (
    <div className={cn("rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-4", className)}>
      {children}
    </div>
  );
}

interface AIThinkingProps {
  children: ReactNode;
  className?: string;
}

export function AIThinking({ children, className }: AIThinkingProps) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className={cn("rounded-lg border border-[var(--color-border)] bg-[var(--color-secondary-50)] p-3", className)}>
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center gap-2 text-xs font-medium text-[var(--color-secondary-600)] hover:text-[var(--color-foreground)] transition-colors"
      >
        {expanded ? "▼" : "▶"} AI Thinking
      </button>
      {expanded && <div className="mt-2 text-xs text-[var(--color-secondary-600)]">{children}</div>}
    </div>
  );
}

interface EvidenceCardProps {
  title: string;
  evidence: string;
  source?: string;
  confidence?: number;
  className?: string;
}

export function EvidenceCard({ title, evidence, source, confidence, className }: EvidenceCardProps) {
  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>{title}</CardTitle>
          {confidence !== undefined && (
            <Badge variant={confidence >= 0.8 ? "success" : confidence >= 0.5 ? "warning" : "danger"}>
              {(confidence * 100).toFixed(0)}%
            </Badge>
          )}
        </div>
      </CardHeader>
      <div className="px-4 pb-4">
        <p className="text-sm text-[var(--color-foreground)]">{evidence}</p>
        {source && <p className="text-xs text-[var(--color-secondary-500)] mt-2">Source: {source}</p>}
      </div>
    </Card>
  );
}

interface ReasoningCardProps {
  reasoning: string;
  steps?: string[];
  className?: string;
}

export function ReasoningCard({ reasoning, steps, className }: ReasoningCardProps) {
  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle>Reasoning</CardTitle>
      </CardHeader>
      <div className="px-4 pb-4 space-y-2">
        <p className="text-sm text-[var(--color-foreground)]">{reasoning}</p>
        {steps && steps.length > 0 && (
          <div className="mt-3 space-y-1">
            {steps.map((step, i) => (
              <div key={i} className="flex items-start gap-2 text-xs text-[var(--color-secondary-600)]">
                <span className="text-[var(--color-primary-500)] font-medium">{i + 1}.</span>
                {step}
              </div>
            ))}
          </div>
        )}
      </div>
    </Card>
  );
}

interface ConfidenceBadgeProps {
  confidence: number;
  className?: string;
}

export function ConfidenceBadge({ confidence, className }: ConfidenceBadgeProps) {
  const variant = confidence >= 0.8 ? "success" : confidence >= 0.5 ? "warning" : "danger";
  return <Badge variant={variant} className={className}>{`${(confidence * 100).toFixed(0)}%`}</Badge>;
}

interface RecommendationCardProps {
  title: string;
  recommendation: string;
  confidence?: number;
  risk?: string;
  className?: string;
}

export function RecommendationCard({ title, recommendation, confidence, risk, className }: RecommendationCardProps) {
  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>{title}</CardTitle>
          {confidence !== undefined && <ConfidenceBadge confidence={confidence} />}
        </div>
      </CardHeader>
      <div className="px-4 pb-4 space-y-2">
        <p className="text-sm text-[var(--color-foreground)]">{recommendation}</p>
        {risk && (
          <div className="text-xs text-[var(--color-secondary-500)]">
            <span className="font-medium">Risk:</span> {risk}
          </div>
        )}
      </div>
    </Card>
  );
}

interface RiskCardProps {
  title: string;
  risk: string;
  level: "low" | "medium" | "high" | "critical";
  className?: string;
}

export function RiskCard({ title, risk, level, className }: RiskCardProps) {
  const levelColors = {
    low: "text-[var(--color-success-500)]",
    medium: "text-[var(--color-warning-500)]",
    high: "text-[var(--color-danger-500)]",
    critical: "text-[var(--color-danger-500)]",
  };

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>{title}</CardTitle>
          <span className={cn("text-xs font-medium uppercase", levelColors[level])}>{level}</span>
        </div>
      </CardHeader>
      <div className="px-4 pb-4">
        <p className="text-sm text-[var(--color-foreground)]">{risk}</p>
      </div>
    </Card>
  );
}

interface CitationCardProps {
  source: string;
  citation: string;
  className?: string;
}

export function CitationCard({ source, citation, className }: CitationCardProps) {
  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle>Citation</CardTitle>
      </CardHeader>
      <div className="px-4 pb-4">
        <p className="text-sm text-[var(--color-foreground)] italic">"{citation}"</p>
        <p className="text-xs text-[var(--color-secondary-500)] mt-2">— {source}</p>
      </div>
    </Card>
  );
}
