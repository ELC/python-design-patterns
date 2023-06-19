from ..files import SealedFileType, Audio, Text, Image

from typing import TypeVar, Generic, assert_never

T = TypeVar("T", bound=SealedFileType)


class Print(Generic[T]):
    def visit(self, element: T) -> None:
        if isinstance(element, Audio):
            self.visit_audio(element)
            return
        elif isinstance(element, Text):
            self.visit_text(element)
            return
        elif isinstance(element, Image):
            self.visit_image(element)
            return
        else:
            assert_never(element)

    def visit_audio(self, element: Audio) -> None:
        print(f"{element.codec=}")

    def visit_text(self, element: Text) -> None:
        print(f"{element.encoding=}")

    def visit_image(self, element: Image) -> None:
        print(f"{element.width=}, {element.height=}")
