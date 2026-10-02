# Cybersecurity Analyst Capability Pack

**Version:** 2.4.0  
**Target Grade:** A (≥90%)  
**Status:** Proposed  

## Ringkasan

Cybersecurity Analyst Capability Pack menyediakan threat modeling (STRIDE),
vulnerability assessment (CVSS-based), incident detection (baseline deviation), dan
compliance mapping (requirement-coverage analysis) untuk analisis keamanan yang
terukur, terlacak, dan berbasis asumsi eksplisit.

## Kemampuan Inti

1. **Threat Modeling (STRIDE)** — mengidentifikasi ancaman spoofing, tampering,
   repudiation, information disclosure, denial of service, dan elevation of
   privilege dari deskripsi sistem, aset, dan trust boundaries.
2. **Vulnerability Assessment** — mengklasifikasikan kerentanan berdasarkan skor
   CVSS dan menghasilkan rekomendasi remediatasi.
3. **Incident Detection** — mendeteksi anomali dengan membandingkan aktivitas
   saat ini terhadap baseline, serta menganalisis severity alert.
4. **Compliance Mapping** — memetakan bukti ke persyaratan framework
   (ISO 27001, SOC 2, NIST CSF) dan melaporkan persentase cakupan.

## Frameworks Supported

- **ISO 27001** — Information Security Management System (ISMS) controls
- **SOC 2** — Trust Services Criteria (security, availability, confidentiality)
- **NIST CSF** — Identify, Protect, Detect, Respond, Recover functions
- **PCI-DSS** — Payment Card Industry Data Security Standard
- **GDPR** — Data protection and privacy controls

## Integration

- **Konsumsi dari**: Security Engineer (vulnerability scanner, threat modeler),
  Infrastructure Engineer (network architecture review), Cloud Architect (cloud
  security controls)
- **Digunakan oleh**: Compliance Officer, System Architect, DevOps Assistant

## Benchmark

- 10 scenarios across 6 dimensions
- Overall target score: A (≥90%)
- Scenarios: STRIDE threat modeling, vulnerability CVSS classification, incident
  anomaly detection, compliance coverage analysis, missing-input handling, source
  reference traceability, safety boundary enforcement, explainability verification

## Real Cases

10 real cases in `real_cases/cybersecurity_analyst/`

## Changelog

- **2026-10-02**: Initial specification (RFC-0034, ADR-014)
