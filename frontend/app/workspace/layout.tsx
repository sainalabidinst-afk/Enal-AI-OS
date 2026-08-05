import { WorkspaceEngine } from "@/components/workspace/engine/workspace-engine";

export default function WorkspaceIndexLayout({ children }: { children: React.ReactNode }) {
  return <WorkspaceEngine>{children}</WorkspaceEngine>;
}
