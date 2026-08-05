"use client";

import { useState } from "react";
import { Shield, Scan, Bug, FileCheck, AlertTriangle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Tabs, TabPanel } from "@/components/ui/tabs";

type Tab = "scan" | "findings" | "reports" | "compliance" | "alerts";

const TABS = [
  { id: "scan" as Tab, label: "Scan", icon: <Scan className="h-3.5 w-3.5" /> },
  { id: "findings" as Tab, label: "Findings", icon: <Bug className="h-3.5 w-3.5" /> },
  { id: "reports" as Tab, label: "Reports", icon: <FileCheck className="h-3.5 w-3.5" /> },
  { id: "compliance" as Tab, label: "Compliance", icon: <Shield className="h-3.5 w-3.5" /> },
  { id: "alerts" as Tab, label: "Alerts", icon: <AlertTriangle className="h-3.5 w-3.5" /> },
];

const FINDINGS = [
  { id: "SEC-001", severity: "critical", title: "SQL Injection in login form", location: "app.py:42" },
  { id: "SEC-002", severity: "high", title: "Hardcoded API key detected", location: "config.py:14" },
  { id: "SEC-003", severity: "medium", title: "Missing HTTPS redirect", location: "nginx.conf" },
];

export function SecurityWorkspace() {
  const [tab, setTab] = useState<Tab>("scan");

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between border-b border-[var(--color-border)] px-4 py-2">
        <h2 className="text-sm font-semibold">Security Workspace</h2>
        <Tabs tabs={TABS} activeTab={tab} onChange={(id) => setTab(id as Tab)} />
      </div>

      <TabPanel>
        {tab === "scan" && (
          <div className="p-4 space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Run Security Scan</CardTitle>
                <CardDescription>Scan your codebase for vulnerabilities, secrets, and compliance issues.</CardDescription>
              </CardHeader>
              <div className="px-4 py-3 flex gap-2">
                <Button>Start Scan</Button>
                <Button variant="secondary">Schedule</Button>
              </div>
            </Card>
          </div>
        )}

        {tab === "findings" && (
          <div className="p-4 space-y-2">
            {FINDINGS.map((finding) => (
              <Card key={finding.id} padding={false}>
                <div className="px-4 py-3 flex items-center justify-between">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                        finding.severity === "critical" ? "bg-red-500/15 text-red-400" :
                        finding.severity === "high" ? "bg-orange-500/15 text-orange-400" :
                        "bg-yellow-500/15 text-yellow-400"
                      }`}>{finding.severity.toUpperCase()}</span>
                      <p className="text-sm font-medium">{finding.title}</p>
                    </div>
                    <p className="text-xs text-[var(--color-text-secondary)] mt-1">{finding.id} • {finding.location}</p>
                  </div>
                  <Button variant="ghost" size="sm">View</Button>
                </div>
              </Card>
            ))}
          </div>
        )}

        {tab === "reports" && (
          <div className="p-4">
            <Card>
              <CardHeader>
                <CardTitle>Reports</CardTitle>
                <CardDescription>Generated security assessment reports.</CardDescription>
              </CardHeader>
              <div className="px-4 py-3 text-sm text-[var(--color-text-secondary)]">No reports generated yet.</div>
            </Card>
          </div>
        )}

        {tab === "compliance" && (
          <div className="p-4">
            <Card>
              <CardHeader>
                <CardTitle>Compliance</CardTitle>
                <CardDescription>OWASP, CIS, PCI-DSS, HIPAA, ISO 27001 mapping.</CardDescription>
              </CardHeader>
              <div className="px-4 py-3 text-sm text-[var(--color-text-secondary)]">Compliance score: 85%</div>
            </Card>
          </div>
        )}

        {tab === "alerts" && (
          <div className="p-4">
            <Card>
              <CardHeader>
                <CardTitle>Alerts</CardTitle>
                <CardDescription>Real-time security alerts and notifications.</CardDescription>
              </CardHeader>
              <div className="px-4 py-3 text-sm text-[var(--color-text-secondary)]">No active alerts.</div>
            </Card>
          </div>
        )}
      </TabPanel>
    </div>
  );
}
