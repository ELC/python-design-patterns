from ..files import SealedFileType, Audio, Text, Image

from typing import Callable, TypeVar, Generic, cast

T = TypeVar("T", bound=SealedFileType)


class Print(Generic[T]):
    def visit(self, element: T) -> None:
        dispatcher = {
            Audio: self.visit_audio,
            Text: self.visit_text,
            Image: self.visit_image,
        }

        algorithm = dispatcher[type(element)]
        algorithm = cast(Callable[[T], None], algorithm)
        algorithm(element)

    def visit_audio(self, element: Audio) -> None:
        print(f"{element.codec=}")

    def visit_text(self, element: Text) -> None:
        print(f"{element.encoding=}")

    def visit_image(self, element: Image) -> None:
        print(f"{element.width=}, {element.height=}")
