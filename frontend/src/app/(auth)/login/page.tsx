'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { cn } from '@/lib/cn';
import { useAuthStore } from '@/stores/auth-store';
import { useToast } from '@/components/shared/toast';
import { Loader2 } from 'lucide-react';

export default function LoginPage() {
  const router = useRouter();
  const login = useAuthStore((state) => state.login);
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const isLoading = useAuthStore((state) => state.isLoading);
  const addToast = useToast((state) => state.addToast);

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  if (isAuthenticated) {
    router.push('/dashboard');
    return null;
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(username, password);
      addToast('success', 'Login successful');
      router.push('/dashboard');
    } catch {
      addToast('error', 'Invalid username or password');
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-surface-primary p-4">
      <div className="w-full max-w-sm rounded-lg border border-border bg-surface-secondary p-6 shadow-xl">
        <h1 className="text-xl font-semibold">Enal Cognitive Platform</h1>
        <p className="mt-1 text-sm text-text-secondary">Sign in to continue</p>

        <form onSubmit={handleSubmit} className="mt-6 space-y-4">
          <div>
            <label className="block text-sm font-medium">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="mt-1 w-full rounded-md border border-border bg-surface-primary px-3 py-2 text-sm outline-none focus:border-primary"
              placeholder="Enter username"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 w-full rounded-md border border-border bg-surface-primary px-3 py-2 text-sm outline-none focus:border-primary"
              placeholder="Enter password"
              required
            />
          </div>
          <button
            type="submit"
            disabled={isLoading}
            className={cn(
              'flex w-full items-center justify-center gap-2 rounded-md bg-primary px-4 py-2 text-sm text-white hover:bg-primary-hover',
              isLoading && 'opacity-70'
            )}
          >
            {isLoading && <Loader2 size={16} className="animate-spin" />}
            {isLoading ? 'Signing in...' : 'Sign in'}
          </button>
        </form>
      </div>
    </div>
  );
}
