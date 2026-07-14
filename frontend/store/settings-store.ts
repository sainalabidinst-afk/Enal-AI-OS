import { create } from "zustand";
import { persist } from "zustand/middleware";

export type Theme = "light" | "dark" | "system";

interface SettingsState {
  theme: Theme;
  recipient: string;
  setTheme: (theme: Theme) => void;
  setRecipient: (recipient: string) => void;
}

export const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      theme: "dark",
      recipient: "default",
      setTheme: (theme) => set({ theme }),
      setRecipient: (recipient) => set({ recipient }),
    }),
    {
      name: "settings-storage",
    }
  )
);
