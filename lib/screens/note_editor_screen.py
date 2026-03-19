# main.py
import os
import sys
import json
import time
from typing import Optional, Callable, List, Dict, Any
from PySide6.QtCore import QTimer

from lib.components.chat_card import ChatCard
from lib.screens.settings_screen import SettingsAndProfileScreen

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath("note-app/lib"))))


# import colors
from lib.constants.colors import *
from lib.constants.theme import AppThemes
from lib.components.header_actions import HeaderActions
from lib.components.ai_controls import AiActionsControls

from plugins.markdown.widget import MarkdownEditor
from plugins.markdown.controller import MarkdownEditorController
from plugins.markdown.style import EditorStyle, EditorGridStyle, EditorContentStyle
from plugins.markdown.utils.sys_font_loader import get_system_fonts_as_json

# Welcome to your new Pythra App!
from pythra import (
    Framework,
    ListTile,
    StatefulWidget,
    State,
    Column,
    Row,
    Key,
    VirtualDropdown,
    VirtualDropdownController,
    VirtualDropdownTheme,
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
    VirtualDropdown,
    VirtualDropdownController,
    VirtualDropdownTheme,
    Dropdown,
    DropdownMenuItem,
    DropdownController,
    DropdownTheme,
    VerticalDirection,
    Navigator,
    PageRoute,
    NavigatorState,
    InputDecoration,
)

DEFAULT_FONTS = [
    {
        "label": "System Default",
        "val": '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
    },
    {"label": "Arial", "val": "Arial, sans-serif"},
    {"label": "Verdana", "val": "Verdana, sans-serif"},
    {"label": "Times New Roman", "val": "'Times New Roman', serif"},
    {"label": "Georgia", "val": "Georgia, serif"},
    {"label": "Courier New", "val": "'Courier New', monospace"},
]

print("Initializing with default fonts...")
SYSTEM_FONTS = DEFAULT_FONTS

show_font = True
FONTS_LOADED = False


def load_system_fonts(callback=None):
    global SYSTEM_FONTS, FONTS_LOADED
    if FONTS_LOADED:
        print("PythraMagic: Fonts already loaded, skipping.")
        # if callback:
        #     callback()
        return

    print("PythraMagic: Loading system fonts...")
    try:
        from plugins.markdown.utils.sys_font_loader import get_system_fonts_as_json

        full_fonts = json.loads(get_system_fonts_as_json())
        if full_fonts:
            SYSTEM_FONTS = full_fonts
            FONTS_LOADED = True
            print(f"PythraMagic: Loaded {len(SYSTEM_FONTS)} system fonts.")
            # if callback:
            #     callback()
    except Exception as e:
        print(f"PythraMagic Error loading fonts: {e}")


