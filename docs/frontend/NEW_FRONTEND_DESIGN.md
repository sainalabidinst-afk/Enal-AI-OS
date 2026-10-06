# Rancangan Frontend Baru — Enal Cognitive Platform

## Ringkasan

Frontend baru dirancang untuk **mencerminkan penuh domain backend**: governance, trading, evaluation, observability, security, capability packs, blueprint builder, voice, dan marketplace provider. Tidak ada lagi menu ganda, setiap halaman memiliki komponen jelas, dan seluruh data mengalir dari backend nyata tanpa mock.

Versi ini juga memasukkan **fitur enterprise tambahan** yang memperkuat ekosistem ECP tanpa mengubah fondasi arsitektur.

---

## 1. Tech Stack

| Layer | Pilihan | Alasan |
|-------|---------|--------|
| Framework | Next.js 14 (App Router) | React Server Components, routing, SEO-ready |
| UI | React 18 + TypeScript | Type safety, ecosystem mature |
| Styling | Tailwind CSS + CSS Variables | Desain token tunggal, tema gelap/terang, performa |
| State | Zustand | Ringan, inferensi TypeScript, sesuai arsitektur backend |
| Data Fetching | TanStack Query (React Query) v5 | Caching, background refresh, optimistic updates |
| Charts | Recharts | Candlestick, area, bar untuk trading + metrics |
| Forms | React Hook Form + Zod | Validasi schema konsisten dengan backend |
| Auth | NextAuth.js / JWT manual | Sesuai `/api/v1/auth/login` + token bearer |
| Voice | Web Speech API + backend voice bridge | STT/TTS tanpa SDK eksternal untuk web |

---

## 2. Struktur Direktori

```
frontend/
  src/
    app/
      (auth)/
        login/page.tsx
      layout.tsx
      page.tsx
      dashboard/page.tsx
      trading/page.tsx
      capability-packs/page.tsx
      builder/page.tsx
      evaluation/page.tsx
      benchmark/page.tsx
      marketplace/page.tsx
      voice/page.tsx
      settings/page.tsx
      observability/page.tsx
      governance/page.tsx
      audit-trail/page.tsx
    components/
      layout/
        app-shell.tsx
        sidebar.tsx
        mobile-nav.tsx
        top-bar.tsx
        error-boundary.tsx
      shared/
        metrics-card.tsx
        status-badge.tsx
        loading-skeleton.tsx
        toast.tsx
        confirmation-dialog.tsx
        json-viewer.tsx
      dashboard/
        governance-cards.tsx
        market-feed-widget.tsx
        system-health-panel.tsx
        audit-trail-preview.tsx
      trading/
        market-chart.tsx
        strategy-panel.tsx
        performance-summary.tsx
        trade-history-table.tsx
        regime-badge.tsx
        backtesting-module.tsx
      capability-packs/
        pack-list.tsx
        pack-card.tsx
        pack-detail-panel.tsx
        dependency-graph-viewer.tsx
      builder/
        pack-form.tsx
        capability-editor.tsx
        policy-editor.tsx
        blueprint-import-export.tsx
      evaluation/
        heuristic-table.tsx
        improvement-list.tsx
        benchmark-runner.tsx
        benchmark-history.tsx
      benchmark/
        benchmark-score-grid.tsx
        benchmark-trend-chart.tsx
        benchmark-detail-modal.tsx
      marketplace/
        provider-card-grid.tsx
        provider-status-badge.tsx
        provider-detail-modal.tsx
        provider-health-monitor.tsx
      voice/
        agent-console.tsx
        transcript-viewer.tsx
        context-memory-panel.tsx
      settings/
        user-profile.tsx
        token-scope-viewer.tsx
        security-policy-list.tsx
        api-key-manager.tsx
      observability/
        metrics-dashboard.tsx
        log-viewer.tsx
        tracing-panel.tsx
        alert-rules-notifications.tsx
      governance/
        adr-list.tsx
        adr-detail.tsx
        quality-gate-list.tsx
        quality-gate-detail.tsx
        governance-status-panel.tsx
      audit-trail/
        audit-timeline.tsx
        audit-filter.tsx
        audit-detail-modal.tsx
        pack-progression-panel.tsx
    features/
      auth/
        use-auth.ts
        auth-store.ts
      chat/
        use-chat-stream.ts
        chat-store.ts
      trading/
        use-trading-feed.ts
        use-regime-detection.ts
        trading-store.ts
      execution/
        use-execution.ts
        execution-store.ts
      benchmark/
        use-benchmark.ts
        benchmark-store.ts
      governance/
        use-governance.ts
        governance-store.ts
      notification/
        use-notifications.ts
        notification-store.ts
    services/
      api.ts
      auth.ts
      chat.ts
      trading.ts
      capabilities.ts
      blueprints.ts
      benchmark.ts
      governance.ts
      marketplace.ts
      voice.ts
      telemetry.ts
      observability.ts
      audit.ts
      adr.ts
    stores/
      auth-store.ts
      ui-store.ts
      notification-store.ts
    types/
      auth.ts
      chat.ts
      execution.ts
      trading.ts
      benchmark.ts
      governance.ts
      marketplace.ts
      observability.ts
      api.ts
      adr.ts
      audit.ts
    lib/
      design-tokens.ts
      cn.ts
      api-client.ts
      stream-handler.ts
      error-handler.ts
      markdown-renderer.ts
      benchmark-parser.ts
    providers/
      auth-provider.tsx
      query-provider.tsx
      theme-provider.tsx
```

