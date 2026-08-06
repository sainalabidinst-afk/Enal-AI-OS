"use client";

import { memo, useMemo, useCallback, useEffect, useRef } from "react";

export function withPerformance<P extends object>(
  Component: React.ComponentType<P>,
  componentName: string
) {
  const MemoizedComponent = memo(Component);
  MemoizedComponent.displayName = `Memoized(${componentName})`;

  return MemoizedComponent;
}

export function useStableMemo<T>(factory: () => T, deps: unknown[]): T {
  return useMemo(factory, deps);
}

export function useStableCallback<T extends (...args: unknown[]) => unknown>(callback: T, deps: unknown[]): T {
  return useCallback(callback, deps);
}

export function useInterval(callback: () => void, delay: number | null, immediate = false) {
  const savedCallback = useRef<(() => void) | null>(null);

  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  useEffect(() => {
    if (delay === null) return;

    const tick = () => {
      if (savedCallback.current) {
        savedCallback.current();
      }
    };

    if (immediate) {
      tick();
    }

    const intervalId = setInterval(tick, delay);
    return () => clearInterval(intervalId);
  }, [delay, immediate]);
}

export function useThrottle<T extends (...args: unknown[]) => void>(callback: T, delay: number): T {
  const lastCall = useRef<number>(0);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  return useCallback(
    (...args: unknown[]) => {
      const now = Date.now();
      const timeSinceLastCall = now - lastCall.current;

      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }

      if (timeSinceLastCall >= delay) {
        callback(...args);
        lastCall.current = now;
      } else {
        timeoutRef.current = setTimeout(() => {
          callback(...args);
          lastCall.current = Date.now();
          timeoutRef.current = null;
        }, delay - timeSinceLastCall);
      }
    },
    [callback, delay]
  ) as unknown as T;
}

export function useDebounce<T extends (...args: unknown[]) => void>(callback: T, delay: number): T {
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  return useCallback(
    (...args: unknown[]) => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }

      timeoutRef.current = setTimeout(() => {
        callback(...args);
        timeoutRef.current = null;
      }, delay);
    },
    [callback, delay]
  ) as unknown as T;
}
