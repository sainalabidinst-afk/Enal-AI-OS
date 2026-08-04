# Product Manager — Spesifikasi Capability

**Versi:** 1.0.0
**Status:** Production Ready (RFC-0017)
**Target Kualitas:** A- (≥85)

---

## 1. Tujuan

Product Manager adalah **otoritas manajemen produk** untuk ECP — Capability Pack yang menerjemahkan visi strategis menjadi roadmap yang dapat dieksekusi, backlog yang terstruktur, dan metrik keberhasilan yang terukur.

Capability Pack ini mengelola roadmap, backlog, sprint, OKR/KPI, prioritas, dan koordinasi rilis — **tanpa memodifikasi Core**.

---

## 2. Ruang Lingkup

### Dalam Ruang Lingkup
- **Product Vision Translation** — Menerjemahkan visi menjadi roadmap yang dapat dieksekusi
- **Roadmap Management** — Membuat dan memelihara roadmap produk dengan milestone dan rilis
- **Backlog Management** — Mengelola backlog dengan prioritas yang jelas
- **Sprint Planning** — Merencanakan sprint dengan kapasitas dan estimasi
- **OKR/KPI Tracking** — Menetapkan dan melacak OKR dan KPI
- **Prioritization** — Menerapkan framework prioritas yang konsisten
- **Release Coordination** — Mengoordinasikan rilis dengan dependensi lintas paket
- **Experience Memory** — Merekam hasil ke riwayat

### Di Luar Cakupan
- Eksekusi teknis
- Manajemen sumber daya manusia
- Penjualan dan pemasaran
- Modifikasi kontrak Core

---

## 3. Kontrak

### Input: ProductManagementRequest
```json
{
  "request_id": "uuid",
  "operation": "roadmap_management | backlog_management | sprint_planning | okr_tracking | prioritization | release_coordination",
  "product_context": {
    "product_name": "string",
    "vision": "string",
    "strategy": "string",
    "target_users": ["string"]
  },
  "inputs": {
    "backlog_items": [
      {
        "id": "string",
        "title": "string",
        "description": "string",
        "effort": "string",
        "value": "string",
        "dependencies": ["string"]
      }
    ],
    "roadmap_items": [
      {
        "id": "string",
        "title": "string",
        "target_date": "string",
        "status": "string"
      }
    ],
    "okrs": [
      {
        "id": "string",
        "objective": "string",
        "key_results": [
          {
            "description": "string",
            "target": "string",
            "current": "string"
          }
        ]
      }
    ]
  },
  "constraints": {
    "team_capacity": "string",
    "budget": "string",
    "timeline": "string"
  },
  "options": {
    "prioritization_framework": "rice | moscow | value_effort | custom",
    "sprint_duration_weeks": 2
  }
}
```

### Output: Laporan Manajemen Produk
```json
{
  "request_id": "uuid",
  "operation": "string",
  "roadmap": {
    "version": "string",
    "milestones": [
      {
        "id": "string",
        "title": "string",
        "target_date": "string",
        "status": "string",
        "dependencies": ["string"]
      }
    ],
    "releases": [
      {
        "id": "string",
        "name": "string",
        "target_date": "string",
        "scope": ["string"]
      }
    ]
  },
  "backlog": {
    "items": [
      {
        "id": "string",
        "title": "string",
        "priority": "high | medium | low",
        "effort": "string",
        "value": "string",
        "score": 0.0,
        "rationale": "string"
      }
    ],
    "summary": {
      "total_items": 0,
      "high_priority": 0,
      "medium_priority": 0,
      "low_priority": 0
    }
  },
  "sprint_plan": {
    "sprint_id": "string",
    "duration_weeks": 2,
    "capacity": "string",
    "committed_items": ["string"],
    "stretch_items": ["string"],
    "goal": "string"
  },
  "okrs": {
    "quarter": "string",
    "objectives": [
      {
        "id": "string",
        "objective": "string",
        "key_results": [
          {
            "description": "string",
            "target": "string",
            "current": "string",
            "progress": 0.0
          }
        ],
        "overall_progress": 0.0,
        "confidence": "string"
      }
    ]
  },
  "prioritization": {
    "framework": "string",
    "ranked_items": [
      {
        "id": "string",
        "rank": 0,
        "score": 0.0,
        "rationale": "string"
      }
    ],
    "top_5": ["string"]
  },
  "release_plan": {
    "releases": [
      {
        "id": "string",
        "name": "string",
        "target_date": "string",
        "scope": ["string"],
        "dependencies": ["string"],
        "risks": ["string"]
      }
    ]
  },
  "quality_score": 0.85,
  "explanation": "string — human-readable summary"
}
```

---

## 4. Operasi

| Operasi | Deskripsi | Input | Output |
|-----------|-------------|--------|---------|
| `roadmap_management` | Membuat dan memelihara roadmap produk | visi, strategi, input stakeholder | Roadmap dengan milestone dan rilis |
| `backlog_management` | Mengelola backlog dengan prioritas | item backlog, estimasi, dependensi | Backlog terstruktur dengan prioritas |
| `sprint_planning` | Merencanakan sprint | backlog, kapasitas tim, dependensi | Rencana sprint dengan item dan estimasi |
| `okr_tracking` | Menetapkan dan melacak OKR/KPI | tujuan strategis, metrik, target | OKR/KPI yang dilacak dengan kemajuan |
| `prioritization` | Menerapkan framework prioritas | item backlog, kriteria, data | Daftar prioritas dengan justifikasi |
| `release_coordination` | Mengoordinasikan rilis | roadmap, backlog, dependensi lintas paket | Rencana rilis dengan dependensi yang terkelola |

---

## 5. Modul Analyzer

| Modul | Tanggung Jawab |
|--------|----------------|
| `roadmap_manager.py` | Membuat dan memelihara roadmap produk |
| `backlog_manager.py` | Mengelola backlog dan perencanaan sprint |
| `okr_tracker.py` | Menetapkan dan melacak OKR dan KPI |
| `prioritizer.py` | Menerapkan framework prioritas yang konsisten |

---

## 6. Dimensi Benchmark

| Dimensi | Target | Grade |
|-----------|--------|-------|
| Roadmap Accuracy | ≥85% | A- |
| Backlog Quality | ≥90% | A |
| OKR Achievement | ≥90% | A |
| Priority Consistency | ≥85% | A- |
| Release Adherence | ≥90% | A |
| Stakeholder Alignment | ≥85% | A- |
| Explainability | ≥85% | A- |

---

## 7. Dependensi

- **apps/base.py** — Definisi model dasar
- **apps/product_manager/schemas.py** — Kontrak publik
- **apps/product_manager/engine.py** — Domain engine
- **apps/product_manager/worker.py** — Adaptor tipis (ADR-003)

---

## 8. Contoh Penggunaan

```python
from apps.product_manager.engine import ProductManagerEngine
from apps.product_manager.schemas import ProductManagementRequest, OperationType

engine = ProductManagerEngine()
request = ProductManagementRequest(
    operation=OperationType.backlog_management,
    product_context={"product_name": "ECP Platform", "vision": "AI-powered development platform"},
    inputs={"backlog_items": [{"id": "BL-001", "title": "Add user authentication", "effort": "medium", "value": "high"}]},
    options={"prioritization_framework": "rice"},
)
report = engine.manage(request)
print(f"Prioritized {len(report.backlog['items'])} backlog items")
print(f"Top priority: {report.backlog['items'][0]['title']}")
```
