"use client";

import { useEffect } from "react";
import { providerRegistry } from "../connectivity/registry/provider-registry";
import { MockMarketProvider } from "../connectivity/providers/mock-market-provider";
import { ReplayMarketProvider } from "../connectivity/replay/replay-market-provider";

export function useProviderInitialization() {
  useEffect(() => {
    const mockProvider = new MockMarketProvider();
    const replayProvider = new ReplayMarketProvider();

    providerRegistry.register(mockProvider);
    providerRegistry.register(replayProvider);
    providerRegistry.setActive("mock");

    return () => {
      providerRegistry.unregister("mock");
      providerRegistry.unregister("replay");
    };
  }, []);
}

export function useProviderSwitcher() {
  const switchToMock = () => {
    providerRegistry.setActive("mock");
  };

  const switchToReplay = () => {
    providerRegistry.setActive("replay");
  };

  return {
    switchToMock,
    switchToReplay,
    activeProvider: providerRegistry.getActive(),
  };
}
