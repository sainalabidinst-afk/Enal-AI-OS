# UI/UX Designer — Spesifikasi Capability

**Versi:** 1.0.0
**Status:** Experimental (RFC-0018)
**Target Kualitas:** A- (≥85)

---

## 1. Tujuan

UI/UX Designer adalah **otoritas desain pengalaman pengguna** untuk ECP — Capability Pack yang menerjemahkan kebutuhan pengguna menjadi spesifikasi desain yang jelas, terstruktur, dan dapat dieksekusi oleh Capability Pack lain.

Capability Pack ini menganalisis riset UX, membangun sistem desain, menghasilkan spesifikasi prototype, dan mengaudit aksesibilitas — **tanpa memodifikasi Core**.

---

## 2. Ruang Lingkup

### Dalam Ruang Lingkup
- **UX Research** — Analisis data riset menjadi persona, user journeys, pain points, opportunities
- **Design System** — Pembangunan sistem desain dengan token, palette, tipografi, spacing, components
- **Prototyping** — Generasi spesifikasi prototype dengan screen layouts, interaction maps, user flows
- **Accessibility Audit** — Audit kepatuhan WCAG 2.1 AA dengan deteksi pelanggaran dan prioritas remediasi
- **Experience Memory** — Merekam hasil ke riwayat

### Di Luar Cakupan
- Fasilitasi wawancara atau survei pengguna
- Eksekusi implementasi kode UI produksi
- Desain visual polos (icon, ilustrasi)
- Pengganti alat desain khusus (Figma, Sketch)
- Manajemen proyek desain
- Modifikasi kontrak Core

---

## 3. Kontrak

### Input: UIUXDesignerRequest
```json
{
  "request_id": "uuid",
  "operation": "ux_research | design_system | prototyping | accessibility_audit | full_design",
  "business_context": {
    "domain": "e-commerce | fintech | healthcare",
    "project_name": "string",
    "description": "string — project overview"
  },
  "inputs": {
    "user_research_data": ["string — raw UX research notes"],
    "product_requirements": ["string — product requirement statements"],
    "current_design": "string — current design documentation",
    "technical_constraints": ["string"],
    "business_goals": ["string"]
  },
  "personas": [
    {
      "name": "string",
      "role": "string",
      "goals": ["string"],
      "pain_points": ["string"],
      "technical_proficiency": "low|medium|high"
    }
  ],
  "quality_attributes": {
    "accessibility_target": "WCAG 2.1 AA",
    "performance_target": "< 100ms interaction",
    "consistency_target": "100% design system compliance"
  },
  "output_format": "json | markdown | figma | html | css | json_schema",
  "target_platforms": ["web|mobile|desktop|tablet"]
}
```

### Output: Laporan Desain UI/UX
```json
{
  "request_id": "uuid",
  "operation": "string",
  "ux_research": {
    "user_personas": [
      {
        "name": "string",
        "role": "string",
        "goals": ["string"],
        "pain_points": ["string"],
        "technical_proficiency": "low|medium|high"
      }
    ],
    "user_journeys": [
      {
        "persona": "string",
        "stages": [
          {
            "stage": "string",
            "actions": ["string"],
            "touchpoints": ["string"],
            "pain_points": ["string"],
            "opportunities": ["string"]
          }
        ]
      }
    ],
    "key_findings": ["string"],
    "pain_points": ["string"],
    "opportunities": ["string"],
    "usability_issues": ["string"],
    "research_confidence": 0.85
  },
  "design_system": {
    "id": "string",
    "name": "string",
    "tokens": [
      {
        "name": "string",
        "type": "color|typography|spacing|shadow|border|motion",
        "value": "string",
        "description": "string",
        "usage": "string"
      }
    ],
    "components": [
      {
        "id": "string",
        "name": "string",
        "component_type": "button|input|card|modal|nav|form",
        "props_schema": {},
        "accessibility_requirements": ["string"],
        "variants": ["string"],
        "responsive_behavior": "string"
      }
    ],
    "color_palette": {},
    "typography_scale": {},
    "spacing_scale": ["string"],
    "motion_principles": ["string"],
    "accessibility_standards": ["WCAG 2.1 AA"],
    "version": "1.0.0"
  },
  "prototype": {
    "id": "string",
    "name": "string",
    "fidelity": "low|medium|high",
    "screens": [
      {
        "id": "string",
        "name": "string",
        "layout": {},
        "components": [{"type": "string", "position": "string", "props": {}}],
        "interactions": [{"trigger": "string", "target": "string", "action": "string"}],
        "states": ["default|hover|focus|disabled|error"],
        "responsive_breakpoints": ["320px", "768px", "1024px", "1440px"]
      }
    ],
    "user_flows": [
      {
        "name": "string",
        "start_screen": "string",
        "steps": [{"screen": "string", "action": "string"}],
        "success_criteria": "string"
      }
    ],
    "interaction_map": {
      "navigation": {},
      "gestures": [],
      "keyboard_shortcuts": [],
      "screen_transitions": {}
    }
  },
  "accessibility_report": {
    "total_checks": 0,
    "violations_found": 0,
    "compliance_score": 0.85,
    "violations": [
      {
        "id": "string",
        "wcag_criterion": "1.4.3",
        "severity": "low|medium|high|critical",
        "description": "string",
        "element_selector": "string",
        "recommendation": "string",
        "impact": "string"
      }
    ],
    "passed_checks": ["string"],
    "remediation_priority": ["string"],
    "wcag_level": "AA"
  },
  "quality_score": 0.85,
  "explanation": "string — human-readable design summary"
}
```

