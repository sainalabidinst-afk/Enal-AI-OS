"use client";

import { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/design-system/layout/card";
import { Badge } from "@/components/design-system/primitives/badge";
import { Button } from "@/components/design-system/primitives/button";
import { Loader2, RefreshCw, Activity, Zap, Shield, AlertTriangle } from "lucide-react";

interface CapabilityLifecycle {
  id: string;
  name: string;
  category: string;
  state: string;
  health: string;
  version: {
    major: number;
    minor: number;
    patch: number;
    build: string;
    contract_version: string;
    display: string;
  };
  dependencies: string[];
  dependents: string[];
  metrics: {
    execution_count: number;
    success_count: number;
    failure_count: number;
    success_rate: number;
    avg_latency_ms: number;
    last_executed_at: number | null;
    last_error: string | null;
  };
  loaded_at: number | null;
  updated_at: number;
}

interface LifecycleSummary {
  total: number;
  loaded: number;
  unloaded: number;
  suspended: number;
  upgrading: number;
  error: number;
  healthy: number;
  degraded: number;
  unhealthy: number;
}

export default function CapabilityLifecyclePage() {
  const [capabilities, setCapabilities] = useState<CapabilityLifecycle[]>([]);
  const [summary, setSummary] = useState<LifecycleSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchLifecycle = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/v1/capabilities/lifecycle", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("enal-auth-token")}`,
        },
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Failed to fetch capability lifecycle");
      }
      const data = await res.json();
      setCapabilities(data.capabilities);
      setSummary(data.summary);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLifecycle();
    const interval = setInterval(fetchLifecycle, 30000);
    return () => clearInterval(interval);
  }, []);

  const getHealthBadge = (health: string) => {
    switch (health) {
      case "healthy":
        return <Badge variant="success">Healthy</Badge>;
      case "degraded":
        return <Badge variant="warning">Degraded</Badge>;
      case "unhealthy":
        return <Badge variant="danger">Unhealthy</Badge>;
      default:
        return <Badge variant="secondary">Unknown</Badge>;
    }
  };

  const getStateBadge = (state: string) => {
    switch (state) {
      case "loaded":
        return <Badge variant="success">Loaded</Badge>;
      case "unloaded":
        return <Badge variant="secondary">Unloaded</Badge>;
      case "suspended":
        return <Badge variant="warning">Suspended</Badge>;
      case "upgrading":
        return <Badge variant="default">Upgrading</Badge>;
      case "error":
        return <Badge variant="danger">Error</Badge>;
      default:
        return <Badge>{state}</Badge>;
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-[var(--color-text-primary)]">Capability Lifecycle</h1>
          <p className="text-sm text-[var(--color-text-secondary)]">
            Monitor and manage capability pack states, health, and metrics
          </p>
        </div>
        <Button onClick={fetchLifecycle} variant="secondary" size="sm">
          {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <RefreshCw className="h-4 w-4" />}
          Refresh
        </Button>
      </div>

      {error && (
        <div className="text-sm text-[var(--color-danger)]">{error}</div>
      )}

      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-9 gap-4">
          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Total</CardDescription>
              <CardTitle className="text-2xl">{summary.total}</CardTitle>
            </CardHeader>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Loaded</CardDescription>
              <CardTitle className="text-2xl text-[var(--color-success)]">{summary.loaded}</CardTitle>
            </CardHeader>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Unloaded</CardDescription>
              <CardTitle className="text-2xl">{summary.unloaded}</CardTitle>
            </CardHeader>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Suspended</CardDescription>
              <CardTitle className="text-2xl text-[var(--color-warning)]">{summary.suspended}</CardTitle>
            </CardHeader>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Upgrading</CardDescription>
              <CardTitle className="text-2xl">{summary.upgrading}</CardTitle>
            </CardHeader>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Error</CardDescription>
              <CardTitle className="text-2xl text-[var(--color-danger)]">{summary.error}</CardTitle>
            </CardHeader>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Healthy</CardDescription>
              <CardTitle className="text-2xl text-[var(--color-success)]">{summary.healthy}</CardTitle>
            </CardHeader>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Degraded</CardDescription>
              <CardTitle className="text-2xl text-[var(--color-warning)]">{summary.degraded}</CardTitle>
            </CardHeader>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Unhealthy</CardDescription>
              <CardTitle className="text-2xl text-[var(--color-danger)]">{summary.unhealthy}</CardTitle>
            </CardHeader>
          </Card>
        </div>
      )}

      {loading && capabilities.length === 0 ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-[var(--color-primary-500)]" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {capabilities.map((cap) => (
            <Card key={cap.id}>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="text-base">{cap.name}</CardTitle>
                    <CardDescription>{cap.category} · v{cap.version.display}</CardDescription>
                  </div>
                  <div className="flex gap-1">
                    {getStateBadge(cap.state)}
                    {getHealthBadge(cap.health)}
                  </div>
                </div>
              </CardHeader>
              <div className="px-4 pb-4 space-y-3">
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div className="flex items-center gap-1">
                    <Activity className="h-3 w-3" />
                    <span className="text-[var(--color-text-secondary)]">Executions:</span>
                    <span className="font-medium">{cap.metrics.execution_count}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Zap className="h-3 w-3" />
                    <span className="text-[var(--color-text-secondary)]">Success:</span>
                    <span className="font-medium">{Math.round(cap.metrics.success_rate * 100)}%</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Shield className="h-3 w-3" />
                    <span className="text-[var(--color-text-secondary)]">Avg Latency:</span>
                    <span className="font-medium">{Math.round(cap.metrics.avg_latency_ms)}ms</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <AlertTriangle className="h-3 w-3" />
                    <span className="text-[var(--color-text-secondary)]">Failures:</span>
                    <span className="font-medium">{cap.metrics.failure_count}</span>
                  </div>
                </div>

                {cap.metrics.last_error && (
                  <div className="text-xs text-[var(--color-danger)] bg-[var(--color-danger)]/10 rounded px-2 py-1">
                    {cap.metrics.last_error}
                  </div>
                )}

                {cap.dependencies.length > 0 && (
                  <div className="text-xs">
                    <span className="text-[var(--color-text-secondary)]">Dependencies: </span>
                    <span className="font-medium">{cap.dependencies.join(", ")}</span>
                  </div>
                )}

                <div className="text-xs text-[var(--color-text-secondary)]">
                  Updated: {new Date(cap.updated_at * 1000).toLocaleString()}
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
