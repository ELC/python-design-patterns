from ..files import SealedFileType, Audio, Text, Image

from functools import singledispatchmethod


class Print:
    @singledispatchmethod
    def visit(self, element: SealedFileType) -> None:
        raise NotImplementedError("Should pass a subclass of FileType")

    @visit.register
    def _(self, element: Audio) -> None:
        print(f"{element.codec=}")

    @visit.register
    def _(self, element: Text) -> None:
        print(f"{element.encoding=}")

    @visit.register
    def _(self, element: Image) -> None:
        print(f"{element.width=}, {element.height=}")
