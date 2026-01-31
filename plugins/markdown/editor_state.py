# plugins/markdown/editor_state.py`
import os
import json
from typing import Optional, Dict, Any

import markdown
from markdownify import markdownify as md

from pythra import State, Container, Key, Framework

from .controller import MarkdownEditorController
from .style import EditorStyle

framework = Framework.instance()  # Placeholder for the framework reference
class MarkdownEditorState(State):
    def __init__(self):
        super().__init__()
        # --- MODIFICATION: Start with None to indicate it's not yet initialized ---
        self._content: Optional[str] = None
        self._callback_name = None
        self._container_html_id = 'fw_id_8'  # Will store the actual framework-assigned ID

        # --- NEW: State variable for toolbar visibility ---
        self._controls_visible = True # Default to visible
        self._toggle_controls_callback_name = None
        self._state_change_callback_name = None
        
        self._cached_js_init = None
       
    
    def _get_html_id_for_key(self, key: Key) -> str:
        """
        Get the framework-assigned HTML ID for a widget with given key.
        Returns None if not found in the render map.
        """
        if not framework or not framework.reconciler:
            return None
            
        # Get the main context map which contains all rendered widgets
        context_map = framework.reconciler.get_map_for_context("main")
        
        # Find the entry with matching key
        for node_data in context_map.values():
            if node_data.get("key") == key:
                return node_data.get("html_id")
        return None

    def initState(self):
        widget = self.get_widget()
        if not widget:
            return

        # --- MODIFICATION: Set initial content from the widget, but only once ---
        # if self._content is None:
        #     self._content = widget.initial_content if hasattr(widget, 'initial_content') else ""

        # Attach controller
        if widget.controller:
            widget.controller._attach(self)

        print("widget.controller.get_content(): ", widget.controller.get_content())

        # Register a callback for content-change events coming from JS
        self._callback_name = f"markdown_content_change_{widget.key.value}"

        # --- NEW: Register the toggle controls callback ---
        self._toggle_controls_callback_name = f"markdown_toggle_controls_{widget.key.value}"
        self._state_change_callback_name = f"markdown_state_change_{widget.key.value}"
        
        # Register our callbacks with the framework's API
        if framework and hasattr(framework, 'api') and framework.api:
            framework.api.register_callback(self._callback_name, self._handle_content_change)
            framework.api.register_callback('markdown_content_change_markdown_default', self._handle_content_change)
            framework.api.register_callback(self._toggle_controls_callback_name, self._handle_toggle_controls) # Register the new handler
            framework.api.register_callback(self._state_change_callback_name, self._handle_cursor_state_update)
        else:
            print('Warning: framework.api not available; callback registration delayed')


    def dispose(self):
        widget = self.get_widget()
        if widget and widget.controller:
            widget.controller._detach()
        super().dispose()

    # Controller-facing methods called by MarkdownEditorController
    def exec_command(self, command: str, value: Optional[str] = None):
        """Ask the frontend to execute a command (e.g., bold, italic)."""
        if not framework or not framework.window:
            return

        # Get the unique instance name for our component
        instance_name = f"{self.get_widget().key.value}_PythraMarkdownEditor"

        # Safely escape the command and value for JS
        command_js = json.dumps(command)

        # Execute command using the known framework-assigned ID
        val_js = json.dumps(value) if value is not None else 'null'
        print(val_js)
        
        js = f"""
            (function(){{
                const editorInstance = window._pythra_instances['{instance_name}'];
                if (editorInstance && typeof editorInstance.execCommand === 'function') {{
                    editorInstance.execCommand({command_js}, {val_js});
                }} else {{
                    console.error("Could not find editor instance '{instance_name}' to execute command.");
                }}
            }})()
        """

        """ old logic
            (function(){{
                var editable = document.querySelector('.editor-inner-container');
                if(editable) {{
                    try {{
                        document.execCommand('{command}', false, {val_js});
                        console.log('Executing command: ', '{command}', false, {val_js});
                    }} catch(e) {{
                        console.warn('Editor command failed:', e);
                    }}
                }}
            }})()
        """
        window_id = getattr(self, '_window_id', framework.id)
        framework.window.evaluate_js(window_id, js)

    # --- ADD THIS NEW METHOD ---
    def run_javascript(self, js: str):
        """Run arbitrary JavaScript in the context of this widget."""
        if hasattr(self, '_window_id') and framework and framework.window:
            framework.window.evaluate_js(self._window_id, js)
        elif framework and framework.window:
            framework.window.evaluate_js(framework.id, js)

    def restore_selection_and_exec(self, command: str, value: Optional[str] = None):
        if not framework or not framework.window:
            return

        instance_name = f"{self.get_widget().key.value}_PythraMarkdownEditor"
        command_js = json.dumps(command)
        val_js = json.dumps(value) if value is not None else 'null'

        js = f"""
            (function(){{
                if (typeof restoreEditorSelection === 'function') {{
                    restoreEditorSelection();
                }}
                const editorInstance = window._pythra_instances['{instance_name}'];
                if (editorInstance) {{
                    editorInstance.execCommand({command_js}, {val_js});
                }}
            }})()
        """
        
        window_id = getattr(self, '_window_id', framework.id)
        framework.window.evaluate_js(window_id, js)

    def set_content(self, html: str):
        if not self._container_html_id or not framework or not framework.window:
            return

        widget = self.get_widget()
        if not widget:
            return
            
        html_js = json.dumps(html)
        container_id = self._container_html_id
        
        js = f"""
            (function(){{
                console.log('Setting editor content');
                    var editable = document.querySelector('.editor-inner-container');
                    if(editable) editable.innerHTML = {html_js};
            }})()
        """
        window_id = getattr(self, '_window_id', framework.id)
        framework.window.evaluate_js(window_id, js)
        widget.controller.content = html

    def get_content(self) -> str:
        widget = self.get_widget()
        if not widget:
            return
        return widget.controller.get_content()


    def focus(self):
        js = "(function(){var ed=document.getElementById('editor'); if(ed) ed.focus(); })()"
        if hasattr(self, '_window_id'):
            framework.window.evaluate_js(self._window_id, js)
        else:
            framework.window.evaluate_js(framework.id, js)

    # API callback invoked from JS when content changes
    def _handle_content_change(self, new_content):
        widget = self.get_widget()
        if not widget:
            return
        try:
            widget.controller.content = new_content
            print("New Content: ", new_content)
        except Exception:
            pass

    def _handle_cursor_state_update(self, state_json: str):
        """
        Internal method to handle cursor state updates from JS.
        It updates the controller and also calls the new JS function to sync external UI.
        """
        # This part updates the Python controller (which is correct)
        widget = self.get_widget()
        if widget and widget.controller:
            widget.controller._update_cursor_state_from_js(state_json)

        # --- NEW LOGIC ---
        # Now, send a command back to JS to update the external toolbar.
        # We pass the raw JSON string directly to the new JS function.
        js_command = f"if (typeof syncExternalToolbarState === 'function') {{ syncExternalToolbarState({state_json}); }}"
        
        window_id = getattr(self, '_window_id', framework.id)
        framework.window.evaluate_js(window_id, js_command)

    # --- NEW: Handler for the toggle event from JavaScript ---
    def _handle_toggle_controls(self, is_visible: bool):
        """Called by JS when the user clicks the Hide/Show Controls button."""
        print(f"Controls visibility changed to: {is_visible}")
        self._controls_visible = is_visible
        # We don't call setState() here because no other part of the UI needs to know.
        # The change is purely internal to this component's state.

     # --- NEW: Implement the core logic for Markdown conversion ---

    def load_from_markdown(self, markdown_text: str):
        """
        Converts Markdown to HTML using the 'markdown' library and updates the editor.
        """
        widget = self.get_widget()
        if not widget:
            return
        # 1. Convert the Markdown to HTML.
        html_content = markdown.markdown(markdown_text, extensions=['fenced_code', 'tables'])
        
        # 2. Update the state's source of truth.
        widget.controller.content = html_content
        self.set_content(widget.controller.content)
        
        # 3. Tell the framework that this state has changed and a rebuild is needed.
        # print("Loading HTML content into editor: ", widget.controller.content)
        # self.setState()

    def export_to_markdown(self) -> Optional[str]:
        """
        Converts the editor's current HTML content to Markdown using 'markdownify'.
        """
        # Get the current, up-to-the-second content from our state.
        html_content = self.get_content()
        if html_content:
            # The 'heading_style="ATX"' option creates clean '#' style headings.
            markdown_text = md(html_content, heading_style="ATX")
            return markdown_text
        return None

    def build(self):
        widget = self.get_widget()
        if not widget:
            return Container(width=0, height=0)

        print("widget.controller.get_content(): ", widget.controller.get_content())

        style = widget.style if widget.style else EditorStyle() # Use default style if none provided
            
        if self._content is None:
             self._content = widget.controller.get_content()

        # --- FIX: Memoize js_init to prevent destruction on setState ---
        if self._cached_js_init is None:
            self._cached_js_init = {
                "engine": "PythraMarkdownEditor",
                "instance_name": f"{widget.key.value}_PythraMarkdownEditor",
                "options": {
                    'callback': self._callback_name,
                    'instanceId': f"{widget.key.value}_PythraMarkdownEditor",
                    "showControls": widget.show_controls,
                    # USE STABLE CONTENT
                    "initialContent": self._content,
                    "width": widget.width,
                    "height": widget.height,
                    "showGrid": widget.show_grid, 
                    "style": style.to_dict(),  
                    "onStateChangeCallback": self._state_change_callback_name,
                },
            }

        editor_container = Container(
            key=widget.key,
            width=widget.width,
            height=widget.height,
            js_init=self._cached_js_init,
        )

        if widget.overlay:
            from pythra import Stack, Positioned
            # Create a separate, stable container for the overlay that JS can move
            overlay_container = Container(
                key=Key(f"{widget.key.value}_overlay_wrapper"),
                # Key for the JS engine to find it
                js_init={
                    "engine": "PythraSelectionOverlay", 
                    "instance_name": f"{widget.key.value}_overlay",
                     # No options needed initially; JS will just grab the element
                     "options": {} 
                },
                child=widget.overlay,
                # Start hidden or letting JS handle display
            )
            
            return Stack(
                children=[
                    editor_container,
                    Positioned(
                        left="0", top="-200px",
                        child=overlay_container
                    )
                ]
            )

        return editor_container
