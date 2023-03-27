from dataclasses import dataclass
from .filetype import FileType


@dataclass
class Audio(FileType):
    codec: str = "mp4"
