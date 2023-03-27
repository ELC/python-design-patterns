from abc import ABC

from dataclasses import dataclass


@dataclass
class FileType(ABC):
    name: str = ""
