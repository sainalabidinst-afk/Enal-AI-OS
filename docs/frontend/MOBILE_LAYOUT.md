<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/frontend/MOBILE_LAYOUT.md`
- Judul: Mobile Layout
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Mobile Layout

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Frontend documentation for MOBILE_LAYOUT
<!-- DOCUMENT_METADATA_END -->

This document defines responsive behavior for v1 screens. Mobile is a first-class target, not an afterthought.
> Terjemahan Indonesia: Ini dokumen defines responsive behavior untuk v1 screens. Mobile adalah sebuah first-class target, not sebuah afterthought.

---

## Breakpoints

| Name | Width | Layout |
|------|-------|--------|
| Mobile | < 640px | Full-screen panels, bottom navigation |
| Tablet | 640px - 1024px | Collapsible sidebar, wider panels |
| Desktop | > 1024px | Fixed sidebar, multi-panel layout |

---

## Screen Behaviors

### Chat

| Behavior | Mobile | Tablet | Desktop |
|----------|--------|--------|---------|
| Sidebar | Hidden (bottom sheet) | Collapsible left | Fixed left |
| Message width | Full width | 90% | 70% |
| PromptBox | Full width, bottom-fixed | Centered, bottom | Centered, bottom |
| ProgressCard | Full width, compact | Full width | Inline with messages |
| ArtifactCard | Full width | Full width | Inline, max 60% |

### Workspace

| Behavior | Mobile | Tablet | Desktop |
|----------|--------|--------|---------|
| Sidebar | Bottom sheet | Collapsible left | Fixed left |
| Tabs | Horizontal scroll | Horizontal scroll | Full tabs |
| File list | Full width cards | List + preview | List + preview |
| Artifact grid | 1 column | 2 columns | 3 columns |

### Artifact Viewer

| Behavior | Mobile | Tablet | Desktop |
|----------|--------|--------|---------|
| Layout | Full screen overlay | Split view | Split view |
| Version selector | Bottom sheet | Inline dropdown | Inline dropdown |
| Action buttons | Bottom bar | Top bar | Top bar |

### Approval Dialog

| Behavior | Mobile | Tablet | Desktop |
|----------|--------|--------|---------|
| Position | Bottom sheet | Center modal | Center modal |
| Button layout | Stacked | Side by side | Side by side |
| Risk indicator | Colored bar | Colored badge | Colored badge |

### Execution History

| Behavior | Mobile | Tablet | Desktop |
|----------|--------|--------|---------|
| List | Full width cards | Compact list | Compact list |
| Detail | Full screen slide | Slide panel | Inline expand |
| Timeline | Vertical | Vertical | Horizontal or vertical |

---

## Touch Targets

All interactive elements must have minimum touch target of 44x44px on mobile.
> Terjemahan Indonesia: All interactive elements must memiliki minimum touch target dari 44x44px pada mobile.

| Element | Size |
|---------|------|
| Send button | 44x44px |
| Approval buttons | 44px height, full width |
| Artifact cards | Full width tap target |
| Tab bar | Fixed bottom, 48px height |
| Sidebar toggle | 44x44px |

---

## Typography Scaling

| Token | Mobile | Tablet | Desktop |
|-------|--------|--------|---------|
| `--font-size-md` | 14px | 15px | 16px |
| `--font-size-lg` | 16px | 18px | 20px |
| `--font-size-xl` | 20px | 22px | 24px |

---

## Performance

| Metric | Target |
|--------|--------|
| First Contentful Paint | < 1.5s on 3G |
| Time to Interactive | < 3s on 3G |
| Bundle size | < 200KB gzipped |
| Images | Lazy load, WebP, responsive srcset |

---

## Offline Behavior

| State | UI Behavior |
|-------|-------------|
| Offline | Show offline banner. Queue messages for retry. |
| Reconnecting | Show "Reconnecting..." banner. |
| Sync failed | Show error with retry button. |
