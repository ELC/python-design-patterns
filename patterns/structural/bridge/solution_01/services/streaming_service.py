from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List
from io import StringIO

from .. import BufferData, BufferOutput, generate_id
from ..devices import StreamingDevice


@dataclass
class StreamingService(ABC):
    devices: List[StreamingDevice] = field(default_factory=list)
    output: BufferData = field(default_factory=StringIO)
    reference: str = field(init=False)

    def __post_init__(self) -> None:
        self.reference = generate_id()

    def add_device(self, device: StreamingDevice) -> None:
        self.devices.append(device)

    def retrieve_buffer_data(self) -> List[BufferData]:
        return [device.get_buffer_data() for device in self.devices]

    @abstractmethod
    def fill_buffer(self) -> None:
        ...

    @abstractmethod
    def collect_and_close_stream(self) -> BufferOutput:
        ...
