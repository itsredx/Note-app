# main.py
import os
import sys
import json
from typing import Optional, Callable, List, Dict, Any

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath('note-app/lib'))))


# import colors
from lib.constants.colors import *
from lib.constants.theme import AppThemes
from lib.screens.components.header_actions import HeaderActions

from plugins.markdown.widget import MarkdownEditor
from plugins.markdown.controller import MarkdownEditorController
from plugins.markdown.style import EditorStyle, EditorGridStyle, EditorContentStyle
from plugins.markdown.utils.sys_font_loader import get_system_fonts_as_json

# Welcome to your new Pythra App!
from pythra import (
    Framework,
    StatefulWidget,
    State,
    Column,
    Row,
    Key,
    Widget,
    Container,
    BoxDecoration,
    BorderSide,
    Text,
    Alignment,
    Colors,
    Center,
    ElevatedButton,
    SizedBox,
    MainAxisAlignment,
    CrossAxisAlignment,
    ClipPath,
    EdgeInsets,
    Icon,
    IconButton,
    Icons,
    ButtonStyle,
    BorderRadius,
    TextStyle,
    Stack,
    Positioned,
    GradientTheme,
    Image,
    AssetImage,
    DerivedDropdown,
    DerivedDropdownController,
    DerivedDropdownTheme,
    Dropdown,
    DropdownController,
    DropdownTheme,
    VerticalDirection,
    Navigator, PageRoute, NavigatorState,
)

formatted_fonts_json = get_system_fonts_as_json()
# print(json.loads(formatted_fonts_json))
fonts = json.loads(formatted_fonts_json)
labels = []
for font in fonts:
    labels.append(font["label"])
    if font["label"] == "Verdana":
        print("val: ", font["val"])
    # print(f"label: {labels.sort()}")
    # print(f"Font-> label: {font['label']} val: {font['val']}")


show_font = True


