"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function SecurityAppPage() {
  const router = useRouter();
  useEffect(() => {
    router.replace("/workspace/security");
  }, [router]);
  return null;
}
