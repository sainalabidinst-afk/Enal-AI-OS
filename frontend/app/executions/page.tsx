"use client";

import { useExecutionStore } from "@/store/execution-store";
import { ExecutionHistoryPanel } from "@/components/execution/execution-history";

export default function ExecutionsPage() {
  const loadExecutions = useExecutionStore((s) => s.loadExecutions);

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-xl font-bold mb-4">Execution History</h1>
      <ExecutionHistoryPanel selectedExecutionId={null} onSelectExecution={() => {}} />
    </div>
  );
}
