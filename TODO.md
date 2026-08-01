# TODO — Restrukturisasi v1_roadmap → Governance Charter + Dokumen Fokus

## Tujuan
Memisahkan `docs/v1_roadmap.md` yang mencampur roadmap, governance, release criteria, dan capability strategy menjadi dokumen-dokumen terfokus dengan tanggung jawab jelas, serta menjadikan ECP memiliki governance charter eksplisit.

## Struktur Target
```
docs/
├── GOVERNANCE_CHARTER.md      ← Dokumen induk (single source of truth)
├── GOVERNANCE.md              ← Aturan operasional (ADR, Capability First, Architecture Freeze)
├── RELEASE_CRITERIA.md        ← Syarat rilis, quality gates, Definition of Done
├── CAPABILITY_STRATEGY.md     ← Capability Pack, maturity model, benchmark, lifecycle
├── ROADMAP.md                 ← Timeline dan target versi
├── DOCUMENT_STRUCTURE.md      ← Fungsi tiap dokumen, SSOT, tingkat stabilitas
└── v1_roadmap.md              ← Landing page (kompatibilitas) → menunjuk dokumen baru
```

## Langkah

- [x] 1. Buat `docs/GOVERNANCE_CHARTER.md` — visi, prinsip inti, filosofi Core frozen / Capability Pack inovasi, aturan yang jarang berubah, proses amendemen charter
- [x] 2. Buat `docs/GOVERNANCE.md` — Capability First Rule, No New Engines, Architecture Freeze Policy, Kernel Stability, Capability Independence, ADR process, enforcement CI/CD, Capability Changelog
- [x] 3. Buat `docs/RELEASE_CRITERIA.md` — Success Criteria, Golden Test Set, CI/CD pipeline, Metrics, Developer Preview Quality Targets, template Definition of Done, DoD per pack, DoD rilis
- [x] 4. Buat `docs/CAPABILITY_STRATEGY.md` — filosofi strategi, Capability Maturity Model (6 level), Quality Grades (A/A-/B+...), Capability Lifecycle, profil 6 pack, benchmark requirement, Knowledge Expansion
- [x] 5. Buat `docs/ROADMAP.md` — Timeline, Post-DP Releases, 12-Month Roadmap, 5-Year Free Roadmap, Model Strategy
- [x] 6. Buat `docs/DOCUMENT_STRUCTURE.md` — tabel fungsi dokumen, SSOT, mana yang stabil vs berubah per rilis
- [x] 7. Ubah `docs/v1_roadmap.md` menjadi landing page (charter ringkas) yang menunjuk ke 5 dokumen baru
- [x] 8. Update referensi `docs/roadmap.md` → `docs/ROADMAP.md` di `docs/baseline_freeze.md`
- [x] 9. Validasi tautan antar dokumen dan konsistensi data (angka benchmark, grade, tanggal)
  - ✓ Grade konsisten: A (≥90), A- (≥85), B+ (≥80)
  - ✓ Timeline konsisten: v1.0.0-dev Q3 2026
  - ✓ 6 Capability Packs konsisten di semua dokumen
  - ✓ Maturity Model 6 level konsisten
  - ✓ Quality Grades 6 level konsisten
  - ✓ Capability Lifecycle konsisten
  - ✓ Architecture Freeze Policy di GOVERNANCE.md
  - ✓ Definition of Done per pack di RELEASE_CRITERIA.md
  - ✓ Semua dokumen baru dirujuk dari v1_roadmap.md

## Implementasi RFC-0006 (Code Knowledge Expansion)

- [x] 10. Buat `apps/code_engineer/architecture_patterns.py` — Clean Architecture, DDD, SOLID, CQRS, Event Sourcing analyzers
- [x] 11. Buat `apps/code_engineer/secure_coding.py` — OWASP Top 10, Auth/Secrets, Secure Coding analyzers
- [x] 12. Update `apps/code_engineer/__init__.py` — ekspos `architecture_pattern_analyzer` dan `secure_coding_analyzer`
- [x] 13. Tulis Unit Tests — 10 test baru (17 total) di `tests/reference/test_code_engineer.py`
- [x] 14. Update Benchmark Code Engineer — tambah metric architecture_pattern_score dan secure_coding_score
- [x] 15. Integrasi ke Pipeline `analyze_code()` — sertakan hasil architecture + security dalam output

## Implementasi RFC-0004 (Network Knowledge Expansion)

- [x] 16. Buat `apps/network_engineer/enterprise_knowledge/base.py` — base class `EnterpriseKnowledgeFinding`
- [x] 17. Buat `apps/network_engineer/enterprise_knowledge/cisco_design_guide.py` — Cisco Design Guide: campus, data center, SD-WAN, HA
- [x] 18. Buat `apps/network_engineer/enterprise_knowledge/mikrotik_best_practice.py` — MikroTik: ISP edge, hotspot, IPv6, FastTrack, admin security
- [x] 19. Buat `apps/network_engineer/enterprise_knowledge/fortinet_hardening.py` — Fortinet: FortiOS, policy, VPN, threat protection
- [x] 20. Buat `apps/network_engineer/enterprise_knowledge/bgp_analysis.py` — BGP: path selection, filtering, communities, monitoring
- [x] 21. Buat `apps/network_engineer/enterprise_knowledge/mpls_analysis.py` — MPLS: forwarding, LDP, VRF, traffic engineering
- [x] 22. Buat `apps/network_engineer/enterprise_knowledge/ipv6_analysis.py` — IPv6: dual-stack, SLAAC, DHCPv6, transition
- [x] 23. Buat `apps/network_engineer/enterprise_knowledge/zero_trust.py` — Zero Trust: principles, micro-segmentation, ZTNA
- [x] 24. Update `apps/network_engineer/enterprise_knowledge/__init__.py` — integrasi semua analyzer ke `EnterpriseKnowledgeEngine`
- [x] 25. Verifikasi import dan integrasi — 7 analyzer terdaftar, smoke test menghasilkan 24 findings

## Implementasi RFC-0005 (Trading Knowledge Expansion)

- [x] 26. Rewrite `apps/trading_analyst/engine.py` — pipeline integrasi semua 9 domain RFC-0005 (MarketAnalyzer, Wyckoff, SMC, Elliott Wave, Volume Profile, Psychology, Macro, Derivatives, Summary)
- [x] 27. Buat `benchmarks/trading_analyst_benchmark.py` — benchmark framework (reasoning quality, explainability, consistency, evidence accuracy)
- [x] 28. Update `apps/trading_analyst/__init__.py` — ekspos TradingEngine dengan analyze_market, analyze_full, assess_risk, generate_strategy
- [x] 29. Perbaiki synthetic data generator — 3 fase pasar (range 60%, trend 25%, volatility 15%) agar semua analyzer mendapat struktur
- [x] 30. Tambah FVG cap (8 per timeframe) — kurangi noise SMC yang banjiri confidence scoring
- [x] 31. Smoke test pipeline — 13 evidence types, semua 9 domain aktif, bullish bias 97% confidence, 83 evidence, 11 reasoning steps ✅
