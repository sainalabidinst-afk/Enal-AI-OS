# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

Please report security vulnerabilities to security@enal.ai.

Do not report security vulnerabilities through public GitHub issues.

## Security Model

### Plugin Security

Plugins are sandboxed and require explicit permissions:

1. **Capability Declaration**: Plugins must declare required permissions
2. **Policy Check**: Platform validates plugin against security policies
3. **Sandbox Execution**: Plugins run in isolated environments
4. **Approval Workflow**: Privileged plugins require manual approval

### Permission Levels

- `read` — Read data
- `write` — Write data
- `execute` — Execute code/commands
- `deploy` — Deploy to production
- `admin` — Administrative operations
- `network` — Network access
- `system` — System-level access

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
