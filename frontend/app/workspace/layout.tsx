import { WorkspaceEngine } from "@/components/workspace/engine/workspace-engine";

export default function WorkspaceIndexLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="legacy-workspace">
      <div className="border-b border-amber-200 bg-amber-50 px-4 py-2 text-center text-xs text-amber-800 dark:border-amber-700 dark:bg-amber-900/30 dark:text-amber-200">
        Legacy workspace layout — migrate to{" "}
        <a href="/console/trading" className="font-medium underline">
          /console/trading
        </a>
      </div>
      <WorkspaceEngine>{children}</WorkspaceEngine>
    </div>
  );
}
