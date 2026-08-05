import { cn } from "@/lib/utils";

interface CapabilityIconProps {
  icon: string;
  color?: string;
  size?: "sm" | "md" | "lg";
  className?: string;
}

export function CapabilityIcon({ icon, color = "var(--color-primary-500)", size = "md", className }: CapabilityIconProps) {
  const sizeClasses = {
    sm: "h-10 w-10 text-lg",
    md: "h-16 w-16 text-3xl",
    lg: "h-24 w-24 text-5xl",
  };

  return (
    <div
      className={cn(
        "flex items-center justify-center rounded-2xl",
        sizeClasses[size],
        className
      )}
      style={{ backgroundColor: `${color}1a` }}
    >
      <span>{icon}</span>
    </div>
  );
}
