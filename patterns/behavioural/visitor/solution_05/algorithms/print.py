from ..files import SealedFileType, Audio, Text, Image

from typing import Callable, Optional, TypeVar, Generic, cast

T = TypeVar("T", bound=SealedFileType)


class Print(Generic[T]):
    def visit(self, element: T):
        method: Optional[Callable[[T], None]] = None
        executed_at_least_once: bool = False

        for element_class in element.__class__.__mro__:
            method_name = f"visit_{element_class.__name__.lower()}"
            method = getattr(self, method_name, None)
            if not method:
                continue
            executed_at_least_once = True
            cast(Callable[[T], None], method)
            method(element)

        if not executed_at_least_once:
            raise ValueError(f"No visit method for {element.__class__.__name__}")

    def visit_audio(self, element: Audio) -> None:
        print(f"{element.codec=}")

    def visit_text(self, element: Text) -> None:
        print(f"{element.encoding=}")

    def visit_image(self, element: Image) -> None:
        print(f"{element.width=}, {element.height=}")