---

## 3. Arsitektur Komponen

### 3.0 Prinsip Integrasi Fitur Tambahan

Semua fitur tambahan di bawah ini dibangun **di atas arsitektur inti**, bukan memodifikasi fondasi. Mereka menggunakan API/SSE yang sudah ada, menambahkan komponen/halaman baru, dan mengikuti aturan yang sama: frontend sebagai proyeksi state backend, tanpa mock, tanpa logika bisnis.

### 3.1 App Shell

```
AppShell
├── Sidebar (desktop) / MobileNav (ponsel)
│   ├── Logo + Brand
│   ├── SearchBar (global search)
│   ├── NavItem per modul inti + fitur tambahan
│   ├── Divider
│   ├── ThemeToggle (dark/light)
│   └── UserMenu + Logout
├── TopBar
│   ├── Breadcrumb / page title
│   ├── Search trigger (ponsel)
│   └── Notification bell + unread count
├── MainPanel
│   └── {children} (halaman aktif)
├── RBAC Gate (opsional, di atas MainPanel)
└── ErrorBoundary global
```

### 3.1.1 Global Search

- Satu search bar global di sidebar/top bar.
- Mencari: pack, provider, log, blueprint, audit trail.
- Hasil dikelompokkan berdasarkan domain.
- Tekan `Ctrl/Cmd + K` untuk focus.

### 3.1.2 Theme Switcher

- Toggle dark/light mode di sidebar.
- Menggunakan CSS variables + `data-theme` pada root.
- Preferensi disimpan di `localStorage`.

### 3.1.3 Role-Based Access Control (RBAC)

- UI menyesuaikan scope token (`model:read`, `capabilities:execute`, `admin`).
- Menu/hide tombol berdasarkan permission.
- Contoh: tanpa `capabilities:execute`, tombol Execute disembunyikan.

### 3.1.4 Offline Cache Layer

- TanStack Query + IndexedDB untuk caching data observability dan trading feed.
- Auto-refresh saat online.
- Indikator offline di top bar.

### 3.1.5 Plugin System (Future)

- Registry plugin di `lib/plugins/`.
- Integrasi eksternal: Telegram bot, Slack alert, webhook.
- Plugin di-load dinamis sesuai konfigurasi.

---

## 4. Rancangan Halaman per Modul

### 4.0 Modul Tambahan Berdasarkan Roadmap

Berdasarkan README dan TODO, 3 modul tambahan diintegrasikan langsung ke arsitektur inti:

| Menu | Tujuan | Sumber Data |
|------|--------|-------------|
| **Governance Explorer** | Menampilkan ADR, Quality Gates, status governance. | `docs/adr/`, `docs/quality/QUALITY_GATES.md` |
| **Benchmark Dashboard** | Menampilkan skor/benchmark tiap Capability Pack. | `benchmarks/dashboards/*.html` |
| **Audit Trail Viewer** | Menampilkan riwayat eksekusi dan peningkatan pack. | `docs/changelog/`, `benchmarks/logs/` |

