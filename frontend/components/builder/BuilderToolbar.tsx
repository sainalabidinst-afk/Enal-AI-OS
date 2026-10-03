'use client';

import React from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Bot,
  Wrench,
  BookOpen,
  GitBranch,
  Clock,
  Play,
  Save,
  Trash2,
  Undo2,
  Redo2,
  ZoomIn,
  ZoomOut,
} from 'lucide-react';

interface BuilderToolbarProps {
  onRun?: () => void;
  onSave?: () => void;
  onClear?: () => void;
}

const BuilderToolbar: React.FC<BuilderToolbarProps> = ({
  onRun,
  onSave,
  onClear,
}) => {
  const onDragStart = (event: React.DragEvent, nodeType: string) => {
    event.dataTransfer.setData('application/reactflow', nodeType);
    event.dataTransfer.effectAllowed = 'move';
  };

  return (
    <div className="flex items-center justify-between border-b bg-white px-4 py-2">
      <div className="flex items-center gap-2">
        <span className="text-sm font-semibold text-gray-700">Builder</span>
        <div className="mx-2 h-6 w-px bg-gray-300" />
        <div className="flex items-center gap-1">
          <div
            draggable
            onDragStart={(e) => onDragStart(e, 'agent')}
            className="cursor-grab rounded-md border bg-blue-50 px-3 py-1.5 text-xs text-blue-700 hover:bg-blue-100"
          >
            <Bot className="mr-1 inline h-3.5 w-3.5" />
            Agent
          </div>
          <div
            draggable
            onDragStart={(e) => onDragStart(e, 'tool')}
            className="cursor-grab rounded-md border bg-green-50 px-3 py-1.5 text-xs text-green-700 hover:bg-green-100"
          >
            <Wrench className="mr-1 inline h-3.5 w-3.5" />
            Tool
          </div>
          <div
            draggable
            onDragStart={(e) => onDragStart(e, 'knowledgeBase')}
            className="cursor-grab rounded-md border bg-purple-50 px-3 py-1.5 text-xs text-purple-700 hover:bg-purple-100"
          >
            <BookOpen className="mr-1 inline h-3.5 w-3.5" />
            KB
          </div>
          <div
            draggable
            onDragStart={(e) => onDragStart(e, 'conditional')}
            className="cursor-grab rounded-md border bg-orange-50 px-3 py-1.5 text-xs text-orange-700 hover:bg-orange-100"
          >
            <GitBranch className="mr-1 inline h-3.5 w-3.5" />
            If/Else
          </div>
          <div
            draggable
            onDragStart={(e) => onDragStart(e, 'delay')}
            className="cursor-grab rounded-md border bg-gray-50 px-3 py-1.5 text-xs text-gray-700 hover:bg-gray-100"
          >
            <Clock className="mr-1 inline h-3.5 w-3.5" />
            Delay
          </div>
        </div>
      </div>
      <div className="flex items-center gap-2">
        <Button variant="ghost" size="sm" onClick={onClear}>
          <Trash2 className="mr-1 h-4 w-4" />
          Clear
        </Button>
        <Button variant="ghost" size="sm">
          <Undo2 className="mr-1 h-4 w-4" />
        </Button>
        <Button variant="ghost" size="sm">
          <Redo2 className="mr-1 h-4 w-4" />
        </Button>
        <Button variant="ghost" size="sm">
          <ZoomOut className="mr-1 h-4 w-4" />
        </Button>
        <Button variant="ghost" size="sm">
          <ZoomIn className="mr-1 h-4 w-4" />
        </Button>
        <div className="mx-1 h-6 w-px bg-gray-300" />
        <Button variant="secondary" size="sm" onClick={onSave}>
          <Save className="mr-1 h-4 w-4" />
          Save
        </Button>
        <Button size="sm" onClick={onRun}>
          <Play className="mr-1 h-4 w-4" />
          Run
        </Button>
      </div>
    </div>
  );
};

export default BuilderToolbar;
