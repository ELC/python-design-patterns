from __future__ import annotations

from abc import ABC, abstractmethod

from dataclasses import dataclass
from typing import Protocol


class FileTypeVisitor(Protocol):
    def visit(self, element: FileType) -> None:
        ...


@dataclass
class FileType(ABC):
    name: str = ""

    @abstractmethod
    def accept(self, visitor: FileTypeVisitor) -> None:
        visitor.visit(self)