---

### 4.1 Dashboard

**Tujuan:** Ringkasan governance, observability, dan status sistem.

**Komponen:**
- `GovernanceCards`: Acceptance Rate, Remediation Success, Compliance Coverage, Avg Response Time.
- `MarketFeedWidget`: BTCUSDT confidence trend (stream dari `/api/v1/trading/feed/stream`).
- `SystemHealthPanel`: status backend, observability metrics.
- `AuditTrailPreview`: 5 aktivitas governance terbaru.

**API Mapping:**
| Data | Method | Endpoint |
|------|--------|----------|
| Metrics | GET | `/api/v1/metrics` |
| Trading regime | GET | `/api/v1/trading/regime/live` |
| System health | GET | `/api/v1/health` |
| Audit trail | GET | `/api/v1/governance/audit` |

### 4.1.1 Audit Trail Viewer (Governance & Compliance)

**Tujuan:** Menampilkan semua aktivitas governance dengan timestamp dan user ID.

**Komponen:**
- `AuditTrailTable`: daftar aktivitas (pack register, evaluation run, capability execute).
- `AuditTrailFilter`: filter by pack_id, user, date range.
- `AuditTrailDetailModal`: detail aktivitas + metadata.

**API Mapping:**
| Data | Method | Endpoint |
|------|--------|----------|
| List audit trail | GET | `/api/v1/governance/audit` |
| Filter by pack | GET | `/api/v1/governance/audit?pack_id={id}` |

### 4.2 Trading Intelligence

**Tujuan:** Chart multi-timeframe, strategi, performance summary.

**Komponen:**
- `MarketChart`: candlestick multi-timeframe (15m, 1h, 4h, 1d).
- `StrategyPanel`: daftar strategi (RSI, EMA, MACD).
- `PerformanceSummary`: win rate, net profit, drawdown.
- `TradeHistoryTable`: entry/exit log.
- `RegimeBadge`: trend/konsolidasi/sideways.
- `BacktestingModule`: form input strategi + tanggal + hasil equity curve + trade list.

**API Mapping:**
| Data | Method | Endpoint |
|------|--------|----------|
| Market analysis | POST | `/api/v1/trading/analyze` |
| Live regime | GET | `/api/v1/trading/regime/live` |
| Feed stream | GET | `/api/v1/trading/feed/stream` |
| Backtest (future) | POST | `/api/v1/trading/backtest` |

### 4.2.1 Backtesting Module (Trading Intelligence)

**Tujuan:** Menjalankan strategi historis dengan data candle lama untuk validasi performa.

**Komponen:**
- `BacktestForm`: input symbol, strategi, date range, initial capital.
- `BacktestResults`: equity curve, trade list, performance metrics.
- `BacktestHistory`: daftar backtest sebelumnya.

**API Mapping:**
| Data | Method | Endpoint |
|------|--------|----------|
| Run backtest | POST | `/api/v1/trading/backtest` |
| List backtest history | GET | `/api/v1/trading/backtest/history` |
| Get backtest result | GET | `/api/v1/trading/backtest/{id}` |

### 4.3 Capability Packs

**Tujuan:** Daftar pack terdaftar, detail, eksekusi capability.

**Komponen:**
- `PackList`: semua pack dari `/api/v1/capabilities` + lifecycle.
- `PackCard`: domain, status, capabilities, health badge.
- `PackDetailPanel`: eksekusi capability (`/api/v1/capabilities/{id}/execute`).
- `DependencyGraphViewer`: visualisasi hubungan antar capability dan pack.

**API Mapping:**
| Data | Method | Endpoint |
|------|--------|----------|
| List capabilities | GET | `/api/v1/capabilities` |
| Capability detail | GET | `/api/v1/capabilities/{id}` |
| Execute capability | POST | `/api/v1/capabilities/{id}/execute` |
| Lifecycle | GET | `/api/v1/capabilities/lifecycle` |

### 4.3.1 Dependency Graph Viewer (Capability Packs)

**Tujuan:** Visualisasi hubungan antar capability dan pack untuk debugging dan optimasi.

