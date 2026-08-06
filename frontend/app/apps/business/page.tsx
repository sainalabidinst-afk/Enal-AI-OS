"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function BusinessAppPage() {
  const router = useRouter();
  useEffect(() => {
    router.replace("/workspace/business");
  }, [router]);
  return null;
}
