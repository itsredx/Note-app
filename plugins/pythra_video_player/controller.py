class VideoPlayerController:
    """
    Controller to programmatically control the VideoPlayer.
    Provides play/pause/stop/seek/volume controls and media switching.
    """

    def __init__(self):
        self._state = None

    def _attach(self, state):
        self._state = state

    def _detach(self):
        self._state = None

    def play(self):
        """Resume or start playback."""
        if self._state:
            self._state._ffmpeg_play()

    def pause(self):
        """Pause playback."""
        if self._state:
            self._state._ffmpeg_pause()

    def stop(self):
        """Stop playback."""
        if self._state:
            self._state._ffmpeg_stop()

    def seek(self, position_ms: int):
        """Seek to a position in milliseconds."""
        if self._state:
            self._state._ffmpeg_seek(position_ms)

    def set_volume(self, volume: int):
        """Set volume (0-100)."""
        if self._state:
            self._state._ffmpeg_set_volume(volume)

    def set_video(self, video_path: str):
        """Change the video source at runtime."""
        if self._state:
            self._state._ffmpeg_set_video(video_path)

    @property
    def is_playing(self) -> bool:
        """Returns True if the player is currently playing."""
        if self._state:
            return self._state._ffmpeg_is_playing()
        return False