**Komponen:**
- `DependencyGraph`: node graph capability (React Flow / D3).
- `GraphControls`: zoom, filter by domain, search capability.
- `GraphDetailPanel`: klik node untuk lihat detail capability.

**API Mapping:**
| Data | Method | Endpoint |
|------|--------|----------|
| Get capability graph | GET | `/api/v1/capabilities` |
| Get dependencies | GET | `/api/v1/capabilities/{id}/dependencies` |

### 4.4 Builder

**Tujuan:** UI untuk membuat/registrasi pack baru.

**Komponen:**
- `PackForm`: nama, domain, capabilities, policy.
- `CapabilityEditor`: skills, dependencies, complexity slider.
- `PolicyEditor`: policy rails, allowed operations.

**API Mapping:**
| Data | Method | Endpoint |
|------|--------|----------|
| Create pack | POST | `/api/v1/governance/packs` |
| List packs | GET | `/api/v1/governance/packs` |
| Create agent blueprint | POST | `/api/v1/blueprints/agent` |
| Create tool blueprint | POST | `/api/v1/blueprints/tool` |

### 4.4.1 Blueprint Import/Export (Builder)

**Tujuan:** Memungkinkan pengguna menyalin atau berbagi blueprint antar environment.

**Komponen:**
- `ExportButton`: export blueprint ke JSON file.
- `ImportDialog`: upload JSON file untuk import.
- `ShareLink`: generate shareable link (opsional).

**API Mapping:**
| Data | Method | Endpoint |
|------|--------|----------|
| Export blueprint | GET | `/api/v1/blueprints/{kind}/{id}/export` |
| Import blueprint | POST | `/api/v1/blueprints/import` |

### 4.5 Evaluation Console

**Tujuan:** Hasil benchmark suite + heuristic scores.

**Komponen:**
- `HeuristicTable`: scalability, cost, compliance, observability, security, accuracy, coherence, completeness, relevance.
- `ImprovementList`: rekomendasi otomatis.
- `BenchmarkRunner`: trigger `/api/v1/benchmark/run`.

**API Mapping:**
| Data | Method | Endpoint |
|------|--------|----------|
| Run benchmark | POST | `/api/v1/benchmark/run` |
| Benchmark suite | GET | `/api/v1/benchmark/suite` |
| Capability scores | GET | `/api/v1/benchmark/capability-scores` |
| CCE status | GET | `/api/v1/benchmark/cce/status` |

### 4.5.1 Benchmark History (Evaluation Console)

**Tujuan:** Menyimpan hasil evaluasi sebelumnya dan menampilkan tren heuristik dari waktu ke waktu.

**Komponen:**
- `BenchmarkHistoryTable`: daftar benchmark run sebelumnya.
- `BenchmarkTrendChart`: line chart tren heuristik per run.
- `BenchmarkComparison`: compare dua run sebelumnya.

**API Mapping:**
| Data | Method | Endpoint |
|------|--------|----------|
| List benchmark history | GET | `/api/v1/benchmark/history` |
| Get benchmark by ID | GET | `/api/v1/benchmark/history/{id}` |
| Compare benchmarks | GET | `/api/v1/benchmark/history/compare` |

### 4.6 Marketplace (Model Providers)

**Tujuan:** Daftar provider AI, status, deskripsi.

**Komponen:**
- `ProviderCardGrid`: OpenAI, Claude, Gemini, Mistral, Cohere, LLaMA, Falcon, Hugging Face.
- `ProviderStatusBadge`: online/offline.
- `ProviderDetailModal`: deskripsi + scope.

**API Mapping:**
| Data | Method | Endpoint |
|------|--------|----------|
| List providers | GET | `/api/v1/models/providers` |
| Provider health | GET | `/api/v1/models/health` |
| Route model | POST | `/api/v1/models/route` |

### 4.6.1 Provider Health Monitor (Marketplace)

**Tujuan:** Menampilkan status uptime dan latency setiap provider AI.

**Komponen:**
- `ProviderHealthGrid`: status uptime, latency, last checked timestamp.
- `ProviderHealthHistory`: line chart latency per provider.
- `ProviderHealthAlerts`: alert jika provider down atau latency tinggi.

**API Mapping:**
| Data | Method | Endpoint |
|------|--------|----------|
| Provider health | GET | `/api/v1/models/health` |
| Provider health history | GET | `/api/v1/models/health/history` |

