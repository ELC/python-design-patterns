from io import StringIO
from typing import Literal

from .. import BufferData
from . import StreamingDevice

Quality = Literal["360p", "480p", "720p", "1080p", "2160p"]


def webcam_buffer_data(quality: Quality = "1080p") -> StreamingDevice:
    def buffer() -> BufferData:
        return StringIO(f"###WEBCAMDATA at {quality}###")

    return buffer
