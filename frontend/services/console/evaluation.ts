import { api } from "@/services/api";
import type {
  EvaluationResult,
  EvaluationResultsResponse,
  ScheduleJob,
} from "@/types/console";

export function evaluateOutput(payload: {
  output: string;
  criteria?: Record<string, unknown>;
}) {
  return api.post<EvaluationResult>("/api/v1/evaluate", payload);
}

export function getEvaluationResults() {
  return api.get<EvaluationResultsResponse>("/api/v1/evaluate/results");
}

export function listSchedules() {
  return api.get<ScheduleJob[]>("/api/v1/schedule");
}

export function createSchedule(payload: {
  cron: string;
  payload?: Record<string, unknown>;
}) {
  return api.post<{ job_id: string; cron: string; next_run: string }>(
    "/api/v1/schedule",
    payload
  );
}

export function deleteSchedule(jobId: string) {
  return api.delete<{ message: string }>(
    `/api/v1/schedule/${encodeURIComponent(jobId)}`
  );
}