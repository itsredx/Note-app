from lib.constants.theme import AppThemes
from lib.screens.settings_screen import SettingsAndProfileScreen
from .note_editor_screen import NoteEditorScreen, load_system_fonts
from lib.components.note_card import NoteCard
from lib.constants.colors import *
from lib.components.header_actions import HeaderActions
from lib.utils.shared_prefernce import PythraPreferences
from lib import pref
from PySide6.QtCore import QTimer

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
    Navigator,
    PageRoute,
    NavigatorState,
    GridView,
    GestureDetector,
    Padding,
    TextField,
    TextEditingController,
    InputDecoration,
    Expandable,
    ExpandableTheme,
)


class DashboardScreen(StatefulWidget):
    def __init__(
        self,
        key: Key,
        navigator: NavigatorState,
    ):
        self.navigator = navigator
        super().__init__(key=key)

    def createState(self):
        return DashboardScreenState(self.navigator)


class DashboardScreenState(State):
    def __init__(
        self,
        navigator: NavigatorState,
    ):
        super().__init__()
        self.navigator = navigator
        # print("==== Dashboard Initializing (__init__) ====")
        self.show_color_picker = False
        self.show_create_dialog = False
        self.selected_color = None
        self.panel_mode = (
            pref.get("panel_state", None)
            if pref.get("panel_state", None) != None
            else False
        )

        self.title_controller = TextEditingController()
        self.note_controller = TextEditingController()

        self.notes = [
            {
                "title": "Design",
                "note": "Make the design looks okay...",
                "date": "20 Dec",
                "color": Colors.hex("#FFAB91"),
            },
            {
                "title": "Project",
                "note": "Finish the project documentation",
                "date": "21 Dec",
                "color": Colors.hex("#CE93D8"),
            },
            {
                "title": "Meeting",
                "note": "Sync with the team at 10am",
                "date": "22 Dec",
                "color": Colors.hex("#4DD0E1"),
            },
        ]
        self.note_colors = [
            Colors.hex("#FFAB91"),  # Orange
            Colors.hex("#CE93D8"),  # Purple
            Colors.hex("#4DD0E1"),  # Cyan
            Colors.hex("#FFF176"),  # Yellow
            Colors.hex("#80CBC4"),  # Teal
        ]

    def initState(self):
        load_system_fonts()
        self.note_editor_route = PageRoute(
            builder=lambda nav: NoteEditorScreen(
                key=Key("note_page"),
                navigator=nav,
            ),
            name="note_editor",
        )
        # print("==== Dashboard Initializing ====")
        self.settings_route = PageRoute(
            builder=lambda nav: SettingsAndProfileScreen(
                key=Key("settings_&_profile_page"), navigator=nav
            ),
            name="settings_page",
        )

        print("🚀 Preloading NoteEditorScreen in background...")
        self.navigator.preload(self.note_editor_route)
        

    def open_note(self):
        self.navigator.push(self.note_editor_route)

    def open_settings(self):
        self.navigator.push(self.settings_route)

    def delete_note(self):
        print("Delete note clicked")

    def chat_note(self):
        print("AI Chat note clicked")

    def toggle_color_picker_depercated(self):
        self.show_color_picker = not self.show_color_picker
        self.setState()

    def toggle_color_picker(self, *args, **kwargs):
        self.show_color_picker = not self.show_color_picker
        print(f"show_color_picker: {self.show_color_picker}")
        self.setState()

    def initiate_create_note(self, color):
        self.selected_color = color
        self.show_color_picker = False
        self.show_create_dialog = True
        self.title_controller.text = ""
        self.note_controller.text = ""
        self.setState()

    def cancel_create_note(self):
        self.show_create_dialog = False
        self.selected_color = None
        self.setState()

    def finalize_create_note(self):
        new_note = {
            "title": (
                self.title_controller.text if self.title_controller.text else "New Note"
            ),
            "note": (
                self.note_controller.text if self.note_controller.text else "No content"
            ),
            "date": "Now",
            "color": self.selected_color if self.selected_color else Colors.white,
        }
        self.notes.insert(0, new_note)
        self.show_create_dialog = False
        self.selected_color = None
        self.setState()

    @property
    def is_dark(self):
        return Framework.instance().theme.brightness == "dark"

    def toggle_theme(self):
        new_theme = AppThemes.light if self.is_dark else AppThemes.dark
        Framework.instance().set_theme(new_theme)
        # Rebuild this row to update all icons (Sun/Moon, Sparkle, etc)
        self.setState()

    def build(self) -> Widget:
        # Sidebar with Create Button and Color Picker
        sidebar = Container(
            key=Key("sidebar_container"),
            width="80px",
            height="100vh" if not self.panel_mode else "100vh",
            color=Colors.surface if not self.panel_mode else Colors.surface,
            padding=EdgeInsets.symmetric(
                vertical=120 if not self.panel_mode else 0, horizontal=4
            ),
            child=Container(
                key=Key("sidebar_inner_container"),
                height="100%",
                padding=EdgeInsets.symmetric(vertical=24, horizontal=10),
                color=Colors.surface if not self.panel_mode else Colors.transparent,
                decoration=BoxDecoration(
                    borderRadius=(
                        BorderRadius.all(16)
                        if not self.panel_mode
                        else BorderRadius.all(0)
                    ),
                    border=BorderSide(
                        width=1 if not self.panel_mode else 0,
                        color=Colors.adaptive(dark="#5a5a5a", light="#d3d3d3"),
                    ),
                ),
                child=Column(
                    key=Key("sidebar_column"),
                    mainAxisAlignment=MainAxisAlignment.START,
                    crossAxisAlignment=CrossAxisAlignment.CENTER,
                    children=[
                        Container(
                            key=Key("sidebar_title_note_container"),
                            padding=EdgeInsets.only(bottom=20),
                            child=Text(
                                "Note",
                                key=Key("sidebar_title_note"),
                                style=TextStyle(
                                    fontSize=16,
                                    fontWeight="bold",
                                    color=Colors.onSurface,
                                ),
                            ),
                        ),
                        # Color Picker Column (Conditional)
                        Expandable(
                            key=Key("myExpandable"),
                            initiallyExpanded=self.show_color_picker,
                            onToggle=self.toggle_color_picker,
                            theme=ExpandableTheme(
                                showIcon=False,
                            ),
                            header=Container(
                                key=Key("sidebar_title_create_note__container"),
                                child=IconButton(
                                    key=Key("create_note_btn"),
                                    icon=Icon(
                                        (
                                            Icons.add_circle_outline_rounded
                                            if not self.show_color_picker
                                            else Icons.close_rounded
                                        ),
                                        key=Key("create_note_icon"),
                                    ),
                                    # onPressed=self.toggle_color_picker,
                                    style=ButtonStyle(
                                        backgroundColor=AppColors.buttonBackgroundColor,
                                        hoverColor=AppColors.buttonHoverColor,
                                        foregroundColor=AppColors.buttonForegroundColor,
                                    ),
                                ),
                            ),
                            child=Column(
                                key=Key("color_picker_column"),
                                children=[
                                    GestureDetector(
                                        key=Key(f"color_pick_btn_{i}"),
                                        onTap=lambda details, c=color: self.initiate_create_note(
                                            c
                                        ),
                                        child=Container(
                                            key=Key(f"color_pick_circle_{i}"),
                                            width=30,
                                            height=30,
                                            margin=EdgeInsets.only(top=10),
                                            decoration=BoxDecoration(
                                                color=color,
                                                borderRadius=BorderRadius.circular(15),
                                                border=BorderSide(
                                                    color=Colors.adaptive(
                                                        dark="#5a5a5a", light="#d3d3d3"
                                                    ),
                                                    width=1,
                                                ),
                                            ),
                                        ),
                                    )
                                    for i, color in enumerate(self.note_colors)
                                ],
                            ),
                        ),
                        # Toggle/Create Button
                        # Container(
                        #     key=Key("create_note_btn_container"),
                        #     padding=EdgeInsets.only(bottom=20),
                        #     child=IconButton(
                        #         key=Key("create_note_btn"),
                        #         icon=Icon(
                        #             Icons.add_circle_outline_rounded if not self.show_color_picker else Icons.close_rounded,
                        #             key=Key("create_note_icon"),
                        #         ),
                        #         onPressed=self.toggle_color_picker,
                        #         style=ButtonStyle(
                        #             backgroundColor=AppColors.buttonBackgroundColor,
                        #             hoverColor=AppColors.buttonHoverColor,
                        #             foregroundColor=AppColors.buttonForegroundColor,
                        #         ),
                        #     ),
                        # ),
                    ],
                ),
            ),
            decoration=BoxDecoration(
                border=BorderSide(
                    width=0 if not self.panel_mode else 1,
                    color=Colors.adaptive(dark="#5a5a5a", light="#d3d3d3"),
                ),
                # color=Colors.adaptive(
                #     dark=AppColors.toolbarBackgroundDarkColor, light=Colors.white
                # ),
            ),
        )

        content = Row(
            key=Key("main_row_layout"),
            children=[
                sidebar,
                # Main Content Area
                Container(
                    key=Key("main_content_area"),
                    height="100vh",
                    width="calc(100vw - 80px)",
                    color=Colors.surface,
                    padding=EdgeInsets.only(left=40, right=40, top=24, bottom=32),
                    child=Column(
                        key=Key("content_column"),
                        crossAxisAlignment=CrossAxisAlignment.STRETCH,
                        children=[
                            Row(
                                key=Key("content_column_s_inner_row"),
                                mainAxisAlignment=MainAxisAlignment.END,
                                children=[
                                    HeaderActions(
                                        key=Key("dashboard_header"),
                                        onAccount=self.open_settings,  # lambda: print('on account')
                                    ),
                                ],
                            ),
                            SizedBox(key=Key("page_heading_sized_box"), height=24),
                            Text(
                                "Dashboard",
                                key=Key("DashBoard_Page_heading"),
                                style=TextStyle(
                                    fontSize=32,
                                    fontWeight="bold",
                                    color=Colors.onSurface,
                                ),
                            ),
                            SizedBox(key=Key("main_sized_box"), height=24),
                            # Grid View
                            Container(
                                key=Key("grid_container"),
                                height="85vh",
                                child=GridView(
                                    key=Key("notes_grid"),
                                    crossAxisCount=5,
                                    mainAxisSpacing=20,
                                    crossAxisSpacing=20,
                                    childAspectRatio=1.0,
                                    childMinWidth=231.0,
                                    shrinkWrap=True,
                                    children=[
                                        NoteCard(
                                            key=Key(f"note_{i}"),
                                            title=note["title"],
                                            note=note["note"],
                                            date=note["date"],
                                            color=note["color"],
                                            on_open=self.open_note,
                                            on_delete=self.delete_note,
                                            on_chat=self.chat_note,
                                        )
                                        for i, note in enumerate(self.notes)
                                    ],
                                ),
                            ),
                        ],
                    ),
                ),
            ],
        )

        # Main Stack to hold content and potential dialog
        return Stack(
            key=Key("root_stack"),
            children=[
                content,
                # Dialog Overlay
                *(
                    [
                        Positioned(
                            top=0,
                            left=0,
                            right=0,
                            bottom=0,
                            key=Key("dialog_overlay_bg"),
                            child=Container(
                                key=Key("dialog_scrim"),
                                height="100vh",
                                width="100vw",
                                zAxisIndex=4999,
                                cssPosition='fixed',
                                color=Colors.rgba(0, 0, 0, 0.5),
                                child=Center(
                                    key=Key("dialog_center"),
                                    child=Container(
                                        key=Key("dialog_box"),
                                        width=500,
                                        # height=300,
                                        zAxisIndex=5000,
                                        padding=EdgeInsets.all(45),
                                        decoration=BoxDecoration(
                                            color=Colors.surface,
                                            borderRadius=BorderRadius.all(24),
                                            boxShadow=[
                                                # Simple shadow simulation if supported, otherwise just border
                                                # BoxShadow(color=Colors.black26, blurRadius=10)
                                            ],
                                        ),
                                        child=Column(
                                            key=Key("dialog_column"),
                                            mainAxisAlignment=MainAxisAlignment.START,
                                            crossAxisAlignment=CrossAxisAlignment.STRETCH,
                                            children=[
                                                Text(
                                                    "Create New Note",
                                                    key=Key("dialog_title"),
                                                    style=TextStyle(
                                                        fontSize=20,
                                                        fontWeight="bold",
                                                        color=Colors.onSurface,
                                                    ),
                                                ),
                                                SizedBox(
                                                    height=20,
                                                    key=Key("dialog_spacer_1"),
                                                ),
                                                TextField(
                                                    key=Key("title_input"),
                                                    controller=self.title_controller,
                                                    decoration=InputDecoration(
                                                        hintText="Title",
                                                        fillColor=Colors.surfaceVariant,
                                                        labelColor=Colors.onSurfaceVariant,
                                                        focusColor=Colors.primary,
                                                        contentPadding=EdgeInsets.symmetric(
                                                            horizontal=24,
                                                            vertical=16,
                                                        ),
                                                        labelStyle=TextStyle(
                                                            fontSize=18,
                                                            fontFamily="Arial",
                                                        ),
                                                        hintStyle=TextStyle(
                                                            fontSize=14,
                                                        ),
                                                        filled=False,
                                                        # label="Title"
                                                    ),
                                                ),
                                                SizedBox(
                                                    height=12,
                                                    key=Key("dialog_txt_spacer_2"),
                                                ),
                                                TextField(
                                                    key=Key("note_input"),
                                                    controller=self.note_controller,
                                                    decoration=InputDecoration(
                                                        hintText="Description",
                                                        fillColor=Colors.surfaceVariant,
                                                        labelColor=Colors.onSurfaceVariant,
                                                        focusColor=Colors.primary,
                                                        contentPadding=EdgeInsets.symmetric(
                                                            horizontal=24,
                                                            vertical=16,
                                                        ),
                                                        labelStyle=TextStyle(
                                                            fontSize=18,
                                                            fontFamily="Arial",
                                                        ),
                                                        hintStyle=TextStyle(
                                                            fontSize=14,
                                                        ),
                                                        filled=False,
                                                        # label="Description"
                                                    ),
                                                ),
                                                SizedBox(
                                                    height=30,
                                                    key=Key("dialog_spacer_3"),
                                                ),
                                                Row(
                                                    key=Key("dialog_btn_row"),
                                                    mainAxisAlignment=MainAxisAlignment.END,
                                                    children=[
                                                        ElevatedButton(
                                                            key=Key("cancel_btn"),
                                                            child=Text(
                                                                "Cancel",
                                                                key=Key("cancel_txt"),
                                                            ),
                                                            onPressed=self.cancel_create_note,
                                                            style=ButtonStyle(
                                                                backgroundColor=Colors.hex(
                                                                    "#f47171"
                                                                ),
                                                                padding=EdgeInsets.symmetric(horizontal=16, vertical=8),
                                                                margin=EdgeInsets.all(0),
                                                                minimumSize=(80, 40),
                                                                maximumSize=(80, 40),
                                                            ),
                                                        ),
                                                        SizedBox(
                                                            width=8,
                                                            key=Key(
                                                                "dialog_btn_spacer"
                                                            ),
                                                        ),
                                                        ElevatedButton(
                                                            key=Key("create_btn"),
                                                            child=Text(
                                                                "Create",
                                                                key=Key("create_txt"),
                                                                style=TextStyle(
                                                                    color=Colors.white
                                                                ),
                                                            ),
                                                            onPressed=self.finalize_create_note,
                                                            style=ButtonStyle(
                                                                backgroundColor=self.selected_color
                                                                or Colors.blue,
                                                                padding=EdgeInsets.symmetric(horizontal=16, vertical=8),
                                                                margin=EdgeInsets.all(0),
                                                                minimumSize=(80, 40),
                                                                maximumSize=(80, 40),
                                                            ),
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ),
                                ),
                            ),
                        )
                    ]
                    if self.show_create_dialog
                    else []
                ),
            ],
        )
