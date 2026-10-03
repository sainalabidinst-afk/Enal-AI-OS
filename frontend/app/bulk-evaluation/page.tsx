"use client";

import BulkRun from '@/components/builder/BulkRun';
import ScheduleConfig from '@/components/builder/ScheduleConfig';
import EvaluationDashboard from '@/components/builder/EvaluationDashboard';
import MetricDetails from '@/components/builder/MetricDetails';
import { Tabs, TabPanel } from '@/components/ui/tabs';

export default function BulkEvaluationPage() {
  return (
    <div className="flex h-screen w-full flex-col bg-gray-50">
      <header className="border-b bg-white px-6 py-4">
        <h1 className="text-2xl font-bold text-gray-900">Bulk, Scheduled & Evaluation</h1>
        <p className="mt-1 text-sm text-gray-500">
          Run bulk executions, manage schedules, and evaluate outputs
        </p>
      </header>

      <div className="flex flex-1 overflow-hidden">
        <div className="flex-1 overflow-y-auto p-6">
          <Tabs
            tabs={[
              { id: 'bulk', label: 'Bulk Run' },
              { id: 'schedule', label: 'Schedules' },
              { id: 'evaluation', label: 'Evaluation' },
            ]}
            activeTab="bulk"
            onChange={() => {}}
            className="w-full"
          />

          <div className="mt-6">
            <BulkRun />
          </div>
        </div>
      </div>
    </div>
  );
}
