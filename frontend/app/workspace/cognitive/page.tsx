"use client";

import { CognitiveLayer, System1ReactiveLayer, System2AnalyticalLayer, System3StrategicLayer } from "@/components/cognitive";

export default function CognitiveWorkspacePage() {
  return (
    <CognitiveLayer>
      <System1ReactiveLayer />
      <System2AnalyticalLayer />
      <System3StrategicLayer />
    </CognitiveLayer>
  );
}
