export function createStreamReader(url: string, onEvent: (event: MessageEvent) => void, onError?: (error: Error) => void) {
  if (typeof window === 'undefined') {
    return () => {};
  }

  const eventSource = new EventSource(url);
  eventSource.onmessage = (event: MessageEvent) => onEvent(event);
  eventSource.onerror = (error: Event) => {
    eventSource.close();
    onError?.(new Error('Stream connection failed'));
  };

  return () => {
    eventSource.close();
  };
}
