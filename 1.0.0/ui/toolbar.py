"""
Aether Browser - UI Components
Handles buttons, icons, search bar, and toolbar
"""

from PyQt6.QtWidgets import (QToolBar, QLineEdit, QPushButton, QWidget, 
                             QHBoxLayout, QTabWidget, QTabBar, QVBoxLayout, QLabel)
from PyQt6.QtCore import pyqtSignal, Qt, QSize, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QKeyEvent, QPainter, QColor

class AddressBar(QLineEdit):
    """Custom address bar with search functionality"""
    
    return_pressed_signal = pyqtSignal(str)
    focus_changed = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Search or enter address")
        self.returnPressed.connect(self._on_return_pressed)
        self.setMinimumHeight(36)
        
    def _on_return_pressed(self):
        """Handle return key press"""
        self.return_pressed_signal.emit(self.text())
    
    def set_url(self, url: str):
        """Set the address bar URL"""
        # Don't show internal URLs
        if url.startswith('file://'):
            self.setText('')
        else:
            self.setText(url)
    
    def keyPressEvent(self, event: QKeyEvent):
        """Handle key press events"""
        if event.key() == Qt.Key.Key_Escape:
            self.clearFocus()
        super().keyPressEvent(event)
    
    def focusInEvent(self, event):
        """Handle focus in"""
        super().focusInEvent(event)
        self.selectAll()
        self.focus_changed.emit(True)
    
    def focusOutEvent(self, event):
        """Handle focus out"""
        super().focusOutEvent(event)
        self.focus_changed.emit(False)


class NavigationButton(QPushButton):
    """Custom styled navigation button"""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(36)
        self.setMinimumWidth(80)
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class NavigationToolbar(QToolBar):
    """Main navigation toolbar with buttons and address bar"""
    
    # Navigation signals
    back_clicked = pyqtSignal()
    forward_clicked = pyqtSignal()
    reload_clicked = pyqtSignal()
    home_clicked = pyqtSignal()
    menu_clicked = pyqtSignal()
    
    # Address bar signal
    navigate_to_url = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMovable(False)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        self.setIconSize(QSize(20, 20))
        self.setMinimumHeight(50)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup toolbar UI"""
        # Add spacing
        self.addWidget(QLabel("  "))
        
        # Back button
        self.back_btn = NavigationButton("← Back")
        self.back_btn.clicked.connect(self.back_clicked.emit)
        self.addWidget(self.back_btn)
        
        # Forward button
        self.forward_btn = NavigationButton("Forward →")
        self.forward_btn.clicked.connect(self.forward_clicked.emit)
        self.addWidget(self.forward_btn)
        
        # Reload button
        self.reload_btn = NavigationButton("⟳ Reload")
        self.reload_btn.clicked.connect(self.reload_clicked.emit)
        self.addWidget(self.reload_btn)
        
        # Home button
        self.home_btn = NavigationButton("⌂ Home")
        self.home_btn.clicked.connect(self.home_clicked.emit)
        self.addWidget(self.home_btn)
        
        # Spacer
        spacer = QWidget()
        spacer.setFixedWidth(10)
        self.addWidget(spacer)
        
        # Address bar (takes up remaining space)
        self.address_bar = AddressBar()
        self.address_bar.return_pressed_signal.connect(self.navigate_to_url.emit)
        self.addWidget(self.address_bar)
        
        # Spacer
        spacer2 = QWidget()
        spacer2.setFixedWidth(10)
        self.addWidget(spacer2)
        
        # Menu button
        self.menu_btn = NavigationButton("☰ Menu")
        self.menu_btn.clicked.connect(self.menu_clicked.emit)
        self.addWidget(self.menu_btn)
        
        # Add spacing
        self.addWidget(QLabel("  "))
    
    def update_buttons(self, can_go_back: bool, can_go_forward: bool):
        """Update navigation button states"""
        self.back_btn.setEnabled(can_go_back)
        self.forward_btn.setEnabled(can_go_forward)
    
    def set_address(self, url: str):
        """Set address bar URL"""
        self.address_bar.set_url(url)
    
    def set_loading(self, loading: bool):
        """Update UI for loading state"""
        self.reload_btn.setText("⊗ Stop" if loading else "⟳ Reload")


class TabBar(QTabBar):
    """Custom tab bar with close buttons"""
    
    tab_close_requested_signal = pyqtSignal(int)
    tab_context_menu_requested = pyqtSignal(int, object)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setExpanding(False)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setElideMode(Qt.TextElideMode.ElideRight)
        self.setUsesScrollButtons(True)
        
        # Connect signals
        self.tabCloseRequested.connect(self.tab_close_requested_signal.emit)
        self.customContextMenuRequested.connect(self._show_context_menu)
    
    def _show_context_menu(self, position):
        """Show context menu for tab"""
        index = self.tabAt(position)
        if index >= 0:
            self.tab_context_menu_requested.emit(index, self.mapToGlobal(position))


class TabWidget(QTabWidget):
    """Custom tab widget for browser tabs"""
    
    # Signals
    new_tab_requested = pyqtSignal()
    tab_changed = pyqtSignal(int)
    tab_close_requested = pyqtSignal(int)
    tab_context_menu_requested = pyqtSignal(int, object)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Use custom tab bar
        self.tab_bar = TabBar()
        self.setTabBar(self.tab_bar)
        
        # Tab position
        self.setTabPosition(QTabWidget.TabPosition.North)
        self.setDocumentMode(True)
        
        # Connect signals
        self.currentChanged.connect(self.tab_changed.emit)
        self.tab_bar.tab_close_requested_signal.connect(self.tab_close_requested.emit)
        self.tab_bar.tab_context_menu_requested.connect(self.tab_context_menu_requested.emit)
        
        # Add new tab button
        self.new_tab_btn = QPushButton("+")
        self.new_tab_btn.setFixedSize(32, 32)
        self.new_tab_btn.clicked.connect(self.new_tab_requested.emit)
        self.new_tab_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.new_tab_btn.setToolTip("New Tab (Ctrl+T)")
        self.setCornerWidget(self.new_tab_btn, Qt.Corner.TopRightCorner)
    
    def add_tab(self, widget: QWidget, title: str) -> int:
        """Add a new tab"""
        index = self.addTab(widget, title)
        self.setCurrentIndex(index)
        return index
    
    def update_tab_title(self, index: int, title: str):
        """Update tab title"""
        if 0 <= index < self.count():
            # Limit title length
            if len(title) > 25:
                title = title[:22] + "..."
            self.setTabText(index, title)
    
    def close_tab(self, index: int):
        """Close a tab"""
        if 0 <= index < self.count():
            widget = self.widget(index)
            self.removeTab(index)
            if widget:
                widget.deleteLater()
