# Pemetaan API

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi frontend untuk API_MAPPING
<!-- DOCUMENT_METADATA_END -->

Dokumen ini memetakan setiap aksi frontend ke panggilan API backend. Tidak ada panggilan API yang tidak terdokumentasi yang diizinkan.

---

## Mengobrol

|Aksi|Metode|Titik akhir|Memminta|Tanggapan|
|--------|--------|----------|---------|----------|
|Kirim pesan|POS|`/api/v1/chat`|`{ message, conversationId?, workspaceId? }`|`ChatResponse`|
|Aliran pesan|POS|`/api/v1/chat/stream`|`{ message, conversationId?, workspaceId? }`|`Stream<ChatEvent>`|
|Ambil riwayat|MENDAPATKAN|`/api/v1/conversations/{conversationId}`| — |`{ messages }`|
|Hapus percakapan|MENGHAPUS|`/api/v1/conversations/{conversationId}`| — |`{ deleted }`|

---

## Ruang kerja

|Aksi|Metode|Titik akhir|Memminta|Tanggapan|
|--------|--------|----------|---------|----------|
|Daftar ruang kerja|MENDAPATKAN|`/api/v1/workspaces`| — |`Workspace[]`|
|Buat ruang kerja|POS|`/api/v1/workspaces`|`{ name, description? }`|`Workspace`|
|Ambil ruang kerja|MENDAPATKAN|`/api/v1/workspaces/{workspaceId}`| — |`Workspace`|
|Daftar file|MENDAPATKAN|`/api/v1/workspaces/{workspaceId}/files`| — |`{ workspaceId, files[] }`|
|Ambil metadata file|MENDAPATKAN|`/api/v1/workspaces/{workspaceId}/files/{filename}`| — |`{ workspaceId, filename, path, size, uploadedAt, metadata }`|
|Tambah file|POS|`/api/v1/workspaces/{workspaceId}/files`|`{ filename, path, size, metadata? }`|`{ workspaceId, filename, path }`|
|Hapus berkas|MENGHAPUS|`/api/v1/workspaces/{workspaceId}/files/{filename}`| — |`{ workspaceId, filename, deleted }`|
|Atur memori|POS|`/api/v1/workspaces/{workspaceId}/memory`|`{ key, value }`|`{ workspaceId, key }`|
|Ambil kenangan|MENDAPATKAN|`/api/v1/workspaces/{workspaceId}/memory/{key}`| — |`{ workspaceId, key, value }`|
|Hapus ruang kerja|MENGHAPUS|`/api/v1/workspaces/{workspaceId}`| — |`{ deleted }`|

---

## Eksekusi

|Aksi|Metode|Titik akhir|Memminta|Tanggapan|
|--------|--------|----------|---------|----------|
|Buat eksekusi|POS|`/api/v1/executions`|`{ goal, conversationId?, workspaceId? }`|`ExecutionSession`|
|Ambil eksekusi|MENDAPATKAN|`/api/v1/executions/{executionId}`| — |`ExecutionSession`|
|Daftar eksekusi|MENDAPATKAN|`/api/v1/executions`|`workspaceId?`|`ExecutionSession[]`|
|Fase tambahan|POS|`/api/v1/executions/{executionId}/phases`|`{ name }`|`ExecutionPhase`|
|Fase pembaruan|tambalan|`/api/v1/executions/{executionId}/phases/{phaseId}`|`{ status, progress? }`|`ExecutionPhase`|
|memperbarui kemajuan|POS|`/api/v1/executions/{executionId}/progress`|`{ progress, etaSeconds? }`|`{ progress, etaSeconds }`|
|Tambah log|POS|`/api/v1/executions/{executionId}/logs`|`{ message, level?, metadata? }`|`LogEntry`|
|Ambil log|MENDAPATKAN|`/api/v1/executions/{executionId}/logs`| — |`{ logs }`|
|Eksekusi Batalkan|POS|`/api/v1/executions/{executionId}/cancel`| — |`{ status, executionId }`|
|Hapus eksekusi|MENGHAPUS|`/api/v1/executions/{executionId}`| — |`{ deleted }`|
|Eksekusi Jalankan|POS|`/api/v1/executions/run`|`{ goal, workspaceId, conversationId? }`|`{ execution, artifacts }`|

---

## Artefak

|Aksi|Metode|Titik akhir|Memminta|Tanggapan|
|--------|--------|----------|---------|----------|
|Daftar artefak|MENDAPATKAN|`/api/v1/artifacts`|`workspaceId?`, `artifactType?`|`Artifact[]`|
|Buat artefak|POS|`/api/v1/artifacts`|`{ workspaceId, name, type, description?, content?, path?, metadata? }`|`Artifact`|
|Ambil artefak|MENDAPATKAN|`/api/v1/artifacts/{artifactId}`| — |`Artifact`|
|Versi Ambil|MENDAPATKAN|`/api/v1/artifacts/{artifactId}/versions/{version}`| — |`ArtifactVersion`|
|Versi tambahan|POS|`/api/v1/artifacts/{artifactId}/versions`|`{ content?, path?, metadata? }`|`Artifact`|
|Pulihkan versi|POS|`/api/v1/artifacts/{artifactId}/restore/{version}`| — |`Artifact`|
|Ambil eksekusi artefak|MENDAPATKAN|`/api/v1/executions/{executionId}/artifacts`| — |`ExecutionArtifact[]`|
|Hapus artefak|MENGHAPUS|`/api/v1/artifacts/{artifactId}`| — |`{ deleted }`|

---

## Kemampuan

|Aksi|Metode|Titik akhir|Memminta|Tanggapan|
|--------|--------|----------|---------|----------|
|Kemampuan mendaftar|MENDAPATKAN|`/api/v1/capabilities`| — |`{ capabilities, domains }`|
|Kemampuan Ambil|MENDAPATKAN|`/api/v1/capabilities/{capabilityId}`| — |`CapabilityDetail`|

---

## Model

|Aksi|Metode|Titik akhir|Memminta|Tanggapan|
|--------|--------|----------|---------|----------|
|Daftar penyedia|MENDAPATKAN|`/api/v1/models/providers`| — |`ModelProviders`|
|Pemeriksaan kesehatan|MENDAPATKAN|`/api/v1/models/health`|`provider?`|`ProviderHealth`|
|Rute model|POS|`/api/v1/models/route`|`{ taskType, capability, context? }`|`ModelRoute`|

---

## Pemberitahuan

|Aksi|Metode|Titik akhir|Memminta|Tanggapan|
|--------|--------|----------|---------|----------|
|Ambil notifikasi|MENDAPATKAN|`/api/v1/notifications/{recipient}`|`limit?`|`{ notifications }`|
|Tandai dibaca|tambalan|`/api/v1/notifications/{recipient}/read/{notificationId}`| — |`{ read }`|

---

## Acara Streaming

Aliran WebSocket/SSE dari `/api/v1/chat/stream`:

|Tipe Acara|Muatan|
|------------|---------|
|`final`|`{ type: 'final', message, conversationId, domain, intent }`|
|`execution_started`|`{ type: 'execution_started', executionId, goal }`|
|`phase`|`{ type: 'phase', phaseId, name, status }`|
|`task`|`{ type: 'task', taskId, name, status }`|
|`log`|`{ type: 'log', level, message }`|
|`artifact`|`{ type: 'artifact', artifactId, name, artifactType }`|
|`progress`|`{ type: 'progress', progress, etaSeconds? }`|
|`execution_complete`|`{ type: 'execution_complete', executionId, progress }`|
|`error`|`{ type: 'error', message }`|
