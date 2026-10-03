# RFC-0025: Self-Correction & Adversarial Testing Agent

|Bidang|Nilai|
|-------|-------|
|**ID RFC**|RFC-0025|
|**Status**|Draft|
|**Versi**|0.1.0|
|**Penulis**|Tim Inti AI OS Akhir|
|**Target Rilis**|v2.1.0 (Fase Keunggulan Kemampuan +)|
|**Capability Pack**|Adversarial Testing|
|**ID Kemampuan**|`adversarial-testing`|
|**Kategori**|Pengujian / Cognitive|
|**Target Kualitas**|A+ (≥95)
|**Target Kematangan**|Level 4 — Domain Expert (L4)|
|**Referensi RFC**|RFC-0025; berelasi dengan RFC-0007 (Decision Intelligence), RFC-0002 (Code Engineer)|

---

## Ringkasan

Capability Pack Adversarial Testing ("Devil's Advocate") adalah agen khusus yang tugasnya selalu mencari kelemahan dari rencana atau hasil yang dihasilkan oleh Agen utama (misalnya AIOrchestrator / Decision Intelligence Engine). Ketika sebuah Capability Pack selesai merencanakan sesuatu, agen ini menyerang rencananya dengan asumsi terburuk dan memaksa rencana yang dihasilkan untuk "lolos uji" sebelum dianggap siap.

---

## Motivasi

Meskipun ada Reflection (`reflection.py`) dan Debate Engine (`debate_engine.py`), kita butuh lapisan pengujian yang lebih agresif — seperti lawan bicara yang iseng.

- **Reflection** (`self_reflection.py`): Meninjau kualitas output secara umum, fokus pada structure dan completeness
- **Debate Engine** (`apps/decision_intelligence/debate_engine.py`): Membandingkan alternatif melalui strategi berbeda
- **Self-Verification** (`self_verification.py`): Verifikasi teknis (compile, lint, test, security scan) untuk code artifacts

Yang **tidak ada**: Agen yang secara eksplisit berperan sebagai "Devil's Advocate" — mencari skenario kegagalan terburuk, mengidentifikasi asumsi rentan, dan memaksa hardening sebelum rencana diterima.

Tanpa lapisan ini, output ECP dapat menjadi **toleransi terhadap kegagalan yang tidak teridentifikasi** — rencana yang tampak baik secara logika tetapi rapuh terhadap shock eksternal.

---

## Pernyataan Masalah

| Aspek | Keterbatasan Saat Ini | Dampak |
|-------|---------------------|--------|
| Adversarial testing | Hanya ada reflection + verification | Skenario kegagalan tidak teridentifikasi secara sistematis |
| Failure injection | Tidak ada | Rencana tidak diuji terhadap shock eksternal |
| Assumption analysis | Manual | Asumsi tersembunyi tidak terdeteksi |
| Hardening recommendation | Reactive (hanya setelah kegagakan) | Output rentan terhadap edge cases |
| Worst-case analysis | Limited (hanya risk score dari risk_analyzer) | Rencana tidak "anti-fragile" |

---

## Tujuan

1. **Attack Vector Generation** — Menghasilkan skenario serangan yang beragam (worst-case assumptions)
2. **Failure Injection** — Menyuntikkan kegagalan ke dalam rencana simulasi
3. **Assumption Auditing** — Mengidentifikasi dan menguji asumsi tersembunyi
4. **Vulnerability Scoring** — Memberi skor kerentanan pada setiap rencana
5. **Hardening Recommendation** — Memberi rekomendasi untuk mengampruh rencana
6. **Pass/Fail Gate** — Rencana harus lolos uji adversarial sebelum siap

### Kriteria Keberhasilan

| Metrik | Target | Nilai |
|--------|--------|-------|
| Attack coverage | Skenario serangan yang beragam | 10+ attack vector |
| Vulnerability detection | Kerentanan yang teridentifikasi | ≥90% dari serangan yang diketahui |
| Hardening effectiveness | Rekomendasi mengurangi kerentanan | ≥80% reducti |
| False positive rate | Serangan yang tidak valid | < 5% |
| Pass rate | Rencana yang lolos setelah hardening | ≥95% |
| Explainability | Jejak serangan dan rekomendasi | ≥95% |

---

## Non-Tujuan

1. **Eksekusi produksi** — Hanya pengujian dan rekomendasi; eksekusi memerlukan persetujuan (ADR-005)
2. **Mengganti Reflection** — Bekerja sama dengan Reflection, bukan menggantikannya
3. **Security penetration testing** — Fokus pada kegagalan logis/strategis, bukan exploit teknis
4. **Modifikasi Core** — Semua implementasi di dalam Capability Pack

---

## Ruang Lingkup Kapabilitas

### Kapabilitas Inti

