"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function CodeAppPage() {
  const router = useRouter();
  useEffect(() => {
    router.replace("/workspace/code");
  }, [router]);
  return null;
}
