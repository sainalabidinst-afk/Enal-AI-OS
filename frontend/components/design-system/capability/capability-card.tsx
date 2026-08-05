import { type ReactNode } from "react";
import { cn } from "@/lib/utils";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/design-system/layout/card";
import { Badge } from "@/components/design-system/primitives/badge";

interface CapabilityCardProps {
  name: string;
  description: string;
  icon: ReactNode;
  status?: "Ready" | "Beta" | "Coming Soon" | "Installed";
  version?: string;
  category?: string;
  className?: string;
  onClick?: () => void;
}

export function CapabilityCard({
  name,
  description,
  icon,
  status = "Ready",
  version = "1.0.0",
  category,
  className,
  onClick,
}: CapabilityCardProps) {
  const statusVariant = {
    Ready: "success",
    Beta: "warning",
    "Coming Soon": "secondary",
    Installed: "default",
  } as const;

  return (
    <Card
      className={cn("cursor-pointer transition-all hover:shadow-md", className)}
      onClick={onClick}
    >
      <CardHeader>
        <div className="flex items-start justify-between gap-2">
          <div className="flex items-center gap-3">
            <div className="text-2xl">{icon}</div>
            <div>
              <CardTitle>{name}</CardTitle>
              <CardDescription>{description}</CardDescription>
            </div>
          </div>
          <Badge variant={statusVariant[status]}>{status}</Badge>
        </div>
        {(category || version) && (
          <div className="flex items-center gap-2 mt-2 text-xs text-[var(--color-secondary-500)]">
            {category && <span>{category}</span>}
            {category && version && <span>·</span>}
            {version && <span>v{version}</span>}
          </div>
        )}
      </CardHeader>
    </Card>
  );
}
