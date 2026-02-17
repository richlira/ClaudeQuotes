"use client";

import { useEffect, useState } from "react";

type Quote = {
  id: number;
  text: string;
  author: string;
  category: string;
};

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
  const [quotes, setQuotes] = useState<Quote[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [activeCategory, setActiveCategory] = useState<string | null>(null);
  const [featured, setFeatured] = useState<Quote | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [quotesRes, categoriesRes, featuredRes] = await Promise.all([
          fetch(`${API_URL}/quotes`),
          fetch(`${API_URL}/categories`),
          fetch(`${API_URL}/quotes/random`),
        ]);
        setQuotes(await quotesRes.json());
        setCategories(await categoriesRes.json());
        setFeatured(await featuredRes.json());
      } catch (err) {
        console.error("Failed to load quotes:", err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  useEffect(() => {
    if (!activeCategory) return;
    async function filter() {
      const res = await fetch(
        `${API_URL}/quotes?category=${activeCategory}`
      );
      setQuotes(await res.json());
    }
    filter();
  }, [activeCategory]);

  async function clearFilter() {
    setActiveCategory(null);
    const res = await fetch(`${API_URL}/quotes`);
    setQuotes(await res.json());
  }

  async function refreshFeatured() {
    const res = await fetch(`${API_URL}/quotes/random`);
    setFeatured(await res.json());
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-8 h-8 border-2 border-accent border-t-transparent rounded-full animate-spin" />
          <p className="text-muted text-sm">Loading quotes...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="border-b border-card-border">
        <div className="max-w-6xl mx-auto px-6 py-8">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-accent/10 flex items-center justify-center">
              <svg
                className="w-5 h-5 text-accent"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={2}
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 01.865-.501 48.172 48.172 0 003.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z"
                />
              </svg>
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight">
                ClaudeQuotes
              </h1>
              <p className="text-muted text-sm">
                50 timeless quotes to inspire your day
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-10 space-y-10">
        {/* Featured Quote */}
        {featured && (
          <section className="animate-fade-in-up">
            <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-accent/10 via-accent-light/30 to-transparent border border-card-border p-8 md:p-12">
              <div className="absolute top-4 right-6 text-accent/20 text-[120px] font-serif leading-none select-none">
                &ldquo;
              </div>
              <div className="relative">
                <p className="text-sm font-medium text-accent uppercase tracking-wider mb-4">
                  Quote of the Moment
                </p>
                <blockquote className="text-2xl md:text-3xl font-light leading-relaxed mb-6 max-w-3xl">
                  &ldquo;{featured.text}&rdquo;
                </blockquote>
                <div className="flex items-center justify-between">
                  <p className="text-muted font-medium">
                    &mdash; {featured.author}
                  </p>
                  <button
                    onClick={refreshFeatured}
                    className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-accent hover:bg-accent/10 rounded-lg transition-colors cursor-pointer"
                  >
                    <svg
                      className="w-4 h-4"
                      fill="none"
                      viewBox="0 0 24 24"
                      strokeWidth={2}
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182"
                      />
                    </svg>
                    New quote
                  </button>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* Category Filters */}
        <section>
          <div className="flex flex-wrap gap-2">
            <button
              onClick={clearFilter}
              className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors cursor-pointer ${
                !activeCategory
                  ? "bg-accent text-white"
                  : "bg-card-bg border border-card-border text-muted hover:text-foreground"
              }`}
            >
              All
            </button>
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setActiveCategory(cat)}
                className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors capitalize cursor-pointer ${
                  activeCategory === cat
                    ? "bg-accent text-white"
                    : "bg-card-bg border border-card-border text-muted hover:text-foreground"
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </section>

        {/* Quotes Grid */}
        <section>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {quotes.map((quote, i) => (
              <div
                key={quote.id}
                className="animate-fade-in-up group rounded-xl border border-card-border bg-card-bg p-6 hover:border-accent/40 hover:shadow-lg hover:shadow-accent/5 transition-all duration-300"
                style={{ animationDelay: `${i * 30}ms` }}
              >
                <div className="text-accent/30 text-3xl font-serif leading-none mb-3 select-none">
                  &ldquo;
                </div>
                <p className="text-[15px] leading-relaxed mb-4">{quote.text}</p>
                <div className="flex items-center justify-between">
                  <p className="text-sm text-muted font-medium">
                    {quote.author}
                  </p>
                  <span className="text-xs px-2.5 py-0.5 rounded-full bg-accent/10 text-accent capitalize">
                    {quote.category}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </section>

        {quotes.length === 0 && (
          <div className="text-center py-20 text-muted">
            <p>No quotes found. Is the API running?</p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-card-border mt-10">
        <div className="max-w-6xl mx-auto px-6 py-6 text-center text-sm text-muted">
          ClaudeQuotes &mdash; Built with Next.js + FastAPI
        </div>
      </footer>
    </div>
  );
}
