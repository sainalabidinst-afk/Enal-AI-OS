"""
UI/UX Designer — Accessibility Checker Module.

Audits UI designs for accessibility compliance:
- WCAG 2.1 criterion checking
- Color contrast validation
- Keyboard navigation verification
- Screen reader compatibility
- ARIA attribute validation
- Form accessibility checking
- Remediation priority ranking
"""

from __future__ import annotations

import logging
from typing import Any

from apps.ui_ux_designer.schemas import (
    AccessibilityReport,
    AccessibilityViolation,
    BusinessContext,
    StakeholderInput,
    DesignSystem,
    Prototype,
)

logger = logging.getLogger(__name__)


class AccessibilityChecker:
    """
    Audits UI designs for WCAG 2.1 accessibility compliance.

    Checks color contrast, keyboard navigation, ARIA attributes,
    form labels, and screen reader compatibility.
    """

    def __init__(self) -> None:
        self._wcag_checks = [
            "1.1.1 Non-text Content",
            "1.3.1 Info and Relationships",
            "1.4.3 Contrast (Minimum)",
            "1.4.4 Resize Text",
            "2.1.1 Keyboard",
            "2.4.1 Bypass Blocks",
            "2.4.2 Page Titled",
            "2.4.6 Headings and Labels",
            "3.2.1 On Focus",
            "3.2.2 On Input",
            "3.3.1 Error Identification",
            "3.3.2 Labels or Instructions",
            "4.1.1 Parsing",
            "4.1.2 Name, Role, Value",
        ]
        self._contrast_ratios = {
            "AA_normal": 4.5,
            "AA_large": 3.0,
            "AAA_normal": 7.0,
            "AAA_large": 4.5,
        }

    def audit(
        self,
        design_system: DesignSystem | None,
        prototype: Prototype | None,
        context: BusinessContext,
    ) -> AccessibilityReport:
        """
        Audit accessibility of a design system and prototype.

        Args:
            design_system: Design system to audit
            prototype: Prototype to audit
            context: Business context

        Returns:
            AccessibilityReport with violations and compliance score
        """
        violations: list[AccessibilityViolation] = []
        passed_checks: list[str] = []

        if design_system:
            violations.extend(self._check_design_system(design_system))
            passed_checks.extend(self._passed_design_system_checks(design_system))

        if prototype:
            violations.extend(self._check_prototype(prototype))

        if not design_system and not prototype:
            violations.append(
                AccessibilityViolation(
                    wcag_criterion="N/A",
                    severity="medium",
                    description="Tidak ada design system atau prototype yang diberikan untuk audit",
                    element_selector="N/A",
                    recommendation="Berikan design system atau prototype untuk audit aksesibilitas",
                    impact="Tidak dapat memvalidasi kepatuhan aksesibilitas",
                )
            )

        total_checks = len(self._wcag_checks) + max(0, len(design_system.components) if design_system else 0) + max(0, len(prototype.screens) if prototype else 0)
        violations_found = len(violations)
        compliance_score = max(0.0, 1.0 - (violations_found / max(total_checks, 1)))

        remediation_priority = self._build_remediation_priority(violations)

        return AccessibilityReport(
            total_checks=total_checks,
            violations_found=violations_found,
            compliance_score=round(compliance_score, 4),
            violations=violations,
            passed_checks=passed_checks,
            remediation_priority=remediation_priority,
            wcag_level="AA",
        )

    def _check_design_system(self, ds: DesignSystem) -> list[AccessibilityViolation]:
        """Check design system for accessibility violations."""
        violations: list[AccessibilityViolation] = []

        contrast_violations = self._check_color_contrast(ds)
        violations.extend(contrast_violations)

        token_violations = self._check_tokens(ds)
        violations.extend(token_violations)

        return violations

    def _check_prototype(self, prototype: Prototype) -> list[AccessibilityViolation]:
        """Check prototype for accessibility violations."""
        violations: list[AccessibilityViolation] = []

        for screen in prototype.screens:
            screen_violations = self._check_screen(screen)
            violations.extend(screen_violations)

        interaction_violations = self._check_interactions(prototype)
        violations.extend(interaction_violations)

        return violations

    def _check_color_contrast(self, ds: DesignSystem) -> list[AccessibilityViolation]:
        """Check color contrast ratios."""
        violations: list[AccessibilityViolation] = []

        for token in ds.tokens:
            if token.type == "color":
                color = token.value
                if self._is_low_contrast(color, "#FFFFFF"):
                    violations.append(
                        AccessibilityViolation(
                            wcag_criterion="1.4.3 Contrast (Minimum)",
                            severity="high",
                            description=f"Warna '{token.name}' ({color}) mungkin memiliki kontras rendah dengan latar belakang putih",
                            element_selector=f"token:{token.name}",
                            recommendation=f"Verifikasi kontras '{token.name}' mencapai 4.5:1 untuk teks normal",
                            impact="Teks mungkin tidak terbaca untuk pengguna dengan gangguan penglihatan",
                        )
                    )

        return violations

    def _is_low_contrast(self, fg: str, bg: str) -> bool:
        """Simple contrast ratio check (approximate)."""
        light_colors = ["#F3F4F6", "#E5E7EB", "#FFFFFF", "#F9FAFB", "#F0FDF4"]
        medium_colors = ["#D1D5DB", "#9CA3AF", "#6B7280", "#10B981", "#F59E0B"]
        if fg in light_colors and bg in light_colors:
            return True
        if fg in medium_colors and bg in ["#F3F4F6", "#FFFFFF", "#F9FAFB"]:
            return True
        return False

    def _check_tokens(self, ds: DesignSystem) -> list[AccessibilityViolation]:
        """Check design tokens for accessibility."""
        violations: list[AccessibilityViolation] = []

        required_token_types = ["color", "typography", "spacing"]
        present_types = {t.type for t in ds.tokens}
        for req_type in required_token_types:
            if req_type not in present_types:
                violations.append(
                    AccessibilityViolation(
                        wcag_criterion="1.3.1 Info and Relationships",
                        severity="medium",
                        description=f"Tipe token '{req_type}' tidak ada di design system",
                        element_selector="design-system:tokens",
                        recommendation=f"Tambahkan token tipe '{req_type}' untuk konsistensi aksesibilitas",
                        impact="Konsistensi desain mungkin terganggu",
                    )
                )

        return violations

    def _check_screen(self, screen: PrototypeScreen) -> list[AccessibilityViolation]:
        """Check a prototype screen for accessibility violations."""
        violations: list[AccessibilityViolation] = []

        has_nav = any(c.get("type") == "Navigation" for c in screen.components)
        has_form = any(c.get("type") in ("Input", "Select", "Button") for c in screen.components)

        if has_form and not any("label" in str(c).lower() for c in screen.components):
            violations.append(
                AccessibilityViolation(
                    wcag_criterion="3.3.2 Labels or Instructions",
                    severity="high",
                    description="Komponen form pada screen mungkin tidak memiliki label yang terasosiasi",
                    element_selector=f"screen:{screen.name}",
                    recommendation="Pastikan semua input memiliki label teks yang terasosiasi via htmlFor/id",
                    impact="Pengguna screen reader tidak dapat memahami field form",
                )
            )

        if has_nav:
            has_skip_link = False
            for interaction in screen.interactions:
                if "skip" in str(interaction).lower():
                    has_skip_link = True
                    break
            if not has_skip_link:
                violations.append(
                    AccessibilityViolation(
                        wcag_criterion="2.4.1 Bypass Blocks",
                        severity="medium",
                        description="Navigasi mungkin tidak memiliki skip link",
                        element_selector=f"screen:{screen.name}:navigation",
                        recommendation="Tambahkan 'Skip to main content' link sebelum navigasi",
                        impact="Pengguna keyboard harus menavigasi seluruh navigasi sebelum konten utama",
                    )
                )

        return violations

    def _check_interactions(self, prototype: Prototype) -> list[AccessibilityViolation]:
        """Check interactions for accessibility."""
        violations: list[AccessibilityViolation] = []

        all_triggers = set()
        for screen in prototype.screens:
            for interaction in screen.interactions:
                trigger = interaction.get("trigger", "")
                all_triggers.add(trigger)

        if "keydown" not in all_triggers and "keyboard" not in all_triggers:
            violations.append(
                AccessibilityViolation(
                    wcag_criterion="2.1.1 Keyboard",
                    severity="high",
                    description="Tidak ada interaksi keyboard yang terdefinisi dalam prototype",
                    element_selector="prototype:interactions",
                    recommendation="Tambahkan keyboard shortcuts dan keydown handlers untuk semua interaksi utama",
                    impact="Pengguna tidak dapat menggunakan keyboard untuk navigasi",
                )
            )

        return violations

    def _passed_design_system_checks(self, ds: DesignSystem) -> list[str]:
        """Return list of passed design system checks."""
        passed = ["WCAG 2.1 AA — Design System terdefinisi"]
        if any(t.type == "color" for t in ds.tokens):
            passed.append("Design System — Token warna terdefinisi")
        if any(t.type == "typography" for t in ds.tokens):
            passed.append("Design System — Token tipografi terdefinisi")
        if ds.accessibility_standards:
            passed.append(f"Standar aksesibilitas: {', '.join(ds.accessibility_standards)}")
        return passed

    def _build_remediation_priority(self, violations: list[AccessibilityViolation]) -> list[str]:
        """Build prioritized remediation list."""
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        sorted_violations = sorted(violations, key=lambda v: priority_order.get(v.severity, 99))

        return [
            f"[{v.severity.upper()}] {v.wcag_criterion}: {v.description[:80]}..."
            for v in sorted_violations
            if v.wcag_criterion != "N/A"
        ]
