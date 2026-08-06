"use client";

import { useEffect, useRef } from "react";

export function useKeyboardNavigation(itemSelector: string, onSelect?: (item: HTMLElement) => void) {
  const containerRef = useRef<HTMLElement>(null);
  const itemsRef = useRef<HTMLElement[]>([]);
  const currentIndexRef = useRef(0);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const items = Array.from(container.querySelectorAll<HTMLElement>(itemSelector));
    itemsRef.current = items.filter((item) => !item.hasAttribute("disabled"));

    const handleKeyDown = (e: KeyboardEvent) => {
      const items = itemsRef.current;
      if (items.length === 0) return;

      switch (e.key) {
        case "ArrowDown":
          e.preventDefault();
          currentIndexRef.current = (currentIndexRef.current + 1) % items.length;
          items[currentIndexRef.current].focus();
          break;
        case "ArrowUp":
          e.preventDefault();
          currentIndexRef.current = (currentIndexRef.current - 1 + items.length) % items.length;
          items[currentIndexRef.current].focus();
          break;
        case "Enter":
        case " ":
          e.preventDefault();
          const currentItem = items[currentIndexRef.current];
          if (currentItem && onSelect) {
            onSelect(currentItem);
          }
          break;
        case "Home":
          e.preventDefault();
          currentIndexRef.current = 0;
          items[0].focus();
          break;
        case "End":
          e.preventDefault();
          currentIndexRef.current = items.length - 1;
          items[items.length - 1].focus();
          break;
      }
    };

    container.addEventListener("keydown", handleKeyDown);
    return () => container.removeEventListener("keydown", handleKeyDown);
  }, [itemSelector, onSelect]);

  return { containerRef, currentIndex: currentIndexRef };
}

export function useFocusTrap(containerRef: React.RefObject<HTMLElement | null>) {
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const focusableElements = container.querySelectorAll<HTMLElement>(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );

    if (focusableElements.length === 0) return;

    const firstFocusable = focusableElements[0];
    const lastFocusable = focusableElements[focusableElements.length - 1];

    const handleTab = (e: KeyboardEvent) => {
      if (e.key !== "Tab") return;

      if (e.shiftKey) {
        if (document.activeElement === firstFocusable) {
          e.preventDefault();
          lastFocusable.focus();
        }
      } else {
        if (document.activeElement === lastFocusable) {
          e.preventDefault();
          firstFocusable.focus();
        }
      }
    };

    container.addEventListener("keydown", handleTab);
    firstFocusable.focus();

    return () => container.removeEventListener("keydown", handleTab);
  }, [containerRef]);
}

export function useAnnounce(message: string, priority: "polite" | "assertive" = "polite") {
  const announcementRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!message) return;

    if (!announcementRef.current) {
      announcementRef.current = document.createElement("div");
      announcementRef.current.setAttribute("aria-live", priority);
      announcementRef.current.setAttribute("aria-atomic", "true");
      announcementRef.current.className = "sr-only";
      document.body.appendChild(announcementRef.current);
    }

    announcementRef.current.textContent = message;

    return () => {
      if (announcementRef.current) {
        announcementRef.current.textContent = "";
      }
    };
  }, [message, priority]);
}