class NoteEditorScreenState(State):
    def __init__(self, navigator: NavigatorState):
        self.count = 0
        parent_key = Key("note_editor_screen")
        self.parent_key = parent_key.value
        self.chatOpen = False
        self.editor = MarkdownEditorController(
            initial_content="<h1>Welcome from Controller!</h1><p>Start writing your document here...</p>"
        )
        self.d_controller = DropdownController(
            selectedValue=SYSTEM_FONTS[0]["val"] if SYSTEM_FONTS else "Arial"
        )
        self.dropdown_controller = VirtualDropdownController(
            value="Arial",
            items=[f["label"] for idx, f in enumerate(SYSTEM_FONTS)],
        )
        # self.dropdown_theme = VirtualDropdownTheme(width=200)

        self.header_action = HeaderActions(
            key=Key("header_actions"),
            onSave=self.incrementCounter,
            onAiChatContext=self.editor,
            onAccount=self.open_settings,
        )

        self.markdown_editor = MarkdownEditor(
            key=Key("markdow_editor_widget"),
            controller=self.editor,
            height="calc(100vh - 70px)",
            width="100vw",
            show_grid=True,
            overlay=AiActionsControls(
                key=Key("ai_controls_popup"),
                editor=self.editor,
                onGenerate=lambda: self.editor.hide_overlay(),
                chatOpen=self.header_action,
            ),
        )

        # Define stable style
        self.editor_style = EditorStyle(
            focus_ring_color=Colors.transparent,
            focus_ring_width="0.0px",
            border_color=Colors.transparent,
            border_width="0.0px",
            accent_color=Colors.adaptive(dark="#333030", light="#e9ecef"),
            grid_enabled=True,
            grid_dot_color=Colors.grey,
            grid_background_color=Colors.adaptive(
                dark="#121212", light=Colors.transparent
            ),
            content_text_color=Colors.adaptive(
                dark=Colors.lightgrey, light=Colors.grey
            ),
        )
        # Inject style immediately
        self.markdown_editor.style = self.editor_style

        self.dropdown = VirtualDropdown(
                controller=self.dropdown_controller,
                key=Key("my_font_dropdown"),
                itemBuilder=self.vlist_item_builder,
                margin=EdgeInsets.only(top=-20),
                # items=[
                #     DropdownMenuItem(
                #         key=Key(f"font_item_{idx}"),
                #         value=f["val"],
                #         label=f["label"],
                #         child=Text(
                #             f["label"],
                #             style=TextStyle(
                #                 fontFamily=f["val"],
                #                 fontSize=14,
                #             ),
                #             key=Key(f"font_text_{idx}"),
                #             overflow="ellipsis",
                #         ),
                #         tooltip=f["label"],
                #     )
                #     for idx, f in enumerate(
                #         SYSTEM_FONTS
                #     )
                # ],
                onChanged=self.changeFont,
                dropDirection=VerticalDirection.UP,
                theme=VirtualDropdownTheme(
                    inputDecoration=InputDecoration(
                        label="Fonts",
                        hintText="Select an option...",
                        fillColor=AppColors.dropDownColor,
                        labelColor=Colors.onSurfaceVariant,
                        focusColor=Colors.primary,
                        borderRadius=BorderRadius.all(12),
                        border=BorderSide(
                            width=2,
                            color=Colors.outline,
                        ),
                        focusedBorder=BorderSide(
                            width=2,
                            color=Colors.primary,
                        ),
                        labelStyle=TextStyle(
                            fontSize=18,
                            fontFamily="Arial",
                        ),
                        hintStyle=TextStyle(fontSize=14),
                        filled=False,
                    ),
                    # dropdownMargin=EdgeInsets.only(
                    #     top=-8
                    # ),
                    width=300,
                    # dropDownHeight=400,
                    # elevation=12,
                    # dropdownColor=Colors.adaptive(
                    #     dark=AppColors.toolbarBackgroundDarkColor,
                    #     light=Colors.white,
                    # ),
                    # dropdownHoverColor=Colors.adaptive(
                    #     dark=AppColors.toolbarBackgroundDarkColor,
                    #     light=Colors.white,
                    # ),
                    dropdownTextColor=AppColors.buttonForegroundColor,
                    # hoverColor=AppColors.dropDownHoverColor,
                    # itemHoverColor=AppColors.dropDownMenuHoverColor,
                    # menuPadding=EdgeInsets.symmetric(
                    #     vertical=8
                    # ),
                    # itemMargin=EdgeInsets.symmetric(
                    #     vertical=4, horizontal=4
                    # ),
                    selectedItemShape=BorderRadius.all(8),
                    selectedItemColor=AppColors.buttonBackgroundColor,
                    # selectedItemTextColor=AppColors.buttonForegroundColor,
                ),
            )
        

        super().__init__()
        self.navigator = navigator

    def initState(self):
        # print("NoteEditorScreenState: initState")
        self.note_editor_route = PageRoute(
            builder=lambda nav: NoteEditorScreen(
                key=Key("note_page"),
                navigator=nav,
            ),
            name="note_editor",
        )
        self.settings_route = PageRoute(
            builder=lambda nav: SettingsAndProfileScreen(
                key=Key("settings_&_profile_page"), navigator=nav
            ),
            name="settings_page",
        )

    #     QTimer.singleShot(100, self._load_fonts)

    # def _load_fonts(self):
    #     load_system_fonts(callback=self.setState)

    @property
    def is_dark(self):
        return Framework.instance().theme.brightness == "dark"

    # changeMode is now handled by ThemeToggleButton internally.
    # We still keep is_dark helper if needed for other logic, but rebuilds
    # will be triggered specifically by the child widgets.

    def bold(self):
        print("Bold executed")
        self.editor.bold()
        # self.setState()

    def italic(self):
        self.editor.italic()

    def underline(self):
        # self.editor.underline()
        self.editor.replace_selection_with_markdown(markdown_text="Underline")
        self.setState()

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
        self.setFont(new_value)

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

    def open_settings(self):
        self.navigator.push(self.settings_route)

    def select_item(self, item):
        print("Selected item: ", item)
        selected_font = item[0] if isinstance(item, list) else item
        self.dropdown_controller.value = selected_font
        self.setFont(
            SYSTEM_FONTS[self.dropdown_controller.items.index(selected_font)]["val"]
        )
        self.dropdown.get_state().toggle_dropdown()
        # self.setState()

    def vlist_item_builder(self, item: int) -> Widget:
        return Container(
            height=32,
            margin=EdgeInsets.symmetric(horizontal=0, vertical=8),
            padding=EdgeInsets.symmetric(horizontal=12, vertical=8),
            color=(
                AppColors.buttonActiveColor
                if self.dropdown_controller.items[item]
                == self.dropdown_controller.value
                else Colors.transparent
            ),
            width="100%",
            decoration=BoxDecoration(
                borderRadius=BorderRadius.circular(4),
            ),
            key=Key(f"dropdown_item_{item}_padding_{self.parent_key}"),
            child=ListTile(
                key=Key(f"dropdown_item_{item}_{self.parent_key}"),
                title=Text(
                    self.dropdown_controller.items[item],
                    key=Key(f"dropdown_item_title_{item}_{self.parent_key}"),
                    style=TextStyle(
                        color=AppColors.buttonForegroundColor,
                        fontFamily=SYSTEM_FONTS[item]["val"],
                        fontSize=14,
                    ),
                    overflow="ellipsis",
                ),
                tooltip=self.dropdown_controller.items[item],
                onTap=self.select_item,
                onTapName=f"item_tap_callback_{self.parent_key}_{item}",
                onTapArg=[self.dropdown_controller.items[item]],
                selected=self.dropdown_controller.items[item]
                == self.dropdown_controller.value,
                selectedTileColor=Colors.primary,
                contentPadding=EdgeInsets.symmetric(horizontal=12, vertical=8),
            ),
        )

    def build(self) -> Widget:
        cursor_state = self.editor.cursor_state

        return Container(
            key=Key("home_page_Pythra_wrapper_container"),
            height="100vh",
            width="100vw",
            color=Colors.adaptive(dark="#121212", light=Colors.transparent),
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
                                    Stack(
                                        key=Key("header_stack"),
                                        children=[
                                            Container(
                                                key=Key("Header_container"),
                                                height="70px",
                                                width="100vw",
                                                color=AppColors.appBackgroundColor,
                                                padding=EdgeInsets.symmetric(
                                                    horizontal=20
                                                ),
                                                child=Row(
                                                    mainAxisAlignment=MainAxisAlignment.SPACE_BETWEEN,
                                                    crossAxisAlignment=CrossAxisAlignment.STRETCH,
                                                    key=Key("Header_row"),
                                                    children=[
                                                        Container(
                                                            key=Key(
                                                                "file_name_and_details_header"
                                                            ),
                                                            padding=EdgeInsets.only(
                                                                top=20
                                                            ),
                                                            child=Row(
                                                                key=Key(
                                                                    "file_name_and_details_and_back_button_header_row"
                                                                ),
                                                                children=[
                                                                    IconButton(
                                                                        key=Key(
                                                                            "back_btn_1"
                                                                        ),
                                                                        icon=Icon(
                                                                            Icons.arrow_back_rounded,
                                                                            key=Key(
                                                                                "back_ico_1"
                                                                            ),
                                                                        ),
                                                                        onPressed=lambda: self.widget.navigator.pop(),
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
                                                                                    color=Colors.adaptive(
                                                                                        dark="#EDEDED",
                                                                                        light=Colors.black,
                                                                                    ),
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
                                                                                    color=Colors.adaptive(
                                                                                        dark="#9E9E9E",
                                                                                        light=Colors.grey,
                                                                                    ),
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
                                                            padding=EdgeInsets.only(
                                                                top=20
                                                            ),
                                                            child=Row(
                                                                key=Key(
                                                                    "search_ai_and_controls_header_row"
                                                                ),
                                                                mainAxisAlignment=MainAxisAlignment.END,
                                                                crossAxisAlignment=CrossAxisAlignment.START,
                                                                children=[
                                                                    self.header_action
                                                                ],
                                                            ),
                                                        ),
                                                    ],
                                                ),
                                            ),
                                        ],
                                    ),
                                    self.markdown_editor,
                                ]
                            ),
                        ),
                        (
                            Positioned(
                                key=Key(f"my_header_posit"),
                                height="610px",
                                width="610px",
                                top="16px",
                                right="4px",
                                child=Container(
                                    height=610,
                                    width=610,
                                    color=Colors.transparent,
                                    child=ChatCard(
                                        key=Key("my_chat_card_0xff"),
                                        context=self.editor,
                                    ),
                                ),
                            )
                            if self.chatOpen
                            else ()
                        ),
                        Positioned(
                            height=40,
                            width="100vw",
                            bottom="18px",
                            key=Key("home_page_Pythra_decrement_btn_Positioned"),
                            child=Center(
                                key=Key("home_page_Pythra_Center_Positioned_Container"),
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
                                            self.dropdown,
                                            SizedBox(
                                                width=(12),
                                                key=Key("sixe_box_header_dropdown"),
                                            ),
                                            IconButton(
                                                key=Key(
                                                    "format_color_text_rounded_btn"
                                                ),
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
                                                    key=Key(
                                                        "format_h1_rounded_btn_ico"
                                                    ),
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
                                                    key=Key(
                                                        "format_bold_rounded_btn_ico"
                                                    ),
                                                ),
                                                onPressed=lambda: self.bold(),
                                                onPressedName="bold_lambda",
                                                style=ButtonStyle(
                                                    backgroundColor=AppColors.buttonBackgroundColor,
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
                                                key=Key(
                                                    "format_italic_rounded_size_box"
                                                ),
                                            ),
                                            IconButton(
                                                key=Key(
                                                    "format_underlined_rounded_btn"
                                                ),
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
                                                key=Key(
                                                    "format_strikethrough_rounded_btn"
                                                ),
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
                                                key=Key(
                                                    "format_list_bulleted_rounded_btn"
                                                ),
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
                                                key=Key(
                                                    "format_list_numbered_rounded_btn"
                                                ),
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
                                                    key=Key(
                                                        "image_rounded_btn_inner_row"
                                                    ),
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
                                        border=BorderSide(
                                            width=1,
                                            color=Colors.adaptive(
                                                dark="#5a5a5a", light="#d3d3d3"
                                            ),
                                        ),
                                        color=Colors.adaptive(
                                            dark=AppColors.toolbarBackgroundDarkColor,
                                            light=Colors.white,
                                        ),
                                    ),
                                ),
                            ),
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
