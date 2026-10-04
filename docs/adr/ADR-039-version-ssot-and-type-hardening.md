<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Platform
**Canonical Owner:** Lead Platform Engineer
**Terakhir Diverifikasi:** 2026-10-04
**Versi:** 1.0.0
**Status:** Accepted
**SSOT:** Version resolution, type-safety hardening, dan cross-pack reachability
<!-- DOCUMENT_METADATA_END -->

# ADR-039: Version Single Source of Truth dan Type-Safety Hardening

## Abstrak

ADR ini menetapkan tiga perubahan yang menutup temuan audit 2026-10-04:
(1) versi platform hanya punya satu sumber kebenaran,
(2) annotation yang selama ini berbohong dihlebarkan agar `mypy` bersih tanpa
menutupi bug, dan (3) `apps/self_development` menjangkau pack lain sebagai data,
bukan import edge.

## Konteks

### 1. Version drift

`/health` dan `/` melaporkan `3.0.0` pada checkout `v3.1.0-rc1`. Tiga
deklarasi versi saling lepas:

| Sumber | Nilai |
|---|---|
| `backend/pyproject.toml` `[project].version` | `3.1.0rc1` |
| `VERSION` | `v3.1.0-rc1` |
| `backend/app/core/config.py` `Settings.VERSION` | `3.0.0` |
| `.env` | `VERSION=3.0.0` |

Penyebabnya bukan hanya konstanta yang dijejak ulang: `.env` dimuat oleh
`BaseSettings(env_file=".env")`, sehingga `VERSION=3.0.0` **menimpa** nilai
default. Nama `VERSION` juga sangat umum dan di-set oleh base image, jadi
menjadi titik tabsir yang rapuh.

### 2. Mypy 20 error, sebagian menandakan bug nyata

`python -m mypy backend/ apps/` melaporkan 20 error di 10 file. Yang menarik:
beberapa annotation justru **menyembunyikan** bug.

- `TemplateRegistry.clone_template()` dianotasi `-> dict[str, Any]` tetapi
  mengembalikan `None` untuk id yang tidak dikenal. Annotation itu berbohong;
  pemanggil `backend/app/api/marketplace.py` lalu mengindeks hasilnya tanpa
  cek `None`.
- `apps/{synthesized,benchmark_pack}/worker.py` menganotasi `engine: object | None`
  lalu memanggil `self.engine.execute(task)`. Singleton modul dibangun dengan
  `engine=None`, jadi setiap `.run()` pasti melempar
  `AttributeError: 'NoneType' object has no attribute 'execute'`.
- `_SUPPORTED_PROVIDERS` di `stt_service.py`/`tts_service.py` dianotasi
  `type[STTProvider]` (abstract), sehingga instantiation tidak type-safe.
- `evaluate_against_vendor_rules()`_progress_menerima `config: dict` padahal
  semua probe bekerja lewat `str(config)` dan dipanggil dengan teks.

### 3. Capability First Rule

`apps/self_development/cross_pack_bridge.py` meng-import lima pack lain secara
statis (di dalam fungsi), sehingga `benchmarks/governance_checks.py` melaporkan
5 pelanggaran `capability_first_rule` dan job `governance-check` merah.
Teks aturan: *"Capability packs must NOT import from other capability packs.
Use Execution Runtime and shared contracts instead."*

## Keputusan

### 1. `backend/app/core/platform_version.py` — satu sumber versi

`resolve_version()` membaca, berurutan prioritas:

1. `ECP_VERSION` (env, untuk image dan release pipeline),
2. metadata distribusi terpasang untuk `enal-backend`,
3. `[project].version` di `pyproject.toml`,
4. `FALLBACK_VERSION`.

Hasilnya di-memoize (`lru_cache`). `Settings.VERSION` memakai
`default_factory=resolve_version` dengan `validation_alias=AliasChoices("ECP_VERSION")`
sehingga kunci `VERSION` di `.env` maupun env container **tidak lagi menimpa**
nilai tersebut. `.env.example` mendokumentasikan perilaku baru.

