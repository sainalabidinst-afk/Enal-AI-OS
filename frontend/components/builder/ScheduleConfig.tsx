'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Tabs, TabPanel } from '@/components/ui/tabs';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  Calendar,
  Plus,
  Trash2,
  Play,
  Pause,
} from 'lucide-react';

interface ScheduleConfigProps {
  schedules: Array<{ id: string; cron: string; name: string }>;
  onChange: (schedules: ScheduleConfigProps['schedules']) => void;
}

const ScheduleConfig: React.FC<ScheduleConfigProps> = ({ schedules, onChange }) => {
  const [newCron, setNewCron] = useState('');
  const [newName, setNewName] = useState('');

  const addSchedule = () => {
    if (!newCron.trim() || !newName.trim()) return;
    onChange([...schedules, { id: `sched-${Date.now()}`, cron: newCron, name: newName }]);
    setNewCron('');
    setNewName('');
  };

  const removeSchedule = (id: string) => {
    onChange(schedules.filter((s) => s.id !== id));
  };

  const tabs = [
    { id: 'active', label: 'Active' },
    { id: 'history', label: 'History' },
  ];

  const [activeTab, setActiveTab] = React.useState('active');

  return (
    <div className="flex h-full w-96 flex-col border-l bg-white">
      <div className="border-b px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Calendar className="h-5 w-5 text-orange-600" />
            <span className="font-semibold text-gray-800">Schedules</span>
            <Badge variant="secondary">{schedules.length}</Badge>
          </div>
        </div>
      </div>

      <ScrollArea className="flex-1 px-4 py-4">
        <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} className="w-full" />

        {activeTab === 'active' && (
          <div className="mt-4 space-y-4">
            <Card className="p-4">
              <h3 className="mb-3 text-sm font-semibold text-gray-700">New Schedule</h3>
              <div className="space-y-3">
                <div className="space-y-1">
                  <Label htmlFor="name">Name</Label>
                  <Input
                    id="name"
                    value={newName}
                    onChange={(e) => setNewName(e.target.value)}
                    placeholder="Daily report"
                  />
                </div>
                <div className="space-y-1">
                  <Label htmlFor="cron">Cron Expression</Label>
                  <Input
                    id="cron"
                    value={newCron}
                    onChange={(e) => setNewCron(e.target.value)}
                    placeholder="0 9 * * *"
                  />
                </div>
                <Button className="w-full" size="sm" onClick={addSchedule}>
                  <Plus className="mr-1 h-4 w-4" />
                  Add Schedule
                </Button>
              </div>
            </Card>

            <div className="space-y-2">
              {schedules.length === 0 && (
                <p className="text-sm text-gray-500">No schedules configured.</p>
              )}
              {schedules.map((schedule) => (
                <Card key={schedule.id} className="p-3">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-sm font-medium text-gray-800">{schedule.name}</div>
                      <div className="text-xs text-gray-500 font-mono">{schedule.cron}</div>
                    </div>
                    <div className="flex items-center gap-1">
                      <Button variant="ghost" size="sm">
                        <Play className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="sm">
                        <Pause className="h-4 w-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => removeSchedule(schedule.id)}
                      >
                        <Trash2 className="h-4 w-4 text-red-500" />
                      </Button>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'history' && (
          <div className="mt-4">
            <p className="text-sm text-gray-500">No execution history yet.</p>
          </div>
        )}
      </ScrollArea>
    </div>
  );
};

export default ScheduleConfig;
