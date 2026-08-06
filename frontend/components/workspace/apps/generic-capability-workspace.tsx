"use client";

import { useState, useEffect, useCallback } from "react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/design-system/layout/card";
import { Badge } from "@/components/design-system/primitives/badge";
import { Button } from "@/components/design-system/primitives/button";
import { Input } from "@/components/design-system/primitives/input";
import { Loader2, Send, Sparkles } from "lucide-react";
import { AIWorkspacePanel } from "../ai/ai-workspace-panel";

interface GenericCapabilityWorkspaceProps {
  capabilityId: string;
  capabilityName: string;
}

interface CapabilityResult {
  app: string;
  version: string;
  input: string;
  pipeline: string[];
  result: Record<string, any>;
  metadata: {
    category: string;
    capabilities_used: string[];
    [key: string]: any;
  };
}

export function GenericCapabilityWorkspace({ capabilityId, capabilityName }: GenericCapabilityWorkspaceProps) {
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<CapabilityResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleExecute = useCallback(async () => {
    if (!input.trim() || isLoading) return;

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`/api/v1/capabilities/${capabilityId}/execute`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("enal-auth-token")}`,
        },
        body: JSON.stringify({
          message: input,
          conversation_id: `conv-${capabilityId}-${Date.now()}`,
          workspace_id: `ws-${capabilityId}`,
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || "Execution failed");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setIsLoading(false);
    }
  }, [capabilityId, input, isLoading]);

  return (
    <div className="flex h-full">
      {/* Main panel */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-[var(--color-text-primary)]">{capabilityName}</h1>
          <p className="text-sm text-[var(--color-text-secondary)]">
            Execute {capabilityName} capabilities with AI-powered decision intelligence
          </p>
        </div>

        {/* Input section */}
        <Card>
          <CardHeader>
            <CardTitle>New Request</CardTitle>
            <CardDescription>Enter your request for {capabilityName}</CardDescription>
          </CardHeader>
          <div className="p-4 space-y-4">
            <div className="flex gap-2">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleExecute()}
                placeholder={`Ask ${capabilityName}...`}
                className="flex-1"
                disabled={isLoading}
              />
              <Button onClick={handleExecute} disabled={isLoading || !input.trim()}>
                {isLoading ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <Send className="h-4 w-4" />
                )}
              </Button>
            </div>
            {error && (
              <div className="text-sm text-[var(--color-danger)]">{error}</div>
            )}
          </div>
        </Card>

        {/* Result section */}
        {result && (
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Sparkles className="h-4 w-4 text-[var(--color-primary-500)]" />
                <CardTitle>Result</CardTitle>
              </div>
            </CardHeader>
            <div className="p-4 space-y-4">
              <div>
                <h3 className="text-sm font-medium text-[var(--color-text-secondary)]">Input</h3>
                <p className="text-sm text-[var(--color-text-primary)]">{result.input}</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-[var(--color-text-secondary)]">Pipeline</h3>
                <div className="flex flex-wrap gap-2 mt-1">
                  {result.pipeline?.map((step, idx) => (
                    <Badge key={idx} variant="secondary">{step}</Badge>
                  ))}
                </div>
              </div>
              <div>
                <h3 className="text-sm font-medium text-[var(--color-text-secondary)]">Output</h3>
                <pre className="mt-2 text-xs bg-[var(--color-bg-secondary)] p-3 rounded-lg overflow-x-auto">
                  {JSON.stringify(result.result, null, 2)}
                </pre>
              </div>
            </div>
          </Card>
        )}
      </div>

      {/* AI Workspace panel with Decision Intelligence */}
      <AIWorkspacePanel capabilityId={capabilityId} />
    </div>
  );
}
