"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function ResearchAppPage() {
  const router = useRouter();
  useEffect(() => {
    router.replace("/workspace/research");
  }, [router]);
  return null;
}
