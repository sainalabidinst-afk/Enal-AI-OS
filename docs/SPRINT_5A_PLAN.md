# Sprint 5A — Network Engineer: Production Ready

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi untuk SPRINT_5A_PLAN
<!-- DOCUMENT_METADATA_END -->

**Tujuan:** Membawa capability Network Engineer ke status production-ready dengan quality gate yang terukur.

**Definition of Done:**
- Akurasi: ≥95%
- False Positive: <5%
- False Negative: <5%
- Latensi: <2 detik per analisis
- Cakupan: >90% dari kelas isu yang diketahui
- Golden Tests: 100% lulus
- Real Cases: 100+ kasus dengan hasil benchmark
- Dokumentasi: Lengkap

---

## Kondisi Saat Ini

| Komponen | Status |
|-----------|--------|
| Parser (RouterOS, Cisco, Fortinet) | ✅ Mature |
| Analyzer (47 rules) | ✅ Mature |
| Graph Builder | ✅ Ada |
| Recommendation Engine | ✅ Ada |
| Generator | ✅ Ada |
| Simulator | ✅ Ada |
| Verification Engine | ✅ Ada |
| Risk Scorer | ✅ Ada |
| Controlled Deployment | ✅ Ada |
| NIC (Knowledge + Inference) | ✅ Ada |
| Golden Tests | ⚠️ 1 sample case |
| Real Cases | ⚠️ 1 sample case |

---

## Minggu 1 — Ekspansi Golden Tests

Target: 100+ golden test cases yang mencakup:
- MikroTik RouterOS: ACL, BGP, OSPF, HSRP, NAT, AAA, SNMP, QoS, VPN, MPLS
- Cisco IOS: ACL, BGP, OSPF, HSRP, NAT, AAA, SNMP, QoS, VPN, MPLS
- Fortinet: Policies, NAT, VPN, Routing, HA

Setiap golden test harus memiliki:
- `config.rsc` / `config.txt` — snippet konfigurasi aktual
- `expected.json` — expected findings, risk score, compliance score
- `metadata.yaml` — vendor, device role, complexity, tags
- `report.md` — laporan expected yang dapat dibaca manusia

Lokasi: `real_cases/mikrotik/`, `real_cases/cisco/`, `real_cases/fortinet/`

---

## Minggu 2 — Otomasi Benchmark

Target: Benchmark runner otomatis yang:
1. Memuat semua real cases dari disk
2. Menjalankan setiap kasus melalui analyzer
3. Membandingkan findings aktual vs expected
4. Menghitung akurasi, false positive, false negative, latensi
5. Menghasilkan perincian capability score
6. Mengekspor hasil ke JSON/CSV

Lokasi: `benchmarks/network_engineer_benchmark.py`

Integrasi:
- Target `make benchmark-network` di Makefile
- CI job: `python benchmarks/network_engineer_benchmark.py`

---

## Minggu 3 — Ekspansi Cakupan

Target: Menambahkan cakupan rule yang hilang:
- VLAN security
- STP/RSTP
- BGP security (prefix filtering, TTL security)
- OSPF security (authentication)
- Validasi IPsec/VPN
- Validasi QoS policy
- SNMPv3 vs SNMPv1/v2c
- Validasi AAA/TACACS+/RADIUS
- Logging dan syslog
- Konfigurasi NTP
- DNS security

---

## Minggu 4 — Integrasi & Telemetry

Target:
- Menghubungkan perekaman telemetry ke analyzer
- Melacak waktu eksekusi per-rule
- Melacak akurasi deteksi vendor
- Melacak penggunaan capability per session
- Endpoint metrik siap dashboard

---

## Rencana Eksekusi

1. Membuat golden test cases (batch 1: 20 kasus MikroTik)
2. Membuat golden test cases (batch 2: 20 kasus Cisco)
3. Membuat golden test cases (batch 3: 20 kasus Fortinet)
4. Membuat golden test cases (batch 4: 40 kasus advanced campuran)
5. Otomasi benchmark
6. Ekspansi cakupan
7. Integration testing
8. Dokumentasi

