<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Linimasa rilis, milestone, dan jadwal pengiriman
<!-- DOCUMENT_METADATA_END -->

# Roadmap ECP

**Status:** Aktif
**Pemilik:** Chief Product Officer
**Tujuan:** Mendefinisikan linimasa, target rilis, dan visi jangka panjang ECP. Semua konten terkait jadwal dan target versi berada di sini.

---

## Visi North Star

> **Platform adalah enabler. Tujuan akhirnya adalah AI Trading yang membuat keputusan investasi cerdas secara otonom.**

ECP dibangun sebagai platform AI eksekusi yang stabil, tetapi **Trading Analyst** adalah Capability Pack utama yang menjadi tujuan akhir. Semua kemampuan lain (Network, Code, Research, DevOps, Self Development, dan yang akan datang) adalah enabler yang memperkuat ekosistem menuju visi tersebut.

---

## Fase Pengembangan

### Fase 1 — Capability Excellence (Sekarang — 13 Pack)

**Fokus:** Menaikkan kualitas semua pack menjadi A/A-.

| Capability Pack | Grade Saat Ini | Target Grade | Target Maturity |
|-----------------|----------------|--------------|-----------------|
| Network Engineer | A | A+ | Domain Expert (L4) |
| Code Engineer | A- | A | Domain Expert (L4) |
| Research Assistant | A- | A | Domain Expert (L4) |
| DevOps Assistant | B+ | A- | Domain Expert (L4) |
| Trading Analyst | B+ (Certification Pending) | A- | Production Ready (L3) |
| Self Development | A | A | Domain Expert (L4) |
| Decision Intelligence | A (91.25%) | A | Domain Expert (L4) |
| System Architect | A (97.50%) | A | Domain Expert (L4) |
| Security Engineer | A- | A- | Production Ready (L3) |
| Data Engineer | A- | A- | Production Ready (L3) |
| Database Engineer | A- | A- | Production Ready (L3) |
| QA Engineer | A | A | Domain Expert (L4) |
| Business Analyst | A- | A- | Production Ready (L3) |

**Key Results:**
- 1.000+ kasus nyata di seluruh pack
- Semua pack berada di grade A- atau lebih tinggi
- Sertifikasi Trading Analyst selesai
- Dashboard benchmark untuk semua 13 pack

---

### Fase 2 — Decision Intelligence + Security + Data (+3 Pack)

Setelah 13 pack mencapai A-/A, tambahkan 3 Capability Pack baru:

| Prioritas | Capability Pack | Fungsi | Dependent Packs |
|-----------|-----------------|--------|-----------------|
| ⭐⭐⭐⭐⭐ | **Decision Intelligence** | "Brain" lintas domain — evidence → reasoning → simulation → debate → risk → decision → explanation | Trading, Network, Code, semua pack |
| ⭐⭐⭐⭐ | **Security Engineer** | OWASP, security audit, penetration test, threat modeling, secret detection, vulnerability assessment | Code, DevOps, Network |
| ⭐⭐⭐⭐ | **Data Engineer** | ETL, data cleaning, dataset versioning, feature engineering, data quality, time-series pipeline | Trading, Research, DevOps |

---

### Fase 3 — Enterprise (+4 Pack)

Setelah 13 pack stabil, tambahkan 4 Capability Pack untuk melayani kebutuhan enterprise:

| Prioritas | Capability Pack | Fungsi |
|-----------|-----------------|--------|
| 4 | **Database Engineer** | Optimasi SQL, desain skema, migrasi, rekomendasi indeks, analisis performa |
| 5 | **QA Engineer** | Generasi test, regression, mutation testing, Golden Test builder, benchmark generator |
| 6 | **Business Analyst** | Analisis requirements, user story, BRD, use case, workflow |

> **Catatan:** **System Architect** (RFC-0011) telah diimplementasikan dan menjadi Capability Pack resmi — lihat `docs/CAPABILITY_STRATEGY.md` §5.8.

---

### Fase 4 — Jangka Panjang (+5 Pack)

Setelah fondasi enterprise kuat, tambahkan Capability Pack untuk produktivitas dan kualitas tim:

