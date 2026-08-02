# Pengujian Strategi ECP

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 02-08-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi untuk pengujian_strategi
<!-- DOCUMENT_METADATA_END -->

ECP menggunakan empat tingkat pengujian untuk memastikan kualitas platform dan resolusi aplikasi.

## Tes Tingkat

### Tingkat 1: Tes Unit

**Fokus**: Fungsi dan kelas individu secara terlindungi.

**Cakupan**:
- Algoritma inti (penalaran, mesin keputusan, simulasi)
- Struktur data (parser RouterOS, model topologi)
- Fungsi utilitas (kompiler cepat, pengoptimal biaya)

**Lokasi**: `tests/unit/`

**Konto**:
```python
def test_routeros_parser():
    config = "/interface\nadd name=ether1 type=ether\n"
    result = parse_routeros_config(config)
    assert len(result.interfaces) == 1
    assert result.interfaces[0].name == "ether1"
```

**Cakupan Sasaran**: ≥80%

---

### Level 2: Tes Integrasi

**Fokus**: Interaksi antar komponen ECP.

**Cakupan**:
- SDK → Runtime komunikasi
- Plugin → Kontrak kernel
- Memori → RAG → Model Dunia
- Bus Acara → Antrean Tugas → Pekerja
- Studio → Observabilitas

**Lokasi**: `tests/integration/`

**Konto**:
```python
async def test_plugin_contract_compliance():
    plugin = load_plugin("mikrotik")
    assert plugin.validate_contract(ToolContract)
    result = await plugin.invoke({"action": "list_interfaces"})
    assert "interfaces" in result
```

**Cakupan Target**: Semua batasan kontrak

---

### Level 3: Tes Alur Kerja

**Fokus**: Pipeline kognitif lengkap end-to-end.

**Cakupan**:
- Persepsi → Perencanaan → Penalaran → Keputusan → Tindakan
- Mesin debat dengan banyak agen
- Simulasi Loop → Verifikasi → Refleksi
- Pemilihan meta-kognisi saluran pipa

**Lokasi**: `tests/workflow/`

**Konto**:
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

**Cakupan Target**: Semua alur kerja aplikasi referensi

---

### Level 4: Tes Aplikasi Referensi

**Fokus**: Kasus penggunaan dunia nyata dari perspektif pengguna.

**Cakupan**:
- Perjalanan pengguna lengkap
- Alur kerja multi-langkah
- Integrasi lintas komponen
- Performa di bawah beban realistis

**Lokasi**: `tests/reference/`

**Konto**:
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

**Cakupan Target**: 100% perjalanan pengguna aplikasi referensi

---

## Golden Test Suite

Golden Test suite adalah **quality gate kanonik** untuk ECP.

**Lokasi**: `benchmarks/golden_test_set.py`

**Kategori**:
1. **Tugas Sederhana** (50 tes) — Penalaran dasar, coding, penjelasan
2. **Tugas Sedang** (50 tes) — Desain API, skema database, konfigurasi
3. **Tugas Kompleks** (50 tes) — Aplikasi full-stack, sistem terdistribusi
4. **Khusus Domain** (50 tes) — Jaringan, perdagangan, DevOps, penelitian

**Ambang Kelulusan**: ≥80% (tes 160/200)

**Eksekusi**:
- Berjalan di setiap PR melalui CI/CD
- Harus lulus sebelum bergabung
- Harus lulus sebelum rilis apa pun

---

## Tes Urutan Eksekusi

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
|Metrik|Target|pengukuran|
|--------|--------|-------------|
|Latensi (rata-rata)|<2dtk|Tugas sederhana|
|Latensi (p95)|<5 detik|Tugas sedang|
|Token Efisiensi|<500 token/respon|Semua tugas|
|determinisme|>0,8|Masukan sama → keluaran sama|
|Tingkat Keberhasilan|>0,9|Semua tugas|

---

## Menambahkan Test Baru

1. **Unit**: Tambahkan ke `tests/unit/test_<module>.py`
2. **Integrasi**: Tambahkan ke `tests/integration/test_<integration>.py`
3. **Alur Kerja**: Tambahkan ke `tests/workflow/test_<workflow>.py`
4. **Emas**: Tambahkan ke `benchmarks/golden_test_set.py` pada kategori yang sesuai
5. **Referensi**: Tambahkan ke `tests/reference/test_<app>.py`

Semua tes baru harus:
- Memiliki kriteria lulus/gagal yang jelas
- Berjalan dalam <30 detik
- Bersifat deterministik (tanpa flaky test)
- Menyertakan kasus error
