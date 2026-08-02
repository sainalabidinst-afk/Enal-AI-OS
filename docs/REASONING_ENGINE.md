# Mesin Penalaran

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi untuk REASONING_ENGINE
<!-- DOCUMENT_METADATA_END -->

## Ikhtisar

Reasoning Engine adalah mesin penalaran simbolik/berbasis aturan untuk penalaran multi-langkah, pengambilan keputusan, dan validasi batasan. Mesin menggunakan aturan deterministik (BUKAN LLM) untuk menghasilkan kesimpulan dan keputusan yang dapat dijelaskan.

## Metode

### 1. Rantai Maju
Mulai dari fakta yang diketahui, menerapkan aturan untuk mencapai kesimpulan.

```
Known Facts → Apply Rules → New Facts → Apply Rules → ... → Conclusions
```

**Use case**: Dekomposisi tujuan, identifikasi kapabilitas

### 2. Rantai Mundur
Mulai dari hasil yang diinginkan, pencarian perenang yang diperlukan.

```
Desired Outcome ← Find Prerequisites ← Find Sub-prerequisites ← ...
```

**Kasus penggunaan**: Menemukan apa yang diperlukan untuk mencapai suatu tujuan

### 3. Pohon Keputusan
Evaluasi opsi-opsi terhadap kriteria yang ditentukan.

```
Options × Criteria → Scoring → Best Option Selected
```

**Kasus penggunaan**: Pemilihan teknologi, keputusan alokasi sumber daya

### 4. Kendala Dakwah
Verifikasi bahwa semua kendala terpenuhi.

```
Variables × Constraints → Satisfied/Violated → Proceed/Block
```

**Kasus penggunaan**: Validasi anggaran, jadwal pemeriksaan

### 5. Penalaran Kausal
Analisis hubungan sebab-akibat.

```
Event → Find Causes → Identify Effects → Generate Recommendations
```

**Kasus penggunaan**: Analisis kegagalan, penilaian dampak

## Struktur Data

### Bukti
- `id`: Pengenal unik
- `type`: FAKTA, ATURAN, KENDALA, PENGAMATAN, BERASAL
- `description`: Deskripsi yang dapat dibaca manusia
- `confidence`: 0,0 - 1,0
- `source`: Dari mana bukti ini berasal

### Aturan Penalaran
- `rule_id`: Pengenal unik
- `conditions[]`: Kondisi yang harus dipenuhi
- `conclusions[]`: Kesimpulan ketika kondisi terpenuhi
- `confidence`: Keyakinan ketika rule aktif
- `priority`: Untuk menyelesaikan konflik

### Keputusan
- `decision_id`: Pengenal unik
- `options[]`: Opsi yang tersedia
- `selected`: Opsi yang dipilih
- `confidence`: Keyakinan dalam mengambil keputusan
- `reasoning`: Penjelasan mengapa
- `urgency`: RENDAH, SEDANG, TINGGI, KRITIS

### Kesimpulan
- `conclusion_id`: Pengenal unik
- `statement`: Kesimpulan
- `confidence`: Tingkat kepercayaan diri
- `evidence_ids[]` : Bukti pendukung
- `derived`: Diturunkan (vs langsung)

### Hasil Penalaran
- `reasoning_id`: sesi ID unik
- `method`: Metode penalaran yang digunakan
- `status`: SELESAI, GAGAL, ​​TIDAK MENYATAKAN
- `evidence[]`, `conclusions[]`, `decisions[]`
- `confidence`: Keyakinan secara keseluruhan
- `explanation`: Penjelasan yang dapat dibaca manusia
- `execution_time_ms`: Waktu yang diambil

## Penggunaan

```python
from apps.organization.reasoning_engine import (
    reasoning_engine,
    ReasoningMethod,
    Evidence, EvidenceType,
)

# Forward chaining
result = reasoning_engine.forward_chaining(
    "Complete a complex software project"
)

# Backward chaining
result = reasoning_engine.backward_chaining(
    "Deploy web app",
    "Application is running in production",
    context={"domain": "devops"}
)

# Decision tree
result = reasoning_engine.decision_tree(
    "Which framework?",
    options=[
        {"name": "FastAPI", "attributes": {"speed": 9, "cost": 3}},
        {"name": "Django", "attributes": {"speed": 6, "cost": 5}},
    ],
    criteria=["speed", "cost"]
)

# Constraint propagation
result = reasoning_engine.constraint_propagation(
    constraints=[
        {"name": "Budget limit", "variable": "budget", "operator": "lt", "value": 1000},
    ],
    variables={"budget": 500}
)

# Causal reasoning
engine.add_fact("Network was unstable", True)
result = engine.causal_reasoning("Pipeline execution failed")

# Knowledge base
engine.add_fact("System is ready", True, confidence=0.95)
evidence = engine.query_evidence("system")

# Rule management
from apps.organization.reasoning_engine import ReasoningRule
engine.register_rule(ReasoningRule(
    rule_id="my-rule",
    name="My Rule",
    description="Custom rule",
    conditions=["condition met"],
    conclusions=["conclusion reached"],
))
```

## Peristiwa Telemetri

- `ReasoningStarted`: Ketika penalaran dimulai
- `ReasoningRuleApplied`: Ketika sebuah aturan diaktifkan
- `ReasoningCompleted`: Ketika penalaran berhasil
- `ReasoningFailed`: Ketika penalaran mengalami error
- `ReasoningDecisionMade`: Ketika sebuah keputusan dibuat

## Aturan Default

1. **Dekomposisi Tujuan** (prioritas 1): Tujuan kompleks → sub-tujuan
2. **Persyaratan kemampuan** (prioritas 2): Domain tujuan → kapabilitas yang diperlukan
3. **Resolusi Ketergantungan** (prioritas 3): Langkah → eksekusi terurut
4. **Constraint Validation** (prioritas 4): Constraint → divalidasi/diblokir
5. **Perencanaan Sumber Daya** (prioritas 5): Persyaratan → alokasi sumber daya
6. **Penilaian Risiko** (prioritas 6): Kompleksitas + ketergantungan → tingkat risiko
7. **Gerbang Kualitas** (prioritas 7): Langkah selesai → verifikasi kualitas
