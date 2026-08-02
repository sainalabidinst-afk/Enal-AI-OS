from __future__ import annotations

import re
import time
from pathlib import Path
from typing import List

from deep_translator import GoogleTranslator

REPO_ROOT = Path(__file__).resolve().parents[1]
COMMON_TRANSLATIONS = {
    "overview": "Ikhtisar",
    "summary": "Ringkasan",
    "introduction": "Pengantar",
    "document": "dokumen",
    "documentation": "dokumentasi",
    "guide": "panduan",
    "project": "proyek",
    "repository": "repositori",
    "status": "status",
    "architecture": "arsitektur",
    "governance": "tata kelola",
    "quality": "kualitas",
    "security": "keamanan",
    "release": "rilis",
    "version": "versi",
    "baseline": "dasar",
    "engineering": "rekayasa",
    "platform": "platform",
    "operating system": "sistem operasi",
    "system": "sistem",
    "cognitive": "kognitif",
    "agent": "agen",
    "agents": "agen",
    "capability": "kapabilitas",
    "capabilities": "kapabilitas",
    "service": "layanan",
    "workflow": "alur kerja",
    "pipeline": "jalur",
    "framework": "kerangka kerja",
    "tool": "alat",
    "tools": "alat",
    "configuration": "konfigurasi",
    "deployment": "penyebaran",
    "integration": "integrasi",
    "api": "API",
    "ai": "AI",
    "ecp": "ECP",
    "mypy": "mypy",
    "python": "Python",
    "docker": "Docker",
    "linux": "Linux",
    "windows": "Windows",
    "provides": "menyediakan",
    "provide": "menyediakan",
    "supports": "mendukung",
    "support": "dukungan",
    "enable": "memungkinkan",
    "enables": "memungkinkan",
    "allows": "memungkinkan",
    "allow": "memungkinkan",
    "create": "membuat",
    "creates": "membuat",
    "build": "membangun",
    "builds": "membangun",
    "develop": "mengembangkan",
    "develops": "mengembangkan",
    "designed": "dirancang",
    "designed to": "dirancang untuk",
    "this": "ini",
    "that": "itu",
    "the": "",
    "and": "dan",
    "for": "untuk",
    "with": "dengan",
    "is": "adalah",
    "are": "adalah",
    "to": "untuk",
    "of": "dari",
    "in": "dalam",
    "on": "pada",
    "from": "dari",
    "by": "oleh",
    "an": "sebuah",
    "a": "sebuah",
    "can": "dapat",
    "will": "akan",
    "be": "menjadi",
    "has": "memiliki",
    "have": "memiliki",
}
SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}
MARKER_START = "<!-- BILINGUAL_DOCS_START -->"
MARKER_END = "<!-- BILINGUAL_DOCS_END -->"

translator = GoogleTranslator(source="en", target="id")


def translate_with_dictionary(text: str) -> str:
    result = text.strip()
    if not result:
        return ""
    for source, target in sorted(COMMON_TRANSLATIONS.items(), key=lambda item: len(item[0]), reverse=True):
        result = re.sub(rf"\b{re.escape(source)}\b", target, result, flags=re.IGNORECASE)
    result = re.sub(r"\s+", " ", result).strip()
    if result:
        result = result[0].upper() + result[1:]
    return result


def normalize_duplicate_prefixes(text: str) -> str:
    pattern = r"(?i)(\b(?:bahasa indonesia|terjemahan indonesia)\s*:\s*)(?:(?:bahasa indonesia|terjemahan indonesia)\s*:)+"
    cleaned = text
    for _ in range(3):
        new_text = re.sub(pattern, r"\1", cleaned)
        if new_text == cleaned:
            break
        cleaned = new_text
    return cleaned


def collect_markdown_files(root: Path) -> List[Path]:
    files: List[Path] = []
    for path in root.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        files.append(path)
    files.sort()
    return files


def build_header(relative_path: Path) -> str:
    title = relative_path.stem.replace("-", " ").replace("_", " ").title()
    return f"""{MARKER_START}
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: isi utama dokumen disajikan dalam versi Indonesia di bawah konten asli.
- English: the main prose content is presented in an Indonesian bilingual section below the original content.

### Informasi Dokumen / Document Info
- File: `{relative_path.as_posix()}`
- Judul: {title}
- Status: natural bilingual content applied

{MARKER_END}

"""


def insert_header(content: str, relative_path: Path) -> str:
    if MARKER_START in content and MARKER_END in content:
        return content

    header = build_header(relative_path)
    if content.startswith("---\n"):
        lines = content.splitlines()
        if len(lines) > 1 and lines[0] == "---":
            end_idx = 1
            while end_idx < len(lines) and lines[end_idx] != "---":
                end_idx += 1
            if end_idx < len(lines):
                frontmatter = "\n".join(lines[: end_idx + 1]) + "\n\n"
                body = "\n".join(lines[end_idx + 1 :])
                return frontmatter + header + body.lstrip("\n")

    return header + content.lstrip("\n")


