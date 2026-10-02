# ADR-023: Voice Provider Architecture

<!-- DOCUMENT_METADATA_START -->
**ADR ID:** ADR-023
**RFC:** RFC-0043
**Tanggal:** 2026-10-02
**Status:** Accepted
**Topik:** Arsitektur provider STT/TTS untuk Jenny Voice Interface
<!-- DOCUMENT_METADATA_END -->

# ADR-023: Voice Provider Architecture

## Konteks

ECP memerlukan Speech-to-Text (STT) dan Text-to-Speech (TTS) untuk interaksi suara ala Jenny. Namun, berbagai provider STT/TTS (whisper.cpp, OpenAI Whisper, Piper, ElevenLabs, pyttsx3, browser Web Speech API) memiliki dependensi yang berbeda dan kondisi operasional yang berbeda (local, cloud, offline).

## Keputusan

### Lazy Provider Pattern

STT dan TTS service menggunakan **lazy import pattern** — provider dipilih berdasarkan konfigurasi (`STT_PROVIDER`, `TTS_PROVIDER`) dan modul provider-specific hanya di-import ketika dibutuhkan.

```python
# stt_service.py
class STTService:
    async def transcribe(self, audio_data, language):
        if self._provider == "whisper":
            return await self._transcribe_whisper_cpp(audio_data, language)
        elif self._provider == "openai":
            return await self._transcribe_openai(audio_data, language)
        ...
```

### Fallback Chain

Jika provider utama gagal (mis. whisper.cpp server down), service otomatis fallback ke provider berikutnya:

```
STT: whisper → openai → web_speech (stub)
TTS: pyttsx3 → piper → elevenlabs → openai
```

### Error Handling

- Provider yang tidak dikenali → `ValueError`
- Network error / timeout → `RuntimeError` dengan pesan jelas
- Missing optional dependency → `RuntimeError` dengan instruksi install

## Consequenses

### Positif

- **Registry loadability**: service dapat di-import tanpa provider terpasang
- **Flexibility**: user bisa ganti provider via config, tidak perlu kode berubah
- **Resilience**: fallback chain memastikan voice tetap berfungsi

### Negatif

- **Debugging complexity**: error hanya muncul saat runtime ketika provider dipanggil
- **Cold start latency**: import pertama ke provider mungkin lambat

## Referensi

- RFC-0043: Jenny Voice Interface
- ADR-003: Thin Adapter Pattern
- ADR-004: Business Logic in Domain Services
