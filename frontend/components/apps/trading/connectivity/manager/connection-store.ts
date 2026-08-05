import { create } from "zustand";
import type { ConnectionStatus, ProviderHealth } from "../providers/market-provider.types";

interface ConnectionState {
  status: ConnectionStatus;
  providerId: string | null;
  providerName: string | null;
  health: ProviderHealth | null;
  setStatus: (status: ConnectionStatus) => void;
  setProvider: (providerId: string, providerName: string) => void;
  updateHealth: (health: ProviderHealth) => void;
  disconnect: () => void;
}

export const useConnectionStore = create<ConnectionState>((set) => ({
  status: "idle",
  providerId: null,
  providerName: null,
  health: null,

  setStatus: (status) => set({ status }),
  setProvider: (providerId, providerName) => set({ providerId, providerName }),
  updateHealth: (health) => set({ health }),
  disconnect: () => set({ status: "disconnected", providerId: null, providerName: null, health: null }),
}));
