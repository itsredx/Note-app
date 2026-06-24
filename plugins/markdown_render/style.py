class RendererStyle:
    """
    CSS Styling options for the Markdown Render widget.
    Provides a way to customize the appearance of the rendered Markdown content.
    You can specify font color, font family, font size, padding, background color, and even custom CSS properties.
    This style will be applied to the container that wraps the rendered Markdown content.

    Attributes:
        fontColor (str): The font color for the rendered Markdown text. Default is "inherit".
        fontFamily (str): The font family for the rendered Markdown text. Default is "inherit".
        fontSize (str): The font size for the rendered Markdown text. Default is "16px".
        padding (str): The padding around the rendered Markdown content. Default is "16px".
        backgroundColor (str): The background color for the rendered Markdown container. Default is "transparent".
        customStyles (dict): A dictionary of additional custom CSS properties to apply to the container.

    Example usage:
        style = RendererStyle(
            fontColor=Colors.hex("#333"),
            fontFamily="Arial, sans-serif",
            fontSize="14px",
            padding=EdgeInsets.all(20),
            backgroundColor=Colors.hex("#f9f9f9"),
            customStyles={
                "border": "1px solid #ddd",
                "borderRadius": "8px"
            }
        )
    """
    def __init__(
        self,
        fontColor: str = "inherit",
        fontFamily: str = "inherit",
        fontSize: str = "16px",
        fontStyle: str = 'normal',
        padding: str = "16px",
        textPadding: str = '1em',
        contentMargin: str = '1em',
        backgroundColor: str = "transparent",
        customStyles: dict = None
    ):
        self.color = fontColor
        self.font_family = fontFamily
        self.font_size = fontSize
        self.font_style = fontStyle
        self.padding = padding
        self.textPadding = textPadding,
        self.contentMargin = contentMargin,
        self.background_color = backgroundColor
        self.custom_css = customStyles or {}

    def to_dict(self):
        style_dict = {
            "color": self.color,
            "fontFamily": self.font_family,
            "fontSize": self.font_size,
            "fontStyle": self.font_style,
            "padding": self.padding,
            "textPadding": self.textPadding,
            "contentMargin": self.contentMargin,
            "backgroundColor": self.background_color
        }
        style_dict.update(self.custom_css)
        return style_dict
