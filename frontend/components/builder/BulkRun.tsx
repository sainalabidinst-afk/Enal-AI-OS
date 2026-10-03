'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Tabs, TabPanel } from '@/components/ui/tabs';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import {
  Play,
  Square,
  ChevronRight,
  Check,
  X,
  Loader2,
} from 'lucide-react';

interface BulkRunProps {
  onRun?: (tasks: unknown[]) => void;
  onStop?: () => void;
}

const BulkRun: React.FC<BulkRunProps> = ({ onRun, onStop }) => {
  const [isRunning, setIsRunning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [results, setResults] = useState<Array<{ id: string; status: string }>>([]);

  const handleRun = () => {
    setIsRunning(true);
    setProgress(0);
    setResults([]);

    let current = 0;
    const total = 5;
    const interval = setInterval(() => {
      current += 1;
      setProgress((current / total) * 100);
      setResults((prev) => [
        ...prev,
        { id: `task-${current}`, status: current % 2 === 0 ? 'success' : 'failed' },
      ]);

      if (current >= total) {
        clearInterval(interval);
        setIsRunning(false);
        onRun?.([]);
      }
    }, 800);
  };

  const handleStop = () => {
    setIsRunning(false);
    onStop?.();
  };

  const tabs = [
    { id: 'run', label: 'Run' },
    { id: 'history', label: 'History' },
  ];

  const [activeTab, setActiveTab] = React.useState('run');

  return (
    <div className="flex h-full w-96 flex-col border-l bg-white">
      <div className="border-b px-4 py-3">
        <div className="flex items-center justify-between">
          <span className="font-semibold text-gray-800">Bulk Run</span>
          <div className="flex items-center gap-1">
            {!isRunning ? (
              <Button size="sm" onClick={handleRun}>
                <Play className="mr-1 h-4 w-4" />
                Run
              </Button>
            ) : (
              <Button variant="danger" size="sm" onClick={handleStop}>
                <Square className="mr-1 h-4 w-4" />
                Stop
              </Button>
            )}
          </div>
        </div>
      </div>

      <ScrollArea className="flex-1 px-4 py-4">
        <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} className="w-full" />

        {activeTab === 'run' && (
          <div className="mt-4 space-y-4">
            <div className="space-y-2">
              <Label htmlFor="taskCount">Task Count</Label>
              <Input id="taskCount" type="number" defaultValue="5" disabled={isRunning} />
            </div>

            <div className="space-y-2">
              <Label htmlFor="concurrency">Max Concurrency</Label>
              <Input id="concurrency" type="number" defaultValue="10" disabled={isRunning} />
            </div>

            {isRunning && (
              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Progress</span>
                  <span className="font-medium">{Math.round(progress)}%</span>
                </div>
                <Progress value={progress} />
              </div>
            )}

            <div className="space-y-2">
              <Label>Results</Label>
              <div className="space-y-2">
                {results.length === 0 && !isRunning && (
                  <p className="text-sm text-gray-500">No runs yet.</p>
                )}
                {results.map((result) => (
                  <div
                    key={result.id}
                    className="flex items-center justify-between rounded-md border p-2"
                  >
                    <span className="text-sm text-gray-700">{result.id}</span>
                    <Badge variant={result.status === 'success' ? 'default' : 'destructive'}>
                      {result.status}
                    </Badge>
                  </div>
                ))}
                {isRunning && (
                  <div className="flex items-center gap-2 text-sm text-gray-500">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Running...
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'history' && (
          <div className="mt-4 space-y-2">
            <p className="text-sm text-gray-500">No history yet.</p>
          </div>
        )}
      </ScrollArea>
    </div>
  );
};

export default BulkRun;