def strip_existing_translations(content: str) -> str:
    lines = content.splitlines()
    cleaned: List[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("> Bahasa Indonesia:") or stripped.startswith("> Terjemahan Indonesia:"):
            continue
        cleaned.append(line)
    return "\n".join(cleaned).strip() + "\n"


def strip_markdown(text: str) -> str:
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"__([^_]+)__", r"\1", text)
    text = re.sub(r"^\s*[-*+]\s+", "", text)
    text = re.sub(r"^\s*\d+\.\s+", "", text)
    text = re.sub(r"^\s*>\s*", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_translation(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"^bahasa indonesia\s*:\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^terjemahan indonesia\s*:\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\bai\b", "AI", text, flags=re.IGNORECASE)
    text = re.sub(r"\bcp\b", "ECP", text, flags=re.IGNORECASE)
    text = re.sub(r"\bmd\b", "MD", text, flags=re.IGNORECASE)
    text = re.sub(r"\benglish\b", "Inggris", text, flags=re.IGNORECASE)
    text = re.sub(r"\bdocument\b", "dokumen", text, flags=re.IGNORECASE)
    text = re.sub(r"\bcontent\b", "konten", text, flags=re.IGNORECASE)
    text = re.sub(r"\bmain\b", "utama", text, flags=re.IGNORECASE)
    text = re.sub(r"\boriginal\b", "asli", text, flags=re.IGNORECASE)
    text = re.sub(r"\boperating\s+system\b", "sistem operasi", text, flags=re.IGNORECASE)
    text = re.sub(r"\bmulti-agent\b", "multi-agen", text, flags=re.IGNORECASE)
    text = re.sub(r"\bcapability\b", "kapabilitas", text, flags=re.IGNORECASE)
    text = re.sub(r"\bcognitive\b", "kognitif", text, flags=re.IGNORECASE)
    text = re.sub(r"\bpipeline\b", "jalur", text, flags=re.IGNORECASE)
    text = re.sub(r"\bgovernance\b", "tata kelola", text, flags=re.IGNORECASE)
    text = re.sub(r"\bframework\b", "kerangka kerja", text, flags=re.IGNORECASE)
    return text


def translate_text(text: str) -> str:
    clean = strip_markdown(text)
    if not clean or len(clean) < 5:
        return ""
    if len(clean) > 1200:
        clean = " ".join(clean.split()[:40]) + "..."

    translated = translate_with_dictionary(clean)
    if translated and translated != clean:
        return normalize_translation(translated)

    try:
        translated = translator.translate(clean).strip()
        normalized = normalize_translation(translated)
        if normalized and normalized != clean:
            return normalized
    except Exception:
        pass
    return clean


def translate_block(block: str) -> str:
    if not block:
        return block
    cleaned_block = normalize_duplicate_prefixes(block)
    lines = [line.rstrip() for line in cleaned_block.splitlines() if line.strip()]
    if not lines:
        return block
    if lines[0].startswith("<!--") or lines[0].startswith("```") or lines[0].startswith("~~~"):
        return block
    if all(re.match(r"^\s*[-*_]{3,}\s*$", line) for line in lines):
        return block

    if len(lines) == 1:
        simple = lines[0].strip()
        if simple.startswith(">"):
            return block
        if re.match(r"^#", simple):
            content = re.sub(r"^#+\s*", "", simple)
            translated = translate_text(content)
            return f"{block}\n> Terjemahan Indonesia: {translated.capitalize()}"
        if re.match(r"^\s*[-*+]\s+", simple) or re.match(r"^\s*\d+\.\s+", simple):
            content = re.sub(r"^\s*[-*+]\s+", "", simple)
            content = re.sub(r"^\s*\d+\.\s+", "", content)
            translated = translate_text(content)
            return f"{block}\n> Terjemahan Indonesia: {translated.capitalize()}"
        if re.match(r"^\s*\[[^\]]+\]\([^)]+\)\s*$", simple):
            return block
        if len(simple) < 25 and not any(ch.isalpha() for ch in simple):
            return block
        translated = translate_text(simple)
        if translated:
            return f"{block}\n> Terjemahan Indonesia: {translated}"
        return block

    combined = " ".join(strip_markdown(line) for line in lines if line.strip())
    if len(combined) < 25:
        return block
    translated = translate_text(combined)
    if translated:
        return f"{block}\n> Terjemahan Indonesia: {translated}"
    return block


def bilingualize_content(content: str) -> str:
    content = normalize_duplicate_prefixes(content)
    content = strip_existing_translations(content)
    lines = content.splitlines()
    out: List[str] = []
    in_code = False
    block: List[str] = []

    def flush_block() -> None:
        if block:
            out.append(translate_block("\n".join(block)))
            block.clear()

    for line in lines:
        if line.startswith("```") or line.startswith("~~~"):
            flush_block()
            in_code = not in_code
            out.append(line)
            continue

        if in_code:
            out.append(line)
            continue

        if line.strip():
            if line.startswith("#") or line.startswith("-") or line.startswith("*") or line.startswith("+") or re.match(r"^\d+\.", line) or re.match(r"^\s*\|", line) or line.startswith(">") or re.match(r"^\s*[-*_]{3,}\s*$", line):
                flush_block()
                out.append(line)
            else:
                block.append(line)
        else:
            flush_block()
            out.append("")

    flush_block()
    return "\n".join(out).strip() + "\n"


def write_index(files: List[Path]) -> None:
    index_path = REPO_ROOT / "docs" / "BILINGUAL_DOCUMENTATION.md"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Dokumentasi Bilingual / Bilingual Documentation",
        "",
        "## Ringkasan / Summary",
        "",
        "Dokumen Markdown di repositori ini kini diberi header bilingual dan terjemahan isi prose yang lebih natural dalam bahasa Indonesia.",
        "",
        "## Daftar Dokumen / Document List",
        "",
    ]
    for path in files:
        relative = path.relative_to(REPO_ROOT).as_posix()
        lines.append(f"- [{relative}]({relative})")
    index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    markdown_files = collect_markdown_files(REPO_ROOT)
    for path in markdown_files:
        try:
            original = path.read_text(encoding="utf-8")
        except Exception:
            continue
        with_header = insert_header(original, path.relative_to(REPO_ROOT))
        updated = bilingualize_content(with_header)
        if updated != original:
            try:
                path.write_text(updated, encoding="utf-8")
            except Exception:
                continue
    write_index(markdown_files)
    print(f"Processed {len(markdown_files)} markdown files.")


if __name__ == "__main__":
    main()
