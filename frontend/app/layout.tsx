import type { Metadata } from "next";
import { Inter } from "next/font/google";
import AppClient from "./app-client";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Enal AI OS",
  description: "AI Execution Platform — One conversation, complete outcomes",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <AppClient>{children}</AppClient>
      </body>
    </html>
  );
}
