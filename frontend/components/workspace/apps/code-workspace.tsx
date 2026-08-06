"use client";

import { memo } from "react";
import { GenericCapabilityWorkspace } from "./generic-capability-workspace";

const CodeWorkspaceInner = () => {
  return <GenericCapabilityWorkspace capabilityId="code" capabilityName="Code Engineer" />;
};

export const CodeWorkspace = memo(CodeWorkspaceInner);
CodeWorkspace.displayName = "CodeWorkspace";
