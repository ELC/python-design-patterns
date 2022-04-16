from .devices import dslr_camera_buffer_data, webcam_buffer_data
from .services import YouTubeStreamingService, TwitchStreamingService


def main() -> None:
    youtube_service = YouTubeStreamingService()
    youtube_service.add_device(webcam_buffer_data(quality="720p"))
    youtube_service.fill_buffer()
    youtube_output = youtube_service.collect_and_close_stream()
    print(youtube_output)

    twitch_service = TwitchStreamingService()
    twitch_service.add_device(dslr_camera_buffer_data)
    twitch_service.add_device(webcam_buffer_data(quality="720p"))
    twitch_service.fill_buffer()
    twitch_output = twitch_service.collect_and_close_stream()
    print(twitch_output)


if __name__ == "__main__":
    main()
