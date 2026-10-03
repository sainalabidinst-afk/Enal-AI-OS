'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Tabs, TabPanel } from '@/components/ui/tabs';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Separator } from '@/components/ui/separator';
import {
  Play,
  BarChart3,
  TrendingUp,
  Award,
} from 'lucide-react';

interface EvaluationDashboardProps {
  onEvaluate?: (output: string, criteria: unknown) => void;
}

const EvaluationDashboard: React.FC<EvaluationDashboardProps> = ({ onEvaluate }) => {
  const [output, setOutput] = useState('');
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [result, setResult] = useState<{ score: number; feedback: string } | null>(null);

  const handleEvaluate = () => {
    setIsEvaluating(true);
    setTimeout(() => {
      setResult({
        score: 0.85,
        feedback: 'Simulated evaluation: output is relevant, accurate, and coherent.',
      });
      setIsEvaluating(false);
      onEvaluate?.(output, {});
    }, 1000);
  };

  const tabs = [
    { id: 'evaluate', label: 'Evaluate' },
    { id: 'results', label: 'Results' },
    { id: 'metrics', label: 'Metrics' },
  ];

  const [activeTab, setActiveTab] = React.useState('evaluate');

  return (
    <div className="flex h-full w-96 flex-col border-l bg-white">
      <div className="border-b px-4 py-3">
        <div className="flex items-center gap-2">
          <BarChart3 className="h-5 w-5 text-teal-600" />
          <span className="font-semibold text-gray-800">Evaluation</span>
        </div>
      </div>

      <ScrollArea className="flex-1 px-4 py-4">
        <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} className="w-full" />

        {activeTab === 'evaluate' && (
          <div className="mt-4 space-y-4">
            <div className="space-y-2">
              <Label htmlFor="output">Output to Evaluate</Label>
              <Textarea
                id="output"
                value={output}
                onChange={(e) => setOutput(e.target.value)}
                placeholder="Paste agent/tool output here..."
                rows={6}
              />
            </div>

            <Button
              className="w-full"
              onClick={handleEvaluate}
              disabled={isEvaluating || !output.trim()}
            >
              {isEvaluating ? (
                <>
                  <div className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                  Evaluating...
                </>
              ) : (
                <>
                  <Play className="mr-2 h-4 w-4" />
                  Run Evaluation
                </>
              )}
            </Button>

            {result && (
              <Card className="p-4">
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-700">Score</span>
                    <Badge variant={result.score >= 0.8 ? 'default' : 'secondary'}>
                      {(result.score * 100).toFixed(0)}%
                    </Badge>
                  </div>
                  <Progress value={result.score * 100} />
                  <p className="text-sm text-gray-600">{result.feedback}</p>
                </div>
              </Card>
            )}
          </div>
        )}

        {activeTab === 'results' && (
          <div className="mt-4 space-y-3">
            {!result && (
              <p className="text-sm text-gray-500">No evaluation results yet.</p>
            )}
            {result && (
              <Card className="p-4">
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <Award className="h-4 w-4 text-yellow-600" />
                    <span className="text-sm font-medium text-gray-800">Latest Evaluation</span>
                  </div>
                  <div className="text-sm text-gray-600">{result.feedback}</div>
                  <div className="text-sm font-medium text-gray-800">
                    Score: {(result.score * 100).toFixed(0)}%
                  </div>
                </div>
              </Card>
            )}
          </div>
        )}

        {activeTab === 'metrics' && (
          <div className="mt-4 space-y-3">
            <Card className="p-4">
              <div className="flex items-center gap-2">
                <TrendingUp className="h-4 w-4 text-green-600" />
                <span className="text-sm font-medium text-gray-800">Quality Trend</span>
              </div>
              <div className="mt-2 text-2xl font-bold text-gray-900">85%</div>
              <p className="text-xs text-gray-500">Average score over last 7 days</p>
            </Card>
            <Card className="p-4">
              <div className="flex items-center gap-2">
                <BarChart3 className="h-4 w-4 text-blue-600" />
                <span className="text-sm font-medium text-gray-800">Evaluations Run</span>
              </div>
              <div className="mt-2 text-2xl font-bold text-gray-900">42</div>
              <p className="text-xs text-gray-500">Total evaluations this month</p>
            </Card>
          </div>
        )}
      </ScrollArea>
    </div>
  );
};

export default EvaluationDashboard;
