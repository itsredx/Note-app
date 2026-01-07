from pythra.base import Widget, Key
from pythra.state import StatefulWidget, State
from pythra.widgets import Row, IconButton, Icon, ButtonStyle, Image, AssetImage, SizedBox, MainAxisAlignment, CrossAxisAlignment
from pythra.styles import Colors, BorderRadius, EdgeInsets
from pythra.icons import Icons
from pythra.core import Framework
from lib.constants.colors import AppColors
from lib.constants.theme import AppThemes

class HeaderActions(StatefulWidget):
    def __init__(self, key: Key, onSave: callable, onAiChat: callable, onAccount: callable):
        self.onSave = onSave
        self.onAiChat = onAiChat
        self.onAccount = onAccount
        super().__init__(key=key)

    def createState(self):
        return HeaderActionsState()

class HeaderActionsState(State):
    @property
    def is_dark(self):
        return Framework.instance().theme.brightness == 'dark'

    def toggle_theme(self):
        new_theme = AppThemes.light if self.is_dark else AppThemes.dark
        Framework.instance().set_theme(new_theme)
        # Rebuild this row to update all icons (Sun/Moon, Sparkle, etc)
        self.setState()

    def build(self):
        return Row(
            key=Key("search_ai_and_controls_header_row"),
            mainAxisAlignment=MainAxisAlignment.END,
            crossAxisAlignment=CrossAxisAlignment.START,
            children=[
                IconButton(
                    key=Key("Header_btn_1"),
                    icon=Icon(
                        Icons.light_mode_rounded if self.is_dark else Icons.dark_mode_rounded,
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
                SizedBox(width=12, key=Key("sixe_box_header_controls_1")),
                IconButton(
                    key=Key("save_rounded_btn"),
                    icon=Icon(Icons.save_rounded, key=Key("save_rounded_ico")),
                    onPressed=self.get_widget().onSave,
                    tooltip="Save",
                    style=ButtonStyle(
                        backgroundColor=AppColors.buttonBackgroundColor,
                        hoverColor=AppColors.buttonHoverColor,
                        foregroundColor=AppColors.buttonForegroundColor,
                    ),
                ),
                SizedBox(width=12, key=Key("sixe_box_save_rounded")),
                IconButton(
                    key=Key("sparkle_btn"),
                    icon=Image(
                        image=(
                            AssetImage("ICON-LIGHT.png")
                            if self.is_dark
                            else AssetImage("ICON.png")
                        ),
                        key=Key("sparkle_ico"),
                    ),
                    onPressed=self.get_widget().onAiChat,
                    tooltip="Ai Chat",
                    style=ButtonStyle(
                        backgroundColor=AppColors.buttonBackgroundColor,
                        hoverColor=AppColors.buttonHoverColor,
                    ),
                ),
                SizedBox(width=12, key=Key("sixe_box_header_sparkle_btn")),
                IconButton(
                    key=Key("account_circle_rounded_btn"),
                    icon=Icon(
                        Icons.account_circle_rounded,
                        key=Key("account_circle_rounded_ico"),
                    ),
                    onPressed=self.get_widget().onAccount,
                    tooltip="User Account & Settings",
                    style=ButtonStyle(
                        backgroundColor=AppColors.buttonBackgroundColor,
                        hoverColor=AppColors.buttonHoverColor,
                        foregroundColor=AppColors.buttonForegroundColor,
                    ),
                ),
            ],
        )
