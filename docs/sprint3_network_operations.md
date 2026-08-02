# ECP Network Engineer — Milestone 3: Network Operations

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi untuk sprint3_network_operations
<!-- DOCUMENT_METADATA_END -->

**Status:** Direncanakan
**Fokus:** Workflow operasional, bukan otomatisasi protokol

---

## Deliverables

### 1. Configuration Compare

**Tujuan:** Membandingkan dua backup konfigurasi dan menampilkan semantic diff + analisis dampak.

**User Story:**
> "Sebagai network engineer, saya ingin membandingkan backup A dengan backup B sehingga saya dapat melihat persis apa yang berubah dan apakah aman."

**Fitur:**
- Memuat dua file backup
- Semantic diff (engine yang sama seperti Milestone 2, diterapkan pada backup)
- Analisis dampak: service/interface mana yang terpengaruh
- Laporan Markdown

**Acceptance Criteria:**
- Dapat memuat dua golden test config apa pun
- Menampilkan rule yang ditambahkan/dihapus/dimodifikasi per kategori
- Mengidentifikasi perubahan yang berpotensi berisiko (firewall, NAT, routes)
- Menghasilkan laporan Markdown

---

### 2. Compliance Audit

**Tujuan:** Memeriksa konfigurasi terhadap kebijakan dan menampilkan Pass/Fail.

**User Story:**
> "Sebagai network engineer, saya ingin menjalankan compliance audit sehingga saya dapat membuktikan router memenuhi kebijakan perusahaan."

**Fitur:**
- Mendefinisikan kebijakan sebagai rule sederhana (JSON/YAML)
- Memeriksa config terhadap kebijakan
- Pass/Fail per rule
- Skor kepatuhan keseluruhan
- Laporan Markdown

**Contoh Kebijakan:**
```yaml
rules:
  - id: SSH-RESTRICTED
    check: "ssh must not be open to 0.0.0.0/0"
    severity: critical
  - id: PASSWORD-SET
    check: "admin password must be set"
    severity: critical
  - id: BACKUP-CONFIGURED
    check: "backup must be configured"
    severity: warning
  - id: NTP-ENABLED
    check: "NTP must be enabled"
    severity: info
```

**Acceptance Criteria:**
- Dapat mendefinisikan kebijakan kustom
- Memeriksa config terhadap setiap rule
- Menampilkan Pass/Fail dengan evidence
- Menghasilkan skor kepatuhan

---

### 3. Health Report

**Tujuan:** Skor kesehatan satu-klik untuk sebuah router.

**User Story:**
> "Sebagai network engineer, saya ingin skor kesehatan sehingga saya dapat menilai kondisi router dengan cepat."

**Fitur:**
- Health Score (0–100)
- Security Score (0–100)
- Performance Score (0–100)
- Maintainability Score (0–100)
- Skor Keseluruhan
- Perincian per kategori
- Laporan Markdown

**Logika Skoring:**
- Mulai dari 100
- Kurangi poin untuk setiap finding berdasarkan severity:
  - Critical: -20
  - Warning: -10
  - Info: -5
  - Suggestion: -2
- Batas bawah di 0

**Acceptance Criteria:**
- Menghasilkan skor untuk golden test config apa pun
- Skor konsisten (config yang sama = skor yang sama)
- Perincian menunjukkan isu mana yang memengaruhi setiap skor
- Laporan Markdown dengan indikator visual

---

### 4. Change Impact Analysis

**Tujuan:** Sebelum deployment, memprediksi apa yang akan terpengaruh oleh perubahan.

**User Story:**
> "Sebagai network engineer, saya ingin tahu apa yang akan rusak sebelum saya deploy, sehingga saya dapat bersiap."

**Fitur:**
- Menganalisis config saat ini + diff yang diusulkan
- Mengidentifikasi service yang terpengaruh:
  - Perubahan firewall → dampak konektivitas
  - Perubahan NAT → dampak akses internet
  - Perubahan rute → risiko lalu lintas blackhole
  - Perubahan DHCP → dampak lease
  - Perubahan interface → isolasi perangkat
