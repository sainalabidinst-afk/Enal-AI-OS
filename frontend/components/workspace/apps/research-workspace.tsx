"use client";

import { memo } from "react";
import { GenericCapabilityWorkspace } from "./generic-capability-workspace";

const ResearchWorkspaceInner = () => {
  return <GenericCapabilityWorkspace capabilityId="research" capabilityName="Research Assistant" />;
};

export const ResearchWorkspace = memo(ResearchWorkspaceInner);
ResearchWorkspace.displayName = "ResearchWorkspace";
