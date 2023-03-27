from typing import overload
from ..files import SealedFileType, Audio, Text, Image

from functools import singledispatchmethod


class Print:
    @singledispatchmethod
    def visit_(self, element: SealedFileType) -> None:
        raise NotImplementedError("Cannot negate a")

    @visit_.register
    def _(self, element: Audio) -> None:
        print(f"{element.codec=}")

    @visit_.register
    def _(self, element: Text) -> None:
        print(f"{element.encoding=}")

    @visit_.register
    def _(self, element: Image) -> None:
        print(f"{element.width=}, {element.height=}")

    @overload
    def visit(self, element: Audio) -> None:
        ...

    @overload
    def visit(self, element: Text) -> None:
        ...

    @overload
    def visit(self, element: Image) -> None:
        ...

    def visit(self, element: SealedFileType) -> None:
        return self.visit_(element)
