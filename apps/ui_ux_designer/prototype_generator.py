"""
UI/UX Designer — Prototype Generator Module.

Generates interactive prototypes:
- Screen layout specification
- Interaction mapping
- User flow definition
- Responsive breakpoints
- Fidelity levels (low/medium/high)
"""

from __future__ import annotations

import logging
from typing import Any

from apps.ui_ux_designer.schemas import (
    Prototype,
    PrototypeScreen,
    BusinessContext,
    StakeholderInput,
    Persona,
    UXResearchResult,
    DesignSystem,
)

logger = logging.getLogger(__name__)


class PrototypeGenerator:
    """
    Generates interactive prototype specifications from design systems
    and UX research results.

    Produces screen layouts, interaction mappings, user flows,
    and responsive breakpoints.
    """

    def __init__(self) -> None:
        self._fidelity_map = {
            "low": {"detail_level": "wireframe", "interactivity": "basic"},
            "medium": {"detail_level": "mockup", "interactivity": "standard"},
            "high": {"detail_level": "production", "interactivity": "full"},
        }

    def generate(
        self,
        context: BusinessContext,
        research: UXResearchResult,
        design_system: DesignSystem | None,
        target_platforms: list[str],
        fidelity: str = "medium",
    ) -> Prototype:
        """
        Generate a prototype specification.

        Args:
            context: Business context
            research: UX research results
            design_system: Design system (optional)
            target_platforms: Target platforms
            fidelity: Prototype fidelity level

        Returns:
            Prototype with screens, flows, and interaction map
        """
        screens = self._generate_screens(context, research, design_system, target_platforms)
        user_flows = self._generate_user_flows(research, screens)
        interaction_map = self._build_interaction_map(screens)
        notes = self._build_notes(fidelity, target_platforms, len(screens))
        estimated_effort = self._estimate_effort(fidelity, len(screens), len(user_flows))

        return Prototype(
            name=f"Prototype — {context.project_name}",
            description=f"Prototipe {fidelity} fidelity untuk {context.project_name} di domain {context.domain}",
            fidelity=fidelity,
            screens=screens,
            user_flows=user_flows,
            interaction_map=interaction_map,
            notes=notes,
            estimated_effort=estimated_effort,
        )

    def _generate_screens(
        self,
        context: BusinessContext,
        research: UXResearchResult,
        design_system: DesignSystem | None,
        target_platforms: list[str],
    ) -> list[PrototypeScreen]:
        """Generate prototype screens from context and research."""
        screens: list[PrototypeScreen] = []
        base_screens = [
            ("Home", "Halaman utama dengan navigasi dan ringkasan konten"),
            ("Dashboard", "Dasbor dengan metrik utama dan ringkasan status"),
            ("List", "Daftar item dengan filter, pencarian, dan paginasi"),
            ("Detail", "Halaman detail item dengan informasi lengkap"),
            ("Form", "Form input dengan validasi dan submit"),
            ("Settings", "Pengaturan pengguna dan preferensi"),
        ]

        if "mobile" in target_platforms:
            base_screens.extend([
                ("MobileHome", "Versi mobile dari halaman utama"),
                ("MobileDetail", "Versi mobile dari halaman detail"),
            ])

        for i, (name, description) in enumerate(base_screens):
            screen = PrototypeScreen(
                name=name,
                description=description,
                layout={
                    "type": "responsive",
                    "columns": 12,
                    "breakpoints": ["mobile", "tablet", "desktop"],
                },
                components=self._screen_components(name),
                interactions=self._screen_interactions(name),
                states=["default", "hover", "focus", "loading", "error", "disabled"],
                responsive_breakpoints=["320px", "768px", "1024px", "1440px"],
            )
            screens.append(screen)

        return screens

    def _screen_components(self, screen_name: str) -> list[dict[str, Any]]:
        """Generate component placements for a screen."""
        component_map = {
            "Home": [
                {"type": "Navigation", "position": "top", "props": {"variant": "topbar"}},
                {"type": "Hero", "position": "top", "props": {"size": "lg"}},
                {"type": "Card", "position": "center", "props": {"columns": 3}},
                {"type": "Footer", "position": "bottom", "props": {}},
            ],
            "Dashboard": [
                {"type": "Navigation", "position": "top", "props": {"variant": "sidebar"}},
                {"type": "MetricCard", "position": "top", "props": {"columns": 4}},
                {"type": "Chart", "position": "center", "props": {"type": "line"}},
                {"type": "Table", "position": "bottom", "props": {"paginated": True}},
            ],
            "List": [
                {"type": "Navigation", "position": "top", "props": {"variant": "topbar"}},
                {"type": "SearchBar", "position": "top", "props": {}},
                {"type": "FilterPanel", "position": "left", "props": {}},
                {"type": "Card", "position": "center", "props": {"columns": 1, "list": True}},
                {"type": "Pagination", "position": "bottom", "props": {}},
            ],
            "Form": [
                {"type": "Navigation", "position": "top", "props": {"variant": "topbar"}},
                {"type": "Input", "position": "form", "props": {}},
                {"type": "Select", "position": "form", "props": {}},
                {"type": "Button", "position": "form", "props": {"variant": "primary"}},
            ],
            "Settings": [
                {"type": "Navigation", "position": "top", "props": {"variant": "sidebar"}},
                {"type": "Toggle", "position": "list", "props": {}},
                {"type": "Select", "position": "list", "props": {}},
            ],
        }
        return component_map.get(screen_name, [
            {"type": "Navigation", "position": "top", "props": {}},
            {"type": "Content", "position": "center", "props": {}},
        ])

    def _screen_interactions(self, screen_name: str) -> list[dict[str, Any]]:
        """Generate interaction definitions for a screen."""
        interaction_map = {
            "Home": [
                {"trigger": "click", "target": "cta-button", "action": "navigate", "destination": "Form"},
                {"trigger": "hover", "target": "card", "action": "elevate", "params": {"shadow": "md"}},
            ],
            "List": [
                {"trigger": "click", "target": "filter-toggle", "action": "toggle", "target_component": "FilterPanel"},
                {"trigger": "search", "target": "search-bar", "action": "filter", "params": {"debounce": "300ms"}},
            ],
            "Form": [
                {"trigger": "submit", "target": "form", "action": "validate", "then": "submit_api"},
                {"trigger": "blur", "target": "input", "action": "validate_field"},
            ],
            "Dashboard": [
                {"trigger": "click", "target": "metric-card", "action": "drill_down", "destination": "Detail"},
            ],
        }
        return interaction_map.get(screen_name, [
            {"trigger": "click", "target": "navigation-link", "action": "navigate"},
        ])

    def _generate_user_flows(
        self,
        research: UXResearchResult,
        screens: list[PrototypeScreen],
    ) -> list[dict[str, Any]]:
        """Generate user flows from research and screens."""
        flows: list[dict[str, Any]] = []
        screen_names = [s.name for s in screens]

        flow_templates = [
            {
                "name": "Onboarding Flow",
                "description": "Alur pengguna baru menuju aktivasi pertama",
                "start_screen": "Home",
                "steps": [
                    {"screen": "Home", "action": "click_signup"},
                    {"screen": "Form", "action": "fill_form"},
                    {"screen": "Dashboard", "action": "view_metrics"},
                ],
                "success_criteria": "User mencapai Dashboard dalam 3 menit",
            },
            {
                "name": "Task Completion Flow",
                "description": "Alur menyelesaikan tugas utama",
                "start_screen": "Dashboard",
                "steps": [
                    {"screen": "List", "action": "select_item"},
                    {"screen": "Detail", "action": "review"},
                    {"screen": "Form", "action": "submit_changes"},
                ],
                "success_criteria": "User menyelesaikan tugas dalam 5 langkah",
            },
        ]

        for template in flow_templates:
            flow = dict(template)
            flow["screens_involved"] = [s for s in screen_names if s in [step["screen"] for step in flow["steps"]]]
            flows.append(flow)

        return flows

    def _build_interaction_map(self, screens: list[PrototypeScreen]) -> dict[str, Any]:
        """Build global interaction map for the prototype."""
        return {
            "navigation": {
                "Home": ["Dashboard", "List", "Form", "Settings"],
                "Dashboard": ["Home", "List"],
                "List": ["Detail", "Form"],
                "Form": ["List", "Dashboard"],
                "Settings": ["Home"],
            },
            "gestures": [
                {"gesture": "swipe_left", "action": "next_item", "context": "List, Detail"},
                {"gesture": "swipe_right", "action": "previous_item", "context": "List, Detail"},
                {"gesture": "pull_to_refresh", "action": "refresh_data", "context": "List, Dashboard"},
            ],
            "keyboard_shortcuts": [
                {"key": "Ctrl+K", "action": "open_search", "context": "global"},
                {"key": "Ctrl+N", "action": "new_item", "context": "List, Dashboard"},
                {"key": "Escape", "action": "close_modal", "context": "Modal"},
            ],
            "screen_transitions": {
                "default": {"animation": "fade", "duration": "200ms"},
                "modal": {"animation": "slide_up", "duration": "300ms"},
                "navigation": {"animation": "slide_horizontal", "duration": "250ms"},
            },
        }

    def _build_notes(self, fidelity: str, platforms: list[str], screen_count: int) -> list[str]:
        """Build prototype notes."""
        notes = [
            f"Prototipe dengan tingkat kepercayaan {fidelity}",
            f"Target platform: {', '.join(platforms)}",
            f"Total {screen_count} layar yang dirancang",
            "Semua screen mengikuti design system yang didefinisikan",
            "Interaction map mencakup desktop dan mobile patterns",
        ]
        return notes

    def _estimate_effort(self, fidelity: str, screen_count: int, flow_count: int) -> str:
        """Estimate implementation effort."""
        base = {"low": "1-2 minggu", "medium": "3-5 minggu", "high": "6-10 minggu"}
        effort = base.get(fidelity, "3-5 minggu")
        if screen_count > 8:
            effort = f"{int(screen_count // 3)}-{int(screen_count // 2)} minggu"
        return effort
