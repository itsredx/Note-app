# constants.theme.py
import darkdetect

class ThemeManager:
    def __init__(self):
        self.dark_mode = darkdetect.isDark()
        self.show_font = True

    def toggle(self):
        self.dark_mode = not self.dark_mode

    def toggle_font(self):
        self.show_font = not self.show_font

# Create a single instance that your whole app will use
theme = ThemeManager()