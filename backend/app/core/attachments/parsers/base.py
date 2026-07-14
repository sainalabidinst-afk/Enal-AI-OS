from __future__ import annotations

from abc import ABC, abstractmethod

from backend.app.core.attachments.models import AttachmentMeta, InfrastructureAST


class BaseParser(ABC):
    """Base parser interface for all infrastructure parsers."""

    @abstractmethod
    def can_parse(self, meta: AttachmentMeta) -> bool:
        """Return True if this parser can handle the given attachment meta."""

    @abstractmethod
    def parse(self, meta: AttachmentMeta, content: str) -> InfrastructureAST:
        """Parse content and return universal AST."""
