import { type InputHTMLAttributes, forwardRef } from "react";
import { cn } from "@/lib/utils";

interface CheckboxProps extends Omit<InputHTMLAttributes<HTMLInputElement>, "type"> {
  label?: string;
  error?: string;
}

export const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(
  ({ label, error, className, id, ...props }, ref) => {
    const checkboxId = id || label?.toLowerCase().replace(/\s+/g, "-");
    return (
      <div className="space-y-1.5">
        <div className="flex items-center gap-2">
          <input
            ref={ref}
            type="checkbox"
            id={checkboxId}
            className={cn(
              "h-4 w-4 rounded border border-[var(--color-border)] bg-[var(--color-surface)] text-[var(--color-primary-500)] focus:ring-2 focus:ring-[var(--color-primary-500)] focus:ring-offset-2 disabled:opacity-50",
              error && "border-[var(--color-danger-500)]",
              className
            )}
            {...props}
          />
          {label && (
            <label htmlFor={checkboxId} className="text-sm font-medium text-[var(--color-foreground)] cursor-pointer">
              {label}
            </label>
          )}
        </div>
        {error && <p className="text-xs text-[var(--color-danger-500)]">{error}</p>}
      </div>
    );
  }
);

Checkbox.displayName = "Checkbox";
