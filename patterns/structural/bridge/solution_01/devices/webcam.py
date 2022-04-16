from io import StringIO
from dataclasses import dataclass
from typing import Literal

from . import StreamingDevice
from .. import BufferData

Quality = Literal["360p", "480p", "720p", "1080p", "2160p"]


@dataclass
class Webcam(StreamingDevice):
    quality: Quality = "1080p"

    def get_buffer_data(self) -> BufferData:
        return StringIO(f"###WEBCAMDATA at {self.quality}###")
