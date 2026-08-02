from __future__ import annotations

import re
from pathlib import Path
from typing import List

from deep_translator import GoogleTranslator

REPO_ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
PRESERVE_TERMS = [
    "Capability Pack",
    "Golden Test",
    "Benchmark",
    "API",
    "SDK",
    "Docker",
    "FastAPI",
    "Runtime",
    "Plugin",
    "Knowledge Graph",
    "Execution Runtime",
    "Decision Intelligence",
    "Security Engineer",
    "Data Engineer",
    "Database Engineer",
    "QA Engineer",
    "Business Analyst",
]
translator = GoogleTranslator(source="en", target="id")


def collect_markdown_files(root: Path) -> List[Path]:
    files: List[Path] = []
    for path in root.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        files.append(path)
    files.sort()
    return files


def strip_bilingual_blocks(content: str) -> str:
    lines = content.splitlines()
    cleaned: List[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("<!-- BILINGUAL_DOCS_START -->") or stripped.startswith("<!-- BILINGUAL_DOCS_END -->"):
            continue
        if re.search(r"\b(Bahasa Indonesia|Terjemahan Indonesia|English)\s*:", stripped):
            continue
        if re.search(r"\b(Bahasa Indonesia|Terjemahan Indonesia)\b", stripped):
            continue
        cleaned.append(line)
    return "\n".join(cleaned).strip() + "\n"


def preserve_segments(text: str) -> tuple[str, List[str]]:
    placeholders: List[str] = []

    def add_placeholder(match: re.Match[str]) -> str:
        placeholder = f"__PRESERVE_{len(placeholders)}__"
        placeholders.append(match.group(0))
        return placeholder

    text = re.sub(r"`[^`]*`", add_placeholder, text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", add_placeholder, text)
    text = re.sub(r"<[^>]+>", add_placeholder, text)

    for term in sorted(PRESERVE_TERMS, key=len, reverse=True):
        if term.lower() in text.lower():
            text = re.sub(rf"\b{re.escape(term)}\b", f"__PRESERVE_{len(placeholders)}__", text, flags=re.IGNORECASE)
            placeholders.append(term)

    return text, placeholders


def restore_segments(text: str, placeholders: List[str]) -> str:
    for index, value in enumerate(placeholders):
        text = text.replace(f"__PRESERVE_{index}__", value)
    return text


def translate_text(text: str) -> str:
    if not text or not text.strip():
        return text
    preserved, placeholders = preserve_segments(text)
    try:
        translated = translator.translate(preserved).strip()
    except Exception:
        translated = preserved
    return restore_segments(translated, placeholders)


def translate_line(line: str) -> str:
    if not line.strip():
        return line
    if line.strip().startswith("```") or line.strip().startswith("~~~"):
        return line

    heading_match = re.match(r"^(\s*)(#{1,6})(\s*)(.*)$", line)
    if heading_match:
        prefix = heading_match.group(1) + heading_match.group(2) + heading_match.group(3)
        return prefix + translate_text(heading_match.group(4))

    bullet_match = re.match(r"^(\s*)([-*+]|\d+\.)\s+(.*)$", line)
    if bullet_match:
        prefix = bullet_match.group(1) + bullet_match.group(2) + " "
        return prefix + translate_text(bullet_match.group(3))

    quote_match = re.match(r"^(\s*>+\s*)(.*)$", line)
    if quote_match:
        return quote_match.group(1) + translate_text(quote_match.group(2))

    if line.strip().startswith("|") and line.count("|") >= 2:
        parts = line.split("|")
        if len(parts) >= 3 and all(re.fullmatch(r"[-: ]+", part.strip()) for part in parts[1:-1]):
            return line
        translated_parts = []
        for index, part in enumerate(parts):
            if index == 0 or index == len(parts) - 1:
                translated_parts.append(part)
            else:
                translated_parts.append(translate_text(part))
        return "|".join(translated_parts)

    return translate_text(line)


def translate_content(content: str) -> str:
    content = strip_bilingual_blocks(content)
    lines = content.splitlines()
    out: List[str] = []
    in_code = False

    for line in lines:
        if line.startswith("```") or line.startswith("~~~"):
            in_code = not in_code
            out.append(line)
            continue
        if in_code:
            out.append(line)
            continue
        out.append(translate_line(line))

    return "\n".join(out).strip() + "\n"


def main() -> None:
    markdown_files = collect_markdown_files(REPO_ROOT)
    for path in markdown_files:
        try:
            original = path.read_text(encoding="utf-8")
        except Exception:
            continue
        updated = translate_content(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
    print(f"Processed {len(markdown_files)} markdown files.")


if __name__ == "__main__":
    main()
