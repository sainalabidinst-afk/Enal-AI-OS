# ADR-030: Voice Agent Enhancements Architecture

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Frontend Platform
**Canonical Owner:** Lead Platform Engineer
**Terakhir Diverifikasi:** 2026-10-03
**Versi:** 1.0.0
**Status:** Accepted
**SSOT:** Arsitektur enhancements untuk Voice Agent: telephony, STT/TTS providers, latency monitoring
<!-- DOCUMENT_METADATA_END -->

## Abstrak

ADR ini mendokumentasikan keputusan arsitektur untuk Voice Agent enhancements, termasuk telephony integration, multi-provider STT/TTS, dan latency monitoring.

## Konteks

ECP sudah memiliki VoiceAgent skeleton (RFC-0043), tetapi perlu enhancements untuk production-ready voice agent.

## Keputusan

### 1. Telephony Integration

**Decision:** Twilio sebagai default provider
**Rationale:**
- Market leader untuk cloud communications
- Excellent documentation
- Support untuk inbound/outbound calls

### 2. Multi-Provider STT/TTS

**Decision:** Lazy provider loading
**Rationale:**
- Avoid hard dependencies
- Support multiple providers
- Easy to switch providers

### 3. Latency Monitoring

**Decision:** Track per-stage latency (STT, LLM, TTS)
**Rationale:**
- Identify bottlenecks
- P50/P90/P99 metrics
- Voice-specific observability

## Consequences

### Positive
- Production-ready voice agent
- Multi-provider support
- Detailed latency metrics

### Negative
- Twilio dependency
- Complexity dari multi-provider support

### Neutral
- Uses existing Observability pack untuk metrics

## References

- RFC-0049: Voice Agent Enhancements
- RFC-0043: Jenny Voice Interface
