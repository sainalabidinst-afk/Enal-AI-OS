"""
Prompt Engineer
===============

Designs prompt templates, optimization strategies, and chain-of-thought
patterns for LLM interactions.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.ai_engineer.schemas import (
    AIEngineerRequest,
    PromptTemplate,
)

logger = logging.getLogger(__name__)


class PromptEngineer:
    """Designs prompt templates and optimization strategies."""

    def design(self, request: AIEngineerRequest) -> list[PromptTemplate]:
        inputs = request.inputs
        task_type = inputs.get("task_type", "general")
        templates = inputs.get("templates", [])

        if templates:
            return [PromptTemplate(**t) if isinstance(t, dict) else t for t in templates]

        defaults: dict[str, PromptTemplate] = {
            "general": PromptTemplate(
                name="general_assistant",
                template="Anda adalah asisten AI yang membantu dalam domain {domain}. Jawab pertanyaan dengan jelas dan akurat.\n\nPertanyaan: {query}\n\nJawaban:",
                variables=["domain", "query"],
                version="1.0",
                description="General-purpose assistant template",
                expected_output_format="text",
            ),
            "code": PromptTemplate(
                name="code_assistant",
                template="Anda adalah programmer ahli dalam bahasa {language}. Tulis kode yang bersih, efisien, dan terdokumentasi.\n\nPermintaan: {query}\n\nKode:\n```{language}\n",
                variables=["language", "query"],
                version="1.0",
                description="Code generation template with best practices",
                expected_output_format="markdown",
            ),
            "analysis": PromptTemplate(
                name="analysis_assistant",
                template="Lakukan analisis {analysis_type} untuk data berikut:\n\n{data}\n\nBerikan analisis terstruktur dengan:\n1. Ringkasan\n2. Temuan utama\n3. Rekomendasi\n\nAnalisis:",
                variables=["analysis_type", "data"],
                version="1.0",
                description="Structured analysis template with reasoning chain",
                expected_output_format="json",
            ),
            "rag": PromptTemplate(
                name="rag_assistant",
                template="Gunakan konteks berikut untuk menjawab pertanyaan:\n\nKonteks:\n{context}\n\nPertanyaan: {query}\n\nInstruksi:\n- Jawab hanya berdasarkan konteks yang diberikan\n- Jika konteks tidak cukup, katakan 'Saya tidak memiliki informasi yang cukup'\n- Sertakan kutipan sumber\n\nJawaban:",
                variables=["context", "query"],
                version="1.0",
                description="RAG prompt with source attribution",
                expected_output_format="text",
            ),
            "agentic": PromptTemplate(
                name="agentic_reasoning",
                template="Anda adalah agent AI yang dapat menggunakan tools berikut:\n{tools}\n\nTugas: {task}\n\nLangkah-langkah:\n1. Analisis tugas\n2. Pilih tool yang tepat\n3. Eksekusi\n4. Verifikasi hasil\n5. Berikan jawaban akhir\n\nMulai:",
                variables=["tools", "task"],
                version="1.0",
                description="Agentic reasoning with tool use",
                expected_output_format="json",
            ),
        }
        return [defaults.get(task_type, defaults["general"])]

    def get_recommendations(self, templates: list[PromptTemplate]) -> list[str]:
        recs: list[str] = []
        for tpl in templates:
            if len(tpl.variables) < 2:
                recs.append(f"Template '{tpl.name}': pertimbangkan parameterisasi lebih banyak")
            if "{" not in tpl.template and "}" not in tpl.template:
                recs.append(f"Template '{tpl.name}': gunakan variabel template untuk reuse")
            if tpl.expected_output_format not in ("json", "markdown", "text"):
                recs.append(f"Template '{tpl.name}': format output tidak dikenali")
        return recs

    def score_quality(self, templates: list[PromptTemplate]) -> float:
        if not templates:
            return 0.0
        score = 0.0
        for tpl in templates:
            s = 0.7
            if tpl.variables:
                s += 0.1
            if tpl.version and tpl.version != "1.0":
                s += 0.05
            if tpl.description:
                s += 0.05
            if tpl.expected_output_format in ("json", "markdown"):
                s += 0.05
            score = max(score, s)
        return min(score, 1.0)
