'use client';

import React from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import {
  Star,
  Users,
  Copy,
  ExternalLink,
} from 'lucide-react';

interface TemplateCardProps {
  template: {
    id: string;
    name: string;
    description: string;
    category: string;
    author: string;
    clones: number;
    rating: number;
    tags: string[];
  };
  onClone?: () => void;
  onUse?: () => void;
}

const TemplateCard: React.FC<TemplateCardProps> = ({
  template,
  onClone,
  onUse,
}) => {
  return (
    <Card className="flex flex-col overflow-hidden">
      <div className="p-5">
        <div className="flex items-start justify-between">
          <div>
            <h3 className="text-base font-semibold text-gray-900">{template.name}</h3>
            <p className="mt-1 text-sm text-gray-500">{template.description}</p>
          </div>
          <Badge variant="secondary">{template.category}</Badge>
        </div>

        <div className="mt-4 flex items-center gap-4 text-sm text-gray-500">
          <div className="flex items-center gap-1">
            <Users className="h-4 w-4" />
            <span>{template.clones} clones</span>
          </div>
          <div className="flex items-center gap-1">
            <Star className="h-4 w-4 text-yellow-500" />
            <span>{template.rating}</span>
          </div>
        </div>

        <div className="mt-3 flex flex-wrap gap-1.5">
          {template.tags.map((tag) => (
            <span
              key={tag}
              className="rounded-full bg-gray-100 px-2.5 py-0.5 text-xs text-gray-600"
            >
              {tag}
            </span>
          ))}
        </div>
      </div>

      <div className="mt-auto border-t bg-gray-50 px-5 py-3">
        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-500">by {template.author}</span>
          <div className="flex items-center gap-2">
            <Button variant="ghost" size="sm" onClick={onClone}>
              <Copy className="mr-1 h-4 w-4" />
              Clone
            </Button>
            <Button size="sm" onClick={onUse}>
              <ExternalLink className="mr-1 h-4 w-4" />
              Use
            </Button>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default TemplateCard;
