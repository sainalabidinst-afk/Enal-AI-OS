# memulai dengan Enal Cognitive Platform

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi untuk memulai
<!-- DOCUMENT_METADATA_END -->

## Prasyarat

- Python 3.11+
- Docker & Docker Menulis
- pip

## Instalasi

### 1. Gudang Klon

```bash
git clone https://github.com/sainalabidinst-afk/Enal-AI-OS.git
cd Enal-AI-OS
```

### 2. Instal Inti

```bash
pip install -e .
```

### 3. Instal SDK (Opsional)

```bash
cd sdk
pip install -e .
```

### 4. Tes Jalankan

```bash
pytest tests/ -v
# 426 tests passing
```

## Agen Pertama Anda

```python
from enal_ai import Agent

class MyAgent(Agent):
    name = "my-first-agent"
    capabilities = ["custom"]

    async def execute(self, task: str) -> str:
        return f"Processed: {task}"

agent = MyAgent()
result = await agent.run("Your task here")
print(result)
```

## Alur Kerja Pertama Anda (dengan Checkpoint/Resume)

```python
from apps.organization.workflow_executor import WorkflowExecutor

# Buat executor dengan dukungan checkpoint
executor = WorkflowExecutor()

# Eksekusi workflow
result = await executor.execute({"goal": "Configure network"})

# Checkpoint untuk dilanjutkan nanti
checkpoint = await executor.create_checkpoint("work-001")

# Lanjutkan dari checkpoint
await executor.resume_from_checkpoint("work-001")
```

## Saluran Kognitif

```python
# Pipeline lengkap tersedia melalui orchestrator
from backend.app.agents.orchestrator_v2 import AIOrchestrator

orchestrator = AIOrchestrator()
result = await orchestrator.orchestrate_goal("Configure BGP on Cisco router")
```

## Contoh kemampuan

|Kemampuan|Penggunaan|
|------------|-------|
|Insinyur Jaringan|`apps/network_engineer/config_generator.py`|
|Kode Insinyur|`apps/code_engineer/__init__.py`|
|Asisten Peneliti|`apps/research/rag.py`|
|Asisten DevOps|`apps/devops/docker_manager.py`|

## Langkah Berikutnya

1. [Panduan Pengembangan Agent](agent_guide.md)
2. [Ringkasan Arsitektur](architecture.md)
3. [Referensi API](api_reference.md)
4. Jalankan: `pytest tests/reference/ -v` (referensi test suite)