---

## 4. Operasi

| Operasi | Deskripsi | Input | Output |
|-----------|-------------|--------|---------|
| `ux_research` | Analisis riset UX menjadi insights | user_research_data, personas | UXResearchResult |
| `design_system` | Bangun sistem desain | requirements, quality_attributes | DesignSystem |
| `prototyping` | Hasilkan spesifikasi prototype | research, design_system, target_platforms | Prototype |
| `accessibility_audit` | Audit kepatuhan WCAG 2.1 AA | design_system, prototype | AccessibilityReport |
| `full_design` | Pipeline desain lengkap | semua inputs | UIUXDesignerReport |

---

## 5. Modul Analyzer

| Modul | Tanggung Jawab |
|--------|----------------|
| `ux_researcher.py` | Analisis riset UX menjadi persona, journeys, pain points, opportunities |
| `design_system.py` | Pembangunan sistem desain (tokens, palette, typography, components) |
| `prototype_generator.py` | Generasi spesifikasi prototype (screens, flows, interactions) |
| `accessibility_checker.py` | Audit kepatuhan WCAG 2.1 AA (contrast, keyboard, ARIA) |

---

## 6. Dimensi Benchmark

| Dimensi | Target | Grade |
|-----------|--------|-------|
| UX Research Quality | ≥85% | A- |
| Design System Completeness | ≥90% | A |
| Prototype Completeness | ≥85% | A- |
| Accessibility Compliance | ≥85% | A- |
| Design Consistency | ≥90% | A |
| Explainability | ≥90% | A |
| Consistency | ≥85% | A- |

---

## 7. Dependensi

- **apps/base.py** — Definisi model dasar
- **apps/ui_ux_designer/schemas.py** — Kontrak publik
- **apps/ui_ux_designer/engine.py** — Domain engine
- **apps/ui_ux_designer/worker.py** — Adaptor tipis (ADR-003)

---

## 8. Contoh Penggunaan

```python
from apps.ui_ux_designer.engine import UIUXDesignerEngine
from apps.ui_ux_designer.schemas import UIUXDesignerRequest, OperationType

engine = UIUXDesignerEngine()
request = UIUXDesignerRequest(
    operation=OperationType.full_design,
    business_context={"domain": "e-commerce", "project_name": "TokoOnline"},
    inputs={"product_requirements": ["Users must checkout in 3 steps"]},
    personas=[{"name": "Rina", "role": "Customer", "goals": ["Fast checkout"], "pain_points": ["Complex forms"]}],
)
report = engine.design(request)
print(f"Personas: {len(report.ux_research.user_personas)}")
print(f"Design tokens: {len(report.design_system.tokens)}")
print(f"Screens: {len(report.prototype.screens)}")
print(f"Accessibility score: {report.accessibility_report.compliance_score:.0%}")
print(f"Quality score: {report.quality_score:.0%}")
```
