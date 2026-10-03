"use client";

import { useEffect, useState, useCallback } from "react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Dialog } from "@/components/ui/dialog";
import { useCognitiveStore } from "@/store/cognitive-store";
import {
  getPendingConsents,
  respondToConsent,
  RiskLevel,
  ConsentRequest,
} from "@/services/consent";

const RISK_COLORS: Record<RiskLevel, string> = {
  low: "bg-green-500",
  medium: "bg-yellow-500",
  high: "bg-red-500",
};

const RISK_LABELS: Record<RiskLevel, string> = {
  low: "Low Risk",
  medium: "Medium Risk",
  high: "High Risk",
};

interface ConsentDialogProps {
  open?: boolean;
  onClose?: () => void;
  pollIntervalMs?: number;
}

export function ConsentDialog({
  open: controlledOpen,
  onClose,
  pollIntervalMs = 5000,
}: ConsentDialogProps) {
  const [internalOpen, setInternalOpen] = useState(false);
  const [pendingRequests, setPendingRequests] = useState<ConsentRequest[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [processingId, setProcessingId] = useState<string | null>(null);

  const pendingCount = useCognitiveStore((s) => s.orchestration.capabilities.length);
  const setMetaFlags = useCognitiveStore((s) => s.setMetaCognitiveFlags);

  const isOpen = controlledOpen ?? internalOpen;
  const handleClose = onClose ?? (() => setInternalOpen(false));

  const fetchPending = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const requests = await getPendingConsents();
      setPendingRequests(requests);
      if (requests.length > 0) {
        setInternalOpen(true);
        setMetaFlags({ uncertainty: true });
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load consent requests");
    } finally {
      setIsLoading(false);
    }
  }, [setMetaFlags]);

  const handleRespond = async (requestId: string, decision: "approve" | "deny") => {
    setProcessingId(requestId);
    setError(null);
    try {
      await respondToConsent(requestId, decision);
      setPendingRequests((prev) => prev.filter((r) => r.request_id !== requestId));
      setMetaFlags({ uncertainty: false });
      if (pendingRequests.length <= 1) {
        handleClose();
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to respond to consent request");
    } finally {
      setProcessingId(null);
    }
  };

  const handleApprove = (request: ConsentRequest) => {
    handleRespond(request.request_id, "approve");
  };

  const handleDeny = (request: ConsentRequest) => {
    handleRespond(request.request_id, "deny");
  };

  const handleExpire = (request: ConsentRequest) => {
    setPendingRequests((prev) => prev.filter((r) => r.request_id !== request.request_id));
  };

  useEffect(() => {
    if (!isOpen) return;
    fetchPending();
    const interval = setInterval(fetchPending, pollIntervalMs);
    return () => clearInterval(interval);
  }, [isOpen, fetchPending, pollIntervalMs]);

  const now = Date.now();
  const activeRequests = pendingRequests.filter((r) => {
    const expired = new Date(r.expires_at).getTime() < now;
    if (expired && r.status === "pending") {
      handleExpire(r);
      return false;
    }
    return true;
  });

  return (
    <Dialog
      open={isOpen}
      onClose={handleClose}
      title="Consent Required"
      description={activeRequests.length > 1 ? `${activeRequests.length} pending requests` : undefined}
    >
      <div className="space-y-4">
        {error && (
          <div className="rounded-md border border-[var(--color-danger)] bg-red-50 px-4 py-3 text-sm text-[var(--color-danger)]">
            {error}
          </div>
        )}

        {activeRequests.length === 0 && !isLoading ? (
          <div className="py-8 text-center text-sm text-[var(--color-text-secondary)]">
            No pending consent requests
          </div>
        ) : (
          <div className="space-y-3">
            {activeRequests.map((request) => (
              <ConsentRequestCard
                key={request.request_id}
                request={request}
                onApprove={handleApprove}
                onDeny={handleDeny}
                isProcessing={processingId === request.request_id}
              />
            ))}
          </div>
        )}
      </div>
      <div className="flex justify-end gap-2">
        <Button
          variant="secondary"
          size="sm"
          onClick={handleClose}
          disabled={activeRequests.length > 0}
        >
          Close
        </Button>
      </div>
    </Dialog>
  );
}

interface ConsentRequestCardProps {
  request: ConsentRequest;
  onApprove: (request: ConsentRequest) => void;
  onDeny: (request: ConsentRequest) => void;
  isProcessing: boolean;
}

function ConsentRequestCard({
  request,
  onApprove,
  onDeny,
  isProcessing,
}: ConsentRequestCardProps) {
  const [timeLeft, setTimeLeft] = useState<string>("");

  useEffect(() => {
    const update = () => {
      const diff = new Date(request.expires_at).getTime() - Date.now();
      if (diff <= 0) {
        setTimeLeft("Expired");
      } else {
        const seconds = Math.ceil(diff / 1000);
        setTimeLeft(`${seconds}s`);
      }
    };
    update();
    const interval = setInterval(update, 1000);
    return () => clearInterval(interval);
  }, [request.expires_at]);

  const risk = request.risk_level as RiskLevel;
  const riskColor = RISK_COLORS[risk] || "bg-gray-500";

  return (
    <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3">
          <div className={cn("mt-0.5 h-3 w-3 shrink-0 rounded-full", riskColor)} />
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold uppercase text-[var(--color-text-secondary)]">
                {RISK_LABELS[risk] || risk}
              </span>
              <span
                className={cn(
                  "text-xs px-2 py-0.5 rounded-full font-medium",
                  risk === "high"
                    ? "bg-red-100 text-red-700"
                    : risk === "medium"
                    ? "bg-yellow-100 text-yellow-700"
                    : "bg-green-100 text-green-700",
                )}
              >
                {risk}
              </span>
            </div>
            <p className="mt-1 text-sm font-medium text-[var(--color-text-primary)]">
              {request.description}
            </p>
            {request.action_type && (
              <p className="mt-1 text-xs text-[var(--color-text-secondary)]">
                Action: <code className="rounded bg-[var(--color-bg-primary)] px-1.5 py-0.5">{request.action_type}</code>
              </p>
            )}
            {request.connector_type && (
              <p className="mt-0.5 text-xs text-[var(--color-text-secondary)]">
                Connector: <span className="font-medium">{request.connector_type}</span>
              </p>
            )}
          </div>
        </div>

        <div className="flex flex-col items-end gap-1.5">
          <div className="text-xs font-medium text-[var(--color-text-secondary)]">
            {timeLeft === "Expired" ? (
              <span className="text-red-500">Expired</span>
            ) : (
              <>Expires in <span className="text-[var(--color-text-primary)]">{timeLeft}</span></>
            )}
          </div>
          {timeLeft !== "Expired" && (
            <div className="flex gap-1.5">
              <Button
                variant="secondary"
                size="sm"
                onClick={() => onDeny(request)}
                disabled={isProcessing}
              >
                Deny
              </Button>
              <Button
                variant="primary"
                size="sm"
                onClick={() => onApprove(request)}
                disabled={isProcessing}
              >
                {isProcessing ? "Processing..." : "Approve"}
              </Button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export function useConsentDialog() {
  const [isOpen, setIsOpen] = useState(false);

  const open = useCallback(() => setIsOpen(true), []);
  const close = useCallback(() => setIsOpen(false), []);

  return { ConsentDialog: () => <ConsentDialog open={isOpen} onClose={close} />, open, close };
}
