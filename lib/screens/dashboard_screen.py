from .note_editor_screen import NoteEditorScreen

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

    def initState(self):
        # Create and preload the note editor route
        self.note_editor_route = PageRoute(
            builder=lambda nav: NoteEditorScreen(
                key=Key("note_page"), navigator=nav,
            ),
            name="note_editor"
        )
        print("🚀 Preloading NoteEditorScreen in background...")
        self.navigator.preload(self.note_editor_route)

    def build(self):
        settings_button = ElevatedButton(
            key=Key("main_Elv_Btn"),
            child=Text("Go to Note", key=Key("main_Elv_Btn_child")),
            onPressed=lambda: self.navigator.push(self.note_editor_route)
        )
        return Container(
            key=Key("Build_container"),
            height='80vh',
            padding=EdgeInsets.all(32),
            color=Colors.surfaceVariant,
            child=Column(
                key=Key("main__column"),
                crossAxisAlignment=CrossAxisAlignment.STRETCH,
                children=[
                    Text("DashBoard Page", key=Key("DashBoard_Page_heading")),
                    SizedBox(key=Key("main_sized_box"), height=24),
                    settings_button,
                ],
            ),
        )
