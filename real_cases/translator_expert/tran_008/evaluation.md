# Evaluation

Scenario: translator-008 - Domain Glossary Enforcement (Finance)

## Translation Review
- Finance glossary terms enforced (portofolio, volatilitas, diversifikasi, ekuitas, derivatif, obligasi)
- Custom terms (ekuitas, derivatif, obligasi) correctly override defaults
- No English terms remaining in financial output
- Confidence score exceeds threshold due to glossary use

## Improvements
- Expand finance glossary to 100+ terms per language pair
- Add fuzzy matching for glossary term variants
- Implement glossary term prioritization (domain-specific vs. general)
- Add glossary import/export functionality
