export const tokens = {
  colors: {
    primary: "var(--color-primary)",
    secondary: "var(--color-secondary)",
    accent: "var(--color-accent)",
    success: "var(--color-success)",
    warning: "var(--color-warning)",
    danger: "var(--color-danger)",
    background: "var(--color-background)",
    foreground: "var(--color-foreground)",
    surface: "var(--color-surface)",
    border: "var(--color-border)",
  },
  spacing: {
    xs: "var(--spacing-xs)",
    sm: "var(--spacing-sm)",
    md: "var(--spacing-md)",
    lg: "var(--spacing-lg)",
    xl: "var(--spacing-xl)",
  },
  typography: {
    fontFamily: "var(--font-family-sans)",
    fontSize: "var(--font-size-base)",
    fontWeight: "var(--font-weight-normal)",
    lineHeight: "var(--line-height-normal)",
  },
  radius: {
    sm: "var(--radius-sm)",
    md: "var(--radius-md)",
    lg: "var(--radius-lg)",
    xl: "var(--radius-xl)",
  },
  shadows: {
    sm: "var(--shadow-sm)",
    md: "var(--shadow-md)",
    lg: "var(--shadow-lg)",
  },
  animations: {
    duration: "var(--animation-duration-normal)",
    easing: "var(--animation-easing)",
  },
} as const;

export type DesignTokens = typeof tokens;
