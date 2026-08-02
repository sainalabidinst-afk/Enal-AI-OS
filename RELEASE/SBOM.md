<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `RELEASE/SBOM.md`
- Judul: Sbom
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Enal AI OS â€” SBOM v1.0.0-rc1

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Documentation for SBOM
<!-- DOCUMENT_METADATA_END -->

Generated: 2026-07-31
Commit: 22f581c927454f4577a37af2f5be9beb93b04904
Tag: v1.0.0-rc1
> Terjemahan Indonesia: Dihasilkan: 31-07-2026 Komit: 22f581c927454f4577a37af2f5be9beb93b04904 Tag: v1.0.0-rc1

## Backend Dependencies

### Production
| Package | Version | Source |
|---------|---------|--------|
| fastapi | >=0.109.0 | PyPI |
| uvicorn[standard] | >=0.27.0 | PyPI |
| sqlalchemy | >=2.0.0 | PyPI |
| qdrant-client | >=1.7.0 | PyPI |
| redis | >=5.0.0 | PyPI |
| pydantic | >=2.6.0 | PyPI |
| pydantic-settings | >=2.0.0 | PyPI |
| litellm | >=1.40.0 | PyPI |
| langchain-openai | >=0.1.0 | PyPI |
| langchain-core | >=0.1.0 | PyPI |
| httpx | >=0.26.0 | PyPI |
| pyyaml | >=6.0 | PyPI |
| aiohttp | >=3.9.0 | PyPI |
| python-multipart | >=0.0.9 | PyPI |
| psycopg2-binary | >=2.9.0 | PyPI |

### Development
| Package | Version | Source |
|---------|---------|--------|
| pytest | >=8.0.0 | PyPI |
| pytest-asyncio | >=0.23.0 | PyPI |
| ruff | >=0.4.0 | PyPI |
| black | >=24.4.0 | PyPI |
| mypy | >=1.8.0 | PyPI |
| httpx2 | >=2.0.0 | PyPI |

## Frontend Dependencies

### Production
| Package | Version | Source |
|---------|---------|--------|
| next | 14.2.0 | npm |
| react | ^18.2.0 | npm |
| react-dom | ^18.2.0 | npm |
| lucide-react | ^0.378.0 | npm |
| zustand | ^5.0.14 | npm |

### Development
| Package | Version | Source |
|---------|---------|--------|
| @types/node | ^20.11.0 | npm |
| @types/react | ^18.2.0 | npm |
| @types/react-dom | ^18.2.0 | npm |
| autoprefixer | ^10.4.0 | npm |
| postcss | ^8.4.0 | npm |
| tailwindcss | ^3.4.0 | npm |
| typescript | ^5.3.0 | npm |

## Container Images

| Service | Base Image | Version |
|---------|-----------|---------|
| backend | python:3.11-slim | 3.11-slim |
| frontend | node:20-alpine | 20-alpine |
| postgres | postgres:16-alpine | 16-alpine |
| redis | redis:7-alpine | 7-alpine |
| qdrant | qdrant/qdrant | v1.9.0 |
| ollama | ollama/ollama | latest |

## Notes

- Backend uses multi-stage Docker build to minimize attack surface
- Frontend uses Next.js standalone output for minimal production bundle
- All container images run as non-root users
- Production dependencies exclude dev/test packages
