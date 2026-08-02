<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `SECURITY.md`
- Judul: Security
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Security Policy

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Documentation for SECURITY
<!-- DOCUMENT_METADATA_END -->

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

Please report security vulnerabilities to sainal.abidin.st@gmail.com
> Terjemahan Indonesia: Please report keamanan vulnerabilities untuk sainal.abidin.st@gmail.com

Do not report security vulnerabilities through public GitHub issues.
> Terjemahan Indonesia: Do not report keamanan vulnerabilities through public GitHub issues.

## Security Model

### Plugin Security

Plugins are sandboxed and require explicit permissions:
> Terjemahan Indonesia: Plugins adalah sandboxed dan require explicit permissions:

1. **Capability Declaration**: Plugins must declare required permissions
2. **Policy Check**: Platform validates plugin against security policies
3. **Sandbox Execution**: Plugins run in isolated environments
4. **Approval Workflow**: Privileged plugins require manual approval

### Permission Levels

- `read` â€” Read data
- `write` â€” Write data
- `execute` â€” Execute code/commands
- `deploy` â€” Deploy to production
- `admin` â€” Administrative operations
- `network` â€” Network access
- `system` â€” System-level access

### Security Best Practices

- Never run plugins with more permissions than required
- Always validate plugin manifests
- Use sandbox execution for untrusted code
- Audit plugin dependencies regularly
- Keep runtime and kernel up to date

## Data Protection

- All data stored in workspace is isolated per project
- Sensitive data (API keys, credentials) stored in encrypted vault
- Audit logs for all privileged operations
- Regular security scans of dependencies

## Incident Response

1. **Detection**: Automated monitoring for anomalies
2. **Containment**: Isolate affected components
3. **Eradication**: Remove malicious code
4. **Recovery**: Restore from clean backups
5. **Post-mortem**: Document and improve
