from typing import Any

from pythra import Container, Positioned, Stack
from pythra.base import Widget, Key
from pythra.state import StatefulWidget, State
from pythra.widgets import (
    Row,
    IconButton,
    Icon,
    ButtonStyle,
    Image,
    AssetImage,
    SizedBox,
    MainAxisAlignment,
    CrossAxisAlignment,
)
from pythra.styles import Colors, BorderRadius, EdgeInsets
from pythra.icons import Icons
from pythra.core import Framework
from lib.components.chat_card import ChatCard
from lib.constants.colors import AppColors
from lib.constants.theme import AppThemes
from lib.utils.shared_prefernce import PythraPreferences
from lib import pref


class HeaderActions(StatefulWidget):
    def __init__(
        self,
        key: Key,
        onSave: callable = None,
        onAiChatContext: Any = None,
        onAccount: callable = None,
    ):
        self.onSave = onSave
        self.onAiChatContext = onAiChatContext
        self.onAccount = onAccount
        super().__init__(key=key)

    def createState(self):
        return HeaderActionsState()


class HeaderActionsState(State):
    def __init__(self):
        # super().__init__()
        self.editor = None
        self.chatOpen = False
        self.selctionContext = None
        self.noteContext = None

    

    @property
    def is_dark(self):
        return Framework.instance().theme.brightness == "dark"

    def toggle_theme(self):
        new_theme = AppThemes.light if self.is_dark else AppThemes.dark
        Framework.instance().set_theme(new_theme)
        pref.set("theme", "dark") if self.is_dark else pref.set("theme", "light")
        # Rebuild this row to update all icons (Sun/Moon, Sparkle, etc)
        self.setState()

    def open_chat(self):
        self.chatOpen = not self.chatOpen
        self.setState()

    def open_chat_with_selection_context(self, context):
        self.selctionContext = context
        self.chatOpen = True
        self.setState()

    def get_note_context(self):
        widget = self.widget

        if widget and widget.onAiChatContext:
            self.editor = widget.onAiChatContext

        if self.editor:
            self.noteContext = self.editor.export_to_markdown() if self.noteContext == self.editor.export_to_markdown() else self.noteContext

    # ── Build ─────────────────────────────────────────────────────────────
    def build(self) -> Widget:
        row_children = [
            IconButton(
                key=Key("Header_btn_1"),
                icon=Icon(
                    (
                        Icons.light_mode_rounded
                        if self.is_dark
                        else Icons.dark_mode_rounded
                    ),
                    key=Key("Header_ico_1"),
                ),
                onPressed=self.toggle_theme,
                tooltip="Light Mode" if self.is_dark else "Dark Mode",
                style=ButtonStyle(
                    backgroundColor=AppColors.buttonBackgroundColor,
                    hoverColor=AppColors.buttonHoverColor,
                    foregroundColor=AppColors.buttonForegroundColor,
                ),
            ),
        ]

        if (
            self.widget.onSave
            or self.widget.onAccount
            or self.widget.onAiChatContext
        ):
            row_children.append(
                SizedBox(width=12, key=Key("sixe_box_header_controls_1"))
            )

        if self.widget.onSave:
            row_children.extend([
                IconButton(
                    key=Key("save_rounded_btn"),
                    icon=Icon(
                        Icons.save_rounded, key=Key("save_rounded_ico")
                    ),
                    onPressed=self.widget.onSave,
                    tooltip="Save",
                    style=ButtonStyle(
                        backgroundColor=AppColors.buttonBackgroundColor,
                        hoverColor=AppColors.buttonHoverColor,
                        foregroundColor=AppColors.buttonForegroundColor,
                    ),
                ),
                SizedBox(width=12, key=Key("sixe_box_save_rounded")),
            ])

        if self.widget.onAiChatContext:
            row_children.extend([
                IconButton(
                    key=Key("sparkle_btn"),
                    icon=(
                        Icon(
                            key=Key("spack_close_icon"),
                            icon=Icons.close_rounded,
                            color=AppColors.buttonForegroundColor,
                        )
                        if self.chatOpen
                        else Icon(
                            key=Key("sparkle_ico"),
                            icon=Icons.auto_awesome_rounded,
                            color=AppColors.buttonForegroundColor,
                        )
                    ),
                    onPressed=self.open_chat,
                    tooltip="Ai Chat",
                    style=ButtonStyle(
                        backgroundColor=AppColors.buttonBackgroundColor,
                        hoverColor=AppColors.buttonHoverColor,
                    ),
                ),
                SizedBox(width=12, key=Key("sixe_box_header_sparkle_btn")),
            ])

        if self.widget.onAccount:
            row_children.append(
                IconButton(
                    key=Key("account_circle_rounded_btn"),
                    icon=Icon(
                        Icons.settings_account_box_rounded,
                        key=Key("account_circle_rounded_ico"),
                    ),
                    onPressed=self.widget.onAccount,
                    tooltip="User Account & Settings",
                    style=ButtonStyle(
                        backgroundColor=AppColors.buttonBackgroundColor,
                        hoverColor=AppColors.buttonHoverColor,
                        foregroundColor=AppColors.buttonForegroundColor,
                    ),
                )
            )

        stack_children = [
            Row(
                key=Key("search_ai_and_controls_header_row"),
                mainAxisAlignment=MainAxisAlignment.END,
                crossAxisAlignment=CrossAxisAlignment.START,
                children=row_children,
            )
        ]

        if self.widget.onAiChatContext and self.chatOpen:
            stack_children.append(
                Positioned(
                    key=Key(f"my_header_positgt"),
                    height="610px",
                    width="610px",
                    top="-7px",
                    right="-16px",
                    child=Container(
                        key=Key("my_chat_card_0xffgt_container"),
                        height=610,
                        width=610,
                        color=Colors.transparent,
                        cssPosition="fixed",
                        zAxisIndex=100,
                        child=ChatCard(
                            key=Key("my_chat_card_0xffgt"),
                            context=self.widget.onAiChatContext,
                        ),
                    ),
                )
            )

        return Stack(
            key=Key("header_action_stack_"),
            children=stack_children,
        )
