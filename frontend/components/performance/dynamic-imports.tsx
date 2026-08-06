import React, { type ComponentType, Suspense } from "react";

export function lazyLoad<T extends ComponentType<object>>(
  importFn: () => Promise<{ default: T }>
) {
  const LazyComponent = React.lazy(importFn);

  const WrappedComponent = (props: Record<string, unknown>) => {
    return (
      <Suspense fallback={<div className="flex items-center justify-center h-full">Loading...</div>}>
        <LazyComponent {...(props as any)} />
      </Suspense>
    );
  };

  return WrappedComponent as unknown as ComponentType<React.ComponentProps<T>>;
}

export function prefetchComponent(importFn: () => Promise<{ default: ComponentType<object> }>) {
  if (typeof window !== "undefined") {
    const idle = (window as any).requestIdleCallback || ((cb: () => void) => setTimeout(cb, 0));
    idle(() => {
      importFn().catch(() => {
      });
    });
  }
}

export function prefetchRoute(path: string) {
  if (typeof window !== "undefined") {
    const idle = (window as any).requestIdleCallback || ((cb: () => void) => setTimeout(cb, 0));
    idle(() => {
      import(`${path}`).catch(() => {
      });
    });
  }
}
