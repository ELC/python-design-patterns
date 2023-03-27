from typing import Protocol

from ..files import SealedFileType


class Algorithm(Protocol):
    def visit(self, element: SealedFileType) -> None:
        ...
