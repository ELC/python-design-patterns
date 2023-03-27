from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
from .filetype import FileType


@dataclass
class Text(FileType):
    encoding: str = "utf-8"

    def accept(self, visitor: Callable[[Text], None]) -> None:
        visitor(self)
