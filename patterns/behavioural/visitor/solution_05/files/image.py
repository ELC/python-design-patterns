from dataclasses import dataclass
from .filetype import FileType


@dataclass
class Image(FileType):
    height: float = 1080
    width: float = 1920
