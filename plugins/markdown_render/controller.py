from typing import Optional

class MarkdownRendererController:
    """
    Controller to programmatically update the markdown text shown by MarkdownRender.
    """
    def __init__(self):
        self._state = None
        self._content = ""
        
    def _attach(self, state):
        self._state = state
        
    def _detach(self):
        self._state = None
        
    def set_markdown(self, markdownText: str):
        """Updates the markdown without requiring a full react-style reconciliation."""
        self._content = markdownText
        if self._state:
            self._state.set_markdown(markdownText)
            
    def get_markdown(self) -> str:
        """Returns the current markdown text."""
        return self._content