| Kapabilitas | Deskripsi | Masukan | Keluaran |
|-------------|-----------|---------|---------|
| Attack Vector Generator | Menghasilkan skenario serangan adversarial | Plan/strategy, context | AttackVectors |
| Failure Injector | Menyuntikkan kegagalan ke dalam simulasi | AttackVectors, plan | FailureScenarios |
| Assumption Auditor | Mengidentifikasi asumsi tersembunyi | Plan, evidence | Assumptions |
| Vulnerability Scanner | Menilai kerentanan terhadap serangan | FailureScenarios, plan | VulnerabilityReport |
| Hardening Advisor | Memberi rekomendasi penguatan | VulnerabilityReport | HardeningActions |
| Adversarial Gate | Gate pass/fail berdasarkan hasil uji | HardeningActions, vulnerabilities | GateResult |

---

## Kontrak Publik

### Kontrak Masukan: AdversarialTestRequest

```json
{
  "request_id": "uuid",
  "subject": "string — the plan, strategy, or analysis to attack",
  "subject_type": "plan | recommendation | architecture | code_patch | strategy",
  "context": "string — additional context",
  "evidence": {},
  "constraints": ["string — hard constraints (what should NOT be violated)"],
  "attack_budget": 10,
  "attack_categories": ["external_shock", "dependency_failure", "resource_exhaustion",
                        "competitive_response", "regulatory_change", "data_corruption"],
  "existing_hardening": ["string — already-applied mitigations"]
}
```

### Kontrak Keluaran: AdversarialTestResult

```json
{
  "request_id": "uuid",
  "subject": "string",
  "attack_vectors": [
    {"id": "string", "category": "string", "description": "string", "severity": "low|medium|high|critical"}
  ],
  "vulnerabilities_found": [
    {
      "attack_id": "string",
      "vulnerability": "string",
      "impact": "string",
      "severity": "low|medium|high|critical",
      "exploitable": true
    }
  ],
  "hardening_recommendations": [
    {"attack_id": "string", "recommendation": "string", "priority": "low|medium|high|critical"}
  ],
  "gate_result": "pass | fail",
  "pass_score": 0.0,
  "confidence": 0.0,
  "explanation_chain": {
    "assumptions_audited": ["string"],
    "attacks_survived": ["string"],
    "attacks_failed": ["string"],
    "final_hardening_summary": "string"
  }
}
```

---

## Titik Integrasi

### Integrasi dengan Cognitive Pipeline

Adversarial Testing dapat dipanggil setelah `simulation` dan sebelum `decision` dalam pipeline COMPLEX/Very_COMPLEX:

```
COMPLEX: perception → memory → planning → reasoning → simulation →
         adversarial_testing → debate → decision → verification →
         reflection → action → learning
```

### Integrasi dengan Capability Pack Konsumen

Ketika Capability Pack lain menyelesaai perencanaan, mereka dapat mengirimkan hasilnya ke Adversarial Testing untuk gate:

```python
# Via Execution Runtime task (ADR-002)
task = {
    "domain": "adversarial_testing",
    "intent": "Adversarial test this plan: [plan]",
    "payload": {"subject": plan, "subject_type": "plan", ...}
}
result = await execution_runtime.execute(task)
if result["gate_result"] == "fail":
    # Plan needs hardening before proceeding
```

### Integrasi dengan Scenario Simulator (RFC-0023)

Adversarial Testing menggunakan Scenario Simulator untuk mensimulasikan skenario kegagalan:

```
AdversarialTestRequest
    ↓
Attack Vector Generator (generates worst-case scenarios)
    ↓
Scenario Simulator (runs Monte Carlo on each attack)
    ↓
Vulnerability Assessment
    ↓
Hardening Recommendations
```

---

## Ketergantungan

### Dependensi Internal (Kontrak Bersama)

1. **Execution Runtime** — Task routing (ADR-002)
2. **Scenario Simulator** (RFC-0023) — Monte Carlo failure simulation
3. **Decision Intelligence** — Risk scoring and confidence
4. **Model Router** — LLM untuk attack vector generation dan assumption auditing
5. **Experience Memory** — Learning from past attacks dan kegagalan

### Tidak Ada Perubahan Inti yang Diperlukan

```text
apps/
└── adversarial_testing/
    ├── __init__.py              # App class + factory
    ├── engine.py                # Domain Engine
    ├── worker.py                # Thin adapter
    ├── schemas.py               # Public contracts
    ├── attack_vector_generator.py   # Generates adversarial scenarios
    ├── failure_injector.py      # Injects failures into plans
    ├── assumption_auditor.py    # Identifies hidden assumptions
    ├── vulnerability_scanner.py # Scores vulnerabilities
    ├── hardening_advisor.py     # Recommends mitigations
    └── adversarial_gate.py      # Pass/fail gate logic
```

**Dampak ADR:** Tidak ada. Capability Pack baru, tidak memodifikasi Core.

---

## Spesifikasi Benchmark

