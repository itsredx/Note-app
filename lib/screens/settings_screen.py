from types import prepare_class
from lib.constants.theme import AppThemes
from lib.constants.colors import *
from lib.utils.shared_prefernce import PythraPreferences
from lib.components.header_actions import HeaderActions
from lib.components.settings_widgets import SettingsSection, SettingsTile
from lib import APP_NAME, APP_VERSION, pref
from pythra import (
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
    Text,
    Colors,
    SizedBox,
    CrossAxisAlignment,
    EdgeInsets,
    Icon,
    IconButton,
    Icons,
    ButtonStyle,
    BorderRadius,
    TextStyle,
    Image,
    AssetImage,
    NavigatorState,
    Double,
    InputDecoration,
    BorderSide,
    BorderRadius,
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
        self.navigator = navigator
        self.panel_state = pref.get("panel_state", None) if pref.get("panel_state", None) != None else False
        self.show_recent = pref.get("show_recent", None) if pref.get("show_recent", None) != None else True
        self.spell_check = pref.get("spell_check", None) if pref.get("spell_check", None) != None else True
        self.autocorrect = pref.get("autocorrect", None) if pref.get("autocorrect", None) != None else True
        self.ai_features = pref.get("ai_features", None) if pref.get("ai_features", None) != None else True
        self.open_files = DropdownController(
                selectedValue= pref.get("open_files", None) if pref.get("open_files", None) != None else 'Tab'
            )
        self.open_files_options = ['Tab', 'Window']
        self.open_app = DropdownController(
                selectedValue= pref.get("open_app", None) if pref.get("open_app", None) != None else 'Continue'
            )
        self.open_app_options = ['Continue', 'Renew']

    @property
    def is_dark(self):
        return Framework.instance().theme.brightness == 'dark'

    def toggle_theme(self):
        new_theme = AppThemes.light if self.is_dark else AppThemes.dark
        Framework.instance().set_theme(new_theme)
        pref.set("theme", "dark") if self.is_dark else pref.set("theme", "light")        
        # Rebuild this row to update all icons (Sun/Moon, Sparkle, etc)
        self.setState()
    
    def tog_panel_state(self, t):
        self.panel_state = not self.panel_state
        pref.set("panel_state",self.panel_state)
        print(f"Panel state: {self.panel_state}")
        self.setState()

    def tog_ai_features(self, t):
        self.ai_features = not self.ai_features
        pref.set("ai_features", self.ai_features)
        print(f"AI features: {self.ai_features}")
        self.setState()

    def tog_show_recent(self, t):
        self.show_recent = not self.show_recent
        pref.set("show_recent", self.show_recent)
        print(f"Recent: {self.show_recent}")
        self.setState()

    def tog_spell_check(self, t):
        self.spell_check = not self.spell_check
        pref.set("spell_check", self.spell_check)        
        print(f"Spell check: {self.spell_check}")
        self.setState()

    def tog_autocorrect(self, t):
        self.autocorrect = not self.autocorrect
        pref.set("autocorrect", self.autocorrect)
        print(f"Autocorrect: {self.autocorrect}")
        self.setState()

    def update_open_files(self, value):
        self.open_files.selectedValue = value
        pref.set("open_files", self.open_files.selectedValue)
        self.setState()

    def update_open_app(self, value):
        self.open_app.selectedValue = value
        pref.set("open_app", self.open_app.selectedValue)
        self.setState()

    def update_panel_state(self, value):
        self.panel_state = value
        self.setState()

    def update_show_recent(self, value):
        self.show_recent = value
        self.setState()

    def update_spell_check(self, value):
        self.spell_check = value
        self.setState()

    def update_autocorrect(self, value):
        self.autocorrect = value
        self.setState()

    def update_ai_features(self, value):
        self.ai_features = value
        self.setState()

    def reset_to_default(self):
        self.open_files.selectedValue = "Tab"
        self.open_app.selectedValue = "Continue"
        self.panel_state = True
        self.show_recent = True
        self.spell_check = True
        self.autocorrect = True
        self.ai_features = True
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
                                        SettingsSection(
                                            key=Key("appearance_section"),
                                            title="Appearance",
                                            children=[
                                                SettingsTile(
                                                    key=Key("app_theme_tile"),
                                                    title="App Theme",
                                                    subtitle="Set the color theme of the app",
                                                    trailing=IconButton(
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
                                                ),
                                                SettingsTile(
                                                    key=Key("panel_mode_tile"),
                                                    title="Panel Mode",
                                                    subtitle="The dock extends to the screen edge",
                                                    trailing=Switch(
                                                        key=Key("dock_mode_or_panel_mode"),
                                                        value=self.panel_state,
                                                        onChanged=self.tog_panel_state,
                                                    )
                                                )
                                            ]
                                        ),
                                        SettingsSection(
                                            key=Key("opening_note_app_section"),
                                            title="Opening Note App",
                                            children=[
                                                SettingsTile(
                                                    key=Key("opening_files_tile"),
                                                    title="Opening Files",
                                                    subtitle="Choose where your files are opened",
                                                    trailing=Dropdown(
                                                        key=Key("opening_files_dropdown"),
                                                        controller=self.open_files,
                                                        onChanged=self.update_open_files,
                                                        items=self.open_files_options,
                                                        dropDirection=VerticalDirection.DOWN,
                                                        decoration=InputDecoration(
                                                            fillColor=AppColors.dropDownColor,
                                                            borderRadius=BorderRadius.circular(8),
                                                            border=BorderSide(
                                                                color=AppColors.transparent,
                                                                width=0,
                                                            ),
                                                            focusedBorder=BorderSide(
                                                                color=AppColors.transparent,
                                                                width=0,
                                                            ),
                                                        ),
                                                        theme=DropdownTheme(
                                                            width=200,
                                                            dropDownHeight=86,
                                                            dropdownMargin=EdgeInsets.only(top=14),
                                                            # fontSize=12,
                                                            # borderWidth=0.0,
                                                            # borderColor=AppColors.transparent,
                                                            # backgroundColor=AppColors.dropDownColor,
                                                            dropdownColor=AppColors.dropDownColor,
                                                            # textColor=AppColors.iconColor,
                                                            dropdownTextColor=AppColors.iconColor,
                                                            dropdownHoverColor=AppColors.dropDownMenuHoverColor,
                                                            hoverColor=AppColors.dropDownHoverColor,
                                                            itemHoverColor=AppColors.dropDownMenuHoverColor,
                                                        ),
                                                    )
                                                ),
                                                SettingsTile(
                                                    key=Key("when_note_app_starts_tile"),
                                                    title="When Note App starts",
                                                    subtitle="On every app start the session should",
                                                    trailing=Dropdown(
                                                        key=Key("opening_app_dropdown"),
                                                        controller=self.open_app,
                                                        onChanged=self.update_open_app,
                                                        items=self.open_app_options,
                                                        dropDirection=VerticalDirection.DOWN,
                                                        decoration=InputDecoration(
                                                            fillColor=AppColors.dropDownColor,
                                                            borderRadius=BorderRadius.circular(8),
                                                            border=BorderSide(
                                                                color=AppColors.transparent,
                                                                width=0,
                                                            ),
                                                            focusedBorder=BorderSide(
                                                                color=AppColors.transparent,
                                                                width=0,
                                                            ),
                                                        ),
                                                        theme=DropdownTheme(
                                                            width=200,
                                                            dropDownHeight=86,
                                                            dropdownMargin=EdgeInsets.only(top=14),
                                                            # fontSize=12,
                                                            # borderWidth=0.0,
                                                            # borderColor=AppColors.transparent,
                                                            # backgroundColor=AppColors.dropDownColor,
                                                            dropdownColor=AppColors.dropDownColor,
                                                            # textColor=AppColors.iconColor,
                                                            dropdownTextColor=AppColors.iconColor,
                                                            dropdownHoverColor=AppColors.dropDownMenuHoverColor,
                                                            hoverColor=AppColors.dropDownHoverColor,
                                                            itemHoverColor=AppColors.dropDownMenuHoverColor,
                                                        ),
                                                    )
                                                ),
                                                SettingsTile(
                                                    key=Key("recent_files_tile"),
                                                    title="Recent Files",
                                                    subtitle="Show recent files in the dashboard",
                                                    trailing=Switch(
                                                        key=Key("show_recent_filese_switch"),
                                                        value=self.show_recent,
                                                        onChanged=self.tog_show_recent,
                                                    )
                                                )
                                            ]
                                        ),
                                        SettingsSection(
                                            key=Key("spelling_section"),
                                            title="Spelling",
                                            children=[
                                                SettingsTile(
                                                    key=Key("spell_check_tile"),
                                                    title="Spell Check",
                                                    subtitle="Check files for spelling typos",
                                                    trailing=Switch(
                                                        key=Key("spell_check_switch"),
                                                        value=self.spell_check,
                                                        onChanged=self.tog_spell_check,
                                                    ),
                                                ),
                                                SettingsTile(
                                                    key=Key("autocorrect_tile"),
                                                    title="Autocorrect",
                                                    subtitle="Typos are automatically corrected when spell check is turned on",
                                                    trailing=Switch(
                                                        key=Key("autocorrect_switch"),
                                                        value=self.autocorrect,
                                                        onChanged=self.tog_autocorrect,
                                                    ),
                                                ),
                                            ]
                                        ),
                                        SettingsSection(
                                            key=Key("ai_features_section"),
                                            title="AI Features",
                                            children=[
                                                SettingsTile(
                                                    key=Key("ai_features_tile"),
                                                    title="AI Features",
                                                    subtitle="Turn AI Features on/off",
                                                    trailing=Switch(
                                                        key=Key("ai_features_switch"),
                                                        value=self.ai_features,
                                                        onChanged=self.tog_ai_features,
                                                    ),
                                                ),
                                            ]
                                        ),
                                        SettingsSection(
                                            key=Key("about_app_section"),
                                            title="About This App",
                                            children=[
                                                SettingsTile(
                                                    key=Key("about_app_tile"),
                                                    title=APP_NAME,
                                                    subtitle=f"version: {APP_VERSION}\n© 2025 Ahmura Technologies. All rights reserved.",
                                                ),
                                            ],
                                            last_item=True
                                        ),
                                    ]
                                )
                            ),
                        )                        
                    ]
                )
            )
