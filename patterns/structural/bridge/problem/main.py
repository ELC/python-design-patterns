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


if __name__ == "__main__":
    main()
