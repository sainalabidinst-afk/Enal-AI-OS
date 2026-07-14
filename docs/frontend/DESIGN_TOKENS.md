# Design Tokens

This document defines the complete design token set for ECP v1. All frontend code must use these tokens. No hardcoded values are allowed.

---

## Colors

### Semantic Colors

| Token | Value | Usage |
|-------|-------|-------|
| `--color-bg-primary` | #0f1117 | Main application background |
| `--color-bg-secondary` | #1a1d27 | Sidebar, cards, panels |
| `--color-bg-tertiary` | #252830 | Elevated surfaces, inputs |
| `--color-bg-hover` | #2d3038 | Hovered interactive elements |
| `--color-text-primary` | #e4e6eb | Primary text (headings, body) |
| `--color-text-secondary` | #9ca3af | Secondary text (subtitles, hints) |
| `--color-text-muted` | #6b7280 | Muted text (timestamps, metadata) |
| `--color-accent` | #3b82f6 | Primary action buttons, links |
| `--color-accent-hover` | #2563eb | Hovered primary action |
| `--color-success` | #22c55e | Success states, completed tasks |
| `--color-success-bg` | rgba(34,197,94,0.1) | Success background |
| `--color-warning` | #f59e0b | Warning states |
| `--color-warning-bg` | rgba(245,158,11,0.1) | Warning background |
| `--color-danger` | #ef4444 | Error states, destructive actions |
| `--color-danger-hover` | #dc2626 | Hovered destructive |
| `--color-danger-bg` | rgba(239,68,68,0.1) | Error background |
| `--color-border` | #374151 | Borders, dividers |
| `--color-border-light` | #4b5563 | Light borders |

### Status Colors

| Token | Value | Usage |
|-------|-------|-------|
| `--color-status-pending` | #6b7280 | Pending tasks |
| `--color-status-running` | #3b82f6 | Running tasks |
| `--color-status-completed` | #22c55e | Completed tasks |
| `--color-status-failed` | #ef4444 | Failed tasks |
| `--color-status-warning` | #f59e0b | Warnings |
| `--color-status-info` | #3b82f6 | Informational |

---

## Typography

### Font Family

| Token | Value |
|-------|-------|
| `--font-family` | 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif |
| `--font-family-mono` | 'JetBrains Mono', 'Fira Code', 'Courier New', monospace |

### Font Sizes

| Token | Value | Line Height | Usage |
|-------|-------|-------------|-------|
| `--font-size-xs` | 0.75rem | 1rem | Labels, hints |
| `--font-size-sm` | 0.875rem | 1.25rem | Secondary text, captions |
| `--font-size-md` | 1rem | 1.5rem | Body text |
| `--font-size-lg` | 1.125rem | 1.75rem | Emphasized text |
| `--font-size-xl` | 1.25rem | 1.75rem | Small headings |
| `--font-size-2xl` | 1.5rem | 2rem | Page titles |
| `--font-size-3xl` | 2rem | 2.5rem | Hero text |

### Font Weights

| Token | Value | Usage |
|-------|-------|-------|
| `--font-weight-normal` | 400 | Body text |
| `--font-weight-medium` | 500 | Emphasized text |
| `--font-weight-semibold` | 600 | Subheadings |
| `--font-weight-bold` | 700 | Headings |

---

## Spacing

| Token | Value | Usage |
|-------|-------|-------|
| `--space-0` | 0 | No spacing |
| `--space-1` | 4px | Tight spacing |
| `--space-2` | 8px | Compact spacing |
| `--space-3` | 12px | Default spacing |
| `--space-4` | 16px | Comfortable spacing |
| `--space-5` | 24px | Section spacing |
| `--space-6` | 32px | Page spacing |
| `--space-7` | 48px | Large sections |
| `--space-8` | 64px | Page sections |

---

## Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| `--radius-none` | 0 | Sharp edges |
| `--radius-sm` | 4px | Small elements |
| `--radius-md` | 8px | Cards, buttons |
| `--radius-lg` | 12px | Panels, modals |
| `--radius-full` | 9999px | Pills, avatars |

---

## Shadows

| Token | Value | Usage |
|-------|-------|-------|
| `--shadow-none` | none | No shadow |
| `--shadow-sm` | 0 1px 2px rgba(0,0,0,0.3) | Subtle elevation |
| `--shadow-md` | 0 4px 6px rgba(0,0,0,0.4) | Cards |
| `--shadow-lg` | 0 10px 15px rgba(0,0,0,0.5) | Modals, dialogs |
| `--shadow-inner` | inset 0 2px 4px rgba(0,0,0,0.3) | Inset elements |

---

## Z-Index

| Token | Value | Usage |
|-------|-------|-------|
| `--z-base` | 0 | Base layer |
| `--z-dropdown` | 100 | Dropdown menus |
| `--z-sticky` | 200 | Sticky headers |
| `--z-modal` | 300 | Modal dialogs |
| `--z-toast` | 400 | Toast notifications |
| `--z-tooltip` | 500 | Tooltips |

---

## Transitions

| Token | Value | Usage |
|-------|-------|-------|
| `--transition-fast` | 150ms ease-in-out | Micro-interactions |
| `--transition-normal` | 250ms ease-in-out | Standard transitions |
| `--transition-slow` | 350ms ease-in-out | Panel transitions |

---

## Breakpoints

| Token | Value | Usage |
|-------|-------|-------|
| `--bp-mobile` | 640px | Mobile max |
| `--bp-tablet` | 1024px | Tablet max |
| `--bp-desktop` | 1025px | Desktop min |

---

## Dark Mode / Light Mode

All colors above are defined for dark mode (default).

Light mode overrides:

| Token | Light Mode Value |
|-------|------------------|
| `--color-bg-primary` | #ffffff |
| `--color-bg-secondary` | #f3f4f6 |
| `--color-bg-tertiary` | #e5e7eb |
| `--color-bg-hover` | #d1d5db |
| `--color-text-primary` | #111827 |
| `--color-text-secondary` | #4b5563 |
| `--color-text-muted` | #9ca3af |
| `--color-border` | #d1d5db |
| `--color-border-light` | #e5e7eb |

Theme switching must use CSS custom properties and transition smoothly.
