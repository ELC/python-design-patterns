from typing import Generic, TypeVar, assert_never
from ..files import SealedFileType, Audio, Text, Image

T = TypeVar("T", bound=SealedFileType)


class Print(Generic[T]):
    def visit(self, element: T) -> None:
        match element:
            case Audio() as audio:
                PrintAudio().visit(audio)
            case Text() as text:
                PrintText().visit(text)
            case Image() as image:
                PrintImage().visit(image)
            case _ as unreachable:
                assert_never(unreachable)


class PrintAudio(Print[Audio]):
    def visit(self, element: Audio) -> None:
        print(f"{element.codec=}")


class PrintText(Print[Text]):
    def visit(self, element: Text) -> None:
        print(f"{element.encoding=}")


class PrintImage(Print[Image]):
    def visit(self, element: Image) -> None:
        print(f"{element.width=}, {element.height=}")