### 2. Annotation dibetulkan, bukan exception

Semua 20 error mypy dihilangkan tanpa `type: ignore` baru, kecuali satu yang
sudah berlabel dan dijelaskan (overload `transformers.pipeline` yang memang
salah di stub-nya).

- `clone_template()` → `-> dict[str, Any] | None`, dan `marketplace.py` menangani
  `None` secara eksplisit dengan 404.
- Worker sintetis memakai `Protocol` + guard eksplisit dengan pesan aksi, plus
  `attach_engine()`.
- `_SUPPORTED_PROVIDERS` → `dict[str, Callable[[], STTProvider]]`.
- `evaluate_against_vendor_rules()` dan probe-nya menerima `dict[str, Any] | str`.
- `step_executor` menamai dispatch httpx sebagai
  `dict[str, Callable[..., Awaitable[httpx.Response]]]`.
- `EvaluationDimension` memakai `StrEnum` (Python 3.11+, sudah dipakai
  `apps/organization/execution_runtime.py`).
- `proposal_repository` memakai nama variabel terpisah untuk dua tipe proposal.

### 3. Cross-pack reachability = data

`CrossPackBridge` tidak lagi meng-import pack lain. `PACK_ENTRYPOINTS`
memetakan pack ke `(module_path, class_name)`, di-resolve saat dipanggil lewat
`backend.app.runtime.load_app_engine` — loader dinamis yang memang ada untuk
purpose ini tetapi sebelumnya tidak punya pemanggil.

Konsekuensi yang diinginkan:

- `governance_checks` kembali hijau tanpa melemahkan check-nya.
- Menambah pack = satu baris di registry.
- `register_entrypoint()` membuat titik integrasi dapat di-override tanpa
  menyentuh source — dipakai test.

## Konsekuensi

- **Positif:** `governance-check` hijau; `mypy` 0 error dari 20;
  `ruff` 0 error dari 6.
- **Positif:** `/health` dan `/` melaporkan versi yang benar dan Explainability
  sumbernya.
- **Positif:** `clone_template()` tidak lagi bisa mengembalikan `None` ke
  pemanggil yang mengindeks langsung.
- **Positif:** worker sintetis gagal dengan pesan yang bisa ditindaklanjuti.
- **Negatif:** `resolve_version()` membaca `pyproject.toml` saat import pada
  source checkout. Dibiarkan kecil dan di-memoize; image container memakai
  metadata atau `ECP_VERSION`.
- **Negatif:** `PACK_ENTRYPOINTS` masih menyebut modul pack secara tekstual.
  Itu trade-off yang disengaja: coupling menjadi data yang dapat di-override,
  bukan import edge yang tidak terlihat.
- **Catatan:** checker `capability_first_rule` hanya memindai
  `CAPABILITY_PACKS`. `apps/integration`, `apps/society`, dan
  `apps/organization` tidak ada di daftar itu, sehingga cross-pack import di
  `orchestrator.py` dan `society.py` **tidak** dilaporkan. Itu lubang governance
  yang nyata dan ditangani terpisah (lihat Residual).

## Residual

1. `apps/integration/orchestrator.py` meng-import `apps.trading_analyst` dan
   `apps.network_engineer` secara langsung dan lolos dari
   `capability_first_rule` karena `integration` tidak terdaftar di
   `CAPABILITY_PACKS`..  perlu keputusan apakah `integration`/`society`/
   `organization` memang di luar cakupan aturan.
2. Healthcheck CoreDNS hanya memverifikasi binary dan plugin set, bukan
   resolusi DNS — image `coredns/coredns` tidak punya shell. Probe DNS sungguhan
   harus dijalankan dari container lain.

## Referensi

- `backend/app/core/platform_version.py`
- `backend/app/core/config.py`
- `apps/self_development/cross_pack_bridge.py`
- `docs/audit/COMPREHENSIVE_AUDIT_2026-10-04.md`
- ADR-037: Local GPU Inference Provider
- ADR-038: Relokasi Market Feed Adapter ke Trading Analyst Pack