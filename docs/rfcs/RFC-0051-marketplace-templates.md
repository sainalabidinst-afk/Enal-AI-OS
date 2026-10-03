# RFC-0051: Marketplace & Templates

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Frontend Platform
**Canonical Owner:** Lead Platform Engineer
**Terakhir Diverifikasi:** 2026-10-03
**Versi:** 1.0.0
**Status:** Draft → Proposed
**SSOT:** Rancangan marketplace untuk berbagi dan menemukan agent/tool templates, dengan cloning, analytics, dan sharing controls
<!-- DOCUMENT_METADATA_END -->

## Abstrak

RFC ini mendefinisikan Marketplace & Templates untuk ECP, yang memungkinkan user berbagi, menemukan, dan meng-clone agent/tool templates. Marketplace ini mendukung visibility controls (private/internal/public), analytics (clones, views, trials), dan dependency resolution saat cloning.

## Konteks

ECP memerlukan cara untuk:
1. Share agent/tool ke marketplace
2. Discover templates dari marketplace
3. Clone templates ke project sendiri
4. Track analytics (clones, views, trials)
5. Control visibility (private/internal/public)

## Keputusan

### 1. Marketplace Service

**Core Components:**
- `MarketplaceService` — Manage shared agents/tools
- `TemplateRegistry` — Pre-built templates
- `SharingService` — Share/unshare agents
- `CloningService` — Clone agents with dependency resolution
- `AnalyticsService` — Track clones, views, trials

### 2. Visibility Model

| Visibility | Description |
|------------|-------------|
| `private` | Only owner can access |
| `internal` | Team members can access |
| `public` | Everyone can access |

### 3. Sharing Flow

1. User clicks "Share" on agent/tool
2. Select visibility + allowed roles + allow clone
3. System generates share link
4. Recipient can view/clone based on permissions

### 4. Cloning Flow

1. User browses marketplace
2. Clicks "Clone" on template
3. Select target project
4. System resolves dependencies
5. Creates copy in user's project

### 5. Analytics

Track:
- Views per template
- Clones per template
- Trials per template
- Rating per template

### 6. Frontend Route

`/marketplace` — `MarketplacePage` rendering `Marketplace`

## Implementasi

### Frontend Components

- `Marketplace.tsx` — Browse templates
- `TemplateCard.tsx` — Template preview card
- `CloneWizard.tsx` — Guided cloning flow
- `ShareDialog.tsx` — Share agent dialog

### Backend Modules

- `backend/app/core/marketplace_service.py` — MarketplaceService
- `backend/app/api/marketplace.py` — API endpoints

## Dependencies

- RFC-0046: Visual Builder Foundation
- RFC-0047: Visual Agent Builder
- RFC-0048: Visual Tool Builder

## Testing

- TypeScript: 0 errors
- Ruff: 0 errors
- Mypy: 0 errors

## References

- SimplAI Marketplace: https://simplai.ai/docs/templates-and-marketplace/
