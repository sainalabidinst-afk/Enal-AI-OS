import type { ProviderHealth, ConnectionStatus } from "../providers/market-provider.types";

type ProviderStatusListener = (health: ProviderHealth) => void;

class DiagnosticsMonitor {
  private listeners = new Set<ProviderStatusListener>();
  private startTime = Date.now();
  private packetsReceived = 0;

  recordPacket() {
    this.packetsReceived++;
  }

  getPacketCount() {
    return this.packetsReceived;
  }

  getUptimeMs() {
    return Date.now() - this.startTime;
  }

  subscribe(listener: ProviderStatusListener) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  publish(health: ProviderHealth) {
    this.listeners.forEach((listener) => listener(health));
  }

  getSnapshot() {
    return {
      uptimeMs: this.getUptimeMs(),
      packetsReceived: this.packetsReceived,
      timestamp: Date.now(),
    };
  }
}

export const diagnosticsMonitor = new DiagnosticsMonitor();