### 4.7 Voice Agent

**Tujuan:** Input suara → teks → eksekusi capability.

**Komponen:**
- `AgentConsole`: input suara, transcript, eksekusi.
- `TranscriptViewer`: log percakapan.
- `STTControls`: mikrofon toggle.

**API Mapping:**
| Data | Method | Endpoint |
|------|--------|----------|
| Voice stream | GET/POST | `/api/v1/voice/*` (sesuai router) |

### 4.7.1 Context Memory Panel (Voice Agent)

**Tujuan:** Menunjukkan konteks percakapan aktif dan variabel yang sedang digunakan agent.

**Komponen:**
- `ContextMemoryPanel`: daftar variabel konteks (workspace, conversation, goal).
- `VariableEditor`: edit variabel konteks secara real-time.
- `ContextHistory`: riwayat konteks percakapan sebelumnya.

**API Mapping:**
| Data | Method | Endpoint |
|------|--------|----------|
| Get context memory | GET | `/api/v1/voice/context` |
| Update context memory | POST | `/api/v1/voice/context` |

### 4.8 Settings

**Tujuan:** Konfigurasi user, token, scope.

**Komponen:**
- `UserProfile`: username, role.
- `TokenScopeViewer`: scope model:read, capabilities:execute.
- `SecurityPolicyList`: izin per user.

**API Mapping:**
| Data | Method | Endpoint |
|------|--------|----------|
| Current user | GET | `/api/v1/auth/me` |
| Login | POST | `/api/v1/auth/login` |
| Logout | POST | `/api/v1/auth/logout` |

### 4.8.1 API Key Manager (Settings)

**Tujuan:** Mengelola token eksternal (misalnya Binance, OpenAI) dengan enkripsi lokal.

**Komponen:**
- `ApiKeyList`: daftar API key (masked).
- `ApiKeyForm`: add/edit API key dengan enkripsi lokal.
- `ApiKeyScope`: assign scope per key (read, trade, admin).

**API Mapping:**
| Data | Method | Endpoint |
|------|--------|----------|
| List API keys | GET | `/api/v1/settings/api-keys` |
| Create API key | POST | `/api/v1/settings/api-keys` |
| Update API key | PUT | `/api/v1/settings/api-keys/{id}` |
| Delete API key | DELETE | `/api/v1/settings/api-keys/{id}` |

### 4.9 Observability

**Tujuan:** Metrics, logs, tracing.

**Komponen:**
- `MetricsDashboard`: CPU, memory, latency.
- `LogViewer`: JSON logs.
- `TracingPanel`: distributed tracing.

**API Mapping:**
| Data | Method | Endpoint |
|------|--------|----------|
| All metrics | GET | `/api/v1/metrics` |
| Prometheus | GET | `/api/v1/metrics/prometheus` |
| Alerts | GET | `/api/v1/metrics/alerts` |

### 4.9.1 Alert Rules & Notifications (Observability)

**Tujuan:** Sistem alert berbasis threshold dengan notifikasi ke email/webhook.

**Komponen:**
- `AlertRuleForm`: buat rule (metric, threshold, duration, channels).
- `AlertRuleList`: daftar rule aktif.
- `AlertHistory`: log alert yang triggered.
- `NotificationChannelForm`: konfigurasi email/webhook/Telegram/Slack.

**API Mapping:**
| Data | Method | Endpoint |
|------|--------|----------|
| List alert rules | GET | `/api/v1/observability/alert-rules` |
| Create alert rule | POST | `/api/v1/observability/alert-rules` |
| Update alert rule | PUT | `/api/v1/observability/alert-rules/{id}` |
| Delete alert rule | DELETE | `/api/v1/observability/alert-rules/{id}` |
| List alert history | GET | `/api/v1/observability/alert-history` |
| Notification channels | GET/POST | `/api/v1/notifications/*` |

### 4.10 Governance Explorer

**Tujuan:** Menampilkan ADR, Quality Gates, dan status governance untuk developer.

**Komponen:**
- `ADRList`: daftar ADR dari `docs/adr/ADR-*.md`.
- `ADRDetail`: tampilkan isi ADR + metadata.
- `QualityGateList`: 12 quality gates dari `docs/quality/QUALITY_GATES.md`.
- `QualityGateDetail`: status gate, pass/fail, exception process.

