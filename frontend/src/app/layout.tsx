import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { QueryProvider } from '@/providers/query-provider';
import { AuthProvider } from '@/providers/auth-provider';
import { ThemeProvider } from '@/providers/theme-provider';
import { AppShell } from '@/components/layout/app-shell';
import { ToastProvider } from '@/components/shared/toast';
import { ErrorBoundary } from '@/components/layout/error-boundary';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Enal Cognitive Platform',
  description: 'Enterprise-grade AI orchestration platform',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <QueryProvider>
          <AuthProvider>
            <ThemeProvider>
              <ToastProvider>
                <ErrorBoundary>
                  <AppShell>{children}</AppShell>
                </ErrorBoundary>
              </ToastProvider>
            </ThemeProvider>
          </AuthProvider>
        </QueryProvider>
      </body>
    </html>
  );
}
