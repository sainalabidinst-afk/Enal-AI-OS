"use client";

import { memo } from "react";
import { GenericCapabilityWorkspace } from "./generic-capability-workspace";

const DevOpsWorkspaceInner = () => {
  return <GenericCapabilityWorkspace capabilityId="devops" capabilityName="DevOps Engineer" />;
};

export const DevOpsWorkspace = memo(DevOpsWorkspaceInner);
DevOpsWorkspace.displayName = "DevOpsWorkspace";
