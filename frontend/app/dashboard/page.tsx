"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function DashboardRoute() {
  const router = useRouter();

  useEffect(() => {
    router.replace("/console");
  }, [router]);

  return null;
}

