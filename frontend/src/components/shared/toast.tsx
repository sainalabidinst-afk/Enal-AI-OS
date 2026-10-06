'use client';

import { createContext, useContext, useState } from 'react';
import { cn } from '@/lib/cn';
import { X, CheckCircle, XCircle, AlertTriangle, Info } from 'lucide-react';

type ToastType = 'success' | 'error' | 'warning' | 'info';

interface Toast {
  id: string;
  type: ToastType;
  message: string;
}

interface ToastContextValue {
  toasts: Toast[];
  addToast: (type: ToastType, message: string) => void;
  removeToast: (id: string) => void;
}

const ToastContext = createContext<ToastContextValue | null>(null);

export function useToast() {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within ToastProvider');
  }
  return context;
}

const icons: Record<ToastType, React.ReactNode> = {
  success: <CheckCircle size={16} className="text-success" />,
  error: <XCircle size={16} className="text-danger" />,
  warning: <AlertTriangle size={16} className="text-warning" />,
  info: <Info size={16} className="text-primary" />,
};

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const addToast = (type: ToastType, message: string) => {
    const id = crypto.randomUUID();
    setToasts((prev) => [...prev, { id, type, message }]);
    setTimeout(() => removeToast(id), 4000);
  };

  const removeToast = (id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  return (
    <ToastContext.Provider value={{ toasts, addToast, removeToast }}>
      {children}
      <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2">
        {toasts.map((toast) => (
          <div
            key={toast.id}
            className={cn(
              'flex items-center gap-3 rounded-lg border border-border bg-surface-secondary px-4 py-3 shadow-lg',
              'animate-in slide-in-from-right-full'
            )}
          >
            {icons[toast.type]}
            <p className="text-sm">{toast.message}</p>
            <button
              onClick={() => removeToast(toast.id)}
              className="ml-2 rounded-md p-1 hover:bg-surface-hover"
            >
              <X size={14} />
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}
