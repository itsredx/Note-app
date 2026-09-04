
from pythra import Colors

class VideoPlayerStyle:
    """
    Styling options for the VideoPlayer widget.
    Controls the vid-box appearance: shadow, border, background.
    """

    def __init__(
        self,
        border_radius: str = "24px",
        shadow_color: str = "rgba(0, 0, 0, 0.5)",
        shadow_blur: int = 30,
        shadow_spread: int = 10,
        shadow_offset_y: int = 10,
        border_color: str = "rgba(255, 255, 255, 0.9)",
        border_width: str = "0px",
        background_color: str = Colors.background,
        custom_css: dict = None,
    ):
        self.border_radius = border_radius
        self.shadow_color = shadow_color
        self.shadow_blur = shadow_blur
        self.shadow_spread = shadow_spread
        self.shadow_offset_y = shadow_offset_y
        self.border_color = border_color
        self.border_width = border_width
        self.background_color = background_color
        self.custom_css = custom_css or {}

    def to_dict(self):
        style_dict = {
            "borderRadius": self.border_radius,
            "shadowColor": self.shadow_color,
            "shadowBlur": self.shadow_blur,
            "shadowSpread": self.shadow_spread,
            "shadowOffsetY": self.shadow_offset_y,
            "borderColor": self.border_color,
            "borderWidth": self.border_width,
            "backgroundColor": self.background_color,
        }
        style_dict.update(self.custom_css)
        return style_dict
