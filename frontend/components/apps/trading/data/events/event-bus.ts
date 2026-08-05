export type TradingEventType =
  | "symbol:changed"
  | "timeframe:changed"
  | "market:updated"
  | "chart:updated"
  | "watchlist:updated"
  | "portfolio:updated"
  | "news:updated"
  | "orders:updated"
  | "positions:updated"
  | "logs:updated"
  | "ui:loading"
  | "ui:error";

export interface TradingEvent<T = unknown> {
  type: TradingEventType;
  payload?: T;
}

type Listener = (event: TradingEvent) => void;

class EventBusImpl {
  private listeners = new Map<TradingEventType, Set<Listener>>();

  subscribe(type: TradingEventType, listener: Listener) {
    if (!this.listeners.has(type)) {
      this.listeners.set(type, new Set());
    }
    this.listeners.get(type)!.add(listener);
    return () => this.unsubscribe(type, listener);
  }

  unsubscribe(type: TradingEventType, listener: Listener) {
    this.listeners.get(type)?.delete(listener);
  }

  publish(event: TradingEvent) {
    const listeners = this.listeners.get(event.type);
    if (listeners) {
      listeners.forEach((listener) => listener(event));
    }
  }
}

export const eventBus = new EventBusImpl();
