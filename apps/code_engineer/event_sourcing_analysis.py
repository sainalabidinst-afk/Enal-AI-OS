"""
Event Sourcing Analysis
========================

Event Sourcing pattern analysis.

- Event Store: append-only log of events
- Replay: rebuild state from events
- Projection: read models built from events
- Snapshot: periodic state snapshots for performance
"""

from apps.code_engineer.architecture_patterns import ArchitectureFinding, ArchitectureSeverity


class EventSourcingAnalyzer:
    """Event Sourcing pattern analysis."""

    def analyze_event_store(self, code_ast) -> list[ArchitectureFinding]:
        """Detect Event Store pattern."""
        findings: list[ArchitectureFinding] = []
        raw = "\n".join(code_ast.raw_lines)

        event_store_signals = [
            "event_store", "eventstore", "append", "event_stream",
            "event_repository", "event_log", "journal",
        ]
        for signal in event_store_signals:
            if signal in raw.lower():
                findings.append(ArchitectureFinding(
                    category="event_sourcing",
                    severity=ArchitectureSeverity.INFO,
                    description=f"Event Store pattern detected (signal: '{signal}')",
                    recommendation=(
                        "Event Store is an append-only log. Events are never modified or deleted. "
                        "Use snapshots for performance optimization on long streams."
                    ),
                    line_number=1,
                    confidence=0.8,
                    pattern="event_store",
                ))
                break

        for cls in code_ast.classes:
            cls_name = cls.name.lower()
            if "event" in cls_name and ("store" in cls_name or "repository" in cls_name or "log" in cls_name):
                findings.append(ArchitectureFinding(
                    category="event_sourcing",
                    severity=ArchitectureSeverity.INFO,
                    description=f"Event Store class detected: '{cls.name}'",
                    recommendation=(
                        "Event Store implementation should handle: append (write), "
                        "read_stream (get events by aggregate), and snapshot management."
                    ),
                    line_number=cls.lineno,
                    confidence=0.85,
                    pattern="event_store",
                ))
        return findings

    def analyze_projections(self, code_ast) -> list[ArchitectureFinding]:
        """Detect Projection patterns."""
        findings: list[ArchitectureFinding] = []
        for cls in code_ast.classes:
            cls_name = cls.name.lower()
            if "projection" in cls_name or "projector" in cls_name or "read_model" in cls_name:
                has_when = any(m.name == "when" or m.name.startswith("project") for m in cls.methods)
                if has_when:
                    findings.append(ArchitectureFinding(
                        category="event_sourcing",
                        severity=ArchitectureSeverity.INFO,
                        description=f"Projection detected: '{cls.name}'",
                        recommendation=(
                            "Projections build read models from events. Each projection "
                            "handles specific event types. Rebuild from scratch by replaying all events."
                        ),
                        line_number=cls.lineno,
                        confidence=0.85,
                        pattern="projection",
                    ))
        return findings

    def analyze(self, code_ast) -> list[ArchitectureFinding]:
        findings: list[ArchitectureFinding] = []
        findings.extend(self.analyze_event_store(code_ast))
        findings.extend(self.analyze_projections(code_ast))
        return findings
