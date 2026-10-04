# Android Release Plan — Enal AI OS

## Stage 1 — PWA (v3.1.0-rc2 Developer Preview)
- [x] manifest.json
- [x] Service Worker (`public/sw.js`)
- [x] Service Worker registration in `app-client.tsx`
- [x] PWA metadata in `layout.tsx`
- [x] Add PWA icons (`/public/icons/`)
- [x] Add screenshots for store listing
- [ ] Test Add to Home Screen on Android
- [ ] Test offline caching
- [ ] Test push notifications

## Stage 2 — React Native / Expo (v3.2.0 Beta)
- [x] Project structure created (`enal-ai-os-mobile/`)
- [x] Expo config (`app.json`, `package.json`, `babel.config.js`, `metro.config.js`)
- [x] TypeScript + NativeWind setup (`tsconfig.json`, `tailwind.config.js`, `nativewind-env.d.ts`)
- [x] API bridge (`src/api/client.ts`, `src/api/endpoints.ts`)
- [x] Auth flow (`LoginScreen`, token storage, auth-aware navigation)
- [x] Common components (`Button`, `Card`, `Loader`)
- [x] Chat UI ported (`ChatScreen`, `MessageBubble`, `InputBar`)
- [x] Chat API integration (real backend calls to `/api/v1/chat`)
- [x] ConsentDialog component
- [x] Observability components (`TraceList`, `LogViewer`)
- [x] Hooks (`useConsentDialog`, `useSTT`, `useTTS`)
- [x] Navigation (`AppNavigator`, `routes`)
- [x] Screens (`Home`, `Chat`, `Observability`, `Settings`, `Login`)
- [x] Styles + utilities (`tailwind.ts`, `storage.ts`)
- [x] Install dependencies (`npm install` in `enal-ai-os-mobile/`)
- [x] Expo dev server running on port 8081
- [ ] Test on Android emulator
- [ ] Firebase Test Lab integration
- [ ] QA checklist: chat, consent, observability, STT/TTS

## Stage 4 — Robotics & Edge AI (v3.4.0)
- [x] Pillar 1 RFC (`docs/rfcs/RFC-0056-robotics-edge-integration.md`)
- [x] Pillar 1 design notes (`docs/pillar1/design/`)
- [ ] Edge Runtime subset implementation
- [ ] ROS 2 Connector integration
- [ ] Vision Engine (YOLO/OpenCV/TensorRT)
- [ ] Smart Agri Connector
- [ ] Edge device testing (ESP32, Raspberry Pi 5, Jetson Nano)

## Stage 5 — Decision Intelligence & Digital Twin (v3.5.0)
- [x] Pillar 2 RFC (`docs/rfcs/RFC-0057-decision-intelligence-simulation.md`)
- [x] Pillar 2 design notes (`docs/pillar2/design/`)
- [ ] Digital Twin Engine implementation
- [ ] Scenario Simulator + Monte Carlo Runner
- [ ] Red Team Agent + Hardening Loop
- [ ] Causal Reasoner + Do-Calculus Engine
- [ ] Backend endpoints `/api/v1/simulation/*`, `/api/v1/causal/*`

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
1. Perform physical device testing for PWA (Add to Home Screen & offline caching)
2. Run Android Emulator / Firebase Test Lab for Expo React Native mobile app
3. Finalize Google Play Console configuration for Stage 3 Native Android build
