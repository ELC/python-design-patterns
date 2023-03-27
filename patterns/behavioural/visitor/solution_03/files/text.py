from dataclasses import dataclass
from .filetype import FileType


@dataclass
class Text(FileType):
    encoding: str = "utf-8"
