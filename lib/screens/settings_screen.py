from lib.constants.theme import AppThemes
from lib.constants.colors import *
from lib.screens.components.header_actions import HeaderActions

from pythra import (
    BoxConstraints,
    Divider,
    Framework,
    SingleChildScrollView,
    StatefulWidget,
    State,
    Column,
    Row,
    Key,
    Switch,
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
    Navigator, PageRoute, NavigatorState,
    GridView,
    GestureDetector,
    Padding,
    TextField,
    TextEditingController,
    InputDecoration,
)


class SettingsAndProfileScreen(StatefulWidget):
    def __init__(
        self,
        key: Key,
        navigator: NavigatorState,
    ):
        self.navigator = navigator
        super().__init__(key=key)
        
    def createState(self):
        return SettingsAndProfileScreenState(self.navigator)
    
class SettingsAndProfileScreenState(State):
    def __init__(self, navigator: NavigatorState,):
        super().__init__()
        self.t = True
        self.navigator = navigator
        self.t = True

    @property
    def is_dark(self):
        return Framework.instance().theme.brightness == 'dark'

    def toggle_theme(self):
        new_theme = AppThemes.light if self.is_dark else AppThemes.dark
        Framework.instance().set_theme(new_theme)
        # Rebuild this row to update all icons (Sun/Moon, Sparkle, etc)
        self.setState()
    
    def tog(self, t):
        self.t = t
        self.setState()


    def build(self):
        return Container(
            height='100vh',
            width='100vw',
            key=Key("settings_container"),
            color=Colors.background,
            padding=EdgeInsets.only(left=40, right=40, top=24), # bottom=32
            child=Column(
                    key=Key("settings_column"),
                    children=[
                        Row(
                            key=Key("settings_column_r1"),
                            children=[
                                IconButton(
                                    key=Key("settings_back_btn_1"),
                                    icon=Icon(
                                        Icons.arrow_back_rounded,
                                        key=Key(
                                            "settings_back_ico_1"
                                        ),
                                    ),
                                    onPressed=lambda: self.get_widget().navigator.pop(),
                                    style=ButtonStyle(
                                        backgroundColor=Colors.transparent,
                                        hoverColor=AppColors.buttonHoverColor,
                                        foregroundColor=AppColors.buttonForegroundColor,
                                    ),
                                ),
                                SizedBox(key=Key("Settings_app_bar_sized_box"), width=12),
                                Text(
                                    "Settings & Profile", 
                                    key=Key("DashBoard_Page_heading"), 
                                    style=TextStyle(fontSize=32, fontWeight="bold", color=Colors.onSurface)
                                ),
                            ]
                        ),
                        SizedBox(key=Key("main_sized_box"), height=24),
                        SingleChildScrollView(
                            key=Key("settings_scroll_view"),
                            child=Column(
                                key=Key("settings_scroll_view_column"),
                                children=[
                                    Image(
                                        key=Key("user_profile_pic"),
                                        image=AssetImage("pic.jpg"),
                                        height=200,
                                        width=200,
                                        borderRadius=BorderRadius.all(100)
                                    ),
                                    SizedBox(
                                        key=Key("image_sb_1"),
                                        height=12
                                    ),
                                    Text(
                                        key=Key("profile_user_name"),
                                        data="Ahmad Muhammad",
                                        style=TextStyle(
                                            color=Colors.onSurface,
                                            fontFamily="ubuntu",
                                            fontSize=24,
                                            fontWeight="bold"
                                        )
                                    ),
                                    Container(
                                        margin=EdgeInsets.only(top=-10),
                                        child=Text(
                                        key=Key("profile_user_name"),
                                        data="Developer".upper(),
                                        style=TextStyle(
                                            color=Colors.onSurface,
                                            fontFamily="monospace",
                                            fontSize=12,
                                            # fontWeight="bold"
                                        )
                                    )
                                    ),
                                    SizedBox(
                                        key=Key("image_name_sb_1"),
                                        height=24
                                    ),
                                    Container( 
                                        # ROOT SETTINGS SECTION CONTSINER
                                        key=Key("settings_section_root"),
                                        child=Column(
                                            key=Key("settings_section_root_col"),
                                            children=[
                                                Row(
                                                    key=Key("settings_section_heading_row"),
                                                    children=[
                                                        Text(
                                                            key=Key("settings_section_heading"),
                                                            data="App Settings",
                                                            style=TextStyle(
                                                                color=Colors.onSurface,
                                                                fontFamily="ubuntu",
                                                                fontSize=24,
                                                                # fontWeight="bold"
                                                            )
                                                        )
                                                    ]
                                                ),
                                                SizedBox(
                                                    key=Key("settings_section_heading_sb_1"),
                                                    height=18
                                                ),
                                                Container(
                                                    constraints=BoxConstraints(
                                                        minWidth=500,
                                                    ),
                                                    width=800,
                                                    decoration=BoxDecoration(
                                                        color=AppColors.appBackgroundColor,
                                                        borderRadius=BorderRadius.all(20),
                                                        border=BorderSide(width=1, color=Colors.adaptive(dark="#5a5a5a", light="#d3d3d3")),
                                                    ),
                                                    key=Key("settings_card"),
                                                    child=Column(
                                                        key=Key("settings_card_column"),
                                                        crossAxisAlignment=CrossAxisAlignment.STRETCH,
                                                        children=[
                                                            Container(
                                                                key=Key("setting_option"),
                                                                padding=EdgeInsets.symmetric(horizontal=12, vertical=8),
                                                                # decoration=BoxDecoration(
                                                                #     border=BorderSide(
                                                                #         width=1,
                                                                #         color=Colors.onPrimaryContainer
                                                                #     )
                                                                # ),
                                                                child=Row(
                                                                    key=Key("setting_option_row"),
                                                                    mainAxisAlignment=MainAxisAlignment.SPACE_BETWEEN,
                                                                    children=[
                                                                        Column(
                                                                            key=Key("setting_option_column"),
                                                                            crossAxisAlignment=CrossAxisAlignment.START,
                                                                            children=[
                                                                                Text(
                                                                                    key=Key("setting_option_title"),
                                                                                    data="App Theme",
                                                                                    style=TextStyle(
                                                                                        color=Colors.onSurface,
                                                                                        fontFamily="ubuntu",
                                                                                        fontSize=14,
                                                                                    )
                                                                                ),
                                                                                SizedBox(
                                                                                    key=Key("option_title_sb"),
                                                                                    height=4
                                                                                ),
                                                                                Text(
                                                                                    key=Key("setting_option_subtitle"),
                                                                                    data="Set the color theme of the app",
                                                                                    style=TextStyle(
                                                                                        color=Colors.onSurface,
                                                                                        fontFamily="ubuntu",
                                                                                        fontSize=11,
                                                                                        fontWeight='light'
                                                                                    )
                                                                                ),
                                                                            ]
                                                                        ),
                                                                        IconButton(
                                                                            key=Key("setting_icon_button"),
                                                                            icon=Icon(
                                                                                Icons.light_mode_rounded if self.is_dark else Icons.dark_mode_rounded,
                                                                                key=Key("setting_ico_1"),
                                                                            ),
                                                                            onPressed=self.toggle_theme,
                                                                            tooltip="Light Mode" if self.is_dark else "Dark Mode",
                                                                            style=ButtonStyle(
                                                                                backgroundColor=AppColors.buttonBackgroundColor,
                                                                                hoverColor=AppColors.buttonHoverColor,
                                                                                foregroundColor=AppColors.buttonForegroundColor,
                                                                            ),
                                                                        )
                                                                    ]
                                                                )
                                                            ),
                                                            Divider(
                                                                key=Key("option_divider"),
                                                                color=Colors.adaptive(dark="#5a5a5a", light="#d3d3d3")
                                                            ),
                                                            Container(
                                                                key=Key("setting_option_2"),
                                                                padding=EdgeInsets.symmetric(horizontal=12, vertical=8),
                                                                # decoration=BoxDecoration(
                                                                #     border=BorderSide(width=1, color=Colors.adaptive(dark="#5a5a5a", light="#d3d3d3")),
                                                                #     )
                                                                child=Row(
                                                                    key=Key("setting_option_2_row"),
                                                                    mainAxisAlignment=MainAxisAlignment.SPACE_BETWEEN,
                                                                    children=[
                                                                        Column(
                                                                            key=Key("setting_option_2_column"),
                                                                            crossAxisAlignment=CrossAxisAlignment.START,
                                                                            children=[
                                                                                Text(
                                                                                    key=Key("setting_option_2_title"),
                                                                                    data="Panel Mode",
                                                                                    style=TextStyle(
                                                                                        color=Colors.onSurface,
                                                                                        fontFamily="ubuntu",
                                                                                        fontSize=14,
                                                                                        # fontWeight='light'
                                                                                    )
                                                                                ),
                                                                                SizedBox(
                                                                                    key=Key("option_title_sb"),
                                                                                    height=4
                                                                                ),
                                                                                Text(
                                                                                    key=Key("setting_option_2_subtitle"),
                                                                                    data="The dock extends to the screen edge",
                                                                                    style=TextStyle(
                                                                                        color=Colors.onSurface,
                                                                                        fontFamily="ubuntu",
                                                                                        fontSize=11,
                                                                                        fontWeight='light'
                                                                                    )
                                                                                ),
                                                                            ]
                                                                        ),
                                                                        SizedBox(
                                                                            key=Key("_switch_sb"),
                                                                            height=40
                                                                        ),
                                                                        Switch(
                                                                            key=Key("dock_mode_or_panel_mode"),
                                                                            value=self.t,
                                                                            onChanged=self.tog,
                                                                        ),
                                                                    ]
                                                                )
                                                            ),
                                                        ]
                                                    )
                                                )
                                            ]
                                        )
                                    ),
                                ]
                            )
                        )
                    ]
                )
            )