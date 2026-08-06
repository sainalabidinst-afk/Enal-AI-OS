"use client";

import { memo } from "react";
import { GenericCapabilityWorkspace } from "./generic-capability-workspace";

const DecisionWorkspaceInner = () => {
  return <GenericCapabilityWorkspace capabilityId="decision" capabilityName="Decision Intelligence" />;
};

export const DecisionWorkspace = memo(DecisionWorkspaceInner);
DecisionWorkspace.displayName = "DecisionWorkspace";
