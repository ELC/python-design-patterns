from io import StringIO
from dataclasses import dataclass

from . import StreamingService, Quality
from .. import BufferOutput, BufferData


class TwitchStreamingService(StreamingService):
    def fill_buffer(self) -> None:
        buffer_data = self.retrieve_buffer_data()
        for buffer in buffer_data:
            buffer_content = buffer.getvalue()
            self.output.write(
                f"Received buffer data: {buffer_content}. Sending to Twitch stream: {self.reference}.\n"
            )

    def collect_and_close_stream(self) -> BufferOutput:
        self.output.write(f"Closing Twitch stream with reference {self.reference}.\n")
        collected_buffer = self.output.getvalue()
        self.output.close()
        return collected_buffer

    def get_buffer_data(self) -> BufferData:
        raise NotImplementedError()


class TwitchStreamingServiceWithDSLRCamera(TwitchStreamingService):
    def get_buffer_data(self) -> BufferData:
        return StringIO("###DSLRDATA###")


@dataclass
class TwitchStreamingServiceWithWebcam(TwitchStreamingService):
    quality: Quality = "1080p"

    def get_buffer_data(self) -> BufferData:
        return StringIO(f"###WEBCAMDATA at {self.quality}###")
