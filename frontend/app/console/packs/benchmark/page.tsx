"use client";

import { Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { PackDetailView } from "@/components/console/packs/pack-detail-view";

function BenchmarkCases() {
  const search = useSearchParams();
  return <PackDetailView packId="benchmark" focusCase={search.get("case")} />;
}

export default function ConsoleBenchmarkCasesPage() {
  return (
    <Suspense fallback={null}>
      <BenchmarkCases />
    </Suspense>
  );
}