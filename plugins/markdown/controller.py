# plugins/markdown/controller.py
from typing import Optional, Callable, List, Dict, Any
import json

class EditorCursorState:
    """A dataclass to hold the formatting state at the cursor's position."""

    def __init__(self, data: Dict[str, Any]):
        print("Data: ", data)
        self.is_bold = data.get('isBold', False)
        self.is_italic = data.get('isItalic', False)
        self.is_underline = data.get('isUnderline', False)
        self.is_strike_through = data.get('isStrikeThrough', False)
        self.is_ul = data.get('isUnorderedList', False)
        self.is_ol = data.get('isOrderedList', False)
            
        # Clean up font names that might have quotes
        font_name = data.get('fontName', '')
        self.font_name = font_name.strip('"') if font_name else ''
        
        self.font_color = data.get('fontColor', '') # e.g., 'rgb(255, 0, 0)'
        self.block_format = data.get('blockFormat', 'p') # e.g., 'h1', 'p'

        # --- NEW: Selection State ---
        self.has_selection = data.get('hasSelection', False)
        self.selection_rect = data.get('selectionRect', None)

    def __repr__(self):
        return f"<EditorCursorState bold={self.is_bold}, font={self.font_name}, color={self.font_color}, selection={self.has_selection}>"

  

class MarkdownEditorController:
    """
    Controller exposed to plugin consumers to interact with the editor.
    Provides a clean, Pythonic API for executing rich text commands.

    IMPORTANT USAGE NOTE ON `setState()`:
    This controller manages two types of operations:
    
    1. Direct UI Commands (e.g., `bold()`, `set_font_color()`): These commands
       are sent to the browser, which updates the UI immediately. The browser
       then notifies Python of the change via its `onChange` event. You
       **MUST NOT** call `setState()` in your application after calling these
       methods, as it will cause a race condition and unexpected behavior.

    2. State-Modifying Commands (e.g., `load_from_markdown()`): These methods
       change the editor's content from the Python side. They handle their
       own internal state updates and will trigger a rebuild when `setState()`
        is called. You **SHOULD** call `setState()` after these methods.
    """
    
    def __init__(self, initial_content: str = ""):
        self.content = initial_content
        self._listeners: List[Callable] = []
        self._state_ref = None
        # --- NEW: Store the cursor state ---
        self.cursor_state = EditorCursorState({})
        self.new_state_data = None

    def run_javascript(self, js: str):
        """Run arbitrary JavaScript in the editor."""
        if self._state_ref:
             self._state_ref.run_javascript(js)

    def hide_overlay(self):
        """Hides the AI controls overlay."""
        self.run_javascript("window.hidePythraSelectionOverlay()")

    def add_listener(self, listener: Callable):
        """Subscribe to notifications from this controller."""
        if listener not in self._listeners:
            self._listeners.append(listener)

    def remove_listener(self, listener: Callable):
        """Unsubscribe from notifications."""
        if listener in self._listeners:
            self._listeners.remove(listener)

    def _notify_listeners(self, cursor_state_json: Optional[str] = None):
        """
        Call all subscribed listeners. Now passes the cursor state JSON
        if it's available.
        """
        for listener in self._listeners:
            # Pass the cursor state if this was a cursor update, otherwise pass None
            listener(cursor_state_json=cursor_state_json)
        # self.focus()

    def _attach(self, state):
        self._state_ref = state

    def _detach(self):
        self._state_ref = None

    def _update_content_from_js(self, new_content: str):
        """Internal method called by the editor's state when JS reports a change."""
        if self.content != new_content:
            self.content = new_content
            # Notify listeners that the content has changed, but a rebuild isn't
            # strictly necessary since the UI is already in sync. This is for
            # other widgets that might depend on the content.
            self._notify_listeners()

    # --- NEW: Method to receive cursor state updates from JS ---
    def _update_cursor_state_from_js(self, state_json: str):
        """
        Internal method that receives the raw cursor state JSON from JS
        and passes it up to listeners.
        """
        try:
            # --- THE FIX ---
            # 1. Parse the JSON to create the rich state object.
            new_state_data = json.loads(state_json)
            self.cursor_state = EditorCursorState(new_state_data)
            
            # 2. Notify listeners, passing the raw JSON string for comparison.
            self._notify_listeners(state_json)
        except json.JSONDecodeError:
            print("Warning: Could not decode cursor state from JS.")

    def get_content(self) -> str:
        """Gets the current HTML content from the controller."""
        return self.content

    def exec_command(self, command: str, value: Optional[str] = None):
        """
        The low-level method to send any command to the browser's editor.
        This directly mutates the DOM in the browser.

        **WARNING:** `setState()` should **ABSOLUTELY NOT** be called after this
        method. The browser's `onChange` event will handle state synchronization.
        Prefer using the higher-level convenience methods like `bold()`.
        """
        if self._state_ref:
            self._state_ref.exec_command(command, value)

    def _restore_selection_and_exec(self, command: str, value: Optional[str] = None):
        """
        A helper method that chains the restore, focus, and exec commands
        to ensure the operation is atomic and targets the correct selection.
        """
        if self._state_ref:
            self._state_ref.restore_selection_and_exec(command, value)

    def set_content(self, html: str):
        if self._state_ref:
            self._state_ref.set_content(html)

    # def get_content(self) -> Optional[str]:
    #     """
    #     Gets the current HTML content from the editor's Python state.
    #     This is a read-only operation and does not affect the UI.
    #     `setState()` is not relevant here.
    #     """
    #     if self._state_ref:
    #         return self._state_ref.get_content()
    #     return None

    def focus(self):
        """
        Sets the focus back to the editor's text area. This is a direct UI
        command that does not change any state.

        **NOTE:** `setState()` should **NOT** be called after this method.
        """
        if self._state_ref:
            self._state_ref.focus()

    # --- NEW: CONVENIENCE WRAPPER METHODS ---

    # --- Text Style Toggles ---
    def bold(self):
        """
        Toggles bold on the selected text. This is a direct UI command.

        **WARNING:** `setState()` should **ABSOLUTELY NOT** be called after this
        method. The editor's `onChange` event handles state synchronization.
        """
        self.exec_command('bold')
        

    def italic(self):
        """
        Toggles italic on the selected text. This is a direct UI command.

        **WARNING:** `setState()` should **ABSOLUTELY NOT** be called after this
        method. The editor's `onChange` event handles state synchronization.
        """
        self.exec_command('italic')
        

    def underline(self):
        """
        Toggles underline on the selected text. This is a direct UI command.

        **WARNING:** `setState()` should **ABSOLUTELY NOT** be called after this
        method. The editor's `onChange` event handles state synchronization.
        """
        self.exec_command('underline')
        

    def strike_through(self):
        """
        Toggles strikethrough on the selected text. This is a direct UI command.

        **WARNING:** `setState()` should **ABSOLUTELY NOT** be called after this
        method. The editor's `onChange` event handles state synchronization.
        """
        self.exec_command('strikeThrough')
        

    # --- Block Formatting ---
    def set_heading(self, level: int):
        """
        Changes the current block to a heading. This is a direct UI command.

        **WARNING:** `setState()` should **ABSOLUTELY NOT** be called after this
        method. The editor's `onChange` event handles state synchronization.
        :param level: An integer from 1 to 6.
        """
        if 1 <= level <= 6:
            self.exec_command('formatBlock', f'H{level}')
            
        else:
            print(f"Warning: Heading level must be between 1 and 6, but got {level}.")

    def set_paragraph(self):
        """
        Changes the current block to a normal paragraph. This is a direct UI command.
        
        **WARNING:** `setState()` should **ABSOLUTELY NOT** be called after this
        method. The editor's `onChange` event handles state synchronization.
        """
        self.exec_command('formatBlock', 'P')
        
        
    def insert_unordered_list(self):
        """
        Toggles a bulleted list. This is a direct UI command.

        **WARNING:** `setState()` should **ABSOLUTELY NOT** be called after this
        method. The editor's `onChange` event handles state synchronization.
        """
        self.exec_command('insertUnorderedList')
        

    def insert_ordered_list(self):
        """
        Toggles a numbered list. This is a direct UI command.

        **WARNING:** `setState()` should **ABSOLUTELY NOT** be called after this
        method. The editor's `onChange` event handles state synchronization.
        """
        self.exec_command('insertOrderedList')
        

    # --- Value-Based Commands ---
    def set_font_color(self, color: str):
        """
        Changes the font color of the selected text. This is a direct UI command.

        **WARNING:** `setState()` should **ABSOLUTELY NOT** be called after this
        method. The editor's `onChange` event handles state synchronization.
        :param color: A CSS color string (e.g., '#FF0000', 'red').
        """
        self.exec_command('foreColor', color)
        
        
    def set_font_name(self, font_family: str):
        """
        Changes the font of the selected text. This is a direct UI command.

        **WARNING:** `setState()` should **ABSOLUTELY NOT** be called after this
        method. The editor's `onChange` event handles state synchronization.
        :param font_family: A font family string (e.g., 'Arial', 'Verdana').
        """
        
        self._restore_selection_and_exec('fontName', font_family)
        
        
    def insert_image(self, url: str):
        """
        Inserts an image at the current cursor position. This is a direct UI command.

        **WARNING:** `setState()` should **ABSOLUTELY NOT** be called after this
        method. The editor's `onChange` event handles state synchronization.
        :param url: The URL of the image to insert.
        """
        self.exec_command('insertImage', url)
        

     # --- NEW: Markdown Import/Export Methods ---

    def load_from_markdown(self, markdown_text: str):
        """
        Imports and renders Markdown content into the editor, converting it to rich HTML.
        This is a state-modifying operation that transforms the editor's content.

        This method:
        1. Parses the provided Markdown text
        2. Converts it to semantic HTML with proper formatting
        3. Updates the internal editor state
        4. Triggers a UI rebuild to reflect the changes

        Example usage:
            editor.load_from_markdown("# Hello\n\nThis is **bold** text")
            editor.setState()  # Required to apply changes

        **IMPORTANT:** You MUST call `setState()` after this method to apply the changes.
        This ensures proper synchronization between Python state and UI rendering.

        :param markdown_text: Raw Markdown content to parse and render (e.g., "# Heading\n\nParagraph")
        :raises ValueError: If markdown_text is None or not a valid string
        """
        if self._state_ref:
            self._state_ref.load_from_markdown(markdown_text)

    def replace_selection_with_markdown(self, markdown_text: str):
        """
        Replaces the currently selected text in the editor with content
        converted from the provided Markdown text.

        This method:
        1. Parses the provided Markdown text
        2. Converts it to semantic HTML with proper formatting
        3. Replaces the current selection in the editor with the new HTML
        4. Updates the internal editor state

        Example usage:
            editor.replace_selection_with_markdown("**Bold Text**")
            editor.setState()  # Required to apply changes
            """
        if self._state_ref:
            self._state_ref.replace_selection_with_markdown(markdown_text)

    def export_to_markdown(self) -> Optional[str]:
        """
        Gets the current editor content and converts it to Markdown.
        This is a read-only operation. `setState()` is not relevant here.
        """
        if self._state_ref:
            return self._state_ref.export_to_markdown()
        return None
