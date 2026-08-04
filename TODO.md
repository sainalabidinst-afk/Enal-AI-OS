# UX v2 — Navigation & User Experience

**Scope:** Presentation-layer only. No backend, API, contracts, capability packs, or Core changes.

**Goal:** Splash → Login → EULA → Dashboard (App Launcher) → Capability Pack (apps)

---

## Phase 1 — Navigation & UX

- [ ] 1. EULA types (`frontend/types/eula.ts`)
- [ ] 2. EULA store (`frontend/store/eula-store.ts`) — `accepted_eula`, `accepted_version`, `accepted_at`
- [ ] 3. EULA page (`frontend/app/eula/page.tsx` + `frontend/components/eula/eula-page.tsx`)
- [ ] 4. Splash screen routing (`frontend/app/page.tsx`) — route by auth + EULA state
- [ ] 5. Reusable App Launcher (capability registry + capability card)
- [ ] 6. Dashboard = App Launcher grid (`frontend/components/dashboard/dashboard-page.tsx`)
- [ ] 7. Search / Favorites / Recent in launcher
- [ ] 8. Update `MainLayout` (EULA guard + apps nav)
- [ ] 9. Update `LoginForm` (redirect to EULA after login)

## Phase 2 — App Shell (placeholders only)

- [ ] 10. Shared AppShell component (`frontend/components/apps/app-shell.tsx`)
- [ ] 11. `/apps/trading` shell
- [ ] 12. `/apps/network` shell
- [ ] 13. `/apps/code` shell
- [ ] 14. `/apps/security` shell
- [ ] 15. `/apps/database` shell
- [ ] 16. `/apps/research` shell
- [ ] 17. `/apps/devops` shell
- [ ] 18. `/apps/business` shell
- [ ] 19. `/apps/architect` shell
- [ ] 20. `/apps/decision` shell
- [ ] 21. `/apps/self-development` shell

## Verification

- [ ] `npm run build` passes (no TS errors)
- [ ] Manual test: login → EULA → dashboard → click app icon
