"""
Aether Browser - Settings Dialog
Provides UI for changing theme and other settings
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QGroupBox, QColorDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from theme import Theme


class SettingsDialog(QDialog):
    """Settings dialog for browser configuration"""
    
    def __init__(self, theme: Theme, parent=None):
        super().__init__(parent)
        self.theme = theme
        
        self.setWindowTitle("Aether Settings")
        self.setModal(True)
        self.setMinimumSize(500, 400)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup settings UI"""
        layout = QVBoxLayout(self)
        
        # Appearance section
        appearance_group = QGroupBox("Appearance")
        appearance_layout = QVBoxLayout()
        
        # Dark mode toggle
        dark_mode_layout = QHBoxLayout()
        dark_mode_label = QLabel("Dark Mode:")
        self.dark_mode_btn = QPushButton(
            "Enabled" if self.theme.dark_mode else "Disabled"
        )
        self.dark_mode_btn.setCheckable(True)
        self.dark_mode_btn.setChecked(self.theme.dark_mode)
        self.dark_mode_btn.clicked.connect(self._on_dark_mode_toggled)
        dark_mode_layout.addWidget(dark_mode_label)
        dark_mode_layout.addWidget(self.dark_mode_btn)
        dark_mode_layout.addStretch()
        appearance_layout.addLayout(dark_mode_layout)
        
        # Accent color picker
        accent_layout = QHBoxLayout()
        accent_label = QLabel("Accent Color:")
        self.accent_btn = QPushButton("Choose Color")
        self.accent_btn.clicked.connect(self._on_accent_color_clicked)
        
        # Color preview
        self.color_preview = QLabel()
        self.color_preview.setFixedSize(30, 30)
        self._update_color_preview()
        
        accent_layout.addWidget(accent_label)
        accent_layout.addWidget(self.accent_btn)
        accent_layout.addWidget(self.color_preview)
        accent_layout.addStretch()
        appearance_layout.addLayout(accent_layout)
        
        appearance_group.setLayout(appearance_layout)
        layout.addWidget(appearance_group)
        
        # Add stretch to push everything to top
        layout.addStretch()
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
    
    def _on_dark_mode_toggled(self, checked: bool):
        """Handle dark mode toggle"""
        self.theme.dark_mode = checked
        self.dark_mode_btn.setText("Enabled" if checked else "Disabled")
    
    def _on_accent_color_clicked(self):
        """Handle accent color selection"""
        color = QColorDialog.getColor(
            self.theme.accent_color,
            self,
            "Choose Accent Color"
        )
        
        if color.isValid():
            self.theme.accent_color = color
            self._update_color_preview()
    
    def _update_color_preview(self):
        """Update color preview box"""
        color = self.theme.accent_color
        self.color_preview.setStyleSheet(
            f"background-color: {color.name()}; border: 1px solid #ccc; border-radius: 4px;"
        )
