import { cn } from "@/lib/utils";

interface AvatarProps {
  src?: string;
  alt?: string;
  fallback?: string;
  size?: "sm" | "md" | "lg";
  className?: string;
}

const sizeClasses = {
  sm: "h-6 w-6 text-xs",
  md: "h-8 w-8 text-sm",
  lg: "h-10 w-10 text-base",
};

export function Avatar({ src, alt, fallback, size = "md", className }: AvatarProps) {
  const initial = (fallback || alt || "U").charAt(0).toUpperCase();

  if (src) {
    return (
      <img
        src={src}
        alt={alt || "Avatar"}
        className={cn("rounded-full object-cover", sizeClasses[size], className)}
      />
    );
  }

  return (
    <div
      className={cn(
        "rounded-full bg-[var(--color-accent)] flex items-center justify-center text-white font-medium",
        sizeClasses[size],
        className
      )}
      aria-label={alt || fallback || "User"}
    >
      {initial}
    </div>
  );
}
