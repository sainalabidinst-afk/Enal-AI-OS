import type { NewsArticle } from "../providers/market-provider.types";

type NewsListener = (articles: NewsArticle[]) => void;

class NewsProviderImpl {
  private listeners = new Set<NewsListener>();
  private articles: NewsArticle[] = [];

  subscribe(listener: NewsListener) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  publish(articles: NewsArticle[]) {
    this.articles = articles;
    this.listeners.forEach((listener) => listener(articles));
  }

  getLatest() {
    return this.articles;
  }
}

export const newsProvider = new NewsProviderImpl();
