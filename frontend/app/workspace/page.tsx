"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function WorkspaceIndexPage() {
  const router = useRouter();
  useEffect(() => {
    router.replace("/workspace/trading");
  }, [router]);
  return null;
}
