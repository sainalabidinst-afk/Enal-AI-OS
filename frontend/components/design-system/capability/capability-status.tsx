import { Badge } from "@/components/design-system/primitives/badge";

interface CapabilityStatusProps {
  status: "Ready" | "Beta" | "Coming Soon" | "Installed";
  className?: string;
}

const statusVariant = {
  Ready: "success",
  Beta: "warning",
  "Coming Soon": "secondary",
  Installed: "default",
} as const;

export function CapabilityStatus({ status, className }: CapabilityStatusProps) {
  return <Badge variant={statusVariant[status]} className={className}>{status}</Badge>;
}
