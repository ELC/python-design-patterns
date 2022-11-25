from collections.abc import Iterable

from typing import Protocol


class PrintableItem(Protocol):
    def __str__(self) -> str:
        ...


class ConsolePrinter:
    def print(self, collection: Iterable[PrintableItem]):

        for item in collection:
            print(item)
