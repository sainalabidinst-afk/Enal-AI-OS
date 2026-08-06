"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function DecisionAppPage() {
  const router = useRouter();
  useEffect(() => {
    router.replace("/workspace/decision");
  }, [router]);
  return null;
}
