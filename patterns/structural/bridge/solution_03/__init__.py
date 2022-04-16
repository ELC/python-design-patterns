import uuid
from io import StringIO

BufferData = StringIO
BufferOutput = str


def generate_id() -> str:
    return str(uuid.uuid4())
