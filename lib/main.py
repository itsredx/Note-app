# main.py
import os
import sys
import json
from typing import Optional, Callable, List, Dict, Any

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# import colors
from constants.colors import *
from constants.theme import theme

from screens.note_editor_screen import NoteEditorScreen
from screens.dashboard_screen import DashboardScreen


# Welcome to your new Pythra App!
from pythra import (
    Framework,
    StatefulWidget,
    State,
    Key,
    Widget,
    Container,
    Navigator, 
    PageRoute,
)


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
        return Container(
            key=Key("home_page_Pythra_wrapper_container"),
            height="100vh",
            width="100vw",
            child=Navigator(
                key=Key("app_navigator"),
                # The builder lambda now receives the navigator state
                initialRoute=PageRoute(
                    builder=lambda navigator: DashboardScreen(
                        navigator=navigator, key=Key("my_app_root")
                    )
                ),
                routes={
                    "/settings": lambda navigator: NoteEditorScreen(
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
        self.home_page = HomePage(key=Key("home_page"),)

    def build(self):
        return self.home_page


class Main(StatefulWidget):
    def createState(self) -> MainState:
        return MainState()


if __name__ == "__main__":
    # This allows running the app directly with `python lib/main.py`
    # as well as with the CLI's `pythra run` command.
    app = Framework.instance()
    app.set_root(Main(key=Key("home_page_wrapper")))
    app.run()
