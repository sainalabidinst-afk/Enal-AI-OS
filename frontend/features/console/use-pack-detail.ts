"use client";

import { useEffect, useMemo, useState } from "react";
import {
  getCapabilityCompatibility,
  getCapabilityDependencies,
  getCapabilityLifecycle,
  getGovernancePack,
} from "@/services/console/governance";
import type {
  CapabilityCompatibility,
  CapabilityDependencies,
  CapabilityLifecycleRecord,
  GovernancePack,
} from "@/types/console";

export interface PackDetail {
  packId: string;
  governance: GovernancePack | null;
  lifecycle: CapabilityLifecycleRecord | null;
  dependencies: CapabilityDependencies | null;
  compatibility: CapabilityCompatibility | null;
  errors: string[];
}

export function usePackDetail(
  packId: string
): PackDetail & { loading: boolean; refresh: () => void } {
  const [state, setState] = useState<PackDetail>({
    packId,
    governance: null,
    lifecycle: null,
    dependencies: null,
    compatibility: null,
    errors: [],
  });
  const [loading, setLoading] = useState(true);
  const [nonce, setNonce] = useState(0);

  useEffect(() => {
    let cancelled = false;
    const errors: string[] = [];

    async function load() {
      setLoading(true);
      const [governance, lifecycle, dependencies, compatibility] = await Promise.all([
        getGovernancePack(packId).catch((error) => {
          errors.push(`governance: ${error.message}`);
          return null;
        }),
        getCapabilityLifecycle(packId).catch((error) => {
          errors.push(`lifecycle: ${error.message}`);
          return null;
        }),
        getCapabilityDependencies(packId).catch((error) => {
          errors.push(`dependencies: ${error.message}`);
          return null;
        }),
        getCapabilityCompatibility(packId).catch((error) => {
          errors.push(`compatibility: ${error.message}`);
          return null;
        }),
      ]);

      if (cancelled) return;
      setState({
        packId,
        governance,
        lifecycle,
        dependencies,
        compatibility,
        errors,
      });
      setLoading(false);
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [packId, nonce]);

  return useMemo(
    () => ({ ...state, loading, refresh: () => setNonce((value) => value + 1) }),
    [state, loading]
  );
}