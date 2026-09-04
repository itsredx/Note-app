"""
PyThra Video Player Plugin
A high-performance video player widget using VLC with a transparent WebEngine overlay.
Handles vid-box rendering, canvas shadow effects, scroll-based clipping,
and native video frame synchronization.
"""

from .widget import VideoPlayer

__version__ = "1.0.0"
__all__ = ["VideoPlayer"]

# Plugin definition for Pythra framework
plugin_definition = {
    "name": "pythra-video-player",
    "version": __version__,
    "js_modules": {
        "PythraVideoPlayer": {
            "file": "js/video_player_engine.js",
            "global": "PythraVideoPlayer",
            "initializer": "initialize",
        }
    },
}