| Prioritas | Capability Pack | Fungsi |
|-----------|-----------------|--------|
| 7 | **Product Manager** | Roadmap, prioritisasi, ROI, sprint planning |
| 8 | **Documentation Engineer** | Sinkronisasi dokumentasi, OpenAPI, ADR, changelog, release notes |
| 9 | **UI/UX Designer** | Design system, wireframe, aksesibilitas, UX audit |
| 10 | **AI Engineer** | RAG, fine-tuning, prompt engineering, agent design, evaluasi |
| 11 | **Infrastructure Engineer** | Kubernetes, Docker, storage, monitoring, observability, HA cluster |

---

## Linimasa Rilis

| Rilis | Tanggal Target | Fokus |
|---------|-------------|-------|
| v1.0.0-dev | Q3 2026 | Platform lengkap, Architecture Governance aktif |
| v1.0.0 | Q4 2026 | Developer Preview: 13 pack bersertifikat, dokumentasi, SDK, Studio |
| v1.1.0 | Q1 2027 | Capability Excellence: semua pack A-/A, Sertifikasi Trading |
| v1.2.0 | Q2 2027 | Decision Intelligence + Security Engineer + Data Engineer |
| v1.3.0 | Q3 2027 | Enterprise: Database Engineer + QA Engineer |
| v1.4.0 | Q4 2027 | Enterprise: Business Analyst |
| v2.0.0 | 2028 | Jangka panjang: Product Manager, Documentation, UI/UX, AI Engineer, Infrastructure |

---

## Roadmap Capability 12 Bulan

### Q1 — Sertifikasi Trading & Developer Preview
- Menyelesaikan Sertifikasi Trading Analyst
- Rilis Developer Preview (v1.0.0)
- 500 kasus nyata di seluruh Capability Pack
- Semua pack terdokumentasi dan di-benchmark

### Q2 — Capability Excellence
- Network A+
- Code A
- Trading A-
- Research A
- DevOps A-
- 1.000 kasus nyata
- Semua pack naik satu grade melalui pengetahuan dan kerja benchmark dunia nyata

### Q3 — Decision Intelligence
- RFC dan prototipe untuk Decision Intelligence
- RFC Security Engineer
- RFC Data Engineer
- Melanjutkan peningkatan kualitas pada semua 13 pack

### Q4 — Fondasi Enterprise
- Decision Intelligence Stabil
- Security Engineer Stabil
- Data Engineer Stabil
- 1.500+ kasus nyata

---

## Roadmap Bebas 5 Tahun

### Fase 0 — Arsitektur Lengkap ✅
- Core, Capability Contract, Worker, Conversation, Governance, ADR, UX Contract
- Biaya: Gratis

### Fase 1 — Capability Excellence (0–12 bulan)
- 13 pack yang ada: Network, Code, Research, DevOps, Trading, Self Development, Decision Intelligence, System Architect, Security Engineer, Data Engineer, Database Engineer, QA Engineer, Business Analyst
- Target: semua pack grade A-/A, 1.000 kasus nyata
- Core tetap dibekukan

### Fase 2 — Decision Intelligence (12–18 bulan)
- Pack Decision Intelligence: evidence → reasoning → simulation → debate → risk → decision → explanation
- Digunakan oleh Trading, Network, dan pack lain sebagai "brain" lintas domain
- Security Engineer + Data Engineer

### Fase 3 — Enterprise Pack (18–24 bulan)
- Database Engineer, QA Engineer, Business Analyst
- Target: 9 pack total, 3.000+ kasus nyata

### Fase 4 — Local AI Stack (24–30 bulan)
- Ollama + Qwen/DeepSeek/Llama/Gemma
- Model Router memilih model open-source terbaik per capability
- Semua inferensi lokal atau free-tier
- Biaya: Gratis

### Fase 5 — Productivity Pack (30–36 bulan)
- Product Manager, Documentation Engineer, UI/UX Designer, AI Engineer, Infrastructure Engineer
- Target: 18 pack total, 5.000+ kasus nyata

### Fase 6 — Model Enal (36–48 bulan)
- EnalCoder: Qwen/DeepSeek yang di-fine-tune untuk coding
- EnalNetwork: Llama yang di-fine-tune pada konfigurasi jaringan
- EnalTrading: Qwen yang di-fine-tune pada pola trading
- Semua melalui LoRA, tanpa pretraining
- Biaya: Rendah (single GPU atau cloud sesekali)

