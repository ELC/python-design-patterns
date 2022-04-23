from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Literal
from io import StringIO

from .. import BufferData, BufferOutput, generate_id


Quality = Literal["360p", "480p", "720p", "1080p", "2160p"]


@dataclass
class StreamingService(ABC):
    devices: List["StreamingService"] = field(default_factory=list)
    output: BufferData = field(default_factory=StringIO)
    reference: str = field(init=False)

    def __post_init__(self) -> None:
        self.reference = generate_id()

    def add_device(self, device: "StreamingService") -> None:
        if not isinstance(device, type(self)):
            raise ValueError(
                f"Only subclasses can be used - {type(device)} is not subclass of {type(self)}"
            )

        self.devices.append(device)

    def retrieve_buffer_data(self) -> List[BufferData]:
        return [device.get_buffer_data() for device in self.devices]

    @abstractmethod
    def fill_buffer(self) -> None:
        ...

    @abstractmethod
    def collect_and_close_stream(self) -> BufferOutput:
        ...

    @abstractmethod
    def get_buffer_data(self) -> BufferData:
        ...
