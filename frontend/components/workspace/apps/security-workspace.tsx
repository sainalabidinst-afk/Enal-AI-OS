"use client";

import { memo } from "react";
import { GenericCapabilityWorkspace } from "./generic-capability-workspace";

const SecurityWorkspaceInner = () => {
  return <GenericCapabilityWorkspace capabilityId="security" capabilityName="Security Engineer" />;
};

export const SecurityWorkspace = memo(SecurityWorkspaceInner);
SecurityWorkspace.displayName = "SecurityWorkspace";
