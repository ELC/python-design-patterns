from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
from .filetype import FileType


class AudioVisitor(Protocol):
    def visit(self, element: Audio) -> None:
        ...


@dataclass
class Audio(FileType):
    codec: str = "mp4"

    def accept(self, visitor: AudioVisitor) -> None:
        visitor.visit(self)
