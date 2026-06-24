from typing import Callable, Optional
from lib.constants.colors import AppColors
from lib.backend.models import Note
from lib.state.tab_state import tab_state
from pythra import (
    Axis,
    BoxConstraints,
    BoxDecoration,
    MainAxisSize,
    SingleChildScrollView,
    StatefulWidget,
    State,
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
    EdgeInsets,
    Icon,
    IconButton,
    Icons,
    BorderRadius,
    ButtonStyle,
    GestureDetector,
    TextStyle,
)


class TabNavigationCardState(State):
    def initState(self):
        pass

    def build(self) -> Widget:
        tabs = list(tab_state.open_tabs)
        active_id = tab_state.active_tab_id

        return Container(
            key=Key("tab_root_container"),
            height=40,
            width=210 if len(tabs) == 1 else None,
            constraints=BoxConstraints(maxWidth=500, minWidth=100),
            padding=EdgeInsets.all(4),
            color=AppColors.buttonBackgroundColor,
            decoration=BoxDecoration(borderRadius=BorderRadius.all(12)),
            child=SingleChildScrollView(
                key=Key("tab_scroll"),
                scrollDirection=Axis.HORIZONTAL,
                shape=BorderRadius.all(8),
                child=Row(
                    key=Key("tab_root_row"),
                    mainAxisAlignment=MainAxisAlignment.START,
                    mainAxisSize=MainAxisSize.MIN,
                    children=[
                        self._build_tab(i, note, note.id == active_id)
                        for i, note in enumerate(tabs)
                    ],
                ),
            ),
        )

    def _build_tab(self, i: int, note: Note, active: bool) -> Widget:
        key = Key(f"tab_{note.id}")
        return GestureDetector(
            key=Key(f"{key}_gesture"),
            onTap=lambda details, n=note: self.widget.on_tab_clicked(n.id),
            child=Container(
                key=Key(f"{key}_container"),
                height=32,
                width=200,
                color=AppColors.appBackgroundColor if active else Colors.transparent,
                # margin=EdgeInsets.only(right=4),
                padding=EdgeInsets.all(5),
                decoration=BoxDecoration(
                    borderRadius=BorderRadius.all(10),
                ),
                child=Row(
                    key=Key(f"{key}_row"),
                    mainAxisAlignment=MainAxisAlignment.SPACE_BETWEEN,
                    crossAxisAlignment=CrossAxisAlignment.STRETCH,
                    children=[
                        Container(
                            key=Key(f"{key}_title_wrapper"),
                            child=Row(
                                children=[
                                    Container(
                                        key=Key(f"{key}_color"),
                                        decoration=BoxDecoration(
                                            borderRadius=BorderRadius.all(4)
                                        ),
                                        width=20,
                                        height=20,
                                        color=Colors.hex(note.color),
                                    ),
                                    SizedBox(
                                        width=6, key=Key(f"{key}_color_size_box")
                                    ),
                                    Text(
                                        data=note.title,
                                        key=Key(f"{key}_title"),
                                        style=TextStyle(
                                            color=AppColors.iconColor,
                                        ),
                                    ),
                                ]
                            ),
                        ),
                        Container(
                            key=Key(f"{key}_close_btn_cont"),
                            width=22,
                            height=22,
                            child=Center(
                                key=Key(f"{key}_close_btn_cen"),
                                child=IconButton(
                                    key=Key(f"{key}_close_btn"),
                                    icon=Icon(
                                        icon=Icons.close_rounded,
                                        size=12,
                                    ),
                                    iconSize=12,
                                    onPressed=lambda: self.widget.on_tab_close(
                                        note.id
                                    ),
                                    onPressedName=f"close_tab_{note.id}",
                                    style=ButtonStyle(
                                        maximumSize=(30, 30),
                                        minimumSize=(30, 30),
                                        backgroundColor=AppColors.buttonBackgroundColor,
                                        foregroundColor=AppColors.iconColor,
                                        hoverColor=Colors.adaptive(
                                            light=Colors.rgba(96, 91, 91, 0.2),
                                            dark=Colors.rgba(236, 233, 233, 0.3),
                                        ),
                                        padding=EdgeInsets.all(4),
                                    ),
                                ),
                            ),
                        ),
                    ],
                ),
            ),
        )


class TabNavigationCard(StatefulWidget):
    def __init__(
        self,
        on_tab_close: Callable[[str], None],
        on_tab_clicked: Callable[[str], None],
        key: Key = None,
    ):
        self.on_tab_close = on_tab_close
        self.on_tab_clicked = on_tab_clicked
        super().__init__(key)

    def createState(self) -> TabNavigationCardState:
        return TabNavigationCardState()
