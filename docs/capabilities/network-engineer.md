# Spesifikasi Capability Pack Network Engineer

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Spesifikasi Capability Pack untuk Network Engineer
<!-- DOCUMENT_METADATA_END -->

## Versi: 2.0.0
## Status: Draf (v2.0 belum dikembangkan ke konsultan jaringan)

---

## 1. Tujuan

Memberikan sinyal jaringan vendor-agnostic untuk:
- Parsing & validasi konfigurasi
- Audit postur keamanan
- Analisis & rekomendasi risiko
- Generasi & simulasi konfigurasi
- Design review (analisis dan penilaian tingkat topologi)
- Troubleshooting (bukti terstruktur → hipotesis → akar penyebab)
- Perencanaan migrasi (lintas vendor dengan risiko, rollback, downtime)
- Advisory jaringan (pertanyaan desain tingkat tinggi dengan desain yang dapat dijelaskan)

---

## 2. Ruang Lingkup

### Dalam Ruang Lingkup
- Vendor yang didukung: MikroTik RouterOS, Cisco IOS, Fortinet, Juniper (direncanakan)
- Format file: .rsc, .conf, .txt
- Jenis analisis: Keamanan, Best Practice, Kepatuhan, Design Review, Troubleshooting
- Output: Findings, Risk Score, Rekomendasi, Dokumentasi, Migration Plan, Design Proposal

### Di Luar Ruang Lingkup
- Push konfigurasi perangkat langsung
- Monitoring real-time
- Simulasi lalu lintas
- Terjemahan lintas vendor (peta jalan masa depan)

---

## 3. Kontrak

### Input
```json
{
  "type": "text|topology|symptom|query",
  "content": "string (raw config, topology JSON, symptom description, or design question)",
  "vendor_hint": "mikrotik|cisco|fortinet|auto-detect"
}
```

### Output
```json
{
  "device": "string",
  "vendor": "string",
  "summary": "string",
  "issues": [{"severity": "critical|high|medium|low", "category": "string", "description": "string"}],
  "recommendations": [{"priority": "high|medium|low", "problem": "string", "why": "string", "recommendation": "string"}],
  "risk_score": "float 0-1",
  "design_review": {
    "network_score": "float 0-100",
    "availability_grade": "A|B+|B|C|D|F",
    "security_grade": "A|B+|B|C|D|F",
    "scalability_grade": "A|B+|B|C|D|F",
    "performance_grade": "A|B+|B|C|D|F",
    "issues": []
  },
  "troubleshooting": {
    "session_id": "string",
    "hypotheses": [],
    "root_cause": {}
  },
  "migration_plan": {
    "source_vendor": "string",
    "target_vendor": "string",
    "phases": [],
    "estimated_downtime_minutes": "int"
  },
  "advisory": {
    "proposals": []
  }
}
```

---

## 4. Aturan Analisis (Target 200+)

### Aturan Keamanan
|ID Aturan|Kategori|Vendor|Deskripsi|
|---------|----------|--------|-------------|
|SEC-001|Firewall|Semua|Kebijakan default harus bersifat restrictif|
|SEC-002|Autentikasi|Semua|Autentikasi lemah terdeteksi|
|SEC-003|Layanan|Semua|Layanan yang tidak diperlukan terekspos|
|SEC-004|SNMP|Semua|Community string SNMP terekspos|

### Aturan Best Practice
|ID Aturan|Kategori|Vendor|Deskripsi|
|---------|----------|--------|-------------|
|BP-001|Logging|Semua|Logging tidak dikonfigurasi untuk event penting|
|BP-002|NTP|Semua|Sumber waktu tidak dapat disesuaikan|
|BP-003|SSH|Semua|SSH hardening tidak diterapkan|

### Aturan Design Review
|ID Aturan|Kategori|Deskripsi|
|---------|----------|-------------|
|DR-001|Availability|Single Point of Failure terdeteksi|
|DR-002|Performance|Potensi bottleneck bandwidth|
|DR-003|Security|Eksposur interface manajemen|
|DR-004|Scalability|Segmentasi data dengan terlalu banyak perangkat|
|DR-005|Performance|Komunikasi laten tinggi|
|DR-006|Security|VLAN bocor / VLAN terlalu luas|

