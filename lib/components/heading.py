from typing import Callable, Optional
from pythra import (
    Container,
    StatefulWidget,
    State,
    Row,
    IconButton,
    Icon,
    Icons,
    ButtonStyle,
    BorderRadius,
    BoxDecoration,
    BorderSide,
    SizedBox,
    EdgeInsets,
    Colors,
    Key,
    Widget,
    CrossAxisAlignment,
    MainAxisSize,
)
from lib.constants.colors import AppColors


class HeadingSelectorState(State):
    def initState(self):
        pass

    def build(self) -> Widget:
        return Container(
            key=Key("heading_selector"),
            padding=EdgeInsets.all(8),
            decoration=BoxDecoration(
                borderRadius=BorderRadius.all(16),
                border=BorderSide(
                    width=1,
                    color=Colors.adaptive(dark="#5a5a5a", light="#d3d3d3"),
                ),
                color=Colors.adaptive(
                    dark=AppColors.toolbarBackgroundDarkColor,
                    light=Colors.white,
                ),
            ),
            child=Row(
                mainAxisSize=MainAxisSize.MIN,
                children=[
                    IconButton(
                        key=Key("selector_h1_btn"),
                        icon=Icon(Icons.format_h1_rounded, key=Key("selector_h1_ico")),
                        onPressed=lambda: self.widget.on_heading_selected(1),
                        onPressedName="heading_sel_1",
                        style=ButtonStyle(
                            backgroundColor=AppColors.buttonBackgroundColor,
                            hoverColor=AppColors.buttonHoverColor,
                            shape=BorderRadius.circular(8.0),
                            foregroundColor=AppColors.buttonForegroundColor,
                            activeColor=AppColors.buttonActiveColor,
                        ),
                        tooltip="Heading 1",
                    ),
                    SizedBox(width=8, key=Key("selector_h1_sz")),
                    IconButton(
                        key=Key("selector_h2_btn"),
                        icon=Icon(Icons.format_h2_rounded, key=Key("selector_h2_ico")),
                        onPressed=lambda: self.widget.on_heading_selected(2),
                        onPressedName="heading_sel_2",
                        style=ButtonStyle(
                            backgroundColor=AppColors.buttonBackgroundColor,
                            hoverColor=AppColors.buttonHoverColor,
                            shape=BorderRadius.circular(8.0),
                            foregroundColor=AppColors.buttonForegroundColor,
                            activeColor=AppColors.buttonActiveColor,
                        ),
                        tooltip="Heading 2",
                    ),
                    SizedBox(width=8, key=Key("selector_h2_sz")),
                    IconButton(
                        key=Key("selector_h3_btn"),
                        icon=Icon(Icons.format_h3_rounded, key=Key("selector_h3_ico")),
                        onPressed=lambda: self.widget.on_heading_selected(3),
                        onPressedName="heading_sel_3",
                        style=ButtonStyle(
                            backgroundColor=AppColors.buttonBackgroundColor,
                            hoverColor=AppColors.buttonHoverColor,
                            shape=BorderRadius.circular(8.0),
                            foregroundColor=AppColors.buttonForegroundColor,
                            activeColor=AppColors.buttonActiveColor,
                        ),
                        tooltip="Heading 3",
                    ),
                    SizedBox(width=8, key=Key("selector_h3_sz")),
                    IconButton(
                        key=Key("selector_h4_btn"),
                        icon=Icon(Icons.format_h4_rounded, key=Key("selector_h4_ico")),
                        onPressed=lambda: self.widget.on_heading_selected(4),
                        onPressedName="heading_sel_4",
                        style=ButtonStyle(
                            backgroundColor=AppColors.buttonBackgroundColor,
                            hoverColor=AppColors.buttonHoverColor,
                            shape=BorderRadius.circular(8.0),
                            foregroundColor=AppColors.buttonForegroundColor,
                            activeColor=AppColors.buttonActiveColor,
                        ),
                        tooltip="Heading 4",
                    ),
                    SizedBox(width=8, key=Key("selector_h4_sz")),
                    IconButton(
                        key=Key("selector_h5_btn"),
                        icon=Icon(Icons.format_h5_rounded, key=Key("selector_h5_ico")),
                        onPressed=lambda: self.widget.on_heading_selected(5),
                        onPressedName="heading_sel_5",
                        style=ButtonStyle(
                            backgroundColor=AppColors.buttonBackgroundColor,
                            hoverColor=AppColors.buttonHoverColor,
                            shape=BorderRadius.circular(8.0),
                            foregroundColor=AppColors.buttonForegroundColor,
                            activeColor=AppColors.buttonActiveColor,
                        ),
                        tooltip="Heading 5",
                    ),
                    SizedBox(width=8, key=Key("selector_h5_sz")),
                    IconButton(
                        key=Key("selector_h6_btn"),
                        icon=Icon(Icons.format_h6_rounded, key=Key("selector_h6_ico")),
                        onPressed=lambda: self.widget.on_heading_selected(6),
                        onPressedName="heading_sel_6",
                        style=ButtonStyle(
                            backgroundColor=AppColors.buttonBackgroundColor,
                            hoverColor=AppColors.buttonHoverColor,
                            shape=BorderRadius.circular(8.0),
                            foregroundColor=AppColors.buttonForegroundColor,
                            activeColor=AppColors.buttonActiveColor,
                        ),
                        tooltip="Heading 6",
                    ),
                    SizedBox(width=8, key=Key("selector_h6_sz")),
                    IconButton(
                        key=Key("selector_paragraph_btn"),
                        icon=Icon(Icons.format_paragraph_rounded, key=Key("selector_paragraph_ico")),
                        onPressed=lambda: self.widget.on_heading_selected(0),
                        onPressedName="heading_sel_0",
                        style=ButtonStyle(
                            backgroundColor=AppColors.buttonBackgroundColor,
                            hoverColor=AppColors.buttonHoverColor,
                            shape=BorderRadius.circular(8.0),
                            foregroundColor=AppColors.buttonForegroundColor,
                            activeColor=AppColors.buttonActiveColor,
                        ),
                        tooltip="Normal text",
                    ),
                ],
            ),
        )


class HeadingSelector(StatefulWidget):
    def __init__(
        self,
        on_heading_selected: Callable[[int], None],
        key: Optional[Key] = None,
    ):
        self.on_heading_selected = on_heading_selected
        super().__init__(key or Key("heading_selector_widget"))

    def createState(self) -> HeadingSelectorState:
        return HeadingSelectorState()
