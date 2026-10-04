<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Platform
**Canonical Owner:** Lead Platform Engineer
**Terakhir Diverifikasi:** 2026-10-04
**Versi:** 1.0.0
**Status:** Accepted
**SSOT:** Kebijakan linting dan formatting untuk ECP
<!-- DOCUMENT_METADATA_END -->

# ADR-041: Ruff Format sebagai SSOT, Black Dihapus dari CI

## Abstrak

Repo ini menggunakan `ruff` untuk lint (tercantum di `AGENTS.md` dan `[tool.ruff]`
di `pyproject.toml`). CI `lint` job tetap menjalankan `black --check` secara
paralel, yang bertentangan dengan lint dan tidak pernah di-adopsi sebagai
formatter sehari-hari repo. ADR ini menetapkan `ruff format` sebagai satu-satunya
formatter resmi dan menghapus `black` dari CI.

## Konteks

Repo mengalami ketidaktentuan format yang persisten:

- CI menjalankan `ruff check` + `black --check` secara bersamaan.
- Kedua formatter disagree pada 17–28 file (tergantung path).
- `pyproject.toml` `[tool.black]` ada, tetapi `AGENTS.md` menetapkan
  `python -m ruff format .`.
- Hasilnya, `lint` job CI **tidak pernah hijau** sejak formatter black ditambahkan
  (~530 file sebelum exclude generated dirs, 17 setelah).

Selain itu, ruff mengabaikan pola `extend-exclude` untuk path eksplisit di CLI,
maka CI lint `ruff check backend/app/ benchmarks/ real_cases/ tests/` memindai
`real_cases/` dan menghasilkan 1289 error dari fixture generat. `force-exclude =
true` diperkenankan di ADR-039 untuk memperbaiki hal itu, tetapi hal itu hanya
perbaiki *lint*, bukan *format*.

## Keputusan

1. **Ruff format adalah SSOT formatter.** Semua commit baru harus diformat dengan
   `ruff format .`. Tidak ada formatter lain yang dijalankan di CI.
2. **Black dihapus dari CI dan dari `pyproject.toml`.** Konfigurasi `[tool.black]`
   dihapus. Repo yang sebelumnya diformat black akan direformat ruff dalam satu
   commit besar sebelum tag.
3. **CI `lint` job menjalankan `ruff check . && ruff format --check .`**, bukan
   `ruff check <paths> && black --check <paths>`. Path eksplisit tidak
   diperlukan: ruff membaca konfigurasi dari `pyproject.toml` dan
   `extend-exclude`/`force-exclude` sudah ditetapkan.
4. **`[tool.ruff.format]`** ditambahkan dengan `line-length = 100` agar sama
   dengan `[tool.ruff] line-length` dan konsisten dengan batas yang sudah
   diadopsi di seluruh repo.

## Konsekuensi

- **Positif:** Satu tool untuk lint + format. Pipeline CI lebih sederhana dan
  konsisten dengan `AGENTS.md`.
- **Positif:** `force-exclude = true` pada `[tool.ruff]` membuat exclude untuk
  `real_cases/`, `golden/`, `audit_output/`, dll. berlaku meskipun CI
  menyebutkan path eksplisit.
- **Negatif:** Commit format besar (~28 file) akan bertabrakan dengan sesi
  paralel yang masih aktif. Dieksekusi dengan koordinasi.
- **Negatif:** Developer yang terbiasa black perlu sesi singkat untuk
  `ruff format` sebagai pengganti.

## Perubahan Spesifik

### pyproject.toml

```toml
[tool.ruff]
line-length = 100
target-version = "py311"
force-exclude = true
extend-exclude = [
    "real_cases", "golden", "golden_tests",
    "audit_output", "onboarding_output", "repo_inspect_output*",
    ".kilo", "tools",
]

[tool.ruff.format]
line-length = 100

# [tool.black] dihapus.
```

### CI (.github/workflows/ci.yml)

```yaml
lint:
  steps:
    - run: ruff check .
    - run: ruff format --check .
```

Sebelum:

```yaml
lint:
  steps:
    - run: ruff check backend/app/ benchmarks/ real_cases/ tests/
    - run: black --check backend/app/ benchmarks/ real_cases/ tests/
```

## Referensi

- `AGENTS.md` — `python -m ruff check .` dan `python -m ruff format .`
- ADR-039 — `force-exclude = true` untuk `real_cases/`
- `pyproject.toml` — `[tool.ruff]` existing config
- `.github/workflows/ci.yml` — lint job
