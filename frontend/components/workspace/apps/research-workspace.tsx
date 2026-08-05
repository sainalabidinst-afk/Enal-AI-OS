"use client";

import { useState } from "react";
import { FlaskConical, Search, FileText, GitBranch, Lightbulb } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Tabs, TabPanel } from "@/components/ui/tabs";

type Tab = "search" | "findings" | "synthesis" | "citations" | "report";

const TABS = [
  { id: "search" as Tab, label: "Search", icon: <Search className="h-3.5 w-3.5" /> },
  { id: "findings" as Tab, label: "Findings", icon: <Lightbulb className="h-3.5 w-3.5" /> },
  { id: "synthesis" as Tab, label: "Synthesis", icon: <FlaskConical className="h-3.5 w-3.5" /> },
  { id: "citations" as Tab, label: "Citations", icon: <GitBranch className="h-3.5 w-3.5" /> },
  { id: "report" as Tab, label: "Report", icon: <FileText className="h-3.5 w-3.5" /> },
];

const FINDINGS = [
  { id: "F-1", title: "AI significantly improves software development productivity", confidence: 0.92, sources: 3 },
  { id: "F-2", title: "LLMs improve code generation speed but may introduce subtle bugs", confidence: 0.88, sources: 2 },
  { id: "F-3", title: "ML techniques show promise in automating requirements elicitation", confidence: 0.82, sources: 1 },
];

export function ResearchWorkspace() {
  const [tab, setTab] = useState<Tab>("search");

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between border-b border-[var(--color-border)] px-4 py-2">
        <h2 className="text-sm font-semibold">Research Workspace</h2>
        <Tabs tabs={TABS} activeTab={tab} onChange={(id) => setTab(id as Tab)} />
      </div>

      <TabPanel>
        {tab === "search" && (
          <div className="p-4 space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Search Evidence</CardTitle>
                <CardDescription>Gather evidence from multiple sources with quality ranking.</CardDescription>
              </CardHeader>
              <div className="px-4 py-3">
                <div className="flex gap-2">
                  <input
                    type="text"
                    placeholder="Enter research query..."
                    className="flex-1 rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] px-4 py-2 text-sm"
                  />
                  <Button>Search</Button>
                </div>
              </div>
            </Card>
          </div>
        )}

        {tab === "findings" && (
          <div className="p-4 space-y-2">
            {FINDINGS.map((finding) => (
              <Card key={finding.id}>
                <div className="px-4 py-3">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-medium">{finding.title}</p>
                    <span className="text-xs text-[var(--color-text-secondary)]">Confidence: {(finding.confidence * 100).toFixed(0)}%</span>
                  </div>
                  <p className="text-xs text-[var(--color-text-secondary)] mt-1">{finding.sources} sources</p>
                </div>
              </Card>
            ))}
          </div>
        )}

        {tab === "synthesis" && (
          <div className="p-4">
            <Card>
              <CardHeader>
                <CardTitle>Synthesis</CardTitle>
                <CardDescription>Multi-source narrative synthesis and consensus detection.</CardDescription>
              </CardHeader>
              <div className="px-4 py-3 text-sm text-[var(--color-text-secondary)]">
                Consensus areas: AI improves productivity, LLMs speed up development.
                Conflict areas: Long-term impact on code quality remains uncertain.
              </div>
            </Card>
          </div>
        )}

        {tab === "citations" && (
          <div className="p-4">
            <Card>
              <CardHeader>
                <CardTitle>Citations</CardTitle>
                <CardDescription>Citation management and quality assessment.</CardDescription>
              </CardHeader>
              <div className="px-4 py-3 text-sm text-[var(--color-text-secondary)]">3 citations ready.</div>
            </Card>
          </div>
        )}

        {tab === "report" && (
          <div className="p-4">
            <Card>
              <CardHeader>
                <CardTitle>Research Report</CardTitle>
                <CardDescription>Generated research report with structured findings.</CardDescription>
              </CardHeader>
              <div className="px-4 py-3 text-sm text-[var(--color-text-secondary)]">Report will be generated here.</div>
            </Card>
          </div>
        )}
      </TabPanel>
    </div>
  );
}