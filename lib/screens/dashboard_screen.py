from datetime import datetime

from lib.constants.theme import AppThemes
from lib.screens.settings_screen import SettingsAndProfileScreen
from .note_editor_screen import NoteEditorScreen, load_system_fonts
from lib.components.note_card import NoteCard
from lib.constants.colors import *
from lib.components.header_actions import HeaderActions
from lib.utils.shared_prefernce import PythraPreferences
from lib.backend.repository import NoteRepository
from lib.utils.strip_html import strip_html
from lib.state.tab_state import tab_state
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
    _render_counter = 0

    def __init__(
        self,
        key: Key,
        navigator: NavigatorState,
    ):
        self.navigator = navigator
        super().__init__(key=key)

    def createState(self):
        return DashboardScreenState(self.navigator)

    def render_props(self):
        type(self)._render_counter += 1
        return {"rebuild_guard": type(self)._render_counter}


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

        self.title_controller = TextEditingController()
        self.note_controller = TextEditingController()

        self._repo = NoteRepository()
        self.notes = self._repo.list_notes()

        if not self.notes:
            self._repo.create_note(
                title="Design", content="Make the design looks okay...", color="#FFAB91"
            )
            self._repo.create_note(
                title="Project",
                content="Finish the project documentation",
                color="#CE93D8",
            )
            self._repo.create_note(
                title="Meeting", content="Sync with the team at 10am", color="#4DD0E1"
            )
            self.notes = self._repo.list_notes()

        self.note_colors = [
            "#FFAB91",
            "#CE93D8",
            "#4DD0E1",
            "#FFF176",
            "#80CBC4",
        ]

    @property
    def panel_mode(self) -> bool:
        return pref.get("panel_state", False)

    def initState(self):
        load_system_fonts()
        self.settings_route = PageRoute(
            builder=lambda nav: SettingsAndProfileScreen(
                key=Key("settings_&_profile_page"), navigator=nav
            ),
            name="settings_page",
        )

    def open_note(self, note_id: str):
        repo = NoteRepository()
        note = repo.get_note(note_id)
        if note:
            tab_state.add_tab(note)
        route = PageRoute(
            builder=lambda nav: NoteEditorScreen(
                key=Key(f"note_editor_{note_id}"),
                navigator=nav,
                note_id=note_id,
            ),
            name=f"note_editor_{note_id}",
        )
        self.navigator.push(route)

    def open_settings(self):
        self.navigator.push(self.settings_route)

    def delete_note(self, note_id: str):
        tab_state.remove_tab(note_id)
        self._repo.delete_note(note_id)
        self.notes = self._repo.list_notes()
        self.setState()

    def chat_note(self, note_id: str):
        print(f"AI Chat note clicked: {note_id}")

    @staticmethod
    def _format_date(iso_str: str) -> str:
        try:
            dt = datetime.fromisoformat(iso_str)
            now = datetime.now(dt.tzinfo)
            delta = now - dt
            if delta.total_seconds() < 300:
                return "Now"
            if dt.date() == now.date():
                return dt.strftime("%I:%M %p").lstrip("0")
            if dt.year == now.year:
                return dt.strftime("%d %b")
            return dt.strftime("%d %b %Y")
        except Exception:
            return "Unknown"

    def _note_card(self, i: int, note):
        def on_open():
            self.open_note(note.id)

        on_open.__name__ = f"open_{note.id}"

        def on_delete():
            self.delete_note(note.id)

        on_delete.__name__ = f"delete_{note.id}"

        def on_chat():
            self.chat_note(note.id)

        on_chat.__name__ = f"chat_{note.id}"

        return NoteCard(
            key=Key(f"note_{i}"),
            title=note.title,
            note=strip_html(note.content),
            date=self._format_date(note.updated_at),
            color=Colors.hex(note.color),
            on_open=on_open,
            on_delete=on_delete,
            on_chat=on_chat,
        )

    def toggle_color_picker_depercated(self):
        self.show_color_picker = not self.show_color_picker
        self.setState()

    def toggle_color_picker(self, *args, **kwargs):
        self.show_color_picker = not self.show_color_picker
        print(f"show_color_picker: {self.show_color_picker}")
        self.setState()

    def initiate_create_note(self, color_hex):
        self.selected_color = color_hex
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
        title = self.title_controller.text if self.title_controller.text else "New Note"
        content = (
            self.note_controller.text if self.note_controller.text else "No content"
        )
        color = self.selected_color if self.selected_color else "#4DD0E1"
        self._repo.create_note(title=title, content=content, color=color)
        self.notes = self._repo.list_notes()
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
        self._repo.reload()
        self.notes = self._repo.list_notes()
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
                                width="100%",
                                child=Center(
                                    key=Key("create_note_center"),
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
                                                color=Colors.hex(color),
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
                                    Container(
                                        key=Key("dashboard_header_container"),
                                        width=92,
                                        child=HeaderActions(
                                            key=Key("dashboard_header"),
                                            onAccount=self.open_settings,  # lambda: print('on account')
                                        ),
                                    )
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
                                        self._note_card(i, note)
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
                                cssPosition="fixed",
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
                                                                padding=EdgeInsets.symmetric(
                                                                    horizontal=16,
                                                                    vertical=8,
                                                                ),
                                                                margin=EdgeInsets.all(
                                                                    0
                                                                ),
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
                                                                backgroundColor=(
                                                                    Colors.hex(
                                                                        self.selected_color
                                                                    )
                                                                    if self.selected_color
                                                                    else Colors.blue
                                                                ),
                                                                padding=EdgeInsets.symmetric(
                                                                    horizontal=16,
                                                                    vertical=8,
                                                                ),
                                                                margin=EdgeInsets.all(
                                                                    0
                                                                ),
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
