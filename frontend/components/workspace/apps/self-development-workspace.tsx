"use client";

import { memo } from "react";
import { GenericCapabilityWorkspace } from "./generic-capability-workspace";

const SelfDevelopmentWorkspaceInner = () => {
  return <GenericCapabilityWorkspace capabilityId="self-development" capabilityName="Self Development" />;
};

export const SelfDevelopmentWorkspace = memo(SelfDevelopmentWorkspaceInner);
SelfDevelopmentWorkspace.displayName = "SelfDevelopmentWorkspace";