**Data Source:**
| Data | Method | Endpoint/Source |
|------|--------|----------|
| ADR list | GET | `/api/v1/governance/adr` |
| ADR detail | GET | `/api/v1/governance/adr/{id}` |
| Quality gates | GET | `/api/v1/governance/quality-gates` |
| Governance status | GET | `/api/v1/governance/status` |

### 4.11 Benchmark Dashboard

**Tujuan:** Menampilkan skor/benchmark tiap Capability Pack dari `benchmarks/dashboards/*.html`.

**Komponen:**
- `BenchmarkScoreGrid`: grid skor per pack (Grade A/B/C/D).
- `BenchmarkTrendChart`: line chart tren skor dari waktu ke waktu.
- `BenchmarkDetailModal`: detail benchmark per pack (parser, reasoning, evidence, compliance, executive_report).

**Data Source:**
| Data | Method | Endpoint/Source |
|------|--------|----------|
| Benchmark dashboard | GET | `/api/v1/benchmark/dashboard` |
| Benchmark history | GET | `/api/v1/benchmark/history` |
| Capability scores | GET | `/api/v1/benchmark/capability-scores` |

### 4.12 Audit Trail Viewer

**Tujuan:** Menampilkan riwayat eksekusi dan peningkatan pack dari `docs/changelog/` dan `benchmarks/logs/`.

**Komponen:**
- `AuditTimeline`: timeline visual aktivitas governance (pack register, evaluation run, capability execute).
- `AuditFilter`: filter by pack_id, user, date range, event type.
- `AuditDetailModal`: detail aktivitas + metadata + linked artifacts.

**Data Source:**
| Data | Method | Endpoint/Source |
|------|--------|----------|
| Audit trail | GET | `/api/v1/governance/audit` |
| Pack progression | GET | `/api/v1/governance/packs/{id}/progression` |
| Changelog | GET | `/api/v1/governance/changelog` |

---

## 5. State Management

### 5.1 Stores

| Store | State | Aksi |
|-------|-------|------|
| `auth-store.ts` | user, token, permissions | login, logout, refresh |
| `ui-store.ts` | sidebarCollapsed, theme, activeModule | toggleSidebar, setTheme |
| `chat-store.ts` | messages, conversationId, streaming | addMessage, setStreaming |
| `trading-store.ts` | symbol, timeframe, regime, feedStatus | setSymbol, setRegime, startFeed, stopFeed |
| `execution-store.ts` | executions, phases, logs, artifacts | addExecution, updatePhase, addLog |
| `benchmark-store.ts` | results, heuristicScores | setResults, runBenchmark |
| `governance-store.ts` | packs, auditTrail | fetchPacks, registerPack |
| `notification-store.ts` | notifications, unreadCount | fetchNotifications, markRead |

### 5.2 API Client

Semua panggilan HTTP lewat `services/api.ts` + `lib/api-client.ts`. Injeksi auth header, penanganan 401, normalisasi error.

### 5.3 Stream Handler

SSE stream dari `/api/v1/chat/stream` dan `/api/v1/trading/feed/stream` ditangani oleh satu `useStream` hook yang update store.

---

## 6. Routing

| Route | Modul | Auth | Catatan |
|-------|-------|------|---------|
| `/login` | Auth | Tidak | Redirect ke `/dashboard` jika sudah login |
| `/` | Dashboard | Tidak | Alias ke `/dashboard` |
| `/dashboard` | Dashboard | Tidak | Ringkasan governance + trading + system health |
| `/trading` | Trading | Tidak | Market chart + strategy + performance |
| `/capability-packs` | Capability Packs | Tidak | Pack list + detail + dependency graph |
| `/builder` | Builder | Tidak | Pack/blueprint form + import/export |
| `/evaluation` | Evaluation | Tidak | Heuristic table + benchmark runner + history |
| `/benchmark` | Benchmark Dashboard | Tidak | Skor/benchmark tiap Capability Pack |
| `/marketplace` | Marketplace | Tidak | Provider cards + health monitor |
| `/voice` | Voice Agent | Tidak | Agent console + transcript + context memory |
| `/settings` | Settings | Tidak | Profile + token scope + API key manager |
| `/observability` | Observability | Tidak | Metrics + logs + tracing + alert rules |
| `/audit-trail` | Audit Trail | Tidak | Governance activity log + pack progression |
| `/governance` | Governance Explorer | Tidak | ADR, Quality Gates, status governance |
| `/search` | Global Search | Tidak | Universal search results |

