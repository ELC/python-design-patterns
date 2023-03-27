from ..files import SealedFileType, Audio, Text, Image

from typing import TypeVar, Generic, cast

T = TypeVar("T", bound=SealedFileType)


class Print(Generic[T]):
    def visit(self, element: T) -> None:
        dispatcher = {
            Audio: PrintAudio(),
            Text: PrintText(),
            Image: PrintImage(),
        }

        algorithm = dispatcher[type(element)]
        algorithm = cast(Print[T], algorithm)
        algorithm.visit(element)


class PrintAudio(Print[Audio]):
    def visit(self, element: Audio) -> None:
        print(f"{element.codec=}")


class PrintText(Print[Text]):
    def visit(self, element: Text) -> None:
        print(f"{element.encoding=}")


class PrintImage(Print[Image]):
    def visit(self, element: Image) -> None:
        print(f"{element.width=}, {element.height=}")
