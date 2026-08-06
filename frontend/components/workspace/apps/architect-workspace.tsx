"use client";

import { memo } from "react";
import { GenericCapabilityWorkspace } from "./generic-capability-workspace";

const ArchitectWorkspaceInner = () => {
  return <GenericCapabilityWorkspace capabilityId="architect" capabilityName="System Architect" />;
};

export const ArchitectWorkspace = memo(ArchitectWorkspaceInner);
ArchitectWorkspace.displayName = "ArchitectWorkspace";
