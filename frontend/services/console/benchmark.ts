import { api } from "@/services/api";
import type {
  BenchmarkRunResult,
  BenchmarkSuite,
  CapabilityScores,
  CceStatus,
} from "@/types/console";

export function getBenchmarkSuite() {
  return api.get<BenchmarkSuite>("/api/v1/benchmark/suite");
}

export function runBenchmark() {
  return api.post<BenchmarkRunResult>("/api/v1/benchmark/run");
}

export function getCapabilityScores() {
  return api.get<CapabilityScores>("/api/v1/benchmark/capability-scores");
}

export function getCceStatus() {
  return api.get<CceStatus>("/api/v1/benchmark/cce/status");
}