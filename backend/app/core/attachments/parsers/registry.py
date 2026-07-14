from __future__ import annotations

import importlib
import pkgutil
from typing import Any

from backend.app.core.attachments.models import AttachmentMeta, InfrastructureAST
from backend.app.core.attachments.parsers.base import BaseParser


class ParserRegistry:
    """Registry of all infrastructure parsers.

    Discovers parsers from the parsers package and routes attachments
    to the best matching parser based on confidence.
    """

    def __init__(self) -> None:
        self._parsers: list[BaseParser] = []
        self._load_parsers()

    def _load_parsers(self) -> None:
        package = __import__("backend.app.core.attachments.parsers", fromlist=[""])
        for importer, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
            full_name = f"backend.app.core.attachments.parsers.{module_name}"
            if is_pkg:
                try:
                    subpackage = __import__(full_name, fromlist=[""])
                    for _, sub_name, sub_is_pkg in pkgutil.iter_modules(subpackage.__path__):
                        if sub_is_pkg:
                            continue
                        try:
                            module = importlib.import_module(f"{full_name}.{sub_name}")
                            self._register_parser_classes(module)
                        except Exception:
                            continue
                except Exception:
                    continue
                continue
            try:
                module = importlib.import_module(full_name)
                self._register_parser_classes(module)
            except Exception:
                continue

    def _register_parser_classes(self, module: Any) -> None:
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and issubclass(attr, BaseParser) and attr is not BaseParser:
                self._parsers.append(attr())

    def best_parser(self, meta: AttachmentMeta) -> BaseParser | None:
        candidates = [parser for parser in self._parsers if parser.can_parse(meta)]
        if not candidates:
            return None
        return candidates[0]

    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        parser = self.best_parser(meta)
        if parser is None:
            from backend.app.core.attachments.parsers.network.text_config import TextConfigParser
            return TextConfigParser().parse(meta, content)
        return parser.parse(meta, content)


parser_registry = ParserRegistry()
