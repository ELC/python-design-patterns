from ..files import SealedFileType, Audio, Text, Image

from typing import TypeVar, Generic, assert_never

T = TypeVar("T", bound=SealedFileType)


class Print(Generic[T]):
    def visit(self, element: T) -> None:
        if isinstance(element, Audio):
            PrintAudio().visit(element)
            return
        elif isinstance(element, Text):
            PrintText().visit(element)
            return
        elif isinstance(element, Image):
            PrintImage().visit(element)
            return
        else:
            assert_never(element)


class PrintAudio(Print[Audio]):
    def visit(self, element: Audio) -> None:
        print(f"{element.codec=}")


class PrintText(Print[Text]):
    def visit(self, element: Text) -> None:
        print(f"{element.encoding=}")


class PrintImage(Print[Image]):
    def visit(self, element: Image) -> None:
        print(f"{element.width=}, {element.height=}")
