"use client";

import { useEffect, useRef } from "react";

export class CleanupManager {
  private disposables: (() => void)[] = [];

  add(disposable: () => void) {
    this.disposables.push(disposable);
  }

  addInterval(intervalId: ReturnType<typeof setInterval>) {
    this.add(() => clearInterval(intervalId));
  }

  addTimeout(timeoutId: ReturnType<typeof setTimeout>) {
    this.add(() => clearTimeout(timeoutId));
  }

  addListener(unsubscribe: () => void) {
    this.add(unsubscribe);
  }

  dispose() {
    this.disposables.forEach((dispose) => {
      try {
        dispose();
      } catch (error) {
        console.error("Error during cleanup:", error);
      }
    });
    this.disposables = [];
  }
}

export function useCleanup() {
  const cleanupRef = useRef(new CleanupManager());

  useEffect(() => {
    return () => {
      cleanupRef.current.dispose();
    };
  }, []);

  return cleanupRef.current;
}
