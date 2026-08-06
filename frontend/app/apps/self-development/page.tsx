"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function SelfDevelopmentAppPage() {
  const router = useRouter();
  useEffect(() => {
    router.replace("/workspace/self-development");
  }, [router]);
  return null;
}
