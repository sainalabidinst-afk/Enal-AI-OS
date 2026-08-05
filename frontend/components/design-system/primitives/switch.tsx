import { type InputHTMLAttributes, forwardRef } from "react";
import { cn } from "@/lib/utils";

interface SwitchProps extends Omit<InputHTMLAttributes<HTMLInputElement>, "type"> {
  label?: string;
  error?: string;
}

export const Switch = forwardRef<HTMLInputElement, SwitchProps>(
  ({ label, error, className, id, ...props }, ref) => {
    const switchId = id || label?.toLowerCase().replace(/\s+/g, "-");
    return (
      <div className="space-y-1.5">
        <div className="flex items-center gap-2">
          <button
            type="button"
            role="switch"
            aria-checked={props.checked}
            onClick={() => props.onChange?.(!props.checked as any)}
            className={cn(
              "relative inline-flex h-6 w-11 items-center rounded-full transition-colors",
              props.checked ? "bg-[var(--color-primary-500)]" : "bg-[var(--color-secondary-300)]",
              props.disabled && "opacity-50",
              className
            )}
          >
            <span
              className={cn(
                "inline-block h-4 w-4 rounded-full bg-white transition-transform",
                props.checked ? "translate-x-6" : "translate-x-1"
              )}
            />
          </button>
          {label && (
            <label htmlFor={switchId} className="text-sm font-medium text-[var(--color-foreground)] cursor-pointer">
              {label}
            </label>
          )}
        </div>
        {error && <p className="text-xs text-[var(--color-danger-500)]">{error}</p>}
      </div>
    );
  }
);

Switch.displayName = "Switch";
