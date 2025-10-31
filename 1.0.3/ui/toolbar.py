"""
Aether Browser - UI Components
Handles buttons, icons, search bar, and toolbar
Enhanced with Firefox-inspired professional styling
"""

import os
from PyQt6.QtWidgets import (QToolBar, QLineEdit, QPushButton, QWidget, 
                             QHBoxLayout, QTabWidget, QTabBar, QVBoxLayout, QLabel,
                             QGraphicsDropShadowEffect)
from PyQt6.QtCore import pyqtSignal, Qt, QSize, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QKeyEvent, QIcon, QFont, QColor
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QPixmap, QPainter

class IconLoader:
    """Utility class to load SVG icons"""
    
    _icon_cache = {}
    _icon_dir = None
    
    @classmethod
    def set_icon_directory(cls, directory: str):
        """Set the directory where icons are stored"""
        cls._icon_dir = directory
    
    @classmethod
    def load_icon(cls, icon_name: str, size: int = 20, color: str = None) -> QIcon:
        """Load an SVG icon and return as QIcon"""
        cache_key = f"{icon_name}_{size}_{color}"
        
        if cache_key in cls._icon_cache:
            return cls._icon_cache[cache_key]
        
        if cls._icon_dir is None:
            return QIcon()
        
        icon_path = os.path.join(cls._icon_dir, icon_name)
        
        if not os.path.exists(icon_path):
            print(f"Icon not found: {icon_path}")
            return QIcon()
        
        try:
            # Load SVG
            renderer = QSvgRenderer(icon_path)
            
            # Create pixmap
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.GlobalColor.transparent)
            
            # Render SVG to pixmap
            painter = QPainter(pixmap)
            renderer.render(painter)
            painter.end()
            
            # Create icon
            icon = QIcon(pixmap)
            cls._icon_cache[cache_key] = icon
            return icon
            
        except Exception as e:
            print(f"Error loading icon {icon_name}: {e}")
            return QIcon()


class AddressBar(QLineEdit):
    """Custom address bar with search functionality and modern styling"""
    
    return_pressed_signal = pyqtSignal(str)
    focus_changed = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Search with Google or enter address")
        self.returnPressed.connect(self._on_return_pressed)
        self.setMinimumHeight(32)
        self.setMaximumHeight(32)
        
        # Modern clean styling
        self.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #d0d0d7;
                border-radius: 8px;
                padding: 0 14px;
                font-size: 13px;
                color: #0c0c0d;
                selection-background-color: #0a84ff;
                selection-color: white;
            }
            QLineEdit:hover {
                border: 1px solid #b1b1b8;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                background-color: #ffffff;
                border: 1px solid #0a84ff;
                outline: none;
            }
        """)
        
        # Add subtle shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(6)
        shadow.setColor(QColor(0, 0, 0, 12))
        shadow.setOffset(0, 1)
        self.setGraphicsEffect(shadow)
        
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


class IconButton(QPushButton):
    """Custom icon button for toolbar with modern styling"""
    
    def __init__(self, icon_name: str, tooltip: str = "", parent=None):
        super().__init__(parent)
        self.setFixedSize(34, 34)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(tooltip)
        self.icon_name = icon_name
        
        # Load icon
        self._load_icon(icon_name)
        
        # Clean modern styling
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 6px;
                padding: 7px;
            }
            QPushButton:hover:enabled {
                background-color: rgba(12, 12, 13, 0.1);
            }
            QPushButton:pressed:enabled {
                background-color: rgba(12, 12, 13, 0.15);
            }
            QPushButton:disabled {
                opacity: 0.4;
            }
        """)
    
    def _load_icon(self, icon_name: str):
        """Load icon"""
        icon = IconLoader.load_icon(icon_name, size=18)
        if not icon.isNull():
            self.setIcon(icon)
            self.setIconSize(QSize(18, 18))
    
    def update_icon(self, icon_name: str):
        """Update the button icon"""
        self.icon_name = icon_name
        self._load_icon(icon_name)


