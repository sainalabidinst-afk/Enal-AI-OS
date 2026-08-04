import { create } from "zustand";
import { persist } from "zustand/middleware";

interface LauncherState {
  favorites: string[];
  recent: string[];
}

interface LauncherActions {
  toggleFavorite: (appId: string) => void;
  isFavorite: (appId: string) => boolean;
  recordRecent: (appId: string) => void;
  clearRecent: () => void;
}

export const useLauncherStore = create<LauncherState & LauncherActions>()(
  persist(
    (set, get) => ({
      favorites: [],
      recent: [],

      toggleFavorite: (appId) => {
        const { favorites } = get();
        const exists = favorites.includes(appId);
        set({
          favorites: exists
            ? favorites.filter((id) => id !== appId)
            : [...favorites, appId],
        });
      },

      isFavorite: (appId) => get().favorites.includes(appId),

      recordRecent: (appId) => {
        const { recent } = get();
        const next = [appId, ...recent.filter((id) => id !== appId)].slice(
          0,
          8
        );
        set({ recent: next });
      },

      clearRecent: () => set({ recent: [] }),
    }),
    {
      name: "enal-launcher-storage",
      partialize: (state) => ({
        favorites: state.favorites,
        recent: state.recent,
      }),
    }
  )
);
