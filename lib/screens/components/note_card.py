from lib.constants.colors import *
from pythra import (
    BoxDecoration,
    StatefulWidget,
    State,
    Column,
    Row,
    Key,
    Widget,
    Container,
    Text,
    Colors,
    Center,
    SizedBox,
    MainAxisAlignment,
    CrossAxisAlignment,
    ClipPath,
    EdgeInsets,
    Icon,
    IconButton,
    Icons,
    BorderRadius,
    ButtonStyle,
    TextStyle,
    Stack,
    Positioned,
    ClipBehavior,
    GestureDetector,
)

class NoteCardState(State):
    def __init__(self):
        self.base_key = None
        self.title = None
        self.note = None
        self.date = None
        self.color = None
        self.on_open = None
        self.on_delete = None
        self.on_chat = None

    def initState(self):
        self.base_key = self.get_widget().key.value
        self.title = self.get_widget().title
        self.note = self.get_widget().note
        self.date = self.get_widget().date
        self.color = self.get_widget().color
        self.on_open = self.get_widget().on_open
        self.on_delete = self.get_widget().on_delete
        self.on_chat = self.get_widget().on_chat

    def build(self) -> Widget:
        return Stack(
            key=Key(f"{self.base_key}_stack"),
            clipBehavior=ClipBehavior.NONE,
            children=[
                ClipPath(
                    height="231px",
                    width="231px",
                    viewBox=[100, 100],
                    points=[
                        (0,0),
                        (58,0),
                        (58, 22),
                        (100, 22),
                        (100,78),
                        (78,78),
                        (78,100),
                        (48,100),
                        (48, 78),
                        (0, 78),
                    ],
                    radius=8,
                    key=Key(f"{self.base_key}_clip_path"),
                    child=Container(
                        key=Key(f"{self.base_key}_container"),
                        height="231px",
                        width="231px",
                        padding=EdgeInsets.all(12),
                        color=self.color or Colors.white,
                        child=Column(
                            key=Key(f"{self.base_key}_details_column"),
                            mainAxisAlignment=MainAxisAlignment.START,
                            crossAxisAlignment=CrossAxisAlignment.START,
                            children=[
                                Container(
                                    key=Key(f"{self.base_key}_heading_wrapper"),
                                    width=110,
                                    height=30,
                                    child=Text(
                                        f"{self.title}", 
                                        key=Key(f"{self.base_key}_heading_txt"),
                                        style=TextStyle(fontSize=24, fontFamily="ubuntu"),
                                    ),
                                ),
                                SizedBox(height=24, key=Key(f"{self.base_key}_header_spacer")),
                                Text(
                                    f"{self.note}", 
                                    key=Key(f"{self.base_key}_note_snippet"),
                                    style=TextStyle(fontSize=16, fontFamily="ubuntu"),
                                ),
                            ],
                        ),
                    ),
                ),
                # Top Right Icons: Delete (1) and AI Chat (2)
                Positioned(
                    height="231px",
                    width="231px",
                    key=Key(f"{self.base_key}_top_actions_pos"),
                    child=Container(
                        key=Key(f"{self.base_key}_top_actions_container"),
                        child=Row(
                            mainAxisAlignment=MainAxisAlignment.END,
                            key=Key(f"{self.base_key}_top_actions_row"),
                            children=[
                                IconButton(
                                    key=Key(f"{self.base_key}_delete_btn"),
                                    icon=Icon(
                                        Icons.delete,
                                        key=Key(f"{self.base_key}_delete_icon"),
                                    ),
                                    onPressed=self.on_delete,
                                    style=ButtonStyle(
                                        backgroundColor=AppColors.buttonBackgroundColor,
                                        hoverColor=AppColors.buttonHoverColor,
                                        foregroundColor=AppColors.buttonForegroundColor,
                                    ),
                                ),
                                SizedBox(width=8, key=Key(f"{self.base_key}_top_spacer")),
                                IconButton(
                                    key=Key(f"{self.base_key}_chat_btn"),
                                    icon=Icon(
                                        Icons.chat, # Using chat for AI chat
                                        key=Key(f"{self.base_key}_chat_icon"),
                                    ),
                                    onPressed=self.on_chat,
                                    style=ButtonStyle(
                                        backgroundColor=AppColors.buttonBackgroundColor,
                                        hoverColor=AppColors.buttonHoverColor,
                                        foregroundColor=AppColors.buttonForegroundColor,
                                    ),
                                ),
                            ],
                        ),
                    ),
                ),
                # Bottom Area: Date and Open Button
                Positioned(
                    height="231px",
                    width="231px",
                    top="189px",
                    key=Key(f"{self.base_key}_bottom_actions_pos"),
                    child=Container(
                        key=Key(f"{self.base_key}_bottom_actions_container"),
                        child=Row(
                            mainAxisAlignment=MainAxisAlignment.SPACE_BETWEEN,
                            key=Key(f"{self.base_key}_bottom_actions_row"),
                            children=[
                                Container(
                                    key=Key(f"{self.base_key}_date_container"),
                                    height=40,
                                    width=100,
                                    color=AppColors.buttonBackgroundColor,
                                    decoration=BoxDecoration(
                                        borderRadius=BorderRadius.all(20)
                                    ),
                                    child=Center(
                                        key=Key(f"{self.base_key}_date_center"),
                                        child=Text(
                                            f"{self.date}", 
                                            key=Key(f"{self.base_key}_date_text"),
                                            style=TextStyle(fontSize=12, fontFamily="ubuntu mono", color=AppColors.buttonForegroundColor),
                                        ),
                                    ),
                                ),
                                IconButton(
                                    key=Key(f"{self.base_key}_open_btn"),
                                    icon=Icon(
                                        Icons.open_in_new, # Use open_in_new or arrow
                                        key=Key(f"{self.base_key}_open_icon"),
                                    ),
                                    onPressed=self.on_open,
                                    style=ButtonStyle(
                                        backgroundColor=AppColors.buttonBackgroundColor,
                                        hoverColor=AppColors.buttonHoverColor,
                                        foregroundColor=AppColors.buttonForegroundColor,
                                    ),
                                ),
                            ],
                        ),
                    ),
                ),
            ],
        )

class NoteCard(StatefulWidget):
    def __init__(
        self, 
        title=None, 
        note=None, 
        date=None, 
        color=None, 
        on_open=None, 
        on_delete=None, 
        on_chat=None, 
        key=None
    ):
        self.title = title
        self.note = note
        self.date = date
        self.color = color
        self.on_open = on_open
        self.on_delete = on_delete
        self.on_chat = on_chat
        super().__init__(key)

    def createState(self) -> NoteCardState:
        return NoteCardState()
