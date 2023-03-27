from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
from .filetype import FileType


@dataclass
class Audio(FileType):
    codec: str = "mp4"

    def accept(self, visitor: Callable[[Audio], None]) -> None:
        visitor(self)
