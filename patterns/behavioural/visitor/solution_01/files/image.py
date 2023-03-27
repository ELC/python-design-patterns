from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
from .filetype import FileType


class ImageVisitor(Protocol):
    def visit(self, element: Image) -> None:
        ...


@dataclass
class Image(FileType):
    height: float = 1080
    width: float = 1920

    def accept(self, visitor: ImageVisitor) -> None:
        visitor.visit(self)
