"use client";

import { memo } from "react";
import { GenericCapabilityWorkspace } from "./generic-capability-workspace";

const DatabaseWorkspaceInner = () => {
  return <GenericCapabilityWorkspace capabilityId="database" capabilityName="Database Engineer" />;
};

export const DatabaseWorkspace = memo(DatabaseWorkspaceInner);
DatabaseWorkspace.displayName = "DatabaseWorkspace";
