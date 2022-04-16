from io import StringIO

from .. import BufferData


def dslr_camera_buffer_data() -> BufferData:
    return StringIO("###DSLRDATA###")
