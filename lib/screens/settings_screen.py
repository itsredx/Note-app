from lib.constants.theme import AppThemes
from lib.constants.colors import *
from lib.components.header_actions import HeaderActions

from pythra import (
    BoxConstraints,
    Divider,
    Dropdown,
    DropdownController,
    DropdownTheme,
    Framework,
    SingleChildScrollView,
    StatefulWidget,
    State,
    Column,
    Row,
    Key,
    Switch,
    VerticalDirection,
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
    Double,
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
        self.show_recent = True
        self.spell_check = True
        self.autocorrect = True
        self.ai_features = True
        self.open_files = DropdownController(selectedValue='Tab')
        self.open_files_options = ['Tab', 'Window']
        self.open_app = DropdownController(selectedValue='Continue')
        self.open_app_options = ['Continue', 'Renew']

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

    def tog_ai_features(self, t):
        self.ai_features = t
        self.setState()

    def tog_recent(self, t):
        self.show_recent = t
        self.setState()

    def tog_spell_check(self, t):
        self.spell_check = t
        self.setState()

    def tog_autocorrect(self, t):
        self.autocorrect = t
        self.setState()

    def build(self) -> Widget:
        app_bar = Row(
                    key=Key("settings_column_r1"),
                    children=[
                        SizedBox(key=Key("Settings_app_bar_sized_box_40px"), width=40),
                        IconButton(
                            key=Key("settings_back_btn_1"),
                            icon=Icon(
                                Icons.arrow_back_rounded,
                                key=Key(
                                    "settings_back_ico_1"
                                ),
                            ),
                            onPressed=lambda: self.widget.navigator.pop(),
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
                )
        return Container(
            height='100vh',
            width='100vw',
            key=Key("settings_container"),
            color=Colors.background,
            padding=EdgeInsets.only(top=24), # bottom=32, left=40, right=40, 
            child=Column(
                    key=Key("settings_column"),
                    children=[
                        app_bar,
                        SizedBox(key=Key("main_sized_box"), height=24),
                        
                        Container(
                            key=Key("scroll_holder"),
                            height='88vh',
                            width=Double.INFINITY,
                            child=SingleChildScrollView(
                                key=Key("settings_scroll_view"),
                                child=Column(
                                    key=Key("settings_scroll_view_column"),
                                    crossAxisAlignment=CrossAxisAlignment.CENTER,
                                    children=[
                                        Image(
                                            key=Key("user_profile_pic"),
                                            image=AssetImage("pic.jpg"),
                                            height=200,
                                            width=200,
                                            borderRadius=BorderRadius.all(100)
                                        ),
                                        Container(
                                            key=Key("profile_user_name_title_container"),
                                            margin=EdgeInsets.only(top=0),
                                            child=Column(
                                                key=Key("profile_user_name_title_container_col_"),
                                                children=[
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
                                                    Text(
                                                        key=Key("profile_user_name_title"),
                                                        data="Developer".upper(),
                                                        style=TextStyle(
                                                            color=Colors.onSurface,
                                                            fontFamily="monospace",
                                                            fontSize=12,
                                                            # fontWeight="bold"
                                                        )
                                                    )
                                                ]
                                            )
                                        ),
                                        Container( 
                                            # ROOT SETTINGS SECTION CONTSINER
                                            key=Key("settings_section_root"),
                                            child=Column(
                                                key=Key("settings_section_root_col"),
                                                children=[
                                                    SizedBox(
                                                        key=Key("settings_section_heading_sb_0"),
                                                        height=24
                                                    ),
                                                    Row(
                                                        key=Key("settings_section_heading_row"),
                                                        children=[
                                                            Text(
                                                                key=Key("settings_section_heading"),
                                                                data="Appearance",
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
                                                            minWidth=400,
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
                                                                    key=Key("option_divider_st"),
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
                                        Container( 
                                            # ROOT SETTINGS SECTION CONTSINER
                                            key=Key("opning_note_app_settings_section_root"),
                                            child=Column(
                                                key=Key("opning_note_app_settings_section_root_col"),
                                                children=[
                                                    SizedBox(
                                                    key=Key("opning_note_app_sb_100"),
                                                    height=24
                                                ),
                                                    Row(
                                                        key=Key("opning_note_app_settings_section_heading_row"),
                                                        children=[
                                                            Text(
                                                                key=Key("opning_note_app_settings_section_heading"),
                                                                data="Openeing Note App",
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
                                                        key=Key("opning_note_app_settings_section_heading_sb_1"),
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
                                                        key=Key("opning_note_app_settings_card"),
                                                        child=Column(
                                                            key=Key("opning_note_app_settings_card_column"),
                                                            crossAxisAlignment=CrossAxisAlignment.STRETCH,
                                                            children=[
                                                                Container(
                                                                    key=Key("opning_note_app_setting_option"),
                                                                    padding=EdgeInsets.symmetric(horizontal=12, vertical=8),
                                                                    # decoration=BoxDecoration(
                                                                    #     border=BorderSide(
                                                                    #         width=1,
                                                                    #         color=Colors.onPrimaryContainer
                                                                    #     )
                                                                    # ),
                                                                    child=Row(
                                                                        key=Key("opning_note_app_setting_option_row"),
                                                                        mainAxisAlignment=MainAxisAlignment.SPACE_BETWEEN,
                                                                        children=[
                                                                            Column(
                                                                                key=Key("opning_note_app_setting_option_column"),
                                                                                crossAxisAlignment=CrossAxisAlignment.START,
                                                                                children=[
                                                                                    Text(
                                                                                        key=Key("opning_note_app_setting_option_title"),
                                                                                        data="Openeing Files",
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
                                                                                        key=Key("opning_note_app_setting_option_subtitle"),
                                                                                        data="Choose where your files are opened",
                                                                                        style=TextStyle(
                                                                                            color=Colors.onSurface,
                                                                                            fontFamily="ubuntu",
                                                                                            fontSize=11,
                                                                                            fontWeight='light'
                                                                                        )
                                                                                    ),
                                                                                ]
                                                                            ),
                                                                            Dropdown(
                                                                                key=Key("opening_files_dropdown"),
                                                                                controller=self.open_files,
                                                                                onChanged=lambda v: print(v),
                                                                                items=self.open_files_options,
                                                                                dropDirection=VerticalDirection.DOWN,
                                                                                theme=DropdownTheme(
                                                                                    width=200,
                                                                                    dropDownHeight=86,
                                                                                    dropdownMargin=EdgeInsets.only(
                                                                                        top=14
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
                                                                            )
                                                                        ]
                                                                    )
                                                                ),
                                                                Divider(
                                                                    key=Key("option_divider_op"),
                                                                    color=Colors.adaptive(dark="#5a5a5a", light="#d3d3d3")
                                                                ),
                                                                Container(
                                                                    key=Key("opning_note_app_setting_option_2"),
                                                                    padding=EdgeInsets.symmetric(horizontal=12, vertical=8),
                                                                    # decoration=BoxDecoration(
                                                                    #     border=BorderSide(width=1, color=Colors.adaptive(dark="#5a5a5a", light="#d3d3d3")),
                                                                    #     )
                                                                    child=Row(
                                                                        key=Key("opning_note_app_setting_option_2_row"),
                                                                        mainAxisAlignment=MainAxisAlignment.SPACE_BETWEEN,
                                                                        children=[
                                                                            Column(
                                                                                key=Key("opning_note_app_setting_option_2_column"),
                                                                                crossAxisAlignment=CrossAxisAlignment.START,
                                                                                children=[
                                                                                    Text(
                                                                                        key=Key("opning_note_app_setting_option_2_title"),
                                                                                        data="When Note App starts",
                                                                                        style=TextStyle(
                                                                                            color=Colors.onSurface,
                                                                                            fontFamily="ubuntu",
                                                                                            fontSize=14,
                                                                                            # fontWeight='light'
                                                                                        )
                                                                                    ),
                                                                                    SizedBox(
                                                                                        key=Key("opning_note_app_option_title_sb"),
                                                                                        height=4
                                                                                    ),
                                                                                    Text(
                                                                                        key=Key("opning_note_app_setting_option_2_subtitle"),
                                                                                        data="On every app start the session should",
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
                                                                                key=Key("opning_note_app_switch_sb"),
                                                                                height=40
                                                                            ),
                                                                            Dropdown(
                                                                                key=Key("opening_files_dropdown"),
                                                                                controller=self.open_app,
                                                                                onChanged=lambda v: print(v),
                                                                                items=self.open_app_options,
                                                                                dropDirection=VerticalDirection.DOWN,
                                                                                theme=DropdownTheme(
                                                                                    width=200,
                                                                                    dropDownHeight=86,
                                                                                    dropdownMargin=EdgeInsets.only(
                                                                                        top=14
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
                                                                            )
                                                                        ]
                                                                    )
                                                                ),
                                                                Divider(
                                                                    key=Key("option_divider_2"),
                                                                    color=Colors.adaptive(dark="#5a5a5a", light="#d3d3d3")
                                                                ),
                                                                Container(
                                                                    key=Key("recent_files_app_setting_option_2"),
                                                                    padding=EdgeInsets.symmetric(horizontal=12, vertical=8),
                                                                    # decoration=BoxDecoration(
                                                                    #     border=BorderSide(width=1, color=Colors.adaptive(dark="#5a5a5a", light="#d3d3d3")),
                                                                    #     )
                                                                    child=Row(
                                                                        key=Key("recent_files_app_setting_option_2_row"),
                                                                        mainAxisAlignment=MainAxisAlignment.SPACE_BETWEEN,
                                                                        children=[
                                                                            Column(
                                                                                key=Key("recent_files_app_setting_option_2_column"),
                                                                                crossAxisAlignment=CrossAxisAlignment.START,
                                                                                children=[
                                                                                    Text(
                                                                                        key=Key("recent_files_app_setting_option_2_title"),
                                                                                        data="Recent Files",
                                                                                        style=TextStyle(
                                                                                            color=Colors.onSurface,
                                                                                            fontFamily="ubuntu",
                                                                                            fontSize=14,
                                                                                            # fontWeight='light'
                                                                                        )
                                                                                    ),
                                                                                    SizedBox(
                                                                                        key=Key("recent_files_app_option_title_sb"),
                                                                                        height=4
                                                                                    ),
                                                                                    Text(
                                                                                        key=Key("recent_files_app_setting_option_2_subtitle"),
                                                                                        data="Show recent files in the dashboard",
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
                                                                                key=Key("recent_files_app_switch_sb"),
                                                                                height=40
                                                                            ),
                                                                            Switch(
                                                                                key=Key("show_recent_filese_switch"),
                                                                                value=self.show_recent,
                                                                                onChanged=self.tog_recent,
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
                                        Container( 
                                            # ROOT SETTINGS SECTION CONTSINER
                                            key=Key("spelling_section_settings_section_root"),
                                            child=Column(
                                                key=Key("spelling_section_settings_section_root_col"),
                                                children=[
                                                    SizedBox(
                                                        key=Key("spelling_section_sb_01"),
                                                        height=24
                                                    ),
                                                    Row(
                                                        key=Key("spelling_section_settings_section_heading_row"),
                                                        children=[
                                                            Text(
                                                                key=Key("spelling_section_settings_section_heading"),
                                                                data="Selling",
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
                                                        key=Key("spelling_section_settings_section_heading_sb_1"),
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
                                                        key=Key("spelling_section_settings_card"),
                                                        child=Column(
                                                            key=Key("spelling_section_settings_card_column"),
                                                            crossAxisAlignment=CrossAxisAlignment.STRETCH,
                                                            children=[
                                                                Container(
                                                                    key=Key("spelling_files_app_setting_option_2"),
                                                                    padding=EdgeInsets.symmetric(horizontal=12, vertical=8),
                                                                    # decoration=BoxDecoration(
                                                                    #     border=BorderSide(width=1, color=Colors.adaptive(dark="#5a5a5a", light="#d3d3d3")),
                                                                    #     )
                                                                    child=Row(
                                                                        key=Key("spelling_files_app_setting_option_2_row"),
                                                                        mainAxisAlignment=MainAxisAlignment.SPACE_BETWEEN,
                                                                        children=[
                                                                            Column(
                                                                                key=Key("spelling_files_app_setting_option_2_column"),
                                                                                crossAxisAlignment=CrossAxisAlignment.START,
                                                                                children=[
                                                                                    Text(
                                                                                        key=Key("spelling_files_app_setting_option_2_title"),
                                                                                        data="Spell Check",
                                                                                        style=TextStyle(
                                                                                            color=Colors.onSurface,
                                                                                            fontFamily="ubuntu",
                                                                                            fontSize=14,
                                                                                            # fontWeight='light'
                                                                                        )
                                                                                    ),
                                                                                    SizedBox(
                                                                                        key=Key("spelling_files_app_option_title_sb"),
                                                                                        height=4
                                                                                    ),
                                                                                    Text(
                                                                                        key=Key("spelling_files_app_setting_option_2_subtitle"),
                                                                                        data="Check files for spelling typos",
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
                                                                                key=Key("spelling_files_app_switch_sb"),
                                                                                height=40
                                                                            ),
                                                                            Switch(
                                                                                key=Key("show_spelling_filese_switch"),
                                                                                value=self.spell_check,
                                                                                onChanged=self.tog_spell_check,
                                                                            ),                                                                       
                                                                        ]
                                                                    )
                                                                ),
                                                                Divider(
                                                                    key=Key("option_divider_3"),
                                                                    color=Colors.adaptive(dark="#5a5a5a", light="#d3d3d3")
                                                                ),
                                                                Container(
                                                                    key=Key("spelling_auto_correct_files_app_setting_option_2"),
                                                                    padding=EdgeInsets.symmetric(horizontal=12, vertical=8),
                                                                    # decoration=BoxDecoration(
                                                                    #     border=BorderSide(width=1, color=Colors.adaptive(dark="#5a5a5a", light="#d3d3d3")),
                                                                    #     )
                                                                    child=Row(
                                                                        key=Key("spelling_auto_correct_files_app_setting_option_2_row"),
                                                                        mainAxisAlignment=MainAxisAlignment.SPACE_BETWEEN,
                                                                        children=[
                                                                            Column(
                                                                                key=Key("spelling_auto_correct_files_app_setting_option_2_column"),
                                                                                crossAxisAlignment=CrossAxisAlignment.START,
                                                                                children=[
                                                                                    Text(
                                                                                        key=Key("spelling_auto_correct_files_app_setting_option_2_title"),
                                                                                        data="Autocorrect",
                                                                                        style=TextStyle(
                                                                                            color=Colors.onSurface,
                                                                                            fontFamily="ubuntu",
                                                                                            fontSize=14,
                                                                                            # fontWeight='light'
                                                                                        )
                                                                                    ),
                                                                                    SizedBox(
                                                                                        key=Key("spelling_auto_correct_files_app_option_title_sb"),
                                                                                        height=4
                                                                                    ),
                                                                                    Text(
                                                                                        key=Key("spelling_auto_correct_files_app_setting_option_2_subtitle"),
                                                                                        data="Typos are automatically corrected when spell check is turned on",
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
                                                                                key=Key("spelling_auto_correct_files_app_switch_sb"),
                                                                                height=40
                                                                            ),
                                                                            Switch(
                                                                                key=Key("show_spelling_auto_correct_filese_switch"),
                                                                                value=self.autocorrect,
                                                                                onChanged=self.tog_autocorrect,
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
                                        Container( 
                                            # ROOT SETTINGS SECTION CONTSINER
                                            key=Key("ai_features_section_settings_section_root"),
                                            child=Column(
                                                key=Key("ai_features_section_settings_section_root_col"),
                                                children=[
                                                    SizedBox(
                                                        key=Key("ai_features_section_sb_04"),
                                                        height=24
                                                    ),
                                                    Row(
                                                        key=Key("ai_features_section_settings_section_heading_row"),
                                                        children=[
                                                            Text(
                                                                key=Key("ai_features_section_settings_section_heading"),
                                                                data="AI Features",
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
                                                        key=Key("ai_features_section_settings_section_heading_sb_1"),
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
                                                        key=Key("ai_features_section_settings_card"),
                                                        child=Column(
                                                            key=Key("ai_features_section_settings_card_column"),
                                                            crossAxisAlignment=CrossAxisAlignment.STRETCH,
                                                            children=[
                                                                Container(
                                                                    key=Key("ai_features_files_app_setting_option_2"),
                                                                    padding=EdgeInsets.symmetric(horizontal=12, vertical=8),
                                                                    # decoration=BoxDecoration(
                                                                    #     border=BorderSide(width=1, color=Colors.adaptive(dark="#5a5a5a", light="#d3d3d3")),
                                                                    #     )
                                                                    child=Row(
                                                                        key=Key("ai_features_files_app_setting_option_2_row"),
                                                                        mainAxisAlignment=MainAxisAlignment.SPACE_BETWEEN,
                                                                        children=[
                                                                            Column(
                                                                                key=Key("ai_features_files_app_setting_option_2_column"),
                                                                                crossAxisAlignment=CrossAxisAlignment.START,
                                                                                children=[
                                                                                    Text(
                                                                                        key=Key("ai_features_files_app_setting_option_2_title"),
                                                                                        data="Ai Features",
                                                                                        style=TextStyle(
                                                                                            color=Colors.onSurface,
                                                                                            fontFamily="ubuntu",
                                                                                            fontSize=14,
                                                                                            # fontWeight='light'
                                                                                        )
                                                                                    ),
                                                                                    SizedBox(
                                                                                        key=Key("ai_features_files_app_option_title_sb"),
                                                                                        height=4
                                                                                    ),
                                                                                    Text(
                                                                                        key=Key("ai_features_files_app_setting_option_2_subtitle"),
                                                                                        data="Turn Ai Features on/off",
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
                                                                                key=Key("ai_features_files_app_switch_sb"),
                                                                                height=40
                                                                            ),
                                                                            Switch(
                                                                                key=Key("show_ai_features_filese_switch"),
                                                                                value=self.ai_features,
                                                                                onChanged=self.tog_ai_features,
                                                                            ),                                                                       
                                                                        ]
                                                                    )
                                                                ),
                                                            ]
                                                        )
                                                    ),
                                                    SizedBox(
                                                        key=Key("ai_features_section_sb_5"),
                                                        height=40
                                                    ),
                                                ]
                                            )
                                        ),
                                        Container( 
                                            # ROOT SETTINGS SECTION CONTSINER
                                            key=Key("about_this_app_section_settings_section_root"),
                                            child=Column(
                                                key=Key("about_this_app_section_settings_section_root_col"),
                                                children=[
                                                    Row(
                                                        key=Key("about_this_app_section_settings_section_heading_row"),
                                                        children=[
                                                            Text(
                                                                key=Key("about_this_app_section_settings_section_heading"),
                                                                data="About This App",
                                                                style=TextStyle(
                                                                    color=Colors.onSurface,
                                                                    fontFamily="ubuntu",
                                                                    fontSize=20,
                                                                    fontWeight="bold"
                                                                )
                                                            )
                                                        ]
                                                    ),
                                                    SizedBox(
                                                        key=Key("about_this_app_section_settings_section_heading_sb_1"),
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
                                                        key=Key("about_this_app_section_settings_card"),
                                                        child=Column(
                                                            key=Key("about_this_app_section_settings_card_column"),
                                                            crossAxisAlignment=CrossAxisAlignment.STRETCH,
                                                            children=[
                                                                Container(
                                                                    key=Key("about_this_app_files_app_setting_option_2"),
                                                                    padding=EdgeInsets.symmetric(horizontal=12, vertical=8),
                                                                    # decoration=BoxDecoration(
                                                                    #     border=BorderSide(width=1, color=Colors.adaptive(dark="#5a5a5a", light="#d3d3d3")),
                                                                    #     )
                                                                    child=Row(
                                                                        key=Key("about_this_app_files_app_setting_option_2_row"),
                                                                        mainAxisAlignment=MainAxisAlignment.SPACE_BETWEEN,
                                                                        children=[
                                                                            Column(
                                                                                key=Key("about_this_app_files_app_setting_option_2_column"),
                                                                                crossAxisAlignment=CrossAxisAlignment.START,
                                                                                children=[
                                                                                    Text(
                                                                                        key=Key("about_this_app_files_app_setting_option_2_title"),
                                                                                        data="Note App",
                                                                                        style=TextStyle(
                                                                                            color=Colors.onSurface,
                                                                                            fontFamily="ubuntu",
                                                                                            fontSize=14,
                                                                                            # fontWeight='light'
                                                                                        )
                                                                                    ),
                                                                                    SizedBox(
                                                                                        key=Key("about_this_app_files_app_option_title_sb"),
                                                                                        height=4
                                                                                    ),
                                                                                    Text(
                                                                                        key=Key("about_this_app_files_app_setting_option_2_subtitle"),
                                                                                        data="version: 0.0.1",
                                                                                        style=TextStyle(
                                                                                            color=Colors.onSurface,
                                                                                            fontFamily="ubuntu",
                                                                                            fontSize=11,
                                                                                            fontWeight='light'
                                                                                        )
                                                                                    ),
                                                                                    SizedBox(
                                                                                        key=Key("about_this_app_files_app_option_title_sb_v"),
                                                                                        height=4
                                                                                    ),
                                                                                    Text(
                                                                                        key=Key("about_this_app_files_app_setting_option_2_subtitle_v"),
                                                                                        data="© 2025 Ahmura Technologies. All rights reserved.",
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
                                                                                key=Key("about_this_app_files_app_switch_sb"),
                                                                                height=40
                                                                            ),                                                                      
                                                                        ]
                                                                    )
                                                                ),
                                                            ]
                                                        )
                                                    ),
                                                    SizedBox(
                                                        key=Key("about_this_app_section_sb_5"),
                                                        height=40
                                                    ),
                                                ]
                                            )
                                        ),                     
                                    ]
                                )
                            ),
                        )                        
                    ]
                )
            )