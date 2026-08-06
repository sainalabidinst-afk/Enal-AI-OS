"use client";

import { memo } from "react";
import { GenericCapabilityWorkspace } from "./generic-capability-workspace";

const BusinessWorkspaceInner = () => {
  return <GenericCapabilityWorkspace capabilityId="business" capabilityName="Business Analyst" />;
};

export const BusinessWorkspace = memo(BusinessWorkspaceInner);
BusinessWorkspace.displayName = "BusinessWorkspace";
