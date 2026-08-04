"""
UI/UX Designer — Design System Module.

Builds and manages design systems:
- Design token generation
- Color palette generation
- Typography scale definition
- Spacing scale
- Component specification generation
- Design system validation
"""

from __future__ import annotations

import logging
from typing import Any

from apps.ui_ux_designer.schemas import (
    DesignSystem,
    DesignToken,
    ComponentSpec,
    BusinessContext,
    StakeholderInput,
    QualityAttributes,
)

logger = logging.getLogger(__name__)


class DesignSystemBuilder:
    """
    Builds and manages design systems.

    Generates design tokens, color palettes, typography scales,
    and component specifications from product requirements.
    """

    def __init__(self) -> None:
        self._color_bases = {
            "primary": ["#2563EB", "#1D4ED8", "#1E40AF"],
            "secondary": ["#7C3AED", "#6D28D9", "#5B21B6"],
            "success": ["#059669", "#047857", "#065F46"],
            "warning": ["#D97706", "#B45309", "#92400E"],
            "danger": ["#DC2626", "#B91C1C", "#991B1B"],
            "neutral": ["#6B7280", "#4B5563", "#374151", "#1F2937", "#111827"],
        }
        self._typography_scale = [
            {"name": "xs", "size": "0.75rem", "line_height": "1rem", "weight": "400"},
            {"name": "sm", "size": "0.875rem", "line_height": "1.25rem", "weight": "400"},
            {"name": "base", "size": "1rem", "line_height": "1.5rem", "weight": "400"},
            {"name": "lg", "size": "1.125rem", "line_height": "1.75rem", "weight": "500"},
            {"name": "xl", "size": "1.25rem", "line_height": "1.75rem", "weight": "600"},
            {"name": "2xl", "size": "1.5rem", "line_height": "2rem", "weight": "700"},
            {"name": "3xl", "size": "1.875rem", "line_height": "2.25rem", "weight": "700"},
            {"name": "4xl", "size": "2.25rem", "line_height": "2.5rem", "weight": "800"},
        ]
        self._spacing_scale = ["0", "4px", "8px", "12px", "16px", "24px", "32px", "48px", "64px", "96px"]

    def build(
        self,
        inputs: StakeholderInput,
        context: BusinessContext,
        quality_attrs: QualityAttributes,
        target_platforms: list[str],
    ) -> DesignSystem:
        """
        Build a design system from inputs.

        Args:
            inputs: Stakeholder input
            context: Business context
            quality_attrs: Quality attributes
            target_platforms: Target platforms

        Returns:
            DesignSystem with tokens and component specs
        """
        tokens = self._generate_tokens(context, quality_attrs)
        components = self._generate_components(target_platforms)
        color_palette = self._build_color_palette()
        typography_scale = {t["name"]: t for t in self._typography_scale}
        motion_principles = self._build_motion_principles()

        system_name = context.project_name or f"Design System — {context.domain}"

        return DesignSystem(
            name=system_name,
            description=f"Sistem desain untuk {context.project_name} di domain {context.domain}",
            tokens=tokens,
            components=components,
            color_palette=color_palette,
            typography_scale=typography_scale,
            spacing_scale=self._spacing_scale,
            motion_principles=motion_principles,
            accessibility_standards=["WCAG 2.1 AA"],
            version="1.0.0",
        )

    def _generate_tokens(
        self,
        context: BusinessContext,
        quality_attrs: QualityAttributes,
    ) -> list[DesignToken]:
        """Generate design tokens from context."""
        tokens: list[DesignToken] = []

        for category, colors in self._color_bases.items():
            for i, color in enumerate(colors):
                tokens.append(
                    DesignToken(
                        name=f"{category}-{i+1 if i > 0 else 'base'}",
                        type="color",
                        value=color,
                        description=f"Warna {category} level {i+1}",
                        usage=f"Elemen {category} seperti tombol, link, highlight",
                    )
                )

        for t in self._typography_scale:
            tokens.append(
                DesignToken(
                    name=f"font-{t['name']}",
                    type="typography",
                    value=f"{t['size']}/{t['line_height']} {t['weight']}",
                    description=f"Ukuran font {t['name']}",
                    usage=f"Teks {t['name']} pada layout",
                )
            )

        for spacing in self._spacing_scale:
            tokens.append(
                DesignToken(
                    name=f"spacing-{spacing if spacing != '0' else 'none'}",
                    type="spacing",
                    value=spacing,
                    description=f"Spasi {spacing}",
                    usage="Margin, padding, gap",
                )
            )

        tokens.append(
            DesignToken(
                name="shadow-sm",
                type="shadow",
                value="0 1px 2px 0 rgb(0 0 0 / 0.05)",
                description="Bayangan kecil",
                usage="Card, dropdown",
            )
        )
        tokens.append(
            DesignToken(
                name="shadow-md",
                type="shadow",
                value="0 4px 6px -1px rgb(0 0 0 / 0.1)",
                description="Bayangan medium",
                usage="Modal, drawer",
            )
        )

        return tokens

    def _generate_components(self, target_platforms: list[str]) -> list[ComponentSpec]:
        """Generate component specifications."""
        base_components = [
            ComponentSpec(
                name="Button",
                component_type="button",
                description="Tombol aksi utama dan sekunder",
                props_schema={
                    "type": "object",
                    "properties": {
                        "label": {"type": "string"},
                        "variant": {"type": "string", "enum": ["primary", "secondary", "ghost", "danger"]},
                        "size": {"type": "string", "enum": ["sm", "md", "lg"]},
                        "disabled": {"type": "boolean"},
                    },
                    "required": ["label"],
                },
                accessibility_requirements=[
                    "WCAG 2.1 AA — Kontras warna minimal 4.5:1",
                    "Fokus terlihat dengan ring indicator",
                    "Label aksesibel via aria-label jika icon-only",
                ],
                variants=["primary", "secondary", "ghost", "danger"],
                responsive_behavior="Ukuran responsif via prop size",
            ),
            ComponentSpec(
                name="Input",
                component_type="input",
                description="Kolom input teks dengan label dan validasi",
                props_schema={
                    "type": "object",
                    "properties": {
                        "label": {"type": "string"},
                        "placeholder": {"type": "string"},
                        "error": {"type": "string"},
                        "disabled": {"type": "boolean"},
                        "required": {"type": "boolean"},
                    },
                    "required": ["label"],
                },
                accessibility_requirements=[
                    "Label terasosiasi via htmlFor/id",
                    "Error diumumkan via aria-describedby",
                    "Required diindikasikan via aria-required",
                ],
                variants=["default", "error", "disabled"],
                responsive_behavior="Full width pada mobile, max-width pada desktop",
            ),
            ComponentSpec(
                name="Card",
                component_type="card",
                description="Kontainer konten dengan header, body, dan footer opsional",
                props_schema={
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "elevation": {"type": "string", "enum": ["sm", "md", "lg"]},
                        "padding": {"type": "string"},
                    },
                },
                accessibility_requirements=[
                    "Card memiliki role yang sesuai jika interaktif",
                    "Heading hierarki terjaga (h2 atau h3)",
                ],
                variants=["elevated", "outlined", "filled"],
                responsive_behavior="Padding responsif per breakpoint",
            ),
            ComponentSpec(
                name="Modal",
                component_type="modal",
                description="Dialog overlay untuk konfirmasi dan form",
                props_schema={
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "open": {"type": "boolean"},
                        "on_close": {"type": "function"},
                        "size": {"type": "string", "enum": ["sm", "md", "lg", "xl"]},
                    },
                    "required": ["title", "open"],
                },
                accessibility_requirements=[
                    "Focus trap di dalam modal",
                    "Escape menutup modal",
                    "aria-modal=true dan role=dialog",
                    "Focus restore ke trigger saat close",
                ],
                variants=["sm", "md", "lg", "xl"],
                responsive_behavior="Full width pada mobile, fixed width pada desktop",
            ),
            ComponentSpec(
                name="Navigation",
                component_type="nav",
                description="Menu navigasi utama dengan responsive hamburger",
                props_schema={
                    "type": "object",
                    "properties": {
                        "items": {"type": "array"},
                        "brand": {"type": "string"},
                        "variant": {"type": "string", "enum": ["sidebar", "topbar", "bottom"]},
                    },
                },
                accessibility_requirements=[
                    "nav dengan aria-label",
                    "Current page diindikasikan via aria-current",
                    "Menu toggle dengan aria-expanded",
                ],
                variants=["sidebar", "topbar", "bottom"],
                responsive_behavior="Hamburger menu pada mobile < 768px",
            ),
        ]

        if "mobile" in target_platforms:
            base_components.append(
                ComponentSpec(
                    name="BottomSheet",
                    component_type="bottomsheet",
                    description="Sheet yang naik dari bawah untuk mobile",
                    props_schema={
                        "type": "object",
                        "properties": {
                            "open": {"type": "boolean"},
                            "snap_points": {"type": "array", "items": {"type": "string"}},
                        },
                    },
                    accessibility_requirements=[
                        "Dismiss via swipe dan Escape",
                        "Focus management saat open/close",
                    ],
                    variants=["half", "full", "custom"],
                    responsive_behavior="Mobile-only, hidden pada desktop",
                )
            )

        return base_components

    def _build_color_palette(self) -> dict[str, str]:
        """Build color palette dictionary."""
        palette: dict[str, str] = {}
        for category, colors in self._color_bases.items():
            palette[f"{category}-50" if len(colors) > 1 else category] = colors[0]
            palette[f"{category}-500" if len(colors) > 2 else category] = colors[len(colors) // 2]
            palette[f"{category}-900" if len(colors) > 2 else category] = colors[-1]
        return palette

    def _build_motion_principles(self) -> list[str]:
        """Build motion design principles."""
        return [
            "Transisi durasi 150-300ms untuk interaksi UI",
            "Easing: cubic-bezier(0.4, 0, 0.2, 1) untuk transisi default",
            "Durasi 300-500ms untuk perubahan layout yang signifikan",
            "Animasi tidak mengganggu aksesibilitas (prefers-reduced-motion)",
            "Stagger animation untuk list items (50ms delay per item)",
        ]
