# import colors
from constants.colors import *

# Welcome to your new Pythra App!
from pythra import (
    BoxDecoration,
    InputDecoration,
    SingleChildScrollView,
    StatefulWidget,
    State,
    Column,
    Row,
    Key,
    TextEditingController,
    TextField,
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
    Dropdown,
    DropdownController,
    DropdownTheme,
    VerticalDirection,
    BorderSide,
    Border,
    ElevatedButton,
    Double,
    Divider,
)

from plugins.markdown_render.widget import MarkdownRender
from plugins.markdown_render.style import RendererStyle
from plugins.markdown_render.controller import MarkdownRendererController


MarkdownRender(
    key=Key("markdown_render_chat"),
    controller=MarkdownRendererController(),
    style=RendererStyle()
)


class ChatCardState(State):
    def __init__(self):
        self.text_controller = TextEditingController()
        self.open = True
        self.base_key = None
        self.context = None

    def initState(self):
        self.base_key = self.get_widget().key.value
        self.context = self.get_widget().context

    def _open(self):
        self.open = not self.open
        self.setState()

    def send(self):
        pass

    def build(self) -> Widget:
        return Container(
            key=Key(f"{self.base_key}_warper"),
            height=700,
            width=700,
            color=Colors.transparent,
            child=Stack(
                key=Key(f"{self.base_key}_stakkkkkk"),
                children=[
                    (
                        Positioned(
                            key=Key(f"{self.base_key}_posit_q"),
                            height="610px",
                            width="610px",
                            top="0px",
                            left="-2px",
                            child=Container(
                                key=Key(f"{self.base_key}_warper1_border"),
                                height=610,
                                width=610,
                                # color=Colors.blue,
                                child=ClipPath(
                                    key=Key(f"{self.base_key}_clippy_border"),
                                    points=[
                                        # | --
                                        (34.9, 100),
                                        (100, 100),
                                        (100, 10),
                                        (90.1, 10),
                                        (90.1, 0),
                                        (81.63, 0),
                                        (81.63, 10),
                                        (34.9, 10),
                                    ],
                                    viewBox=[100, 100],
                                    radius=6,
                                    aspectRatio=1.5,
                                    child=Container(
                                        key=Key(f"{self.base_key}_inner_2"),
                                        height=610,
                                        width=610,
                                        color=Colors.adaptive(
                                            dark="#d3d3d35c",
                                            light="#5a5a5a30",
                                        ),
                                    ),
                                ),
                            ),
                        )
                        if self.open
                        else Container(
                            key=Key(f"{self.base_key}_in_warper1_"),
                            height=600,
                            width=600,
                        )
                    ),
                    (
                        Container(
                            key=Key(f"{self.base_key}_warper_1"),
                            height=610,
                            width=610,
                            # color=Colors.blue,
                            padding=EdgeInsets.only(top=1.5),
                            child=ClipPath(
                                key=Key(f"{self.base_key}_clippy"),
                                points=[
                                    # | --
                                    (35, 100),
                                    (100, 100),
                                    (100, 10),
                                    (90, 10),
                                    (90, 0),
                                    (82, 0),
                                    (82, 10),
                                    (35, 10),
                                ],
                                viewBox=[100, 100],
                                radius=6,
                                aspectRatio=1.5,
                                height=607,
                                width=606.8,
                                child=Container(
                                    key=Key(f"{self.base_key}_inner"),
                                    height=610,
                                    width=610,
                                    color=Colors.adaptive(
                                        dark=Colors.hex("#2c2c2c"), light=Colors.white
                                    ),
                                ),
                            ),
                        )
                        if self.open
                        else Container(
                            key=Key(f"{self.base_key}_warper1_"),
                            height=610,
                            width=610,
                        )
                    ),
                    (
                        Positioned(
                            key=Key(f"{self.base_key}_posit2"),
                            height="600px",
                            width="600px",
                            top="60px",
                            left="210px",
                            child=Container(
                                key=Key(f"{self.base_key}_chat_container"),
                                height=550,
                                width=398,
                                # color=Colors.aqua,
                                padding=EdgeInsets.only(left=16, right=16, top=8),
                                child=Column(
                                    key=Key(f"{self.base_key}_chat_container_column"),
                                    children=[
                                        Container(
                                            key=Key(
                                                f"{self.base_key}_chat_container_note_title_context"
                                            ),
                                            height=50,
                                            width="100%",
                                            child=Center(
                                                key=Key(
                                                    f"{self.base_key}_chat_container_note_title_context_center"
                                                ),
                                                child=Text(
                                                    key=Key(
                                                        f"{self.base_key}_chat_container_note_title_context_txt"
                                                    ),
                                                    data="Welcome",
                                                    style=TextStyle(
                                                        fontSize=18,
                                                        fontWeight="bold",
                                                        color=Colors.onBackground,
                                                    ),
                                                ),
                                            ),
                                        ),
                                        Container(
                                            key=Key(
                                                f"{self.base_key}_chat_container_msg_context"
                                            ),
                                            # padding=EdgeInsets.only(left=8, right=8),
                                            width="100%",
                                            height=400,
                                            # color=Colors.pink,
                                            child=SingleChildScrollView(
                                                key=Key(
                                                    f"{self.base_key}_chat_container_mesg_scroll_view"
                                                ),
                                                child=Column(
                                                    key=Key(
                                                        f"{self.base_key}_chat_container_mesg_column"
                                                    ),
                                                    children=[
                                                        Row(
                                                            key=Key(
                                                                f"{self.base_key}_chat_container_mesg_row_{i}"
                                                            ),
                                                            mainAxisAlignment=(
                                                                MainAxisAlignment.START
                                                                if i % 2 == 0
                                                                else MainAxisAlignment.END
                                                            ),
                                                            children=[
                                                                Container(
                                                                    width=(
                                                                        "100%"
                                                                        if i % 2 == 0
                                                                        else "290px"
                                                                    ),
                                                                    key=Key(
                                                                        f"{self.base_key}_chat_container_mesg_{i}"
                                                                    ),
                                                                    height=Double.INFINITY,
                                                                    padding=EdgeInsets.all(
                                                                        8
                                                                    ),
                                                                    color=(
                                                                        Colors.transparent
                                                                        if i % 2 == 0
                                                                        else Colors.adaptive(
                                                                            light=Colors.hex(
                                                                                "#e9ecef"
                                                                            ),
                                                                            dark=Colors.hex(
                                                                                "#4c4c4c"
                                                                            ),
                                                                        )
                                                                    ),
                                                                    margin=EdgeInsets.symmetric(
                                                                        horizontal=0,
                                                                        vertical=2,
                                                                    ),
                                                                    decoration=BoxDecoration(
                                                                        borderRadius=BorderRadius.all(
                                                                            8
                                                                        )
                                                                    ),
                                                                    child=(
                                                                        Container(
                                                                            key=Key(
                                                                                f"{self.base_key}_chat_container_mesg_{i}_cont"
                                                                            ),
                                                                            child=Column(
                                                                                key=Key(
                                                                                    f"{self.base_key}_chat_container_mesg_{i}_col"
                                                                                ),
                                                                                crossAxisAlignment=CrossAxisAlignment.START,
                                                                                children=[
                                                                                    MarkdownRender(
                                                                                        key=Key(
                                                                                            f"{self.base_key}_chat_container_mesg_{i}_markdown_render"
                                                                                        ),
                                                                                        markdownText=f"Here is a funnier take on your introduction:",
                                                                                        style=RendererStyle(
                                                                                            fontSize='14px',
                                                                                            fontColor=Colors.onBackground,
                                                                                            padding='0px'
                                                                                        )
                                                                                    ),
                                                                                    Container(
                                                                                        key=Key(
                                                                                            f"{self.base_key}_chat_container_mesg_{i}_cont_inner"
                                                                                        ),
                                                                                        width=Double.INFINITY,
                                                                                        height=Double.INFINITY,
                                                                                        margin=EdgeInsets.only(
                                                                                            left=24,
                                                                                            top=10,
                                                                                        ),
                                                                                        color=Colors.adaptive(
                                                                                            light=Colors.white,
                                                                                            dark=AppColors.toolbarBackgroundDarkColor,
                                                                                        ),
                                                                                        decoration=BoxDecoration(
                                                                                            borderRadius=BorderRadius.all(
                                                                                                8
                                                                                            ),
                                                                                            border=BorderSide(
                                                                                                width=1,
                                                                                                color=Colors.adaptive(
                                                                                                    dark="#5a5a5a",
                                                                                                    light="#d3d3d3",
                                                                                                ),
                                                                                            ),
                                                                                        ),
                                                                                        child=Column(
                                                                                            key=Key(
                                                                                                f"{self.base_key}_chat_container_mesg_{i}_cont_inner_col_"
                                                                                            ),
                                                                                            crossAxisAlignment=CrossAxisAlignment.STRETCH,
                                                                                            children=[
                                                                                                Container(
                                                                                                    key=Key(
                                                                                                        f"{self.base_key}_chat_container_mesg_{i}_cont_inner_col_txt_cont_ai_sug"
                                                                                                    ),
                                                                                                    padding=EdgeInsets.symmetric(
                                                                                                        horizontal=12,
                                                                                                        vertical=8,
                                                                                                    ),
                                                                                                    child=Text(
                                                                                                        data="Ai Suggestions".upper(),
                                                                                                        key=Key(
                                                                                                            f"{self.base_key}_chat_container_mesg_{i}_cont_inner_col_txt_ai_sug_txt"
                                                                                                        ),
                                                                                                        style=TextStyle(
                                                                                                            fontSize='14px',
                                                                                                            fontFamily="Ubuntu mono",
                                                                                                            color=Colors.onBackground,
                                                                                                        ),
                                                                                                    ),
                                                                                                ),
                                                                                                Divider(
                                                                                                    key=Key(
                                                                                                        f"{self.base_key}_chat_container_mesg_{i}_cont_inner_col_divider"
                                                                                                    ),
                                                                                                    color=Colors.adaptive(
                                                                                                        dark="#5a5a5a",
                                                                                                        light="#d3d3d3",
                                                                                                    ),
                                                                                                    thickness=1,
                                                                                                    indent=16,
                                                                                                    endIndent=16,
                                                                                                ),
                                                                                                Container(
                                                                                                    key=Key(
                                                                                                        f"{self.base_key}_chat_container_mesg_{i}_cont_inner_col_txt_cont_ai_sug_content"
                                                                                                    ),
                                                                                                    padding=EdgeInsets.symmetric(
                                                                                                        horizontal=12,
                                                                                                        vertical=8,
                                                                                                    ),
                                                                                                    decoration=BoxDecoration(
                                                                                                        color=Colors.adaptive(
                                                                                                            light=Colors.hex(
                                                                                                                "#e9ecef"
                                                                                                            ),
                                                                                                            dark=Colors.hex(
                                                                                                                "#4c4c4c"
                                                                                                            ),
                                                                                                        )
                                                                                                    ),
                                                                                                    child=Container(
                                                                                                        key=Key(
                                                                                                            f"{self.base_key}_chat_container_mesg_{i}_cont_inner_col_txt_cont_ai_sug_content_cont_border"
                                                                                                        ),
                                                                                                        padding=EdgeInsets.symmetric(
                                                                                                            horizontal=10,
                                                                                                            vertical=2,
                                                                                                        ),
                                                                                                        decoration=BoxDecoration(
                                                                                                            border=Border(
                                                                                                                left=BorderSide(
                                                                                                                    color=Colors.primary,
                                                                                                                    width=2,
                                                                                                                )
                                                                                                            ),
                                                                                                        ),
                                                                                                        child=MarkdownRender(
                                                                                                            key=Key(
                                                                                                                f"{self.base_key}_chat_container_mesg_{i}_cont_inner_col_txt_ai_sug_txt_content_markdown_render"
                                                                                                            ),
                                                                                                            markdownText=f'# Ai Suggestions...\nHello',
                                                                                                            style=RendererStyle(
                                                                                                                fontSize='12px',
                                                                                                                fontStyle="italic",
                                                                                                                fontColor=Colors.onBackground,
                                                                                                                padding='0px',
                                                                                                                contentMargin='0em',
                                                                                                            )
                                                                                                        ),
                                                                                                    ),
                                                                                                ),
                                                                                                Divider(
                                                                                                    key=Key(
                                                                                                        f"{self.base_key}_chat_container_mesg_{i}_cont_inner_col_divider_2"
                                                                                                    ),
                                                                                                    color=Colors.adaptive(
                                                                                                        dark="#5a5a5a",
                                                                                                        light="#d3d3d3",
                                                                                                    ),
                                                                                                    thickness=1,
                                                                                                    indent=16,
                                                                                                    endIndent=16,
                                                                                                ),
                                                                                                Container(
                                                                                                    key=Key(
                                                                                                        f"{self.base_key}_chat_container_mesg_{i}_cont_inner_col_txt_cont_ai_sug_actions"
                                                                                                    ),
                                                                                                    padding=EdgeInsets.symmetric(
                                                                                                        horizontal=12,
                                                                                                        vertical=8,
                                                                                                    ),
                                                                                                    child=Row(
                                                                                                        key=Key(
                                                                                                            f"{self.base_key}_chat_container_mesg_{i}_cont_inner_col_txt_cont_ai_sug_actions_row"
                                                                                                        ),
                                                                                                        mainAxisAlignment=MainAxisAlignment.SPACE_BETWEEN,
                                                                                                        children=[
                                                                                                            ElevatedButton(
                                                                                                                key=Key(
                                                                                                                    f"{self.base_key}_chat_container_mesg_{i}_cont_inner_col_txt_cont_ai_sug_actions_btn_1"
                                                                                                                ),
                                                                                                                child=Text(
                                                                                                                    data="Discard",
                                                                                                                    key=Key(
                                                                                                                        f"{self.base_key}_chat_container_mesg_{i}_cont_inner_col_txt_cont_ai_sug_actions_btn_1_txt"
                                                                                                                    ),
                                                                                                                ),
                                                                                                                style=ButtonStyle(
                                                                                                                    textStyle=TextStyle(
                                                                                                                        fontSize=12,
                                                                                                                        fontFamily="ubuntu",
                                                                                                                        fontWeight="light",
                                                                                                                        color=Colors.error,
                                                                                                                    ),
                                                                                                                    shape=BorderRadius.all(
                                                                                                                        8
                                                                                                                    ),
                                                                                                                    side=BorderSide(
                                                                                                                        width=1,
                                                                                                                        color=Colors.error,
                                                                                                                    ),
                                                                                                                    backgroundColor=Colors.transparent,
                                                                                                                    elevation=0,
                                                                                                                ),
                                                                                                            ),
                                                                                                            ElevatedButton(
                                                                                                                key=Key(
                                                                                                                    f"{self.base_key}_chat_container_mesg_{i}_cont_inner_col_txt_cont_ai_sug_actions_btn_2"
                                                                                                                ),
                                                                                                                child=Text(
                                                                                                                    data="Preview",
                                                                                                                    key=Key(
                                                                                                                        f"{self.base_key}_chat_container_mesg_{i}_cont_inner_col_txt_cont_ai_sug_actions_btn_2_txt"
                                                                                                                    ),
                                                                                                                ),
                                                                                                                style=ButtonStyle(
                                                                                                                    textStyle=TextStyle(
                                                                                                                        fontSize=12,
                                                                                                                        fontFamily="ubuntu",
                                                                                                                        fontWeight="light",
                                                                                                                        color=Colors.primary,
                                                                                                                    ),
                                                                                                                    shape=BorderRadius.all(
                                                                                                                        8
                                                                                                                    ),
                                                                                                                    side=BorderSide(
                                                                                                                        width=1,
                                                                                                                        color=Colors.primary,
                                                                                                                    ),
                                                                                                                    backgroundColor=Colors.transparent,
                                                                                                                    elevation=0,
                                                                                                                ),
                                                                                                            ),
                                                                                                            ElevatedButton(
                                                                                                                key=Key(
                                                                                                                    f"{self.base_key}_chat_container_mesg_{i}_cont_inner_col_txt_cont_ai_sug_actions_btn_3"
                                                                                                                ),
                                                                                                                child=Text(
                                                                                                                    data="Accept Changes",
                                                                                                                    key=Key(
                                                                                                                        f"{self.base_key}_chat_container_mesg_{i}_cont_inner_col_txt_cont_ai_sug_actions_btn_3_txt"
                                                                                                                    ),
                                                                                                                ),
                                                                                                                style=ButtonStyle(
                                                                                                                    textStyle=TextStyle(
                                                                                                                        fontSize=12,
                                                                                                                        fontFamily="ubuntu",
                                                                                                                        fontWeight="light",
                                                                                                                        color=Colors.onPrimary,
                                                                                                                    ),
                                                                                                                    shape=BorderRadius.all(
                                                                                                                        8
                                                                                                                    ),
                                                                                                                    backgroundColor=Colors.primary,
                                                                                                                ),
                                                                                                            ),
                                                                                                        ],
                                                                                                    ),
                                                                                                ),
                                                                                            ],
                                                                                        ),
                                                                                    ),
                                                                                ],
                                                                            ),
                                                                        )
                                                                        if i % 2 == 0
                                                                        else Text(
                                                                            key=Key(
                                                                                f"{self.base_key}_chat_container_mesg_{i}_txt"
                                                                            ),
                                                                            data=f"Hello {i}"
                                                                            * 10,
                                                                            style=TextStyle(
                                                                                fontSize=14,
                                                                                color=Colors.onBackground,
                                                                            ),
                                                                        )
                                                                    ),
                                                                )
                                                            ],
                                                        )
                                                        for i in range(50)
                                                    ],
                                                ),
                                            ),
                                            decoration=BoxDecoration(
                                                borderRadius=BorderRadius.only(
                                                    topLeft=8,
                                                    topRight=8,
                                                )
                                            ),
                                        ),
                                        SizedBox(
                                            key=Key(
                                                f"{self.base_key}_chat_container_text_field_margin"
                                            ),
                                            height=4,
                                        ),
                                        TextField(
                                            key=Key(
                                                f"{self.base_key}_chat_container_text_field"
                                            ),
                                            controller=self.text_controller,
                                            trailing=IconButton(
                                                icon=Icon(
                                                    Icons.send_rounded,
                                                    key=Key(
                                                        f"{self.base_key}_icon_senf_bt_ico"
                                                    ),
                                                ),
                                                key=Key(
                                                    f"{self.base_key}_icon_senf_bt"
                                                ),
                                                onPressed=self.send,
                                                style=ButtonStyle(
                                                    backgroundColor=Colors.primary,
                                                    foregroundColor=Colors.onPrimary,
                                                    hoverColor=Colors.hex("#9688b9"),
                                                ),
                                            ),
                                            decoration=InputDecoration(
                                                hintText="Ask anything...",
                                                fillColor=Colors.surfaceVariant,
                                                labelColor=Colors.onSurfaceVariant,
                                                focusColor=Colors.primary,
                                                borderRadius=BorderRadius.all(28),
                                                border=BorderSide(
                                                    width=2,
                                                    color=Colors.transparent,
                                                ),
                                                focusedBorder=BorderSide(
                                                    width=2,
                                                    color=Colors.transparent,
                                                ),
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
                                                    # color=Colors.red,
                                                ),
                                                filled=True,
                                            ),
                                        ),
                                        SizedBox(
                                            key=Key(
                                                f"{self.base_key}_chat_container_text_field_margin_be_careful"
                                            ),
                                            height=8,
                                        ),
                                        Text(
                                            key=Key(f"{self.base_key}_be_careful"),
                                            data="Becareful Ai can make mistakes.",
                                            style=TextStyle(
                                                fontSize=10,
                                                color=Colors.onBackground,
                                            ),
                                        ),
                                        SizedBox(
                                            key=Key(
                                                f"{self.base_key}_chat_container_text_field_margin_be_careful_end"
                                            ),
                                            height=8,
                                        ),
                                    ],
                                ),
                            ),
                        )
                        if self.open
                        else Container()
                    ),
                    # Positioned(
                    #     key=Key(f"{self.base_key}_posit"),
                    #     height="600px",
                    #     width="600px",
                    #     top="4px",
                    #     left="502px",
                    #     child=IconButton(
                    #         icon=Icon(
                    #             (
                    #                 Icons.close_rounded
                    #                 if self.open
                    #                 else Icons.chat_rounded
                    #             ),
                    #             key=Key(f"{self.base_key}_icon_bt_pos"),
                    #         ),
                    #         key=Key(f"{self.base_key}_icon_bt"),
                    #         onPressed=self._open,
                    #     ),
                    # ),
                ],
            ),
        )


class ChatCard(StatefulWidget):
    def __init__(
        self,
        context=None,
        key=None,
    ):
        self.context = context
        super().__init__(key)

    def createState(self) -> ChatCardState:
        return ChatCardState()
