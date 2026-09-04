# main.py
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants.colors import *
from constants.theme import initial_theme

# ── Imports ───────────────────────────────────────────────────────────
from screens.note_editor_screen import NoteEditorScreen
from screens.dashboard_screen import DashboardScreen
from screens.login_screen import LoginScreen

from utils import shared_prefernce


from pythra import (
    Framework,
    StatefulWidget,
    State,
    Key,
    Widget,
    Container,
    Navigator,
    PageRoute,
    ContextMenu,
    MenuItem,
    Icons,
    ContextMenuTheme,
    BorderRadius,
    Colors,
)

# ── Preferences & Theme Setup ─────────────────────────────────────────
pref = shared_prefernce.PythraPreferences()
if pref.get("theme", None) is None:
    print("---- Perf theme is not set ----")
    pref.set("theme", "light")


# ── Home Page & Navigation ────────────────────────────────────────────
class HomePageState(State):
    def __init__(self):
        self.count = 0

    def incrementCounter(self):
        self.count += 1
        print("self.count: ", self.count)
        self.setState()

    def decrementCounter(self):
        self.count -= 1
        print("self.count: ", self.count)
        self.setState()

    def build(self) -> Widget:
        is_logged_in = pref.get("is_logged_in", False)
        initial_builder = (
            (lambda navigator: DashboardScreen(navigator=navigator, key=Key("my_app_root")))
            if is_logged_in
            else (lambda navigator: LoginScreen(navigator=navigator, key=Key("my_login_root")))
        )

        return Container(
            key=Key("home_page_Pythra_wrapper_container"),
            height="100vh",
            width="100vw",
            color=Colors.surface,
            child=Navigator(
                key=Key("app_navigator"),
                initialRoute=PageRoute(
                    builder=initial_builder
                ),
                routes={
                    "/login": lambda navigator: LoginScreen(
                        key=Key("login_page"), navigator=navigator
                    ),
                    "/dashboard": lambda navigator: DashboardScreen(
                        key=Key("dashboard_page"), navigator=navigator
                    ),
                    "/note": lambda navigator: NoteEditorScreen(
                        key=Key("note_page"), navigator=navigator
                    ),
                },
            ),
        )


class HomePage(StatefulWidget):
    def createState(self) -> HomePageState:
        return HomePageState()


class MainState(State):
    def __init__(self):
        self.home_page = HomePage(key=Key("home_page"))

    def on_copy(self):
        print("Copy pressed")

    def on_paste(self):
        print("Paste pressed")

    def on_delete(self):
        print("Delete pressed")

    def build(self):
        return ContextMenu(
                items=[
                    MenuItem(
                        "New Note",
                        icon=Icons.add_circle_outline_rounded,
                        onPressed=self.on_copy,
                    ),
                    MenuItem(
                        "Settings",
                        icon=Icons.settings_account_box_rounded,
                        onPressed=self.on_paste,
                    ),
                    MenuItem(divider=True),
                    MenuItem(
                        "Close App",
                        icon=Icons.delete_outline_rounded,
                        onPressed=self.on_delete,
                    ),
                ],
                child=self.home_page,
                theme=ContextMenuTheme(
                    backgroundColor=Colors.surface,
                    borderColor=Colors.outline,
                    itemTextColor=Colors.onSurface,
                    itemHoverColor=Colors.surfaceVariant,
                    iconSize=20,
                    borderRadius=BorderRadius.all(8),
                    elevation=8,
                ),
            )


class Main(StatefulWidget):
    def createState(self) -> MainState:
        return MainState()


if __name__ == "__main__":
    app = Framework.instance()
    app.set_theme(initial_theme)
    app.set_root(Main(key=Key("home_page_wrapper")))
    app.run()
