from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
from .filetype import FileType


@dataclass
class Image(FileType):
    height: float = 1080
    width: float = 1920

    def accept(self, visitor: Callable[[Image], None]) -> None:
        visitor(self)