### Fase 7 — Continuous Learning (Berlangsung)
- Kasus nyata → Review → Pembaruan Pengetahuan → Benchmark
- Siklus peningkatan harian

### Fase 8 — Foundation Model (48–60 bulan, kondisional)
- Hanya jika pengguna >100k, pendapatan stabil, GPU tersedia
- EnalLM: dibuat khusus untuk eksekusi ECP
- Bukan klon GPT, tetapi model yang dioptimalkan untuk eksekusi

---

## Yang Tidak Akan Menjadi Capability Pack

Berikut adalah komponen yang **tidak akan dijadikan Capability Pack** sendiri. Mereka akan diposisikan sebagai **Plugin**, **service**, atau **infrastruktur platform**:

- Authentication / Authorization
- PostgreSQL / Redis / MinIO / Kafka
- Plugin Marketplace
- Broker Connector / Exchange Connector
- Infrastruktur murni (load balancer, DNS, container runtime)

Keputusan ini menjaga ECP tetap fokus pada **domain expertise** dan mencegah platform melebar ke infrastruktur yang sudah ada solusinya.

---

## Strategi Model: Progressive Independence

**Tahun 1:** 100% model eksternal (Claude, GPT, Gemini, Qwen, DeepSeek)
**Tahun 2:** 80% eksternal, 20% model Enal
**Tahun 3:** 50% eksternal, 50% model Enal
**Tahun 5:** 90% model Enal

Model Router membuat hal ini transparan bagi pengguna dan Capability Pack.
Semua Capability Pack tetap berfungsi tanpa perubahan apa pun terkait sumber model.

---

## Rencana Perluasan Pengetahuan

Semua penambahan pengetahuan yang direncanakan dilacak melalui RFC dan diimplementasikan hanya di dalam Capability Pack. Core tetap tidak berubah.

### Penambahan Pengetahuan per Capability Pack

| Capability Pack | Topik yang Direncanakan | RFC Referensi |
|-----------------|---------------|---------------|
| Network Engineer | Cisco Design Guide, MikroTik Best Practice, Fortinet Hardening, BGP, MPLS, IPv6, Zero Trust | RFC-0004 |
| Code Engineer | Clean Architecture, DDD, SOLID, CQRS, Event Sourcing, Secure Coding | RFC-0006 |
| Trading Analyst | Wyckoff, ICT, SMC, Elliott Wave, Volume Profile, Macro, Options, Futures, Psychology | RFC-0005 |
| Research Assistant | Peringkat evidence, deteksi kontradiksi, kualitas sitasi, estimasi confidence | — |
| DevOps Assistant | Multi-cloud, GitOps, Platform engineering, Policy-as-code, Chaos engineering | — |
| Self Development | Pembelajaran pola lintas proyek, prediksi dampak, taksonomi architecture smell | — |

Untuk rincian topik yang lebih detail, lihat `docs/CAPABILITY_STRATEGY.md` (bagian Knowledge Expansion).

---

## Dokumen Terkait

| Dokumen | Tujuan |
|----------|---------|
| `docs/GOVERNANCE_CHARTER.md` | Visi, prinsip inti, filosofi, aturan konstitusional |
| `docs/GOVERNANCE.md` | Aturan operasional — ADR, Capability First, Architecture Freeze, enforcement |
| `docs/RELEASE_CRITERIA.md` | Syarat rilis — quality gates, Definition of Done, benchmark targets |
| `docs/CAPABILITY_STRATEGY.md` | Strategi Capability Pack — maturity model, lifecycle, profil pack |
| `docs/DOCUMENT_STRUCTURE.md` | Fungsi dan SSOT setiap dokumen dalam dokumentasi strategis |
| `docs/v1_roadmap.md` | Landing page kompatibilitas — menunjuk ke dokumen-dokumen di atas |
| `docs/rfcs/README.md` | Proses RFC dan daftar RFC aktif |
| `ARCHITECTURE_DECISIONS.md` | ADR yang sudah disetujui dan dibekukan |

