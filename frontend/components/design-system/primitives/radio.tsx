import { type InputHTMLAttributes, forwardRef } from "react";
import { cn } from "@/lib/utils";

interface RadioProps extends Omit<InputHTMLAttributes<HTMLInputElement>, "type"> {
  label?: string;
  error?: string;
}

export const Radio = forwardRef<HTMLInputElement, RadioProps>(
  ({ label, error, className, id, ...props }, ref) => {
    const radioId = id || label?.toLowerCase().replace(/\s+/g, "-");
    return (
      <div className="space-y-1.5">
        <div className="flex items-center gap-2">
          <input
            ref={ref}
            type="radio"
            id={radioId}
            className={cn(
              "h-4 w-4 border border-[var(--color-border)] bg-[var(--color-surface)] text-[var(--color-primary-500)] focus:ring-2 focus:ring-[var(--color-primary-500)] focus:ring-offset-2 disabled:opacity-50",
              error && "border-[var(--color-danger-500)]",
              className
            )}
            {...props}
          />
          {label && (
            <label htmlFor={radioId} className="text-sm font-medium text-[var(--color-foreground)] cursor-pointer">
              {label}
            </label>
          )}
        </div>
        {error && <p className="text-xs text-[var(--color-danger-500)]">{error}</p>}
      </div>
    );
  }
);

Radio.displayName = "Radio";
