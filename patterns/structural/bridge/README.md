# Strategy Pattern

## Problem

The development team of a new multimedia software wants to connect different
devices with different streaming services.

Each device and streaming service will have its own distinct characteristics.

It is expected that all supported devices can be used with all supported
streaming services. At the moment there are only two devices: WebCam and DSLR
Camara; and two streaming services: Youtube and Twitch.

Design a solution that can be easily extended when a new device or streaming
service is added.

**Develop a solution for the stated problem before continue reading**


## Naive Solution

Without knowledge of this pattern, one may develop a solution that looks like
the following.

First, an abstract class called StreamingService is defined. This class will
hold a list of devices, an output an an id for reference.

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Literal
from io import StringIO

BufferData = StringIO
BufferOutput = str

def generate_id() -> str:
    return str(uuid.uuid4())


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
```

In this implementation there is a heavy use of inheritance so to keep devices
and streaming services linked, each device is implemented as a specialized
class that inherits from a concrete class.

The Twitch streaming service class and devices will look like the following:


```python
from io import StringIO
from dataclasses import dataclass

from .streaming_service import StreamingService, Quality
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
        raise NotImplementedError


class TwitchStreamingServiceWithDSLRCamera(TwitchStreamingService):
    def get_buffer_data(self) -> BufferData:
        return StringIO("###DSLRDATA###")


@dataclass
class TwitchStreamingServiceWithWebcam(TwitchStreamingService):
    quality: Quality = "1080p"

    def get_buffer_data(self) -> BufferData:
        return StringIO(f"###WEBCAMDATA at {self.quality}###")
```


The Youtube version is practically identical:

```python
from io import StringIO
from dataclasses import dataclass

from .streaming_service import StreamingService, Quality
from .. import BufferOutput, BufferData


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

    def get_buffer_data(self) -> BufferData:
        raise NotImplementedError


class YouTubeStreamingServiceWithDSLRCamera(YouTubeStreamingService):
    def get_buffer_data(self) -> BufferData:
        return StringIO("###DSLRDATA###")


@dataclass
class YouTubeStreamingServiceWithWebcam(YouTubeStreamingService):
    quality: Quality = "1080p"

    def get_buffer_data(self) -> BufferData:
        return StringIO(f"###WEBCAMDATA at {self.quality}###")
```

Lastly, to execute the code a main script is also defined:

```python
from .services import (
    YouTubeStreamingService,
    YouTubeStreamingServiceWithWebcam,
    TwitchStreamingService,
    TwitchStreamingServiceWithDSLRCamera,
    TwitchStreamingServiceWithWebcam,
)


def main() -> None:
    youtube_service = YouTubeStreamingService()
    youtube_service.add_device(YouTubeStreamingServiceWithWebcam(quality="720p"))
    youtube_service.fill_buffer()
    youtube_output = youtube_service.collect_and_close_stream()
    print(youtube_output)

    twitch_service = TwitchStreamingService()
    twitch_service.add_device(TwitchStreamingServiceWithDSLRCamera())
    twitch_service.add_device(TwitchStreamingServiceWithWebcam(quality="720p"))
    twitch_service.fill_buffer()
    twitch_output = twitch_service.collect_and_close_stream()
    print(twitch_output)
```

Some of the problems with this solution are:

- It has extensive code duplicated between the Twitch and Youtube classes
- Each time a new device or a streaming service is added, the number of classes
  increases exponentially

Below are different solutions to this problem,

## Solution 1: GoF Approach

The first step is to divide the business concepts, devices and services are
independent from each other, and as such, they should not belong to the same
class hierarchy.

This implies that the original abstract class will be split into two
`StreamingDevice` and `StreamingService`.

The key of this pattern is to create a *bridge* between abstractions, meaning
that the only place where there is a link between the devices and the services
happens at the abstract class. This allows for concrete classes to written
without the need to know the specifics of their counterpart concrete class.

```python
from abc import ABC, abstractmethod

from .. import BufferData


class StreamingDevice(ABC):
    @abstractmethod
    def get_buffer_data(self) -> BufferData:
        ...
```

```python
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
```

Now the different devices can be defined independently of the services that
will consume them:

```python
from io import StringIO

from .streaming_device import StreamingDevice
from .. import BufferData


class DSLRCamera(StreamingDevice):
    def get_buffer_data(self) -> BufferData:
        return StringIO("###DSLRDATA###")
```

```python
from io import StringIO
from dataclasses import dataclass
from typing import Literal

from .streaming_device import StreamingDevice
from .. import BufferData

Quality = Literal["360p", "480p", "720p", "1080p", "2160p"]


@dataclass
class Webcam(StreamingDevice):
    quality: Quality = "1080p"

    def get_buffer_data(self) -> BufferData:
        return StringIO(f"###WEBCAMDATA at {self.quality}###")
```

The same applies to the different streaming services:

```python
from .streaming_service import StreamingService
from .. import BufferOutput


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
```

```python
from .streaming_service import StreamingService
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
```

Finally the way to combine this classes also changes:

```python
from .devices import DSLRCamera, Webcam
from .services import YouTubeStreamingService, TwitchStreamingService


