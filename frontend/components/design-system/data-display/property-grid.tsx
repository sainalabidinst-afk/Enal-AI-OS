import { type ReactNode } from "react";
import { cn } from "@/lib/utils";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/design-system/layout/card";

interface Property {
  label: string;
  value: string;
  type?: "text" | "number" | "boolean";
}

interface PropertyGridProps {
  properties: Property[];
  title?: string;
  description?: string;
  className?: string;
}

export function PropertyGrid({ properties, title, description, className }: PropertyGridProps) {
  return (
    <Card className={className}>
      {(title || description) && (
        <CardHeader>
          {title && <CardTitle>{title}</CardTitle>}
          {description && <CardDescription>{description}</CardDescription>}
        </CardHeader>
      )}
      <div className="divide-y divide-[var(--color-border)]">
        {properties.map((prop, i) => (
          <div key={i} className="flex items-center justify-between px-4 py-2">
            <span className="text-xs text-[var(--color-secondary-500)]">{prop.label}</span>
            <span className="text-xs text-[var(--color-foreground)]">{prop.value}</span>
          </div>
        ))}
      </div>
    </Card>
  );
}
