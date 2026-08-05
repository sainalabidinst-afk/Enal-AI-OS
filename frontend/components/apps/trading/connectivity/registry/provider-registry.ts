import type { MarketProvider, MarketProviderRegistry } from "../providers/market-provider.interface";

class ProviderRegistry implements MarketProviderRegistry {
  private providers = new Map<string, MarketProvider>();
  private activeProviderId: string | null = null;

  register(provider: MarketProvider) {
    this.providers.set(provider.id, provider);
  }

  unregister(providerId: string) {
    this.providers.delete(providerId);
    if (this.activeProviderId === providerId) {
      this.activeProviderId = null;
    }
  }

  get(providerId: string) {
    return this.providers.get(providerId);
  }

  getAll() {
    return this.providers;
  }

  getActive() {
    if (!this.activeProviderId) return undefined;
    return this.providers.get(this.activeProviderId);
  }

  setActive(providerId: string) {
    if (!this.providers.has(providerId)) {
      throw new Error(`Provider ${providerId} not found`);
    }
    this.activeProviderId = providerId;
  }
}

export const providerRegistry = new ProviderRegistry();
