"""Custom button widget with hover effects."""

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

class HoverButton(QPushButton):
    """Button with dynamic hover effects and cursor changes."""
    
    def __init__(self, text: str = "", base_color: str = "#3498db", text_color: str = "#ffffff", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self._base_color = QColor(base_color)
        self._text_color = text_color
        self._custom_padding = "8px 16px"
        self._custom_font_weight = "bold"
        self._update_style()
        
    def set_colors(self, base_color: str, text_color: str = "#ffffff"):
        self._base_color = QColor(base_color)
        self._text_color = text_color
        self._update_style()
        
    def set_padding(self, padding: str):
        self._custom_padding = padding
        self._update_style()
        
    def set_font_weight(self, weight: str):
        self._custom_font_weight = weight
        self._update_style()

    def _update_style(self):
        hover_color = self._base_color.darker(115).name()
        pressed_color = self._base_color.darker(130).name()
        
        style = f"""
        HoverButton {{
            background-color: {self._base_color.name()};
            color: {self._text_color};
            border: none;
            border-radius: 6px;
            padding: {self._custom_padding};
            font-weight: {self._custom_font_weight};
        }}
        HoverButton:hover {{
            background-color: {hover_color};
        }}
        HoverButton:pressed {{
            background-color: {pressed_color};
        }}
        HoverButton:disabled {{
            background-color: #e0e0e0;
            color: #a0a0a0;
        }}
        """
        self.setStyleSheet(style)
