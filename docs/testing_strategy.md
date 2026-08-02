# Strategi Testing ECP

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi untuk testing_strategy
<!-- DOCUMENT_METADATA_END -->

ECP menggunakan empat tingkat pengujian untuk memastikan kualitas platform dan keandalan aplikasi.

## Tingkat Test

### Level 1: Unit Tests

**Fokus**: Fungsi dan class individual secara terisolasi.

**Scope**:
- Algoritma inti (reasoning, decision engine, simulation)
- Struktur data (RouterOS parser, model topologi)
- Fungsi utilitas (prompt compiler, cost optimizer)

**Lokasi**: `tests/unit/`

**Contoh**:
```python
def test_routeros_parser():
    config = "/interface\nadd name=ether1 type=ether\n"
    result = parse_routeros_config(config)
    assert len(result.interfaces) == 1
    assert result.interfaces[0].name == "ether1"
```

**Target Coverage**: ≥80%

---

### Level 2: Integration Tests

**Fokus**: Interaksi antar komponen ECP.

**Scope**:
- SDK → Runtime communication
- Plugin → Kernel contracts
- Memory → RAG → World Model
- Event Bus → Task Queue → Workers
- Studio → Observability

**Lokasi**: `tests/integration/`

**Contoh**:
```python
async def test_plugin_contract_compliance():
    plugin = load_plugin("mikrotik")
    assert plugin.validate_contract(ToolContract)
    result = await plugin.invoke({"action": "list_interfaces"})
    assert "interfaces" in result
```

**Target Coverage**: Semua contract boundaries

---

### Level 3: Workflow Tests

**Fokus**: Pipeline kognitif lengkap end-to-end.

**Scope**:
- Perception → Planning → Reasoning → Decision → Action
- Debate engine dengan banyak agen
- Loop Simulation → Verification → Reflection
- Pemilihan pipeline meta-cognition

**Lokasi**: `tests/workflow/`

**Contoh**:
```python
async def test_network_analysis_workflow():
    app = NetworkEngineerApp()
    result = await app.run("Analyze this MikroTik config", {
        "config": sample_config,
        "project_id": "test-001"
    })
    assert result["result"]["analysis"]["issues"] is not None
    assert result["result"]["documentation"] is not None
```

**Target Coverage**: Semua alur kerja aplikasi referensi

---

### Level 4: Reference Application Tests

**Fokus**: Use case dunia nyata dari perspektif pengguna.

**Scope**:
- Perjalanan pengguna lengkap
- Alur kerja multi-langkah
- Integrasi lintas komponen
- Performa di bawah beban realistis

**Lokasi**: `tests/reference/`

**Contoh**:
```python
async def test_network_engineer_e2e():
    app = NetworkEngineerApp()
    
    # 1. Upload config
    config = await load_test_config("isp-backbone.rsc")
    
    # 2. Analyze
    analysis = await app.analyze_config(config)
    assert len(analysis["issues"]) > 0
    
    # 3. Generate improved config
    improved = await app.generate_config(analysis)
    
    # 4. Simulate
    sim = await app.simulate_config(improved)
    assert sim["status"] == "success"
    
    # 5. Document
    docs = await app.generate_documentation(improved)
    assert "# Network Configuration" in docs
    
    # 6. Verify artifacts
    artifacts = await get_artifacts("network-engineer")
    assert len(artifacts) >= 3  # config, analysis, docs
```

**Target Coverage**: 100% perjalanan pengguna aplikasi referensi

---

## Golden Test Suite

Golden test suite adalah **quality gate kanonik** untuk ECP.

**Lokasi**: `benchmarks/golden_test_set.py`

**Kategori**:
1. **Simple Tasks** (50 test) — Reasoning dasar, coding, explanation
2. **Medium Tasks** (50 test) — Desain API, skema database, konfigurasi
3. **Complex Tasks** (50 test) — Aplikasi full-stack, sistem terdistribusi
4. **Domain-Specific** (50 test) — Networking, trading, DevOps, research

**Ambang Kelulusan**: ≥80% (160/200 test)

**Eksekusi**:
- Berjalan di setiap PR melalui CI/CD
- Harus lulus sebelum merge
- Harus lulus sebelum rilis apa pun

---

## Urutan Eksekusi Test

```
Unit Tests
  ↓
Integration Tests
  ↓
Workflow Tests
  ↓
Golden Test Suite
  ↓
Reference Application Tests
```

Kegagalan apa pun di tingkat mana pun menghambat kemajuan.

---

## Benchmark Performa

**Lokasi**: `benchmarks/performance_benchmark.py`

**Metrik**:
| Metrik | Target | Pengukuran |
|--------|--------|-------------|
| Latensi (avg) | <2s | Simple tasks |
| Latensi (p95) | <5s | Medium tasks |
| Efisiensi Token | <500 token/respon | Semua tugas |
| Determinisme | >0.8 | Input sama → output sama |
| Tingkat Keberhasilan | >0.9 | Semua tugas |

---

## Menambahkan Test Baru

1. **Unit**: Tambahkan ke `tests/unit/test_<module>.py`
2. **Integration**: Tambahkan ke `tests/integration/test_<integration>.py`
3. **Workflow**: Tambahkan ke `tests/workflow/test_<workflow>.py`
4. **Golden**: Tambahkan ke `benchmarks/golden_test_set.py` pada kategori yang sesuai
5. **Reference**: Tambahkan ke `tests/reference/test_<app>.py`

Semua test baru harus:
- Memiliki kriteria pass/fail yang jelas
- Berjalan dalam <30 detik
- Bersifat deterministik (tanpa flaky test)
- Menyertakan kasus error

