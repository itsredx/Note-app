# main.py
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
    DerivedDropdown,
    DerivedDropdownController,
    DerivedDropdownTheme,
    Dropdown,
    DropdownController,
    DropdownTheme,
    VerticalDirection,
    Navigator,
)

from lib.constants.colors import *
import time

labels = ['Funny', 'Serious', 'Professional', 'Casual', 'Poetic', 'Sarcastic', 'Friendly', 'Formal', 'Informal', 'Creative', 'Witty', 'Humorous', 'Playful', 'Quirky', 'Eccentric', 'Whimsical', 'Zany', 'Silly', 'Goofy', 'Jocular', 'Comical', 'Hilarious', 'Amusing', 'Entertaining', 'Droll', 'Facetious', 'Jesting', 'Jocular', 'Jocular', 'Jocular']
action_label = ['Summarize', 'Expand', 'Rewrite', 'Translate', 'Paraphrase', 'Rephrase']

action_to_perform = {
    "model": "",
    "action": ""
}

from PySide6.QtCore import QTimer

class AiActionsControlsState(State):
    def __init__(self):
        super().__init__()
        self.mode_controller = DropdownController(selectedValue=labels[0])
        self.action_controller = DropdownController(selectedValue=action_label[0])
        self.is_loading = False

    def setMode(self, new_value):
        print("Mode changed!: ", new_value)
        action_to_perform["model"] = new_value

    def setAction(self, new_value):
        print("Action changed!: ", new_value)
        action_to_perform["action"] = new_value

    def _finish_generation(self):
        self.is_loading = False
        self.setState()
        
        widget = self.get_widget()
        if widget and widget.onGenerate:
            widget.onGenerate()

    def generate(self):
        if self.is_loading:
            return

        print("Generating...")
        print(action_to_perform)
        
        self.is_loading = True
        self.setState()
        
        # Simulate network request with QTimer to invoke callback on the main thread safely
        QTimer.singleShot(2000, self._finish_generation)

    def _build_styled_dropdown(self, key_str, controller, items, on_changed):
        return Dropdown(
            controller=controller,
            key=Key(key_str),
            items=items,
            onChanged=on_changed,
            dropDirection=VerticalDirection.DOWN,
            theme=DropdownTheme(
                width=200,
                dropDownHeight=250,
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


    def build(self):
        return Container(
                key=Key(
                    "ai_controls_container"
                ),
                # color=Colors.white,
                padding=EdgeInsets.all(8),
                child=Row(
                    mainAxisAlignment=MainAxisAlignment.CENTER,
                    crossAxisAlignment=CrossAxisAlignment.CENTER,
                    key=Key(
                        "ai_controls_row"
                    ),
                    children=[
                        # self.dropdown,
                        self._build_styled_dropdown("ai_mode_dropdown", self.mode_controller, labels, self.setMode),
                        SizedBox(
                            width=12,
                            key=Key("ai_controls_sized_box_1"),
                        ),
                        self._build_styled_dropdown("ai_action_dropdown", self.action_controller, action_label, self.setAction),
                        
                        Container(
                            key=Key("ai_controls_divider_container"),
                            color=AppColors.iconColor,
                            height=30,
                            width=2,
                            margin=EdgeInsets.symmetric(
                                horizontal=12,
                            ),
                        ),
                        ElevatedButton(
                            key=Key("generate_btn"),
                            child=Row(
                                key=Key("generate_btn_inner_row"),
                                children=[
                                    Text(
                                        "Generating..." if self.is_loading else "Generate",
                                        key=Key(
                                            "generate_btn_txt"
                                        ),
                                        style=TextStyle(
                                            fontSize=20,
                                        ),
                                    ),
                                ],
                            ),
                            style=ButtonStyle(
                                backgroundColor=AppColors.buttonBackgroundColor,
                                foregroundColor=AppColors.buttonForegroundColor,
                                elevation=0,
                                shape=BorderRadius.circular(8.0),
                                margin=EdgeInsets.all(0),
                                hoverColor=AppColors.buttonHoverColor,
                            ),
                            onPressed= self.generate,
                            tooltip="Generate",
                        ),
                    ],
                ),
                decoration=BoxDecoration(
                    borderRadius=BorderRadius.all(16),
                    border=BorderSide(width=1, color=Colors.adaptive(dark="#5a5a5a", light="#d3d3d3")),
                    color=Colors.adaptive(dark=AppColors.toolbarBackgroundDarkColor, light=Colors.white),
                ),
            )

class AiActionsControls(StatefulWidget):
    def __init__(self, key = None, onGenerate = None):
        super().__init__(key)
        self.onGenerate = onGenerate

    def createState(self) -> AiActionsControlsState:
        return AiActionsControlsState()