from . import StreamingService
from .. import BufferOutput


class YouTubeStreamingService(StreamingService):
    def fill_buffer(self) -> None:
        buffer_data = self.retrieve_buffer_data()
        for buffer in buffer_data:
            buffer_content = buffer.getvalue()
            self.output.write(
                f"Received buffer data: {buffer_content}. Sending to YouTube stream: {self.reference}.\n"
            )

    def collect_and_close_stream(self) -> BufferOutput:
        self.output.write(f"Closing YouTube stream with reference {self.reference}.\n")
        collected_buffer = self.output.getvalue()
        self.output.close()
        return collected_buffer