### Pola Troubleshooting
|ID Pola|Gejala|Hipotesis|
|------------|---------|------------|
|TSH-001|Ping timeout|Downstream tidak terjangkau, routing black hole, firewall block|
|TSH-002|Konektivitas terputus-putus|Interface flapping, ketidakstabilan routing|
|TSH-003|Jaringan lambat|Saturasi bandwidth, latensi DNS|

---

## 5. Persyaratan Benchmark

### Target Metrik
|Metrik|Target|Kriteria Lulus|
|--------|--------|---------------|
|Accuracy|≥95%|Findings benar ≥95%|
|Precision|≥95%|False positive ≤5%|
|Recall|≥95%|True positive ≥95%|
|Latency|<2 detik|Rata-rata respons <2 detik|
|Coverage|≥90%|Code coverage ≥90%|

---

## 6. Vendor yang Didukung

|Vendor|Format|Status Parser|Status Analyzer|
|--------|--------|---------------|----------------|
|MikroTik|.rsc, .conf|✅|⏳|
|Cisco IOS|.conf, .txt|✅|⏳|
|Fortinet|.conf|✅|⏳|

---

## 7. Keterbatasan yang Diketahui

- Timeout 60 detik untuk file > 10MB
- Hanya mendukung analisis konfigurasi tunggal (bukan template)
- Design review memerlukan input topologi manual untuk skenario multi-perangkat
- Estimasi migration planner berbasis heuristik
- Mesin troubleshooting memerlukan input bukti terstruktur

---

## 8. Peta Jalan Network Engineer 2.0

### N1 — Deep Network Knowledge
- Ontologi yang digabungkan: TCP/IP, Routing, Switching, MPLS, BGP, OSPF, IS-IS, VXLAN, EVPN, SD-WAN, WiFi, IPv6, DNS, DHCP, QoS, Multicast, NAT, Firewall, Zero Trust
- Penjelasan tingkat konsep dengan referensi RFC
- Pemetaan konsep lintas vendor

### N2 — Design Review
- Analisis tingkat topologi untuk SPOF, bottleneck, routing loop, asymmetric routing, VLAN leak, gap keamanan, skalabilitas
- Penilaian bertingkat: Network Score (0-100), Availability, Security, Scalability, Performance

### N3 — Troubleshooting Engine
- Workflow terstruktur: gejala → mengumpulkan bukti → hipotesis → menguji hipotesis → verifikasi → akar penyebab
- Pattern matching untuk gejala jaringan umum
- Peringkat hipotesis tertimbang keyakinan

### N4 — Migration Planner
- Migration plan lintas vendor dengan eksekusi bertahap
- Penilaian risiko, langkah rollback, estimasi downtime, validation checkpoint
- Pemetaan keselarasan vendor (Cisco ↔ MikroTik ↔ Fortinet)

### N5 — Network Advisor
- Query desain bahasa alami: "500 cabang", "data center HA", "Zero Trust", "SD-WAN"
- Design proposal yang dapat dijelaskan dengan ringkasan arsitektur, komponen, rekomendasi, dan risiko

---

## 9. Target Coverage Dataset

|Milestone|Kasus|Vendor yang Dicakup|Domain yang Dicakup|
|-----------|-------|-----------------|-----------------|
|5A.1|25|MikroTik: 10, Cisco: 10, Fortinet: 5|Security: 15, Best Practice: 10|
|5A.2|50|Distribusi seimbang|Security: 25, HA: 10, QoS: 5, Wireless: 5, Monitoring: 5|
|5A.3|100|Ketiga vendor × 25+ kasus|Coverage penuh|

---

## 10. Metrik Evaluasi

### Golden Test
- ✅ Harus lulus 100% sebelum dimasukkan
- Kasus uji disimpan di `benchmarks/golden/`

### Real Cases
- Benchmark pass rate minimal 95%
- Dievaluasi melalui `make benchmark-network`

### Performance
- Waktu eksekusi dicatat melalui telemetry
- Alert jika rata-rata >2 detik