| Dimensi | Definisi | Target |
|---------|----------|--------|
| Attack Coverage | Jumlah kategori serangan yang didukung | 6+ kategori |
| Vulnerability Detection | Serangan yang valid terdeteksi | ≥90% |
| Hardening Effectiveness | Reduksi kerentanan setelah hardening | ≥80% |
| False Positive Rate | Serangan yang tidak valid | < 5% |
| Pass Rate | Rencana yang lolos setelah hardening | ≥95% |
| Explainability | Jejak serangan dan rekomendasi | ≥95% |

---

## Definisi Selesai

```text
Definition of Done — Adversarial Testing Capability Pack

Functional
- [x] Attack Vector Generator: 6+ attack categories
- [x] Failure Injector: scenario-based failure simulation
- [x] Assumption Auditor: hidden assumption detection
- [x] Vulnerability Scanner: severity-scored vulnerability report
- [x] Hardening Advisor: prioritized mitigation recommendations
- [x] Adversarial Gate: pass/fail decision with confidence

Benchmark
- [x] Attack coverage: 6+ categories
- [x] Vulnerability detection ≥ 90%
- [x] Hardening effectiveness ≥ 80%
- [x] False positive rate < 5%
- [x] Pass rate ≥ 95%

Golden Tests
- [x] 10 skenario golden test lulus pada ≥90%
- [x] External shock scenario (competitor price war)
- [x] Dependency failure (payment system down)
- [x] Resource exhaustion (budget overrun)
- [x] Competitive response (new entrant)
- [x] Regulatory change (compliance shift)
- [x] Data corruption scenario
- [x] Assumption audit on trading strategy
- [x] Hardening recommendation verification
- [x] Gate pass/fail logic
- [x] Multi-attack vector on single plan

Real Cases
- [x] ≥5 real cases in real_cases/adversarial_testing/
- [x] Cases from Trading Analyst, Network Engineer, Decision Intelligence

Documentation
- [x] docs/capabilities/adversarial-testing.md
- [x] API reference / contract
- [x] Integration guide
```

---

## Linimana

### Fase 1: Prototipe (RFC → Eksperimental)

**Durasi:** 3 minggu

- [x] Struktur paket `apps/adversarial_testing/`
- [x] Attack Vector Generator (3 kategori serangan)
- [x] Failure Injector (basic injection)
- [x] Vulnerability Scanner (severity scoring)
- [x] Hardening Advisor (basic recommendations)
- [x] Adversarial Gate (pass/fail)
- [x] 5 skenario golden test dasar
- [x] **Gerbang:** 5/5 golden test lulus ≥80%

### Fase 2: Kapabilitas Lengkap (Eksperimental → Stabil)

**Durasi:** 4 minggu

- [x] Semua 6 kategori serangan
- [x] Assumption Auditor
- [ ] Integrasi dengan Scenario Simulator (RFC-0023)
- [ ] Integrasi dengan Decision Intelligence
- [x] 10 skenario golden test lengkap
- [ ] ≥10 real cases
- [x] **Gerbang:** Semua golden test lulus ≥90%; Benchmark ≥90%

### Fase 3: Ekosistem (Stabil → Bersertifikat)

**Durasi:** 6 minggu

- [ ] Integration dengan semua Capability Pack utama
- [ ] Event-driven: otomatis menguji rencana yang baru selesai
- [ ] Learning dari Attack Database (Experience Memory)
- [ ] UI untuk visualisasi serangan dan hardening
- [ ] Audit independen
- [ ] **Gerbang:** RFC, Benchmark ≥90%, Golden Test 100%, Real Cases ≥10

---

## Risiko

|Risiko|Dampak|Kemungkinan|Mitigasi|
|------|------|-----------|--------|
|False positives berlebihan|Delay produktivitas|Tinggi|Refine attack thresholds, user feedback loop|
|Over-hardening|Over-engineering|Rendah|Risk-based prioritization, constraint-aware attacks|
|Attack vector tidak realistis|Serangan tidak relevan|Tinggi|Use real case library, expert validation|
|Circular testing|Infinite loop|Rendah|Max iteration, gate timeout|
|User resistance|Adopsi rendah|Tinggi|Configurable aggressiveness, opt-in gate|

---

## Dampak ADR

**Apakah ini memerlukan perubahan Core?** Tidak.

Adversarial Testing adalah Capability Pack baru:

- **ADR-001 (Core Pipeline Freeze):** Tidak ada perubahan Core.
- **ADR-002 (Capability Pack Independence):** Berkomunikasi melalui Execution Runtime dan kontrak bersama.
- **ADR-003 (Worker = Adapter):** Worker tipis.
- **ADR-004 (Domain Engine Owns Business Logic):** Logika di `engine.py`.
- **ADR-005 (Human Approval Required):** Hanya pengujian dan rekomendasi; rencana final memerlukan persetujuan.
- **ADR-006 (Capability Contract v1):** Menggunakan kontrak yang ada.
- **ADR-007 (Conversation Boundary):** Dipanggil melalui Execution Runtime.
- **ADR-008 (Core Change Requires Cross-Capability Proof):** Tidak ada perubahan Core.

**ADR yang diperlukan:** Tidak ada. Ini adalah Capability Pack baru.
