# ADR-001: Arsitektur Bus Acara


**Status:** ✅ Diterima
**Tanggal:** 2024
**Pengambilan Keputusan:** Kepala Arsitek, Tim Teknik

---

## Konteks

Platform Kognitif Enal memerlukan komunikasi lintas modul antara:
- Paket Kemampuan (Insinyur Jaringan, Insinyur Kode, dll.)
- Layanan inti (memori, eksekusi, telemetri)
- Lapisan orkestrasi
- Bagian depan

Impor langsung antar modul akan menciptakan hubungan erat dan ketergantungan melingkar.

---

## Keputusan

Gunakan pola **Bus Peristiwa** ringkasan untuk semua komunikasi lintas modul.

### Pendekatan yang Dipilih

- Pola Publikasikan-Berlangganan melalui `event_bus.py`
- Emisi peristiwa asinkron menggunakan `asyncio`
- Skema acara yang diketik dengan validasi Pydantic
- Instansiasi tunggal yang malas untuk menghindari impor melingkar saat memuat modul

### Desain Kunci

```python
class EventBus:
    _subscribers: dict[str, list[Callable]]
    
    async def publish(self, event_type: str, data: Any) -> None
    def subscribe(self, event_type: str, handler: Callable) -> None
```

---

## Alternatif yang Dipertimbangkan


|Alternatif|Alasan Ditolak|
|-------------|-----------------|
|Panggilan fungsi langsung|Menciptakan hubungan erat antar modul|
|Komunikasi RPC/HTTP|Jaringan overhead yang tidak diperlukan untuk komunikasi dalam proses|
|Keadaan global yang bisa berubah|Tidak aman untuk thread, sulit untuk diuji|
|Pesan Antrean (Redis Pub/Sub)|Tersedia tetapi disediakan untuk komunikasi proses|

---

## Lanjutnya

- **Positif:** Penggabungan yang longgar, mudah untuk menambahkan jenis acara baru, dapat diuji melalui pelanggan tiruan
- **Positif:** Pencegahan impor melingkari pola singleton yang malas
- **Negatif:** Alur peristiwa bersifat implisit — memerlukan dokumentasi untuk dilacak
- **Negatif:** Tidak ada waktu kompilasi yang memeriksa kebenaran jenis peristiwa

---

## Kepatuhan

Semua komunikasi lintas modul HARUS menggunakan Event Bus. Impor langsung antara paket kemampuan atau modul inti dilarang tanpa penggantian ADR.
