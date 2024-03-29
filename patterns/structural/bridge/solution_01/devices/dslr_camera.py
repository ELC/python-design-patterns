from io import StringIO

from .streaming_device import StreamingDevice
from .. import BufferData


class DSLRCamera(StreamingDevice):
    def get_buffer_data(self) -> BufferData:
        return StringIO("###DSLRDATA###")
