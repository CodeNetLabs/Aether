"""
Aether Browser - Theme Management
Handles light/dark mode and accent color customization
"""

from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import QObject, pyqtSignal
from typing import Dict

class Theme(QObject):
    theme_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self._dark_mode = False
        self._accent_color = QColor(66, 133, 244)  # Default blue
        
    @property
    def dark_mode(self) -> bool:
        return self._dark_mode
    
    @dark_mode.setter
    def dark_mode(self, value: bool):
        self._dark_mode = value
        self.theme_changed.emit()
    
    @property
    def accent_color(self) -> QColor:
        return self._accent_color
    
    @accent_color.setter
    def accent_color(self, color: QColor):
        self._accent_color = color
        self.theme_changed.emit()
    
    def get_colors(self) -> Dict[str, str]:
        """Returns color scheme for current theme"""
        if self._dark_mode:
            return {
                'background': '#1a1a1a',
                'surface': '#222222',
                'surface_elevated': '#2a2a2a',
                'surface_hover': '#333333',
                'text': '#e8e8e8',
                'text_secondary': '#a8a8a8',
                'border': '#3a3a3a',
                'accent': self._accent_color.name(),
                'accent_hover': self._lighten_color(self._accent_color, 1.15).name(),
                'accent_pressed': self._darken_color(self._accent_color, 0.85).name(),
                'tab_active': '#2a2a2a',
                'tab_inactive': '#1a1a1a',
                'tab_hover': '#252525',
                'input_bg': '#2a2a2a',
                'input_border': '#3a3a3a',
                'input_focus': self._accent_color.name(),
                'icon_button_hover': '#333333',
            }
        else:
            return {
                'background': '#f8f9fa',
                'surface': '#ffffff',
                'surface_elevated': '#ffffff',
                'surface_hover': '#f0f0f0',
                'text': '#202124',
                'text_secondary': '#5f6368',
                'border': '#e0e0e0',
                'accent': self._accent_color.name(),
                'accent_hover': self._darken_color(self._accent_color, 0.92).name(),
                'accent_pressed': self._darken_color(self._accent_color, 0.85).name(),
                'tab_active': '#ffffff',
                'tab_inactive': '#f1f3f4',
                'tab_hover': '#e8eaed',
                'input_bg': '#f8f9fa',
                'input_border': '#dadce0',
                'input_focus': self._accent_color.name(),
                'icon_button_hover': '#f0f0f0',
            }
    
    def get_stylesheet(self) -> str:
        """Generate complete stylesheet for the browser"""
        colors = self.get_colors()
        
        return f"""
            * {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            }}
            
            QMainWindow {{
                background-color: {colors['background']};
            }}
            
            QWidget {{
                color: {colors['text']};
            }}
            
            QToolBar {{
                background-color: {colors['surface_elevated']};
                border: none;
                border-bottom: 1px solid {colors['border']};
                spacing: 4px;
                padding: 0px;
            }}
            
            /* Icon Buttons */
            QPushButton[iconButton="true"] {{
                background-color: transparent;
                border: none;
                border-radius: 6px;
                padding: 6px;
            }}
            
            QPushButton[iconButton="true"]:hover {{
                background-color: {colors['icon_button_hover']};
            }}
            
            QPushButton[iconButton="true"]:pressed {{
                background-color: {colors['surface_hover']};
            }}
            
            QPushButton[iconButton="true"]:disabled {{
                opacity: 0.4;
            }}
            
            /* New Tab Button */
            QPushButton[newTabButton="true"] {{
                background-color: transparent;
                border: none;
                border-radius: 6px;
                padding: 4px;
                margin: 2px;
            }}
            
            QPushButton[newTabButton="true"]:hover {{
                background-color: {colors['icon_button_hover']};
            }}
            
            QPushButton[newTabButton="true"]:pressed {{
                background-color: {colors['surface_hover']};
            }}
            
            /* Regular Buttons */
            QPushButton {{
                background-color: {colors['surface']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                padding: 8px 16px;
                color: {colors['text']};
                font-size: 13px;
                font-weight: 500;
            }}
            
            QPushButton:hover {{
                background-color: {colors['surface_hover']};
                border-color: {colors['accent']};
            }}
            
            QPushButton:pressed {{
                background-color: {colors['border']};
            }}
            
            QPushButton:disabled {{
                background-color: {colors['surface']};
                color: {colors['text_secondary']};
                border-color: {colors['border']};
            }}
            
            QPushButton#accent_button {{
                background-color: {colors['accent']};
                color: white;
                border: none;
                font-weight: 600;
            }}
            
            QPushButton#accent_button:hover {{
                background-color: {colors['accent_hover']};
            }}
            
            QPushButton#accent_button:pressed {{
                background-color: {colors['accent_pressed']};
            }}
            
            /* Address Bar */
            QLineEdit {{
                background-color: {colors['input_bg']};
                border: 1px solid {colors['input_border']};
                border-radius: 16px;
                padding: 6px 16px;
                color: {colors['text']};
                font-size: 13px;
                selection-background-color: {colors['accent']};
            }}
            
            QLineEdit:hover {{
                background-color: {colors['surface_elevated']};
                border-color: {colors['text_secondary']};
            }}
            
            QLineEdit:focus {{
                border: 2px solid {colors['input_focus']};
                padding: 5px 15px;
                background-color: {colors['surface_elevated']};
            }}
            
            /* Tabs */
            QTabWidget::pane {{
                border: none;
                background-color: {colors['background']};
                top: 0px;
            }}
            
            QTabBar {{
                background-color: {colors['surface']};
                border-bottom: 1px solid {colors['border']};
            }}
            
            QTabBar::tab {{
                background-color: {colors['tab_inactive']};
                border: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 8px 16px;
                margin-right: 2px;
                margin-top: 4px;
                color: {colors['text_secondary']};
                font-size: 13px;
                min-width: 100px;
                max-width: 220px;
            }}
            
            QTabBar::tab:selected {{
                background-color: {colors['tab_active']};
                color: {colors['text']};
                font-weight: 500;
                border-bottom: 2px solid {colors['accent']};
                padding-bottom: 6px;
            }}
            
            QTabBar::tab:hover {{
                background-color: {colors['tab_hover']};
            }}
            
            QTabBar::close-button {{
                margin-left: 6px;
                subcontrol-position: right;
                border-radius: 3px;
            }}
            
            QTabBar::close-button:hover {{
                background-color: {colors['surface_hover']};
            }}
            
            QTabBar QToolButton {{
                background-color: {colors['surface']};
                border: 1px solid {colors['border']};
                border-radius: 4px;
                padding: 2px;
                margin: 2px;
            }}
            
            QTabBar QToolButton:hover {{
                background-color: {colors['surface_hover']};
            }}
            
            /* Menus */
            QMenu {{
                background-color: {colors['surface_elevated']};
                border: 1px solid {colors['border']};
                border-radius: 10px;
                padding: 6px;
            }}
            
            QMenu::item {{
                padding: 10px 30px 10px 20px;
                border-radius: 6px;
                margin: 2px;
            }}
            
            QMenu::item:selected {{
                background-color: {colors['surface_hover']};
            }}
            
            QMenu::separator {{
                height: 1px;
                background-color: {colors['border']};
                margin: 6px 10px;
            }}
            
            /* Scrollbars */
            QScrollBar:vertical {{
                background-color: transparent;
                width: 12px;
                border-radius: 6px;
                margin: 2px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {colors['border']};
                border-radius: 5px;
                min-height: 30px;
                margin: 2px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: {colors['text_secondary']};
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            
            QScrollBar:horizontal {{
                background-color: transparent;
                height: 12px;
                border-radius: 6px;
                margin: 2px;
            }}
            
            QScrollBar::handle:horizontal {{
                background-color: {colors['border']};
                border-radius: 5px;
                min-width: 30px;
                margin: 2px;
            }}
            
            QScrollBar::handle:horizontal:hover {{
                background-color: {colors['text_secondary']};
            }}
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
            
            /* Dialogs */
            QDialog {{
                background-color: {colors['surface']};
            }}
            
            QGroupBox {{
                border: 1px solid {colors['border']};
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 16px;
                font-weight: 600;
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                color: {colors['text']};
            }}
        """
    
    def _lighten_color(self, color: QColor, factor: float) -> QColor:
        """Lighten a color by a factor"""
        h, s, v, a = color.getHsvF()
        v = min(1.0, v * factor)
        s = max(0.0, s * 0.95)
        result = QColor()
        result.setHsvF(h, s, v, a)
        return result
    
    def _darken_color(self, color: QColor, factor: float) -> QColor:
        """Darken a color by a factor"""
        h, s, v, a = color.getHsvF()
        v = max(0.0, v * factor)
        result = QColor()
        result.setHsvF(h, s, v, a)
        return result
    
    def toggle_dark_mode(self):
        """Toggle between light and dark mode"""
        self.dark_mode = not self.dark_mode
