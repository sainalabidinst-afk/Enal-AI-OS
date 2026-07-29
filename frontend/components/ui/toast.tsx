"use client";

import { useState, useEffect, useCallback } from "react";
import { create } from "zustand";

export type ToastType = "success" | "error" | "warning" | "info";

export interface Toast {
  id: string;
  type: ToastType;
  title: string;
  message?: string;
  duration?: number;
}

interface ToastState {
  toasts: Toast[];
  addToast: (toast: Omit<Toast, "id">) => string;
  removeToast: (id: string) => void;
  clearToasts: () => void;
}

export const useToastStore = create<ToastState>()((set) => ({
  toasts: [],
  addToast: (toast) => {
    const id = `toast-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`;
    set((state) => ({
      toasts: [...state.toasts, { ...toast, id }],
    }));
    return id;
  },
  removeToast: (id) => {
    set((state) => ({
      toasts: state.toasts.filter((t) => t.id !== id),
    }));
  },
  clearToasts: () => set({ toasts: [] }),
}));

const typeStyles: Record<ToastType, { bg: string; border: string; icon: string }> = {
  success: {
    bg: "bg-green-900/30",
    border: "border-green-500/50",
    icon: "✓",
  },
  error: {
    bg: "bg-red-900/30",
    border: "border-red-500/50",
    icon: "✕",
  },
  warning: {
    bg: "bg-yellow-900/30",
    border: "border-yellow-500/50",
    icon: "⚠",
  },
  info: {
    bg: "bg-blue-900/30",
    border: "border-blue-500/50",
    icon: "ℹ",
  },
};

function ToastItem({ toast, onRemove }: { toast: Toast; onRemove: (id: string) => void }) {
  const style = typeStyles[toast.type];
  const duration = toast.duration ?? 5000;

  useEffect(() => {
    if (duration <= 0) return;
    const timer = setTimeout(() => onRemove(toast.id), duration);
    return () => clearTimeout(timer);
  }, [toast.id, duration, onRemove]);

  return (
    <div
      className={`flex items-start gap-3 rounded-lg border px-4 py-3 shadow-lg ${style.bg} ${style.border} backdrop-blur-sm`}
      role="alert"
    >
      <span className="mt-0.5 text-sm">{style.icon}</span>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-[var(--color-text-primary)]">{toast.title}</p>
        {toast.message && (
          <p className="text-xs text-[var(--color-text-secondary)] mt-0.5">{toast.message}</p>
        )}
      </div>
      <button
        onClick={() => onRemove(toast.id)}
        className="text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] transition-colors"
        aria-label="Dismiss"
      >
        ✕
      </button>
    </div>
  );
}

export function ToastContainer() {
  const toasts = useToastStore((s) => s.toasts);
  const removeToast = useToastStore((s) => s.removeToast);

  if (toasts.length === 0) return null;

  return (
    <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2 max-w-sm w-full">
      {toasts.map((toast) => (
        <ToastItem key={toast.id} toast={toast} onRemove={removeToast} />
      ))}
    </div>
  );
}

// Helper hooks
export function useToast() {
  const addToast = useToastStore((s) => s.addToast);

  const showSuccess = useCallback(
    (title: string, message?: string) => addToast({ type: "success", title, message }),
    [addToast]
  );
  const showError = useCallback(
    (title: string, message?: string) => addToast({ type: "error", title, message, duration: 8000 }),
    [addToast]
  );
  const showWarning = useCallback(
    (title: string, message?: string) => addToast({ type: "warning", title, message, duration: 6000 }),
    [addToast]
  );
  const showInfo = useCallback(
    (title: string, message?: string) => addToast({ type: "info", title, message }),
    [addToast]
  );

  return { showSuccess, showError, showWarning, showInfo };
}

