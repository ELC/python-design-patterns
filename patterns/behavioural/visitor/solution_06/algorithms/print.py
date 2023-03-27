from ..files import SealedFileType, Audio, Text, Image

from typing import Optional, Type, TypeVar, Generic, cast

T = TypeVar("T", bound=SealedFileType)


class Print(Generic[T]):
    def visit(self, element: T) -> None:
        class_: Optional[Type[Print[T]]] = None
        executed_at_least_once: bool = False

        for element_class in element.__class__.__mro__:
            class_name = f"Print{element_class.__name__}"
            class_ = next(
                (
                    class_
                    for class_ in type(self).__subclasses__()
                    if class_.__name__ == class_name
                ),
                None,
            )
            if not class_:
                continue

            executed_at_least_once = True
            class_ = cast(Type[Print[T]], class_)
            algorithm = class_()
            algorithm.visit(element)

        if not executed_at_least_once:
            raise ValueError(f"No visit method for {element.__class__.__name__}")


class PrintAudio(Print[Audio]):
    def visit(self, element: Audio) -> None:
        print(f"{element.codec=}")


class PrintText(Print[Text]):
    def visit(self, element: Text) -> None:
        print(f"{element.encoding=}")


class PrintImage(Print[Image]):
    def visit(self, element: Image) -> None:
        print(f"{element.width=}, {element.height=}")