def main() -> None:
    youtube_service = YouTubeStreamingService()
    youtube_service.add_device(Webcam(quality="720p"))
    youtube_service.fill_buffer()
    youtube_output = youtube_service.collect_and_close_stream()
    print(youtube_output)

    twitch_service = TwitchStreamingService()
    twitch_service.add_device(DSLRCamera())
    twitch_service.add_device(Webcam(quality="720p"))
    twitch_service.fill_buffer()
    twitch_output = twitch_service.collect_and_close_stream()
    print(twitch_output)
```

This first solution decouples the devices from the services and it also reduces
much of the code repetition. It also prevents the exponential growth of
classes.

## Solution 2: Using Protocol

One potential improvement is to use `Protocols` instead of abstract classes.
This change will allow to use any class that has the `get_buffer_data` method,
and not just the ones that inherit from a particular Abstract class.

Note: In Python, types are not check at runtime and are merely to improve the
developer experience, unlike other programming languages, changing from
abstract classes to Protocols should produce the exact same behaviour at run
time.

The changes in the code are minimal:

```diff
from io import StringIO

-from .streaming_device import StreamingDevice
from .. import BufferData


-class DSLRCamera(StreamingDevice):
+class DSLRCamera:
    def get_buffer_data(self) -> BufferData:
        return StringIO("###DSLRDATA###")
```


```diff
+from typing import Protocol
-from abc import ABC, abstractmethod

from .. import BufferData

+class StreamingDevice(Protocol):
-class StreamingDevice(ABC):
-    @abstractmethod
    def get_buffer_data(self) -> BufferData:
        ...
```

```diff
from io import StringIO
from dataclasses import dataclass
from typing import Literal

-from .streaming_device import StreamingDevice
from .. import BufferData

Quality = Literal["360p", "480p", "720p", "1080p", "2160p"]


@dataclass
-class Webcam(StreamingDevice):
+class Webcam:
    quality: Quality = "1080p"

    def get_buffer_data(self) -> BufferData:
        return StringIO(f"###WEBCAMDATA at {self.quality}###")
```


# Solution 3: Combine with Strategy Pattern

In this particular instance, the device is an object with a single method, this
could be a good candidate to apply the Strategy pattern.

To implement the GoF version of the Strategy pattern, no additional changes are
needed. However, it has been shown in the Strategy Pattern section that it is
also possible to reduce some of the boilerplate of the GoF Strategy by using
functions and callables instead of classes.


This implies that `StreamingDevice` is no longer a protocol but a `Type`

```diff
-from typing import Protocol
+from typing import Callable

from .. import BufferData


-class StreamingDevice(Protocol):
-    def get_buffer_data(self) -> BufferData:
-        ...
+StreamingDevice = Callable[[], BufferData]
```

This impacts the implementation of the `DSLRCamera` and the `Webcam` as they
are now functions instead of classes:


```diff
-class DSLRCamera:
-    def get_buffer_data(self) -> BufferData:
-        return StringIO("###DSLRDATA###")
+def dslr_camera_buffer_data() -> BufferData:
+    return StringIO("###DSLRDATA###")
```


```diff
from io import StringIO
-from dataclasses import dataclass
from typing import Literal

from .. import BufferData

+from .streaming_device import StreamingDevice

Quality = Literal["360p", "480p", "720p", "1080p", "2160p"]


-@dataclass
-class Webcam:
-    quality: Quality = "1080p"
-
-    def get_buffer_data(self) -> BufferData:
-        return StringIO(f"###WEBCAMDATA at {self.quality}###")

+def webcam_buffer_data(quality: Quality = "1080p") -> StreamingDevice:
+    def buffer() -> BufferData:
+        return StringIO(f"###WEBCAMDATA at {quality}###")
+
+    return buffer
```

Regarding the StreamingService, a minimal change is needed as now there is no
method called `get_buffer_data`, rather the device itself is callable.

```diff
@dataclass
class StreamingService(ABC):
    ...

    def retrieve_buffer_data(self) -> List[BufferData]:
-        return [device.get_buffer_data() for device in self.devices]
+        return [device() for device in self.devices]
    ...
```

Finally the main script changes slightly to accomodate for this change

```diff
-from .devices import DSLRCamera, Webcam
+from .devices import dslr_camera_buffer_data, webcam_buffer_data
from .services import YouTubeStreamingService, TwitchStreamingService


def main() -> None:
    youtube_service = YouTubeStreamingService()
-    youtube_service.add_device(Webcam(quality="720p"))
+    youtube_service.add_device(webcam_buffer_data(quality="720p"))
    youtube_service.fill_buffer()
    youtube_output = youtube_service.collect_and_close_stream()
    print(youtube_output)

    twitch_service = TwitchStreamingService()
-    twitch_service.add_device(DSLRCamera())
-    twitch_service.add_device(Webcam(quality="720p"))
+    twitch_service.add_device(dslr_camera_buffer_data)
+    twitch_service.add_device(webcam_buffer_data(quality="720p"))    
    twitch_service.fill_buffer()
    twitch_output = twitch_service.collect_and_close_stream()
    print(twitch_output)
```

This third solution shows the advantages of the pattern, a change in all the
devices had no impact in any of the concrete services, only the abstract class
for StreamingService had to be updated. Such a change in the original
implementation would have required changes in all the concrete services.