---

## 7. API Mapping Lengkap

### 7.1 Dashboard

```typescript
// services/dashboard.ts
export async function getDashboardMetrics() {
  return apiClient.get('/api/v1/metrics');
}
export async function getTradingRegime(symbol: string) {
  return apiClient.get('/api/v1/trading/regime/live', { params: { symbol } });
}
export async function getSystemHealth() {
  return apiClient.get('/api/v1/health');
}
```

### 7.2 Trading

```typescript
// services/trading.ts
export async function analyzeMarket(symbol: string, timeframes?: string[]) {
  return apiClient.post('/api/v1/trading/analyze', { symbol, timeframes });
}
export async function startLiveFeed(symbol: string, timeframes?: string[]) {
  return apiClient.post('/api/v1/trading/feed/start', { symbol, timeframes });
}
export async function stopLiveFeed() {
  return apiClient.post('/api/v1/trading/feed/stop');
}
export function getFeedStream(symbol: string) {
  return eventSource(`/api/v1/trading/feed/stream?symbol=${symbol}`);
}
```

### 7.3 Capability Packs

```typescript
// services/capabilities.ts
export async function getCapabilities() {
  return apiClient.get('/api/v1/capabilities');
}
export async function getCapability(id: string) {
  return apiClient.get(`/api/v1/capabilities/${id}`);
}
export async function executeCapability(id: string, payload: { message: string; workspace_id?: string }) {
  return apiClient.post(`/api/v1/capabilities/${id}/execute`, payload);
}
```

### 7.4 Builder

```typescript
// services/blueprints.ts
export async function createAgentBlueprint(data: BlueprintInput) {
  return apiClient.post('/api/v1/blueprints/agent', data);
}
export async function createToolBlueprint(data: ToolBlueprintInput) {
  return apiClient.post('/api/v1/blueprints/tool', data);
}
```

### 7.5 Evaluation

```typescript
// services/benchmark.ts
export async function runBenchmark() {
  return apiClient.post('/api/v1/benchmark/run');
}
export async function getBenchmarkSuite() {
  return apiClient.get('/api/v1/benchmark/suite');
}
export async function getCapabilityScores() {
  return apiClient.get('/api/v1/benchmark/capability-scores');
}
export async function getBenchmarkDashboard() {
  return apiClient.get('/api/v1/benchmark/dashboard');
}
export async function getBenchmarkHistory() {
  return apiClient.get('/api/v1/benchmark/history');
}
```

### 7.5.1 Governance & ADR Explorer

```typescript
// services/adr.ts
export async function getADRList() {
  return apiClient.get('/api/v1/governance/adr');
}
export async function getADRDetail(id: string) {
  return apiClient.get(`/api/v1/governance/adr/${id}`);
}
export async function getQualityGates() {
  return apiClient.get('/api/v1/governance/quality-gates');
}
export async function getGovernanceStatus() {
  return apiClient.get('/api/v1/governance/status');
}
```

### 7.5.2 Audit Trail Viewer

```typescript
// services/audit.ts
export async function getAuditTrail(filters?: { pack_id?: string; user?: string; date_range?: string }) {
  return apiClient.get('/api/v1/governance/audit', { params: filters });
}
export async function getPackProgression(packId: string) {
  return apiClient.get(`/api/v1/governance/packs/${packId}/progression`);
}
export async function getChangelog() {
  return apiClient.get('/api/v1/governance/changelog');
}
```

### 7.6 Marketplace

```typescript
// services/marketplace.ts
export async function getProviders() {
  return apiClient.get('/api/v1/models/providers');
}
export async function getProviderHealth(provider?: string) {
  return apiClient.get('/api/v1/models/health', { params: { provider } });
}
export async function routeModel(taskType: string, capability: string) {
  return apiClient.post('/api/v1/models/route', { taskType, capability });
}
```

