"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function ArchitectAppPage() {
  const router = useRouter();
  useEffect(() => {
    router.replace("/workspace/architect");
  }, [router]);
  return null;
}
