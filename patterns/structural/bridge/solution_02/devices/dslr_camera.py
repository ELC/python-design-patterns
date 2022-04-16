from io import StringIO

from .. import BufferData


class DSLRCamera:
    def get_buffer_data(self) -> BufferData:
        return StringIO("###DSLRDATA###")