class NoteEditorScreenState(State):
    def __init__(self, navigator: NavigatorState):
        self.count = 0
        self.editor = MarkdownEditorController(
            initial_content="<h1>Welcome from Controller!</h1><p>Start writing your document here...</p>"
        )
        self.d_controller = DropdownController(selectedValue=labels[0])
        # self.dropdown_controller = DerivedDropdownController(value='Agency FB',items=labels)
        # self.dropdown_theme = DerivedDropdownTheme(width=200)

        self.dropdown = Dropdown(
            controller=self.d_controller,
            key=Key("my_dropdown"),
            items=labels,
            onChanged=self.changeFont,
            dropDirection=VerticalDirection.UP,
            theme=DropdownTheme(
                width=330,
                dropDownHeight=500,
                dropdownMargin=EdgeInsets.only(bottom=12),
                fontSize=12,
                borderWidth=0.0,
                backgroundColor=AppColors.dropDownColor,
                dropdownColor=AppColors.dropDownColor,
                textColor=AppColors.iconColor,
            ),
        )

        self.markdown_editor = MarkdownEditor(
            key=Key("markdow_editor_widget"),
            controller=self.editor,
            height="calc(100vh - 70px)",
            width="100vw",
            show_grid=True,
        )

        super().__init__()
        self.navigator = navigator

    @property
    def is_dark(self):
        return Framework.instance().theme.brightness == 'dark'

    # changeMode is now handled by ThemeToggleButton internally.
    # We still keep is_dark helper if needed for other logic, but rebuilds
    # will be triggered specifically by the child widgets.

    def bold(self):
        print('Bold executed')
        self.editor.bold()
        # self.setState()

    def italic(self):
        self.editor.italic()

    def underline(self):
        self.editor.underline()

    def strikeThrough(self):
        self.editor.strike_through()

    def setParagraph(self):
        self.editor.set_paragraph()

    def insertUnorderedList(self):
        self.editor.insert_unordered_list()

    def insertOrderedList(self):
        self.editor.insert_ordered_list()

    def setFontColor(self, color):
        self.editor.set_font_color(color)

    def setHeading(self, level: int):
        self.editor.set_heading(level=level)

    def setFont(self, font_family: str):
        self.editor.set_font_name(font_family=font_family)
        self.editor.focus()

    def changeFont(self, new_value):
        print("Font changed!: ", new_value)
        for font in fonts:
            if font["label"] == new_value:
                self.setFont(font["val"])

    def insertImage(
        self, url: str = "c:\\Users\\SMILETECH COMPUTERS\\Documents\\food.png"
    ):
        self.editor.insert_image(url=url)

    def incrementCounter(self):
        self.count += 1
        print("self.count: ", self.count)
        self.setState()

    def decrementCounter(self):
        self.count -= 1
        print("self.count: ", self.count)
        self.setState()

    def build(self) -> Widget:
        cursor_state = self.editor.cursor_state
        editor_style = style = EditorStyle(
            focus_ring_color=Colors.transparent,
            focus_ring_width="0.0px",
            border_color=Colors.transparent,
            border_width="0.0px",
            accent_color=Colors.adaptive(dark="#333030", light="#e9ecef"),
            grid_enabled=True,
            grid_dot_color=Colors.grey,
            grid_background_color=Colors.adaptive(dark="#121212", light=Colors.transparent),
            content_text_color=Colors.adaptive(dark=Colors.lightgrey, light=Colors.grey),
        )

        # 4. CRITICAL: Inject the dynamic style directly into the persistent widget instance.
        #    This updates the widget's configuration without recreating it.
        self.markdown_editor.style = editor_style
        return Container(
            key=Key("home_page_Pythra_wrapper_container"),
            height="100vh",
            width="100vw",
            child=Center(
                key=Key("home_page_Pythra_center"),
                child=Stack(
                    key=Key("home_page_Pythra_center_Stack"),
                    # clipBehavior=ClipBehavior.NONE,
                    children=[
                        Container(
                            key=Key("markdown_editor_wrapper_container"),
                            height="100vh",
                            width="100vw",
                            child=Column(
                                children=[
                                    Container(
                                        key=Key("Header_container"),
                                        height="70px",
                                        width="100vw",
                                        color=AppColors.appBackgroundColor,
                                        padding=EdgeInsets.symmetric(horizontal=20),
                                        child=Row(
                                            mainAxisAlignment=MainAxisAlignment.SPACE_BETWEEN,
                                            crossAxisAlignment=CrossAxisAlignment.STRETCH,
                                            key=Key("Header_row"),
                                            children=[
                                                Container(
                                                    key=Key(
                                                        "file_name_and_details_header"
                                                    ),
                                                    padding=EdgeInsets.only(top=20),
                                                    child=Row(
                                                        key=Key(
                                                            "file_name_and_details_and_back_button_header_row"
                                                        ),
                                                        children=[
                                                            IconButton(
                                                                key=Key("back_btn_1"),
                                                                icon=Icon(
                                                                    Icons.arrow_back_rounded,
                                                                    key=Key(
                                                                        "back_ico_1"
                                                                    ),
                                                                ),
                                                                onPressed=lambda: print("Back button pressed"),
                                                                style=ButtonStyle(
                                                                    backgroundColor=AppColors.buttonBackgroundColor,
                                                                    hoverColor=AppColors.buttonHoverColor,
                                                                    foregroundColor=AppColors.buttonForegroundColor,
                                                                ),
                                                            ),
                                                            SizedBox(
                                                                width=16,
                                                                key=Key(
                                                                    "sixe_box_back_controls_1"
                                                                ),
                                                            ),
                                                            Column(
                                                                key=Key(
                                                                    "file_name_and_details_header_column"
                                                                ),
                                                                mainAxisAlignment=MainAxisAlignment.START,
                                                                crossAxisAlignment=CrossAxisAlignment.START,
                                                                children=[
                                                                    Text(
                                                                        "Welcome",
                                                                        key=Key(
                                                                            "file_name"
                                                                        ),
                                                                        style=TextStyle(
                                                                            fontSize=18,
                                                                            fontWeight="bold",
                                                                            color=Colors.adaptive(dark="#EDEDED", light=Colors.black),
                                                                            # fontFamily='verdana',
                                                                        ),
                                                                    ),
                                                                    Text(
                                                                        "first file",
                                                                        key=Key(
                                                                            "file_detail"
                                                                        ),
                                                                        style=TextStyle(
                                                                            fontSize=14,
                                                                            color=Colors.adaptive(dark="#9E9E9E", light=Colors.grey),
                                                                        ),
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                ),
                                                Container(
                                                    key=Key(
                                                        "search_ai_and_controls_header"
                                                    ),
                                                    padding=EdgeInsets.only(top=20),
                                                    child=Row(
                                                        key=Key(
                                                            "search_ai_and_controls_header_row"
                                                        ),
                                                        mainAxisAlignment=MainAxisAlignment.END,
                                                        crossAxisAlignment=CrossAxisAlignment.START,
                                                        children=[
                                                            HeaderActions(
                                                                key=Key("header_actions"),
                                                                onSave=self.incrementCounter,
                                                                onAiChat=self.incrementCounter,
                                                                onAccount=self.incrementCounter,
                                                            )
                                                        ],
                                                    ),
                                                ),
                                            ],
                                        ),
                                    ),
                                    self.markdown_editor,
                                ]
                            ),
                        ),
                        Positioned(
                            height=40,
                            width="100vw",
                            bottom="18px",
                            key=Key("home_page_Pythra_decrement_btn_Positioned"),
                            child=Center(
                                key=Key(
                                    "home_page_Pythra_Center_Positioned_Container"
                                ),
                                child=Container(
                                key=Key(
                                    "home_page_Pythra_decrement_btn_Positioned_Container"
                                ),
                                # color=Colors.white,
                                padding=EdgeInsets.all(8),
                                child=Row(
                                    mainAxisAlignment=MainAxisAlignment.CENTER,
                                    crossAxisAlignment=CrossAxisAlignment.CENTER,
                                    key=Key(
                                        "home_page_Pythra_decrement_btn_Positioned_Container_Row"
                                    ),
                                    children=[
                                        # self.dropdown,
                                        Dropdown(
                                            controller=self.d_controller,
                                            key=Key("my_dropdown"),
                                            items=labels,
                                            onChanged=self.changeFont,
                                            dropDirection=VerticalDirection.UP,
                                            theme=DropdownTheme(
                                                width=330,
                                                dropDownHeight=500,
                                                dropdownMargin=EdgeInsets.only(
                                                    bottom=12
                                                ),
                                                fontSize=12,
                                                borderWidth=0.0,
                                                borderColor=AppColors.transparent,
                                                backgroundColor=AppColors.dropDownColor,
                                                dropdownColor=AppColors.dropDownColor,
                                                textColor=AppColors.iconColor,
                                                dropdownTextColor=AppColors.iconColor,
                                                dropdownHoverColor=AppColors.dropDownMenuHoverColor,
                                                hoverColor=AppColors.dropDownHoverColor,
                                                itemHoverColor=AppColors.dropDownMenuHoverColor,
                                            ),
                                        ),
                                        SizedBox(
                                            width=(12),
                                            key=Key("sixe_box_header_dropdown"),
                                        ),
                                        IconButton(
                                            key=Key("format_color_text_rounded_btn"),
                                            icon=Icon(
                                                Icons.format_color_text_rounded,  # format_color_text_rounded
                                                key=Key(
                                                    "format_color_text_rounded_btn_ico"
                                                ),
                                                # color=(
                                                #     AppColors.iconDarkMode
                                                #     if self.is_dark
                                                #     else AppColors.iconLightModeFormatColorTextRounded
                                                # ),
                                                cssClass="pythra-toolbar-font-color-btn",
                                            ),
                                            onPressed=self.setFontColor,
                                            onPressedArgs=["red"],
                                            style=ButtonStyle(
                                                backgroundColor=AppColors.buttonBackgroundColor,
                                                hoverColor=AppColors.buttonHoverColor,
                                                shape=BorderRadius.circular(8.0),
                                                foregroundColor=AppColors.buttonForegroundColor,
                                                activeColor=AppColors.buttonActiveColor,
                                            ),
                                            tooltip="Text Color",
                                        ),
                                        SizedBox(
                                            width=12,
                                            key=Key(
                                                "format_color_text_rounded_size_box"
                                            ),
                                        ),
                                        IconButton(
                                            key=Key("format_h1_rounded_btn"),
                                            icon=Icon(
                                                Icons.format_h1_rounded,
                                                key=Key("format_h1_rounded_btn_ico"),
                                            ),
                                            onPressed=self.setHeading,
                                            style=ButtonStyle(
                                                backgroundColor=AppColors.buttonBackgroundColor,
                                                hoverColor=AppColors.buttonHoverColor,
                                                shape=BorderRadius.circular(8.0),
                                                foregroundColor=AppColors.buttonForegroundColor,
                                                activeColor=AppColors.buttonActiveColor,
                                            ),
                                            tooltip="Heading 1",
                                        ),
                                        SizedBox(
                                            width=12,
                                            key=Key("format_h1_rounded_size_box"),
                                        ),
                                        IconButton(
                                            key=Key("format_paragraph_rounded_btn"),
                                            icon=Icon(
                                                Icons.format_paragraph_rounded,
                                                key=Key(
                                                    "format_paragraph_rounded_btn_ico"
                                                ),
                                            ),
                                            onPressed=self.setParagraph,
                                            style=ButtonStyle(
                                                backgroundColor=AppColors.buttonBackgroundColor,
                                                hoverColor=AppColors.buttonHoverColor,
                                                shape=BorderRadius.circular(8.0),
                                                foregroundColor=AppColors.buttonForegroundColor,
                                                activeColor=AppColors.buttonActiveColor,
                                            ),
                                            tooltip="Paragraph",
                                        ),
                                        SizedBox(
                                            width=12,
                                            key=Key(
                                                "format_paragraph_rounded_size_box"
                                            ),
                                        ),
                                        IconButton(
                                            key=Key("format_bold_rounded_btn"),
                                            icon=Icon(
                                                Icons.format_bold_rounded,
                                                key=Key("format_bold_rounded_btn_ico"),
                                            ),
                                            onPressed=lambda: self.bold(),
                                            onPressedName= 'bold_lambda',
                                            style=ButtonStyle(
                                                backgroundColor=(
                                                    Colors.red
                                                    if cursor_state.is_bold and self.is_dark
                                                    else AppColors.buttonBackgroundColor
                                                ),
                                                hoverColor=AppColors.buttonHoverColor,
                                                shape=BorderRadius.circular(8.0),
                                                foregroundColor=AppColors.buttonForegroundColor,
                                                activeColor=AppColors.buttonActiveColor,
                                            ),
                                            tooltip="Bold",
                                            cssClass="pythra-toolbar-bold",
                                        ),
                                        SizedBox(
                                            width=12,
                                            key=Key("format_bold_rounded_size_box"),
                                        ),
                                        IconButton(
                                            key=Key("format_italic_rounded_btn"),
                                            icon=Icon(
                                                Icons.format_italic_rounded,
                                                key=Key(
                                                    "format_italic_rounded_btn_ico"
                                                ),
                                            ),
                                            onPressed=self.italic,
                                            style=ButtonStyle(
                                                backgroundColor=AppColors.buttonBackgroundColor,
                                                hoverColor=AppColors.buttonHoverColor,
                                                shape=BorderRadius.circular(8.0),
                                                foregroundColor=AppColors.buttonForegroundColor,
                                                activeColor=AppColors.buttonActiveColor,
                                            ),
                                            tooltip="Italic",
                                            cssClass="pythra-toolbar-italic",
                                        ),
                                        SizedBox(
                                            width=12,
                                            key=Key("format_italic_rounded_size_box"),
                                        ),
                                        IconButton(
                                            key=Key("format_underlined_rounded_btn"),
                                            icon=Icon(
                                                Icons.format_underlined_rounded,
                                                key=Key(
                                                    "format_underlined_rounded_btn_ico"
                                                ),
                                            ),
                                            onPressed=self.underline,
                                            style=ButtonStyle(
                                                backgroundColor=AppColors.buttonBackgroundColor,
                                                hoverColor=AppColors.buttonHoverColor,
                                                shape=BorderRadius.circular(8.0),
                                                foregroundColor=AppColors.buttonForegroundColor,
                                                activeColor=AppColors.buttonActiveColor,
                                            ),
                                            tooltip="Underline",
                                            cssClass="pythra-toolbar-underline",
                                        ),
                                        SizedBox(
                                            width=12,
                                            key=Key(
                                                "format_underlined_rounded_size_box"
                                            ),
                                        ),
                                        IconButton(
                                            key=Key("format_strikethrough_rounded_btn"),
                                            icon=Icon(
                                                Icons.format_strikethrough_rounded,
                                                key=Key(
                                                    "format_strikethrough_rounded_btn_ico"
                                                ),
                                            ),
                                            onPressed=self.strikeThrough,
                                            style=ButtonStyle(
                                                backgroundColor=AppColors.buttonBackgroundColor,
                                                hoverColor=AppColors.buttonHoverColor,
                                                shape=BorderRadius.circular(8.0),
                                                foregroundColor=AppColors.buttonForegroundColor,
                                                activeColor=AppColors.buttonActiveColor,
                                            ),
                                            tooltip="Strike Through",
                                            cssClass="pythra-toolbar-strikethrough",
                                        ),
                                        SizedBox(
                                            width=12,
                                            key=Key(
                                                "format_strikethrough_rounded_size_box"
                                            ),
                                        ),
                                        IconButton(
                                            key=Key("format_list_bulleted_rounded_btn"),
                                            icon=Icon(
                                                Icons.format_list_bulleted_rounded,
                                                key=Key(
                                                    "format_list_bulleted_rounded_btn_ico"
                                                ),
                                            ),
                                            onPressed=self.insertUnorderedList,
                                            style=ButtonStyle(
                                                backgroundColor=AppColors.buttonBackgroundColor,
                                                hoverColor=AppColors.buttonHoverColor,
                                                shape=BorderRadius.circular(8.0),
                                                foregroundColor=AppColors.buttonForegroundColor,
                                                activeColor=AppColors.buttonActiveColor,
                                            ),
                                            tooltip="List Bulleted",
                                            cssClass="pythra-toolbar-ul",
                                        ),
                                        SizedBox(
                                            width=12,
                                            key=Key(
                                                "format_list_bulleted_rounded_size_box"
                                            ),
                                        ),
                                        IconButton(
                                            key=Key("format_list_numbered_rounded_btn"),
                                            icon=Icon(
                                                Icons.format_list_numbered_rounded,
                                                key=Key(
                                                    "format_list_numbered_rounded_btn_ico"
                                                ),
                                            ),
                                            onPressed=self.insertOrderedList,
                                            style=ButtonStyle(
                                                backgroundColor=AppColors.buttonBackgroundColor,
                                                hoverColor=AppColors.buttonHoverColor,
                                                shape=BorderRadius.circular(8.0),
                                                foregroundColor=AppColors.buttonForegroundColor,
                                                activeColor=AppColors.buttonActiveColor,
                                            ),
                                            tooltip="List Numbered",
                                            cssClass="pythra-toolbar-ol",
                                        ),
                                        Container(
                                            key=Key("divider_container"),
                                            color=AppColors.iconColor,
                                            height=30,
                                            width=2,
                                            margin=EdgeInsets.symmetric(
                                                horizontal=12,
                                            ),
                                        ),
                                        ElevatedButton(
                                            key=Key("image_rounded_btn"),
                                            child=Row(
                                                key=Key("image_rounded_btn_inner_row"),
                                                children=[
                                                    Icon(
                                                        Icons.image_rounded,
                                                        key=Key(
                                                            "image_rounded_btn_ico"
                                                        ),
                                                        size=24,
                                                        color=AppColors.iconColor,
                                                    ),
                                                    SizedBox(
                                                        width=8,
                                                        key=Key(
                                                            "image_rounded_btn_sized_box"
                                                        ),
                                                    ),
                                                    Text(
                                                        "Image",
                                                        key=Key(
                                                            "image_rounded_btn_txt"
                                                        ),
                                                        style=TextStyle(
                                                            fontSize=20,
                                                        ),
                                                    ),
                                                ],
                                            ),
                                            style=ButtonStyle(
                                                backgroundColor=AppColors.buttonBackgroundColor,
                                                foregroundColor=AppColors.buttonForegroundColor,
                                                elevation=0,
                                                shape=BorderRadius.circular(8.0),
                                                margin=EdgeInsets.all(0),
                                                hoverColor=AppColors.buttonHoverColor,
                                            ),
                                            onPressed=self.insertImage,
                                            tooltip="Image",
                                        ),
                                    ],
                                ),
                                decoration=BoxDecoration(
                                    borderRadius=BorderRadius.all(16),
                                    border=BorderSide(width=1, color=Colors.adaptive(dark="#5a5a5a", light="#d3d3d3")),
                                    color=Colors.adaptive(dark=AppColors.toolbarBackgroundDarkColor, light=Colors.white),
                                ),
                            ),),
                        ),
                    ],
                ),
            ),
        )


class NoteEditorScreen(StatefulWidget):
    def __init__(
        self,
        key: Key,
        navigator: NavigatorState,
    ):
        self.navigator = navigator
        super().__init__(key=key)

    def createState(self) -> NoteEditorScreenState:
        return NoteEditorScreenState(self.navigator)


class MainState(State):
    def __init__(self):
        self.home_page = NoteEditorScreen(key=Key("home_page"))

    def build(self):
        return self.home_page


class Main(StatefulWidget):
    def createState(self) -> MainState:
        return MainState()


if __name__ == "__main__":
    # This allows running the app directly with `python lib/main.py`
    # as well as with the CLI's `pythra run` command.
    app = Framework.instance()
    app.set_root(Main(key=Key("home_page_wrapper")))
    app.run()
