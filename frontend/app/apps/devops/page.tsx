"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function DevopsAppPage() {
  const router = useRouter();
  useEffect(() => {
    router.replace("/workspace/devops");
  }, [router]);
  return null;
}
