"use client";

import { useEffect, useRef, useCallback } from "react";

export interface PerformanceMetrics {
  renderTime: number;
  interactionLatency: number;
  analysisLatency: number;
  decisionLatency: number;
  memoryUsage: number | null;
  timestamp: number;
}

type MetricListener = (metrics: PerformanceMetrics) => void;

class PerformanceMonitor {
  private listeners = new Set<MetricListener>();
  private metrics: PerformanceMetrics[] = [];
  private maxMetrics = 1000;

  recordRender(componentName: string, renderTime: number) {
    this.record({
      renderTime,
      interactionLatency: 0,
      analysisLatency: 0,
      decisionLatency: 0,
      memoryUsage: this.getMemoryUsage(),
      timestamp: Date.now(),
    });
  }

  recordInteraction(latency: number) {
    this.record({
      renderTime: 0,
      interactionLatency: latency,
      analysisLatency: 0,
      decisionLatency: 0,
      memoryUsage: this.getMemoryUsage(),
      timestamp: Date.now(),
    });
  }

  recordAnalysis(latency: number) {
    this.record({
      renderTime: 0,
      interactionLatency: 0,
      analysisLatency: latency,
      decisionLatency: 0,
      memoryUsage: this.getMemoryUsage(),
      timestamp: Date.now(),
    });
  }

  recordDecision(latency: number) {
    this.record({
      renderTime: 0,
      interactionLatency: 0,
      analysisLatency: 0,
      decisionLatency: latency,
      memoryUsage: this.getMemoryUsage(),
      timestamp: Date.now(),
    });
  }

  subscribe(listener: MetricListener) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  getMetrics() {
    return [...this.metrics];
  }

  getAverageRenderTime() {
    const renders = this.metrics.filter((m) => m.renderTime > 0);
    if (renders.length === 0) return 0;
    return renders.reduce((sum, m) => sum + m.renderTime, 0) / renders.length;
  }

  private record(metrics: PerformanceMetrics) {
    this.metrics.push(metrics);
    if (this.metrics.length > this.maxMetrics) {
      this.metrics.shift();
    }
    this.listeners.forEach((listener) => listener(metrics));
  }

  private getMemoryUsage(): number | null {
    if (typeof performance !== "undefined" && (performance as any).memory) {
      return (performance as any).memory.usedJSHeapSize;
    }
    return null;
  }
}

export const performanceMonitor = new PerformanceMonitor();

export function usePerformanceMonitor(componentName: string) {
  const renderStartRef = useRef<number>(0);

  useEffect(() => {
    renderStartRef.current = performance.now();
  });

  useEffect(() => {
    const renderTime = performance.now() - renderStartRef.current;
    performanceMonitor.recordRender(componentName, renderTime);
  });

  const measureInteraction = useCallback((callback: () => void) => {
    const start = performance.now();
    callback();
    const latency = performance.now() - start;
    performanceMonitor.recordInteraction(latency);
    return latency;
  }, []);

  return { measureInteraction };
}
