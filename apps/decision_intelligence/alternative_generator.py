"""
Alternative Generation — enumerate viable alternatives.

Generates multiple viable alternatives for a decision context, applies
hard-constraint filtering, and assigns initial feasibility scores so
downstream risk/trade-off/scoring stages have a bounded candidate set.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class GeneratedAlternative:
    """An alternative produced by the generator."""

    description: str
    feasibility: float = 1.0
    tags: list[str] = field(default_factory=list)
    source_hint: str = "generated"


class AlternativeGenerator:
    """
    Generates decision alternatives from a context and evidence set.

    Uses keyword/template heuristics to enumerate alternatives, then
    filters against hard constraints.

    Usage::

        gen = AlternativeGenerator()
        alts = gen.generate(context, evidence_set, constraints, max_alternatives)
    """

    # Template library keyed by domain keywords present in the context.
    _TEMPLATES: dict[str, list[str]] = {
        "refactor": [
            "Incremental refactoring of the current module (small, safe changes)",
            "Targeted refactor of the highest-risk components only",
            "Full rewrite of the module with a new architecture",
            "Hybrid: incremental refactor plus selective rewrite of core paths",
        ],
        "deployment": [
            "Blue-green deployment with instant rollback",
            "Canary deployment with progressive traffic shift",
            "Rolling deployment with gradual instance replacement",
            "Recreate deployment (stop old, start new)",
        ],
        "trading": [
            "Enter position now with tight stop-loss",
            "Wait for pullback to key support level before entering",
            "Enter partial position, add on confirmation",
            "Stand aside until market structure confirms direction",
        ],
        "network": [
            "Apply configuration change to a low-risk subset first",
            "Staged migration across all devices with rollback snapshots",
            "Keep current configuration; add monitoring and verification only",
            "Full migration with parallel maintenance window",
        ],
        "architecture": [
            "Adopt proposed architecture with incremental migration",
            "Adopt proposed architecture with full rewrite",
            "Maintain current architecture; address defects individually",
            "Hybrid: adopt core elements, keep stable modules intact",
        ],
        "research": [
            "Synthesize conclusion from strongest evidence clusters",
            "Defer conclusion until conflicting evidence is resolved",
            "Report both positions with confidence-weighted framing",
            "Expand evidence collection before drawing conclusions",
        ],
        "security": [
            "Apply hardening measures to exposed services immediately",
            "Stage hardening behind a maintenance window",
            "Harden only critical paths; document residual risk",
            "Full security overhaul with vendor-validated baselines",
        ],
    }

    # Generic fallback alternatives when no keyword matches.
    _FALLBACK_TEMPLATES: list[str] = [
        "Proceed with the recommended approach now",
        "Defer the decision pending additional evidence",
        "Proceed with a smaller-scope pilot first",
        "Select the lowest-risk option and monitor outcomes",
        "Pursue the highest-value option with risk mitigation",
        "Combine the top recommendations into a staged plan",
    ]

    def generate(
        self,
        context: str,
        evidence_set: Any,
        constraints: list[str],
        max_alternatives: int = 5,
    ) -> list[GeneratedAlternative]:
        """
        Generate up to max_alternatives viable alternatives.

        Args:
            context: Natural-language decision context.
            evidence_set: Processed EvidenceSet (used to inform feasibility).
            constraints: Hard constraints that eliminate alternatives.
            max_alternatives: Maximum number of alternatives to return.

        Returns:
            A list of feasible generated alternatives.
        """
        templates = self._select_templates(context)
        alternatives: list[GeneratedAlternative] = []

        for tpl in templates:
            alt = GeneratedAlternative(description=tpl)
            if self._passes_constraints(tpl, constraints):
                alt.feasibility = self._score_feasibility(context, evidence_set, tpl)
                alternatives.append(alt)
            if len(alternatives) >= max_alternatives:
                break

        # If no template matched, fall back to generic alternatives.
        if not alternatives:
            for tpl in self._FALLBACK_TEMPLATES:
                alt = GeneratedAlternative(description=tpl, source_hint="fallback")
                if self._passes_constraints(tpl, constraints):
                    alternatives.append(alt)
                if len(alternatives) >= max_alternatives:
                    break

        return alternatives

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _select_templates(self, context: str) -> list[str]:
        """Pick the template set whose keyword best matches the context."""
        lowered = context.lower()
        for keyword, templates in self._TEMPLATES.items():
            if keyword in lowered:
                return templates
        # Secondary keyword pass for synonyms.
        synonyms = {
            "refactor": ["restructure", "clean up", "improve code", "rewrite"],
            "deployment": ["deploy", "rollout", "release"],
            "trading": ["trade", "invest", "position", "market", "buy", "sell"],
            "network": ["router", "config", "firewall", "vlan", "bgp", "mikrotik"],
            "architecture": ["system design", "layers", "boundaries", "monolith"],
            "research": ["evidence", "study", "paper", "hypothesis"],
            "security": ["vulnerability", "harden", "threat", "audit"],
        }
        for keyword, words in synonyms.items():
            if any(w in lowered for w in words):
                return self._TEMPLATES[keyword]
        return []

    def _passes_constraints(self, description: str, constraints: list[str]) -> bool:
        """Check whether a description violates any hard constraint.

        A negation heuristic: if a constraint contains a negative word
        (no, not, without, avoid, must not) and the description contains
        the constrained term, the alternative is filtered.
        """
        if not constraints:
            return True
        lowered = description.lower()
        for constraint in constraints:
            c = constraint.lower().strip()
            if not c:
                continue
            if any(neg in c for neg in ("no ", "not ", "without ", "avoid ", "must not", "cannot", "never ")):
                # Extract the key term after the negation.
                for neg in ("no ", "not ", "without ", "avoid ", "must not", "cannot", "never "):
                    if neg in c:
                        term = c.split(neg)[-1].strip().rstrip(".,;")
                        if term and term.lower() in lowered:
                            return False
        return True

    def _score_feasibility(self, context: str, evidence_set: Any, description: str) -> float:
        """
        Heuristic feasibility score (0-1).

        Higher when evidence supports the direction implied by the
        description and when the description aligns with context keywords.
        """
        score = 0.6  # baseline

        # Evidence alignment.
        if evidence_set is not None:
            if description.lower().startswith("stand aside") or description.lower().startswith("defer"):
                if evidence_set.avg_quality < 0.5:
                    score += 0.2
                else:
                    score -= 0.1
            elif evidence_set.dominant_sentiment == "positive" and evidence_set.positive_weight > 0.3:
                score += 0.15
            elif evidence_set.dominant_sentiment == "negative":
                score -= 0.1

        # Context keyword alignment.
        lowered = context.lower()
        if any(w in description.lower() for w in ("pilot", "subset", "small", "incremental", "staged")):
            score += 0.05
        if any(w in lowered for w in ("urgent", "critical", "immediately", "asap")):
            score -= 0.05

        return max(0.0, min(1.0, score))
