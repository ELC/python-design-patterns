from .audio import Audio
from .text import Text
from .image import Image

from typing import Union

SealedFileType = Union[Audio, Text, Image]

__all__ = ["Audio", "Text", "Image", "SealedFileType"]
