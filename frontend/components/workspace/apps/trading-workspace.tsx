"use client";

import { memo } from "react";
import { GenericCapabilityWorkspace } from "./generic-capability-workspace";

const TradingWorkspaceInner = () => {
  return <GenericCapabilityWorkspace capabilityId="trading" capabilityName="Trading Analyst" />;
};

export const TradingWorkspace = memo(TradingWorkspaceInner);
TradingWorkspace.displayName = "TradingWorkspace";
