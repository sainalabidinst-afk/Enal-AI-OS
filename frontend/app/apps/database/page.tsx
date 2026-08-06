"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function DatabaseAppPage() {
  const router = useRouter();
  useEffect(() => {
    router.replace("/workspace/database");
  }, [router]);
  return null;
}
