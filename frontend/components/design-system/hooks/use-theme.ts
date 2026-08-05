import { useTheme } from "@/components/design-system/theme/theme-provider";

export function useThemeMode() {
  const { theme, setTheme, resolvedTheme } = useTheme();
  return { theme, setTheme, resolvedTheme };
}