class NavigationToolbar(QToolBar):
    """Main navigation toolbar with buttons and address bar"""
    
    # Navigation signals
    back_clicked = pyqtSignal()
    forward_clicked = pyqtSignal()
    reload_clicked = pyqtSignal()
    home_clicked = pyqtSignal()
    new_tab_clicked = pyqtSignal()  # NEW TAB SIGNAL
    menu_clicked = pyqtSignal()
    
    # Address bar signal
    navigate_to_url = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMovable(False)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        self.setIconSize(QSize(18, 18))
        self.setFixedHeight(48)
        
        # Clean toolbar styling
        self.setStyleSheet("""
            QToolBar {
                background-color: #f9f9fa;
                border: none;
                border-bottom: 1px solid #d7d7db;
                spacing: 4px;
                padding: 7px 10px;
            }
        """)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup toolbar UI"""
        # Add left spacing
        left_spacer = QWidget()
        left_spacer.setFixedWidth(4)
        self.addWidget(left_spacer)
        
        # Back button
        self.back_btn = IconButton('arrow_back.svg', "Back")
        self.back_btn.clicked.connect(self.back_clicked.emit)
        self.addWidget(self.back_btn)
        
        # Forward button
        self.forward_btn = IconButton('arrow_forward.svg', "Forward")
        self.forward_btn.clicked.connect(self.forward_clicked.emit)
        self.addWidget(self.forward_btn)
        
        # Reload button
        self.reload_btn = IconButton('refresh.svg', "Reload")
        self.reload_btn.clicked.connect(self.reload_clicked.emit)
        self.addWidget(self.reload_btn)
        
        # Home button
        self.home_btn = IconButton('home.svg', "Home")
        self.home_btn.clicked.connect(self.home_clicked.emit)
        self.addWidget(self.home_btn)
        
        # Spacer before address bar
        spacer = QWidget()
        spacer.setFixedWidth(10)
        self.addWidget(spacer)
        
        # Address bar container
        address_container = QWidget()
        address_layout = QHBoxLayout(address_container)
        address_layout.setContentsMargins(0, 0, 0, 0)
        address_layout.setSpacing(0)
        
        self.address_bar = AddressBar()
        address_layout.addWidget(self.address_bar)
        
        self.address_bar.return_pressed_signal.connect(self.navigate_to_url.emit)
        self.addWidget(address_container)
        
        # Spacer after address bar
        spacer2 = QWidget()
        spacer2.setFixedWidth(10)
        self.addWidget(spacer2)
        
        # New tab button with add.svg icon
        self.new_tab_btn = IconButton('add.svg', "New Tab (Ctrl+T)")
        self.new_tab_btn.clicked.connect(self.new_tab_clicked.emit)  # EMIT THE SIGNAL
        self.addWidget(self.new_tab_btn)
        
        # Menu button
        self.menu_btn = IconButton('menu.svg', "Menu")
        self.menu_btn.clicked.connect(self.menu_clicked.emit)
        self.addWidget(self.menu_btn)
        
        # Add right spacing
        right_spacer = QWidget()
        right_spacer.setFixedWidth(4)
        self.addWidget(right_spacer)
    
    def update_buttons(self, can_go_back: bool, can_go_forward: bool):
        """Update navigation button states"""
        self.back_btn.setEnabled(can_go_back)
        self.forward_btn.setEnabled(can_go_forward)
    
    def set_address(self, url: str):
        """Set address bar URL"""
        self.address_bar.set_url(url)
    
    def set_loading(self, loading: bool):
        """Update UI for loading state"""
        if loading:
            self.reload_btn.update_icon('close.svg')
            self.reload_btn.setToolTip("Stop")
        else:
            self.reload_btn.update_icon('refresh.svg')
            self.reload_btn.setToolTip("Reload")


class TabBar(QTabBar):
    """Custom tab bar with close buttons and beautiful styling"""
    
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
        self.setDrawBase(False)
        
        # Beautiful light tab styling
        self.setStyleSheet("""
            QTabBar {
                background-color: #f5f5f5;
                border: none;
                qproperty-drawBase: 0;
            }
            QTabBar::tab {
                background-color: #f5f5f5;
                border: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                padding: 8px 14px;
                margin-right: 2px;
                margin-top: 3px;
                min-width: 120px;
                max-width: 240px;
                color: #0c0c0d;
                font-size: 13px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                color: #0c0c0d;
                font-weight: 500;
                margin-top: 1px;
                padding-top: 10px;
                padding-bottom: 8px;
                border: 1px solid #d7d7db;
                border-bottom: none;
            }
            QTabBar::tab:hover:!selected {
                background-color: #e9e9e9;
                color: #0c0c0d;
            }
            QTabBar::close-button {
                image: none;
                subcontrol-position: right;
                margin: 2px;
                border-radius: 3px;
                width: 16px;
                height: 16px;
                background-color: transparent;
            }
            QTabBar::close-button:hover {
                background-color: rgba(12, 12, 13, 0.15);
            }
        """)
        
        # Connect signals
        self.tabCloseRequested.connect(self.tab_close_requested_signal.emit)
        self.customContextMenuRequested.connect(self._show_context_menu)
    
    def _show_context_menu(self, position):
        """Show context menu for tab"""
        index = self.tabAt(position)
        if index >= 0:
            self.tab_context_menu_requested.emit(index, self.mapToGlobal(position))
    
    def tabSizeHint(self, index):
        """Custom tab size"""
        size = super().tabSizeHint(index)
        size.setHeight(34)
        return size


class TabCloseButton(QPushButton):
    """Custom close button for tabs using close.svg icon"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(16, 16)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("Close tab")
        
        # Load close icon
        icon = IconLoader.load_icon('close.svg', size=10)
        if not icon.isNull():
            self.setIcon(icon)
            self.setIconSize(QSize(10, 10))
        
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 3px;
                padding: 3px;
            }
            QPushButton:hover {
                background-color: rgba(12, 12, 13, 0.2);
            }
            QPushButton:pressed {
                background-color: rgba(12, 12, 13, 0.3);
            }
        """)


class TabWidget(QTabWidget):
    """Custom tab widget for browser tabs with modern design"""
    
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
        
        # Clean tab widget styling
        self.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #ffffff;
                top: 0px;
            }
            QTabWidget::tab-bar {
                alignment: left;
            }
        """)
        
        # Connect signals
        self.currentChanged.connect(self.tab_changed.emit)
        self.tab_bar.tab_close_requested_signal.connect(self.tab_close_requested.emit)
        self.tab_bar.tab_context_menu_requested.connect(self.tab_context_menu_requested.emit)
        
        # No corner widget (new tab button is in toolbar now)
        self.setCornerWidget(None)
    
    def add_tab(self, widget: QWidget, title: str) -> int:
        """Add a new tab with custom close button"""
        index = self.addTab(widget, title)
        
        # Add custom close button with close.svg icon
        close_btn = TabCloseButton()
        close_btn.clicked.connect(lambda: self.tab_close_requested.emit(index))
        self.tabBar().setTabButton(index, QTabBar.ButtonPosition.RightSide, close_btn)
        
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
