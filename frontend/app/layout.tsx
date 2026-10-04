import type { Metadata } from "next";
import AppClient from "./app-client";
import "./globals.css";

const inter = "font-sans";

export const metadata: Metadata = {
  title: "Enal AI OS",
  description: "AI Execution Platform — One conversation, complete outcomes",
  manifest: "/manifest.json",
  appleWebApp: {
    capable: true,
    statusBarStyle: "default",
    title: "Enal AI OS",
  },
  formatDetection: {
    telephone: false,
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="manifest" href="/manifest.json" />
        <meta name="theme-color" content="#3b82f6" />
        <link rel="apple-touch-icon" href="/icons/icon-192x192.png" />
      </head>
      <body className={inter}>
        <AppClient>{children}</AppClient>
      </body>
    </html>
  );
}
