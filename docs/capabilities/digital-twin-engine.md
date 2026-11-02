# Digital Twin Engine Capability Pack

## Ringkasan

Digital Twin Engine menyediakan API gabungan untuk mencerminkan state sistem,
menjalankan simulasi skenario, melakukan audit adversarial, dan menelusuri
relasi kausal. Engine ini mengorkestrasi Scenario Simulator, Adversarial
Testing, dan Cross-Domain Graph.

## Operasi

- `mirror_state(system_state)` menyimpan salinan state dan mengembalikan
  `TwinState`.
- `run_simulation(scenario, parameters, iterations)` menjalankan simulasi
  menggunakan state atau `base_state` yang diberikan. Jumlah iterasi dibatasi
  oleh kontrak simulasi.
- `run_red_team(subject, subject_type)` mengembalikan ringkasan risiko, temuan,
  gate, dan rekomendasi hardening.
- `run_causal_trace(treatment, outcome, conditions)` meminta estimasi efek
  kausal beserta confidence dan counterfactual.
- `get_status()` melaporkan kesehatan mirror dan aktivitas engine.

## Batasan

Simulasi bergantung pada model dan parameter yang diberikan; hasil bukan
prediksi pasti. Temuan red-team dan estimasi kausal perlu ditinjau sebelum
dipakai untuk keputusan operasional.

Kontrak publik berada di `apps/digital_twin_engine/schemas.py`, sedangkan
orchestration ada di `apps/digital_twin_engine/engine.py`.
