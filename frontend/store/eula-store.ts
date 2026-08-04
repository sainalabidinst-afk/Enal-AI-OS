import { create } from "zustand";
import { persist } from "zustand/middleware";
import { EULA_CURRENT_VERSION, type EulaState } from "@/types/eula";

interface EulaActions {
  acceptEula: () => void;
  resetEula: () => void;
  hasAccepted: () => boolean;
}

export const useEulaStore = create<EulaState & EulaActions>()(
  persist(
    (set, get) => ({
      accepted_eula: false,
      accepted_version: null,
      accepted_at: null,

      acceptEula: () => {
        set({
          accepted_eula: true,
          accepted_version: EULA_CURRENT_VERSION,
          accepted_at: new Date().toISOString(),
        });
      },

      resetEula: () => {
        set({
          accepted_eula: false,
          accepted_version: null,
          accepted_at: null,
        });
      },

      hasAccepted: () => {
        const { accepted_eula, accepted_version } = get();
        return (
          accepted_eula === true &&
          accepted_version === EULA_CURRENT_VERSION
        );
      },
    }),
    {
      name: "enal-eula-storage",
      partialize: (state) => ({
        accepted_eula: state.accepted_eula,
        accepted_version: state.accepted_version,
        accepted_at: state.accepted_at,
      }),
    }
  )
);