### 7.7 Voice

```typescript
// services/voice.ts
export async function startSTT() {
  return apiClient.post('/api/v1/voice/stt/start');
}
export async function sendTranscript(text: string) {
  return apiClient.post('/api/v1/voice/transcript', { text });
}
```

### 7.8 Settings / Auth

```typescript
// services/auth.ts
export async function login(username: string, password: string) {
  return apiClient.post('/api/v1/auth/login', { username, password });
}
export async function getMe() {
  return apiClient.get('/api/v1/auth/me');
}
```

### 7.9 Observability

```typescript
// services/observability.ts
export async function getAllMetrics() {
  return apiClient.get('/api/v1/metrics');
}
export async function getAlerts() {
  return apiClient.get('/api/v1/metrics/alerts');
}
```

---

## 12. Plan Implementasi

### Phase 1 — Fondasi (Week 1)
- Setup Next.js + Tailwind + CSS variables.
- Auth flow: login page, token storage, protected routes.
- App shell: sidebar + top bar + mobile nav + global search + theme switcher.
- API client + error handler + stream handler.
- Base components: `MetricsCard`, `StatusBadge`, `LoadingSkeleton`, `Toast`.
- RBAC gate + offline cache layer.

### Phase 2 — Modul Inti (Week 2)
- Dashboard: metrics + trading regime + system health + audit trail preview.
- Trading: chart, strategy panel, performance summary, feed stream + backtesting module.
- Capability Packs: list + detail + execute + dependency graph viewer.

### Phase 3 — Builder & Evaluation (Week 3)
- Builder: pack form + blueprint CRUD + import/export.
- Evaluation: heuristic table + benchmark runner + benchmark history.
- Benchmark Dashboard: score grid + trend chart + detail modal.
- Governance Explorer: ADR list + quality gates + governance status.

### Phase 4 — Marketplace, Voice, Settings, Observability (Week 4)
- Marketplace: provider cards + health monitor.
- Voice: console + transcript + context memory panel.
- Settings: profile + token scope + API key manager.
- Observability: metrics + logs + tracing + alert rules & notifications.
- Audit Trail Viewer: timeline + filter + pack progression.

### Phase 5 — Integrasi & Polishing (Week 5)
- Plugin system: Telegram bot, Slack alert, webhook.
- Global search: indexing pack, provider, log, blueprint.
- Offline cache: TanStack Query + IndexedDB untuk observability dan trading feed.
- Testing: E2E tests untuk semua modul + fitur enterprise.
- Documentation: user guide + admin guide + API docs.

---

## 13. Mockup Visual (Referensi)

```
┌─────────────┬──────────────────────────────────────────────┐
│ Sidebar     │  TopBar: Dashboard | Breadcrumb | Notif bell │
│             ├──────────────────────────────────────────────┤
│ Dashboard   │                                              │
│ Trading     │  Main Content Area                           │
│ Capability  │  - Halaman aktif sesuai route                │
│ Builder     │  - Setiap modul punya komponen spesifik      │
│ Evaluation  │  - Fitur enterprise di atas inti             │
│ Benchmark   │  - Tanpa duplikasi, tanpa mock               │
│ Marketplace │                                              │
│ Voice       │                                              │
│ Settings    │                                              │
│ Observability│                                             │
│ Governance  │  Fitur Enterprise & Roadmap:                 │
│ Audit Trail │  - Benchmark Dashboard                       │
│             │  - Governance Explorer                       │
│ [Search]    │  - Audit Trail Viewer                        │
│ [Theme]     │  - Backtesting Module                        │
│ [RBAC]      │  - Dependency Graph                          │
│             │  - Blueprint Import/Export                   │
│             │  - Provider Health Monitor                   │
│             │  - Context Memory Panel                      │
│             │  - API Key Manager                           │
│             │  - Alert Rules & Notifications               │
└─────────────┴──────────────────────────────────────────────┘
```

Setiap kartu, tabel, dan chart pada mockup akan diimplementasikan sebagai komponen spesifik di atas, dengan binding langsung ke endpoint backend yang sudah ada. Fitur-fitur enterprise dibangun sebagai modul tambahan di atas arsitektur inti, menjaga fondasi tetap stabil dan future-proof.
