import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { cva as baseCva, type VariantProps } from "class-variance-authority";
import type { ReactNode } from "react";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function cva(base: string, config?: any) {
  return baseCva(base, config as any);
}

export type { VariantProps };
export { ReactNode };
export type { ButtonHTMLAttributes } from "react";
