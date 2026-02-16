from pythra import (
    Widget,
    StatelessWidget,
    Container,
    Column,
    Row,
    Text,
    TextStyle,
    Colors,
    SizedBox,
    BoxDecoration,
    BorderRadius,
    BorderSide,
    EdgeInsets,
    CrossAxisAlignment,
    MainAxisAlignment,
    Divider,
    BoxConstraints,
    Icon,
    Key,
)
from lib.constants.colors import AppColors

class SettingsTile(StatelessWidget):
    def __init__(
        self, 
        title: str, 
        subtitle: str = None, 
        trailing: Widget = None, 
        icon: Widget = None,
        key=None
    ):
        self.title = title
        self.subtitle = subtitle
        self.trailing = trailing
        self.icon = icon
        super().__init__(key=key)

    def build(self):
        children_row = []
        
        # Add Icon if present
        if self.icon:
            children_row.append(self.icon)
            children_row.append(SizedBox(width=12))

        # Title and Subtitle Column
        text_column_children = [
            Text(
                key=Key(f"{self.title}_{self.key}_tile_title"),
                data=self.title,
                style=TextStyle(
                    color=Colors.onSurface,
                    fontFamily="ubuntu",
                    fontSize=14,
                )
            )
        ]
        
        if self.subtitle:
            text_column_children.append(SizedBox(height=4))
            text_column_children.append(
                Text(
                    key=Key(f"{self.title}_{self.key}_tile_subtitle"),
                    data=self.subtitle,
                    style=TextStyle(
                        color=Colors.onSurface,
                        fontFamily="ubuntu",
                        fontSize=11,
                        fontWeight='light'
                    )
                )
            )

        children_row.append(
            Column(
                key=Key(f"{self.title}_{self.key}_tile_text"),
                crossAxisAlignment=CrossAxisAlignment.START,
                children=text_column_children
            ),
        )

        children_row.append(
            SizedBox(
                key=Key(f"{self.title}_{self.key}_tile_padding"),
                height=40,
            )
        )
        
        main_row_children = [
            Row(key=Key(f"{self.title}_{self.key}_tile_row"),children=children_row), # Left side (Icon + Texts)
        ]

        if self.trailing:
            main_row_children.append(self.trailing)

        return Container(
            key=Key(f"{self.title}_{self.key}_tile"),
            padding=EdgeInsets.symmetric(horizontal=12, vertical=8),
            child=Row(
                key=Key(f"{self.title}_{self.key}_tile_main_row"),
                mainAxisAlignment=MainAxisAlignment.SPACE_BETWEEN,
                children=main_row_children
            )
        )

class SettingsCard(StatelessWidget):
    def __init__(self, children: list[Widget], key=None, last_item_margin=0):
        self.children = children
        self.last_item_margin = last_item_margin
        super().__init__(key=key)

    def build(self):
        card_content = []
        for i, child in enumerate(self.children):
            card_content.append(child)
            # Add divider if not the last item
            if i != len(self.children) - 1:
                card_content.append(
                    Divider(
                        key=Key(f"{self.key}_tile_divider_{i}"),
                        color=Colors.adaptive(dark="#5a5a5a", light="#d3d3d3")
                    )
                )

        return Container(
            key=Key(f"{self.key}_card"),
            constraints=BoxConstraints(
                minWidth=400, # Using value from original code
            ),
            width=800,
            margin=EdgeInsets.only(bottom=self.last_item_margin),
            decoration=BoxDecoration(
                color=AppColors.appBackgroundColor,
                borderRadius=BorderRadius.all(20),
                border=BorderSide(width=1, color=Colors.adaptive(dark="#5a5a5a", light="#d3d3d3")),
            ),
            child=Column(
                key=Key(f"{self.key}_card_column"),
                crossAxisAlignment=CrossAxisAlignment.STRETCH,
                children=card_content
            )
        )

class SettingsSection(StatelessWidget):
    def __init__(self, title: str, children: list[Widget], key=None, last_item=False):
        self.title = title
        self.children_widgets = children
        self.last_item = last_item
        super().__init__(key=key)

    def build(self):
        return Container(
            key=Key(f"{self.key}_section"),
            margin=EdgeInsets.only(top=24),
            child=Column(
                key=Key(f"{self.key}_section_column"),
                children=[
                    Row(
                        key=Key(f"{self.key}_section_row"),
                        children=[
                            Text(
                                key=Key(f"{self.key}_section_title"),
                                data=self.title,
                                style=TextStyle(
                                    color=Colors.onSurface,
                                    fontFamily="ubuntu",
                                    fontSize=24,
                                )
                            )
                        ]
                    ),
                    SizedBox(key=Key(f"{self.key}_section_padding"),height=18),
                    SettingsCard(key=Key(f"{self.key}_section_card"),children=self.children_widgets, last_item_margin= 24 if self.last_item else 0)
                ]
            )
        )
