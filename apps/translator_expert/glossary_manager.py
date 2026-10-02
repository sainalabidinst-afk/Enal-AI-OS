"""
Translator Expert — Glossary Manager module.

Manages domain-specific glossaries (finance, legal, medical, technical, general)
and provides term lookup, replacement, and enforcement pre/post-processing.
"""

from __future__ import annotations

import logging

from apps.translator_expert.schemas import (
    DomainGlossary,
    GlossaryConfig,
)

logger = logging.getLogger(__name__)


class GlossaryManager:
    """
    Provides domain glossary management and enforcement for translations.

    Glossaries are stored as in-memory dictionaries keyed by (domain, language_pair).
    Custom terms can be injected at runtime via GlossaryConfig.
    """

    DEFAULT_GLOSSARIES: dict[DomainGlossary, dict[str, dict[str, str]]] = {
        DomainGlossary.finance: {
            "en→id": {
                "portfolio": "portofolio",
                "yield": "hasil pengembalian",
                "diversification": "diversifikasi",
                "liquidity": "likuiditas",
                "volatility": "volatilitas",
                "equity": "ekuitas",
                "derivative": "derivatif",
                "underwriting": "penempatan",
                "securities": "sekuritas",
                "bond": "obligasi",
            },
            "id→en": {
                "portofolio": "portfolio",
                "likuiditas": "liquidity",
                "volatilitas": "volatility",
                "ekuitas": "equity",
                "derivatif": "derivative",
                "sekuritas": "securities",
                "obligasi": "bond",
            },
            "en→es": {
                "portfolio": "cartera",
                "yield": "rendimiento",
                "diversification": "diversificación",
                "liquidity": "liquidez",
                "volatility": "volatilidad",
                "equity": "capital",
                "derivative": "derivado",
                "securities": "valores",
                "bond": "bono",
            },
            "en→zh": {
                "portfolio": "投资组合",
                "yield": "收益率",
                "diversification": "分散投资",
                "liquidity": "流动性",
                "volatility": "波动性",
                "equity": "权益",
                "derivative": "衍生品",
                "securities": "证券",
                "bond": "债券",
            },
        },
        DomainGlossary.legal: {
            "en→id": {
                "contract": "kontrak",
                "liability": "kewajipan",
                "indemnification": "guguran ganti rugi",
                "jurisdiction": "yurisdiksi",
                "tort": "kesalahan",
                "negligence": "kecuaian",
                "clause": "klausal",
                "stipulation": "perenggan",
                "arbitration": " arbitrase",
                "litigation": "litigasi",
            },
            "id→en": {
                "kontrak": "contract",
                "kewajibawan": "liability",
                "guguran ganti rugi": "indemnification",
                "yurisdiksi": "jurisdiction",
                "klausal": "clause",
                "perenggan": "stipulation",
                "arbitrase": "arbitration",
                "litigasi": "litigation",
            },
            "en→es": {
                "contract": "contrato",
                "liability": "responsabilidad",
                "jurisdiction": "jurisdicción",
                "tort": "delito",
                "negligence": "negligencia",
                "clause": "cláusula",
                "arbitration": "arbitraje",
                "litigation": "litigación",
            },
            "en→zh": {
                "contract": "合同",
                "liability": "责任",
                "jurisdiction": "管辖权",
                "tort": "侵权",
                "negligence": "疏忽",
                "clause": "条款",
                "arbitration": "仲裁",
                "litigation": "诉讼",
            },
        },
        DomainGlossary.medical: {
            "en→id": {
                "diagnosis": "diagnosis",
                "prognosis": "prognosis",
                "contraindication": "kontraindikasi",
                "symptom": "gejala",
                "prescription": "resep",
                "hypertension": "hipertensi",
                "cholesterol": "kolesterol",
                "cardiology": "kardiologi",
            },
            "en→es": {
                "diagnosis": "diagnóstico",
                "prognosis": "pronóstico",
                "contraindication": "contraindicación",
                "symptom": "síntoma",
                "prescription": "receta",
                "hypertension": "hipertensión",
                "cholesterol": "colesterol",
                "cardiology": "cardiología",
            },
            "en→zh": {
                "diagnosis": "诊断",
                "prognosis": "预后",
                "contraindication": "禁忌",
                "symptom": "症状",
                "prescription": "处方",
                "hypertension": "高血压",
                "cholesterol": "胆固醇",
                "cardiology": "心病学",
            },
        },
        DomainGlossary.technical: {
            "en→id": {
                "algorithm": "algoritma",
                "framework": "kerangka kerja",
                "middleware": "perantara",
                "asynchronous": "asinkron",
                "containerization": "kontainerisasi",
                "orchestration": "orkestrapasi",
                "microservices": "mikroservice",
            },
            "en→es": {
                "algorithm": "algoritmo",
                "framework": "marco de trabajo",
                "middleware": "middleware",
                "containerization": "contenerización",
                "orchestration": "orquestación",
            },
            "en→zh": {
                "algorithm": "算法",
                "framework": "框架",
                "middleware": "中间件",
                "asynchronous": "异步",
                "containerization": "容器化",
                "orchestration": "编排",
            },
        },
        DomainGlossary.general: {},
    }

    def __init__(self) -> None:
        self.custom_glossaries: dict[str, dict[str, str]] = {}

    def get_glossary(
        self, domain: DomainGlossary, source_lang: str, target_lang: str
    ) -> dict[str, str]:
        """Get the glossary terms for a domain and language pair."""
        key = f"{source_lang}→{target_lang}"
        domain_glossaries = self.DEFAULT_GLOSSARIES.get(domain, {})
        base = dict(domain_glossaries.get(key, {}))

        custom_key = f"{domain.value}:{key}"
        custom = self.custom_glossaries.get(custom_key, {})
        base.update(custom)
        return base

    def apply_preprocessing(
        self,
        text: str,
        config: GlossaryConfig,
        source_lang: str,
        target_lang: str,
    ) -> tuple[str, list[str]]:
        """Replace glossary terms in source text with tagged placeholders."""
        glossary = self.get_glossary(
            config.domain, source_lang, target_lang
        )
        glossary.update(config.custom_terms)

        used_terms: list[str] = []
        processed = text

        for term in sorted(glossary.keys(), key=len, reverse=True):
            if term in processed:
                placeholder = f"[{term}]"
                if placeholder not in processed:
                    processed = processed.replace(term, placeholder)
                    used_terms.append(term)

        return processed, used_terms

    def apply_postprocessing(
        self,
        translated_text: str,
        config: GlossaryConfig,
        source_lang: str,
        target_lang: str,
    ) -> tuple[str, list[str]]:
        """Replace tagged placeholders with approved target glossary terms."""
        glossary = self.get_glossary(
            config.domain, source_lang, target_lang
        )
        glossary.update(config.custom_terms)

        used_terms: list[str] = []
        processed = translated_text

        for term, target_term in sorted(glossary.items(), key=lambda x: len(x[0]), reverse=True):
            placeholder = f"[{term}]"
            if placeholder in processed:
                processed = processed.replace(placeholder, target_term)
                used_terms.append(target_term)

        return processed, used_terms

    def add_custom_glossary(
        self, domain: DomainGlossary, lang_pair: str, terms: dict[str, str]
    ) -> None:
        """Register custom glossary terms for a domain and language pair."""
        key = f"{domain.value}:{lang_pair}"
        existing = self.custom_glossaries.get(key, {})
        existing.update(terms)
        self.custom_glossaries[key] = existing
        logger.info("Added %d custom terms for %s", len(terms), key)

    def load_from_plugin(self, domain: str, language_pairs: dict[str, dict[str, str]]) -> DomainGlossary:
        """Merge a glossary domain loaded from a marketplace plugin into custom glossaries.

        Args:
            domain: domain name (e.g. 'finance', 'legal')
            language_pairs: dict like {'en→id': {'term': 'translation'}}

        Returns the DomainGlossary enum member the data was registered under.
        """
        try:
            domain_enum = DomainGlossary(domain)
        except ValueError:
            domain_enum = DomainGlossary.general

        for lang_pair, terms in language_pairs.items():
            key = f"{domain_enum.value}:{lang_pair}"
            existing = self.custom_glossaries.get(key, {})
            existing.update(terms)
            self.custom_glossaries[key] = existing
        logger.info(
            "Loaded %d language pairs for domain '%s' from plugin",
            len(language_pairs),
            domain,
        )
        return domain_enum

    def load_installed_plugins(self) -> int:
        """Load all installed glossary plugins from the Plugin Marketplace.

        Returns the number of plugin glossaries merged.
        """
        from apps.translator_expert.glossary_plugin import glossary_plugin_registry

        installed = glossary_plugin_registry.get_installed_glossaries()
        count = 0
        for plugin_data in installed:
            self.load_from_plugin(plugin_data.domain, plugin_data.language_pairs)
            count += 1
        return count

    def export_glossary(self, domain: DomainGlossary, source_lang: str, target_lang: str) -> dict[str, str]:
        """Export the full merged glossary for a domain and language pair."""
        return self.get_glossary(domain, source_lang, target_lang)

    def list_domains(self) -> list[str]:
        """Return all supported domain glossary names."""
        return [d.value for d in DomainGlossary]

    def get_entry_count(self, domain: DomainGlossary | None = None) -> dict[str, int]:
        """Get the count of glossary entries per language pair."""
        domains = [domain] if domain else list(DomainGlossary)
        result: dict[str, int] = {}
        for dom in domains:
            total = 0
            for lang_pair_glossary in self.DEFAULT_GLOSSARIES.get(dom, {}).values():
                total += len(lang_pair_glossary)
            custom_total = 0
            for key, terms in self.custom_glossaries.items():
                if key.startswith(f"{dom.value}:"):
                    custom_total += len(terms)
            result[dom.value] = total + custom_total
        return result


__all__ = ["GlossaryManager"]
