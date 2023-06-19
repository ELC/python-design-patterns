from typing import assert_never
from ..files import SealedFileType, Audio, Text, Image


class Print:
    def visit(self, element: SealedFileType) -> None:
        match element:
            case Audio() as audio:
                self.visit_audio(audio)
            case Text() as text:
                self.visit_text(text)
            case Image() as image:
                self.visit_image(image)
            case _ as unreachable:
                assert_never(unreachable)

    def visit_audio(self, element: Audio) -> None:
        print(f"{element.codec=}")

    def visit_text(self, element: Text) -> None:
        print(f"{element.encoding=}")

    def visit_image(self, element: Image) -> None:
        print(f"{element.width=}, {element.height=}")
