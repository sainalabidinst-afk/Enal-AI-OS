import { type ReactNode } from "react";
import { cn } from "@/lib/utils";
import { Card, CardHeader, CardTitle } from "@/components/design-system/layout/card";

interface StatCardProps {
  title: string;
  value: string | number;
  change?: string;
  changeType?: "positive" | "negative" | "neutral";
  icon?: ReactNode;
  className?: string;
}

export function StatCard({ title, value, change, changeType = "neutral", icon, className }: StatCardProps) {
  const changeColors = {
    positive: "text-[var(--color-success-500)]",
    negative: "text-[var(--color-danger-500)]",
    neutral: "text-[var(--color-secondary-500)]",
  };

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>{title}</CardTitle>
          {icon && <div className="text-[var(--color-secondary-400)]">{icon}</div>}
        </div>
      </CardHeader>
      <div className="px-4 pb-4">
        <p className="text-2xl font-bold text-[var(--color-foreground)]">{value}</p>
        {change && <p className={cn("text-xs mt-1", changeColors[changeType])}>{change}</p>}
      </div>
    </Card>
  );
}
