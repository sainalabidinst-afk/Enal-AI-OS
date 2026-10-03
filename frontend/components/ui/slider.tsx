import { forwardRef } from "react";
import { cn } from "@/lib/utils";

interface SliderProps {
  className?: string;
  value?: number[];
  onValueChange?: (value: number[]) => void;
  min?: number;
  max?: number;
  step?: number;
}

const Slider = forwardRef<HTMLInputElement, SliderProps>(
  ({ className, value, onValueChange, min = 0, max = 100, step = 1, ...props }, ref) => {
    return (
      <input
        ref={ref}
        type="range"
        value={value?.[0] ?? 0}
        min={min}
        max={max}
        step={step}
        onChange={(e) => {
          onValueChange?.([parseFloat(e.target.value)]);
        }}
        className={cn(
          "h-2 w-full cursor-pointer appearance-none rounded-lg bg-[var(--color-border)] accent-[var(--color-accent)]",
          className
        )}
        {...props}
      />
    );
  }
);

Slider.displayName = "Slider";

export { Slider };
