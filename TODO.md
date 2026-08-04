# UX v2 — Navigation & User Experience

**Scope:** Presentation-layer only. No backend, API, contracts, capability packs, or Core changes.

**Goal:** Splash → Login → EULA → Dashboard (App Launcher) → Capability Pack (apps)

---

## Phase 1 — Navigation & UX

- [x] 1. EULA types (`frontend/types/eula.ts`)
- [x] 2. EULA store (`frontend/store/eula-store.ts`) — `accepted_eula`, `accepted_version`, `accepted_at`
- [x] 3. EULA page (`frontend/app/eula/page.tsx` + `frontend/components/eula/eula-page.tsx`)
- [x] 4. Splash screen routing (`frontend/app/page.tsx`) — route by auth + EULA state
- [x] 5. Reusable App Launcher (capability registry + capability card)
- [x] 6. Dashboard = App Launcher grid (`frontend/components/dashboard/dashboard-page.tsx`)
- [x] 7. Search / Favorites / Recent in launcher
- [x] 8. Update `MainLayout` (EULA guard + apps nav)
- [x] 9. Update `LoginForm` (redirect to EULA after login)

## Phase 2 — App Shell (placeholders only)

- [x] 10. Shared AppShell component (`frontend/components/apps/app-shell.tsx`)
- [x] 11. `/apps/trading` shell
- [x] 12. `/apps/network` shell
- [x] 13. `/apps/code` shell
- [x] 14. `/apps/security` shell
- [x] 15. `/apps/database` shell
- [x] 16. `/apps/research` shell
- [x] 17. `/apps/devops` shell
- [x] 18. `/apps/business` shell
- [x] 19. `/apps/architect` shell
- [x] 20. `/apps/decision` shell
- [x] 21. `/apps/self-development` shell

## Verification

- [x] `npm run build` / `tsc --noEmit` passes (no TS errors, EXIT_CODE=0)
- [ ] Manual test: login → EULA → dashboard → click app icon
