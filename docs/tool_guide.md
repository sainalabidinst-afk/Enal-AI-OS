<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/tool_guide.md`
- Judul: Tool Guide
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Tool Development Guide

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Documentation for tool_guide
<!-- DOCUMENT_METADATA_END -->

## Creating a Tool

```python
from enal_ai import Tool, EnalAI

enal = EnalAI()

@enal.tool(
    name="my_tool",
    description="Description of what this tool does",
    parameters={
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "Parameter description"},
            "param2": {"type": "integer", "description": "Another parameter"},
        },
        "required": ["param1"],
    },
    sandbox=True,
    permissions=["read", "write"],
)
async def my_tool(param1: str, param2: int = 0):
    # Your tool logic here
    return {"result": f"Processed {param1}"}
```

## Tool Contracts

All tools must implement:
> Terjemahan Indonesia: All alat must implement:
- `invoke(parameters)` â€” Execute tool with parameters
- `get_schema()` â€” Return OpenAI-compatible schema

## Sandboxing

Tools marked with `sandbox=True` run in isolated environment:
> Terjemahan Indonesia: Alat marked dengan sandbox=True run dalam isolated environment:
- No direct filesystem access
- No network access (unless explicitly allowed)
- Resource limits enforced

## Permissions

Tools require explicit permissions:
> Terjemahan Indonesia: Alat require explicit permissions:
- `read` â€” Read data
- `write` â€” Write data
- `execute` â€” Execute code/commands
- `deploy` â€” Deploy to production
- `admin` â€” Administrative operations

## Best Practices

- Keep tools single-purpose
- Validate all inputs
- Return structured output
- Document parameters thoroughly
- Use appropriate permissions
