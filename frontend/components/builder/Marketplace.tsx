'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabPanel } from '@/components/ui/tabs';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  Search,
  Share2,
  Copy,
  Star,
  Users,
  Filter,
} from 'lucide-react';

interface Template {
  id: string;
  name: string;
  description: string;
  category: string;
  author: string;
  clones: number;
  rating: number;
  tags: string[];
}

const mockTemplates: Template[] = [
  {
    id: 'tpl-1',
    name: 'Customer Support Agent',
    description: 'A customer support agent with knowledge base integration',
    category: 'Agents',
    author: 'Enal-AI-OS',
    clones: 42,
    rating: 4.5,
    tags: ['support', 'kb'],
  },
  {
    id: 'tpl-2',
    name: 'Data Pipeline Tool',
    description: 'ETL pipeline with validation and error handling',
    category: 'Tools',
    author: 'Enal-AI-OS',
    clones: 28,
    rating: 4.2,
    tags: ['etl', 'data'],
  },
  {
    id: 'tpl-3',
    name: 'Voice Receptionist',
    description: 'Voice agent for handling inbound calls',
    category: 'Voice',
    author: 'Enal-AI-OS',
    clones: 15,
    rating: 4.8,
    tags: ['voice', 'telephony'],
  },
];

const Marketplace: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');

  const filteredTemplates = mockTemplates.filter((tpl) => {
    const matchesSearch = tpl.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      tpl.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || tpl.category.toLowerCase() === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const categories = ['all', ...Array.from(new Set(mockTemplates.map((t) => t.category.toLowerCase())))];

  return (
    <div className="flex h-screen w-full flex-col bg-gray-50">
      <header className="border-b bg-white px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Marketplace</h1>
            <p className="mt-1 text-sm text-gray-500">
              Discover and clone agents, tools, and voice agents
            </p>
          </div>
          <div className="flex items-center gap-3">
            <Button variant="secondary" size="sm">
              <Share2 className="mr-2 h-4 w-4" />
              Share Agent
            </Button>
          </div>
        </div>
      </header>

      <div className="border-b bg-white px-6 py-3">
        <div className="flex items-center gap-4">
          <div className="relative flex-1 max-w-xl">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
            <Input
              placeholder="Search templates..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9"
            />
          </div>
          <div className="flex items-center gap-2">
            <Filter className="h-4 w-4 text-gray-500" />
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm text-gray-700 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            >
              {categories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat === 'all' ? 'All Categories' : cat}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-6">
        <Tabs
          tabs={[
            { id: 'all', label: 'All' },
            { id: 'agents', label: 'Agents' },
            { id: 'tools', label: 'Tools' },
            { id: 'voice', label: 'Voice' },
          ]}
          activeTab="all"
          onChange={() => {}}
          className="w-full"
        />

        <div className="mt-6">
          <TemplateGrid templates={filteredTemplates} />
        </div>
      </div>
    </div>
  );
};

interface TemplateGridProps {
  templates: Template[];
}

const TemplateGrid: React.FC<TemplateGridProps> = ({ templates }) => {
  if (templates.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-center">
        <Search className="mb-4 h-12 w-12 text-gray-300" />
        <h3 className="text-lg font-medium text-gray-900">No templates found</h3>
        <p className="mt-1 text-sm text-gray-500">
          Try adjusting your search or filter criteria
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
      {templates.map((template) => (
        <Card key={template.id} className="flex flex-col overflow-hidden">
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
                <Button variant="ghost" size="sm">
                  <Copy className="mr-1 h-4 w-4" />
                  Clone
                </Button>
                <Button size="sm">Use</Button>
              </div>
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
};

export default Marketplace;
