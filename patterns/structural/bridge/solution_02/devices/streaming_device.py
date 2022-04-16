from typing import Protocol

from .. import BufferData


class StreamingDevice(Protocol):
    def get_buffer_data(self) -> BufferData:
        ...
