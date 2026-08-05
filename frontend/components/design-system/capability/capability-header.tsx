import { type ReactNode } from "react";
import { cn } from "@/lib/utils";
import { CapabilityIcon } from "@/components/design-system/capability/capability-icon";
import { CapabilityStatus } from "@/components/design-system/capability/capability-status";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/design-system/layout/card";

interface CapabilityHeaderProps {
  name: string;
  description: string;
  icon: string;
  iconColor?: string;
  status?: "Ready" | "Beta" | "Coming Soon" | "Installed";
  version?: string;
  category?: string;
  action?: ReactNode;
  className?: string;
}

export function CapabilityHeader({
  name,
  description,
  icon,
  iconColor,
  status = "Ready",
  version,
  category,
  action,
  className,
}: CapabilityHeaderProps) {
  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-start gap-4">
          <CapabilityIcon icon={icon} color={iconColor} />
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1">
              <CardTitle>{name}</CardTitle>
              <CapabilityStatus status={status} />
            </div>
            <CardDescription>{description}</CardDescription>
            {(category || version) && (
              <div className="flex items-center gap-2 mt-2 text-xs text-[var(--color-secondary-500)]">
                {category && <span>{category}</span>}
                {category && version && <span>·</span>}
                {version && <span>v{version}</span>}
              </div>
            )}
          </div>
          {action && <div className="shrink-0">{action}</div>}
        </div>
      </CardHeader>
    </Card>
  );
}
