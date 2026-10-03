# Android Release Plan — Enal AI OS

## Stage 1 — PWA (v3.1.0-rc2 Developer Preview)
- [x] manifest.json
- [x] Service Worker (`public/sw.js`)
- [x] Service Worker registration in `app-client.tsx`
- [x] PWA metadata in `layout.tsx`
- [ ] Add PWA icons (`/public/icons/`)
- [ ] Add screenshots for store listing
- [ ] Test Add to Home Screen on Android
- [ ] Test offline caching
- [ ] Test push notifications

## Stage 2 — React Native / Expo (v3.2.0 Beta)
- [x] Project structure created (`enal-ai-os-mobile/`)
- [x] Expo config (`app.json`, `package.json`, `babel.config.js`, `metro.config.js`)
- [x] TypeScript + NativeWind setup (`tsconfig.json`, `tailwind.config.js`, `nativewind-env.d.ts`)
- [x] API bridge (`src/api/client.ts`, `src/api/endpoints.ts`)
- [x] Common components (`Button`, `Card`, `Loader`)
- [x] Chat UI ported (`ChatScreen`, `MessageBubble`, `InputBar`)
- [x] ConsentDialog component
- [x] Observability components (`TraceList`, `LogViewer`)
- [x] Hooks (`useConsentDialog`, `useSTT`, `useTTS`)
- [x] Navigation (`AppNavigator`, `routes`)
- [x] Screens (`Home`, `Chat`, `Observability`, `Settings`)
- [x] Styles + utilities (`tailwind.ts`, `storage.ts`)
- [ ] Install dependencies (`npm install` in `enal-ai-os-mobile/`)
- [ ] Test on Android emulator
- [ ] Firebase Test Lab integration
- [ ] QA checklist: chat, consent, observability, STT/TTS

## Stage 3 — Native Android (v3.3.0 Stable)
- [ ] Setup Kotlin/Jetpack Compose project
- [ ] Implement offline AI module
- [ ] Native observability integration
- [ ] Consent Manager via Android notifications
- [ ] Performance optimization

## Stage 4 — Distribution & Governance (v3.4.0 Enterprise)
- [ ] Google Play Console setup
- [ ] Internal testing track
- [ ] Closed beta track
- [ ] Production release
- [ ] Mobile observability dashboard
- [ ] Compliance audit (GDPR/ISO)

## CI/CD Pipeline
- [x] `.github/workflows/android-ci.yml` created
- [ ] Configure GitHub Secrets (keystore, Play Console)
- [ ] Setup Firebase Test Lab
- [ ] Configure Slack/Teams notifications
- [ ] Setup Datadog/Grafana observability

## Next Steps
1. Add PWA icons to `frontend/public/icons/`
2. Test PWA on Android device
3. Initialize Expo project for Stage 2
