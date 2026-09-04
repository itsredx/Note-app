from pythra import StatefulWidget, Key
from .player_state import VideoPlayerState
from .style import VideoPlayerStyle
from .controller import VideoPlayerController


class VideoPlayer(StatefulWidget):
    """
    High-performance video player widget for Pythra.

    Uses an FFmpeg subprocess driving a high-speed MJPEG stream into a local WebSocket.
    The frames are decoded natively in Chromium (WebEngine) and rendered via Canvas API
    supporting full CSS rules like rounded corners, opacity, and transforms natively.

    Usage:
        VideoPlayer(
            key=Key("my_video"),
            video_path="/path/to/video.mp4",
            width="600px",
            height="350px",
        )
    """

    def __init__(
        self,
        key: Key,
        video_path: str = "",
        controller: VideoPlayerController = None,
        width: str = "600px",
        height: str = "338px",
        border_radius: str = "24px",
        style: VideoPlayerStyle = None,
    ):
        self.video_path = video_path
        self.controller = controller
        self.width = width
        self.height = height
        self.border_radius = border_radius
        self.style = style if style else VideoPlayerStyle()
        super().__init__(key=key)

    def createState(self):
        return VideoPlayerState()
