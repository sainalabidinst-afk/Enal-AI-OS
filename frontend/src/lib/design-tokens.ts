export const designTokens = {
  colors: {
    bgPrimary: 'var(--color-bg-primary)',
    bgSecondary: 'var(--color-bg-secondary)',
    bgTertiary: 'var(--color-bg-tertiary)',
    bgHover: 'var(--color-bg-hover)',
    textPrimary: 'var(--color-text-primary)',
    textSecondary: 'var(--color-text-secondary)',
    textMuted: 'var(--color-text-muted)',
    accent: 'var(--color-accent)',
    accentHover: 'var(--color-accent-hover)',
    success: 'var(--color-success)',
    warning: 'var(--color-warning)',
    danger: 'var(--color-danger)',
    border: 'var(--color-border)',
    borderLight: 'var(--color-border-light)',
  },
  font: {
    family: 'var(--font-family)',
    mono: 'var(--font-family-mono)',
  },
  radius: {
    md: 'var(--radius-md)',
    lg: 'var(--radius-lg)',
  },
  shadow: {
    md: 'var(--shadow-md)',
  },
  transition: {
    fast: 'var(--transition-fast)',
  },
} as const;
