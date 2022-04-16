from abc import ABC, abstractmethod

from .. import BufferData


class StreamingDevice(ABC):
    @abstractmethod
    def get_buffer_data(self) -> BufferData:
        ...