- Memprediksi level dampak (Low/Medium/High/Critical)
- Menyarankan langkah mitigasi

**Acceptance Criteria:**
- Dapat menganalisis diff golden test apa pun
- Mengidentifikasi setidaknya: dampak firewall, NAT, route, interface, DHCP
- Memprediksi level dampak dengan benar untuk skenario yang diketahui
- Menyarankan mitigasi yang dapat ditindaklanjuti

---

### 5. Explain Like Engineer

**Tujuan:** Menjelaskan aturan konfigurasi dalam bahasa sederhana untuk onboarding.

**User Story:**
> "Sebagai network engineer junior, saya ingin memahami apa yang dilakukan setiap rule sehingga saya dapat belajar."

**Fitur:**
- Klik pada finding/rule apa pun
- Mendapatkan penjelasan:
  - Apa yang dilakukan rule ini
  - Mengapa rule ini dibuat
  - Apa yang terjadi jika dihapus
  - Dependensi (apa lagi yang bergantung pada ini)
  - Kesalahan umum
- Bahasa sederhana, tidak sarat jargon

**Contoh Output:**
```
Rule: masquerade on WAN
------------------------
What it does:
  Allows all devices on the LAN to access the internet by
  translating their private IPs to the router's public IP.

Why it exists:
  Without this, LAN devices cannot reach the internet.
  Only the router itself would have internet access.

Impact if removed:
  - LAN devices lose internet access
  - Hotspot users cannot browse
  - DHCP clients can get IPs but no internet

Dependencies:
  - Requires WAN interface to have public IP
  - Often paired with srcnat chain rule
  - Works with FastTrack for performance

Common mistakes:
  - Applying to LAN interface instead of WAN
  - Forgetting to create DHCP server
  - Not setting default route
```

**Acceptance Criteria:**
- Dapat menjelaskan semua 45 analysis rules
- Penjelasan akurat dan dapat ditindaklanjuti
- Dependensi diidentifikasi dengan benar
- Bahasa sederhana yang cocok untuk engineer junior

---

## Apa yang TIDAK Akan Dibangun di Milestone 3

- Otomatisasi BGP
- Otomatisasi MPLS
- Otomatisasi CAPsMAN
- Otomatisasi WireGuard
- Orkestrasi multi-router
- Integrasi API MikroTik live

Ini adalah konsekuensi dari pemahaman operasional yang baik, bukan prasyarat.

---

## Metrik Keberhasilan

| Metrik | Target |
|--------|--------|
| Akurasi Configuration Compare | ≥95% |
| Cakupan Compliance Audit | ≥90% dari kebijakan umum |
| Korelasi Health Score | ≥0.8 dengan penilaian ahli |
| Akurasi Change Impact | ≥80% untuk skenario yang diketahui |
| Kelengkapan Penjelasan | 100% dari 45 rule dijelaskan |
| Golden Test Pass | ≥95% |
| Item Feedback Dogfooding | ≥20 item dicatat |
| Waktu yang Dihemat (dogfooding) | ≥50% dibanding analisis manual |

---

## Prasyarat

- Milestone 2 baseline difreeze (`v1.0.0-dev+network-sprint2`)
- Dogfooding selesai (1–2 minggu)
- Feedback dari setidaknya 10 config nyata yang direview
- 5 prioritas teratas dari dogfooding didokumentasikan

---

## Definition of Done

- [ ] Configuration Compare berfungsi di semua skenario golden test
- [ ] Compliance Audit lolos semua test case kebijakan
- [ ] Health Report menghasilkan skor yang konsisten
- [ ] Change Impact Analysis memprediksi dampak dengan benar
- [ ] Explain Like Engineer mencakup semua 45 rule
- [ ] Semua test Milestone 3 lulus (≥95%)
- [ ] Feedback dogfooding diintegrasikan
- [ ] Dokumentasi diperbarui
- [ ] Demo siap

