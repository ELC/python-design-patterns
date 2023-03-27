from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
from .filetype import FileType


class TextVisitor(Protocol):
    def visit(self, element: Text) -> None:
        ...


@dataclass
class Text(FileType):
    encoding: str = "utf-8"

    def accept(self, visitor: TextVisitor) -> None:
        visitor.visit(self)
