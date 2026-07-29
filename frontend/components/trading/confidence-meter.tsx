"use client";

interface ConfidenceMeterProps {
  confidence: number;
  bias: string;
  size?: "sm" | "md" | "lg";
}

export function ConfidenceMeter({ confidence, bias, size = "md" }: ConfidenceMeterProps) {
  const barColor =
    bias === "bullish" ? "bg-green-500" :
    bias === "bearish" ? "bg-red-500" :
    "bg-yellow-500";

  const sizes: Record<string, string> = {
    sm: "h-1.5",
    md: "h-2.5",
    lg: "h-4",
  };

  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-xs text-[var(--color-text-secondary)]">
        <span>Confidence: {confidence}%</span>
        <span className={
          bias === "bullish" ? "text-green-500" :
          bias === "bearish" ? "text-red-500" :
          "text-yellow-500"
        }>
          {bias.toUpperCase()}
        </span>
      </div>
      <div className={`w-full bg-[var(--color-bg-tertiary)] rounded-full ${sizes[size] || sizes.md}`}>
        <div
  );
}
