"use client";

import { memo } from "react";
import { GenericCapabilityWorkspace } from "./generic-capability-workspace";

const NetworkWorkspaceInner = () => {
  return <GenericCapabilityWorkspace capabilityId="network" capabilityName="Network Engineer" />;
};

export const NetworkWorkspace = memo(NetworkWorkspaceInner);
NetworkWorkspace.displayName = "NetworkWorkspace";
