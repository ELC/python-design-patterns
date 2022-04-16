from typing import Callable

from .. import BufferData

StreamingDevice = Callable[[], BufferData]
