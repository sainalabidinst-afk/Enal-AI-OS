"use client";

import { type ReactNode } from "react";
import { WorkspaceProvider } from "./workspace-provider";
import { WorkspaceLayout } from "./workspace-layout";

export function WorkspaceEngine({ children }: { children: ReactNode }) {
  return (
    <WorkspaceProvider>
      <WorkspaceLayout>{children}</WorkspaceLayout>
    </WorkspaceProvider>
  );
}
