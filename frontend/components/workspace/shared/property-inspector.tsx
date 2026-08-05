"use client";

import { type ReactNode } from "react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

interface Property {
  label: string;
  value: string;
  type?: "text" | "number" | "boolean";
}

interface PropertyInspectorProps {
  title?: string;
  properties?: Property[];
  className?: string;
}

export function PropertyInspector({ title = "Properties", properties = [], className }: PropertyInspectorProps) {
  return (
    <div className={className}>
      <Card>
        <CardHeader>
          <CardTitle>{title}</CardTitle>
          <CardDescription>Object properties and metadata</CardDescription>
        </CardHeader>
        <div className="divide-y divide-[var(--color-border)]">
          {properties.length === 0 && (
            <div className="px-4 py-3 text-sm text-[var(--color-text-secondary)]">No properties</div>
          )}
          {properties.map((prop, i) => (
            <div key={i} className="flex items-center justify-between px-4 py-2">
              <span className="text-xs text-[var(--color-text-secondary)]">{prop.label}</span>
              <span className="text-xs text-[var(--color-text-primary)]">{prop.value}</span>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
