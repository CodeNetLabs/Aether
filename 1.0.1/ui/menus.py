"""
Aether Browser - Menu Management
Handles context menus and main browser menu
"""

from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtCore import QObject, pyqtSignal

class MenuManager(QObject):
    # Tab context menu signals
    new_tab_requested = pyqtSignal()
    close_tab_requested = pyqtSignal(int)
    reload_tab_requested = pyqtSignal(int)
    duplicate_tab_requested = pyqtSignal(int)
    pin_tab_requested = pyqtSignal(int)
    mute_tab_requested = pyqtSignal(int)
    close_other_tabs_requested = pyqtSignal(int)
    close_tabs_right_requested = pyqtSignal(int)
    
    # Main menu signals
    new_window_requested = pyqtSignal()
    new_private_window_requested = pyqtSignal()
    settings_requested = pyqtSignal()
    history_requested = pyqtSignal()
    downloads_requested = pyqtSignal()
    bookmarks_requested = pyqtSignal()
    extensions_requested = pyqtSignal()
    print_requested = pyqtSignal()
    find_requested = pyqtSignal()
    zoom_in_requested = pyqtSignal()
    zoom_out_requested = pyqtSignal()
    zoom_reset_requested = pyqtSignal()
    fullscreen_requested = pyqtSignal()
    developer_tools_requested = pyqtSignal()
    about_requested = pyqtSignal()
    quit_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
    def create_tab_context_menu(self, tab_index: int, is_pinned: bool = False, is_muted: bool = False) -> QMenu:
        """Create context menu for tab right-click"""
        menu = QMenu()
        
        # Reload tab
        reload_action = QAction("Reload", menu)
        reload_action.triggered.connect(lambda: self.reload_tab_requested.emit(tab_index))
        menu.addAction(reload_action)
        
        # Duplicate tab
        duplicate_action = QAction("Duplicate", menu)
        duplicate_action.triggered.connect(lambda: self.duplicate_tab_requested.emit(tab_index))
        menu.addAction(duplicate_action)
        
        menu.addSeparator()
        
        # Pin/Unpin tab
        pin_text = "Unpin Tab" if is_pinned else "Pin Tab"
        pin_action = QAction(pin_text, menu)
        pin_action.triggered.connect(lambda: self.pin_tab_requested.emit(tab_index))
        menu.addAction(pin_action)
        
        # Mute/Unmute tab
        mute_text = "Unmute Tab" if is_muted else "Mute Tab"
        mute_action = QAction(mute_text, menu)
        mute_action.triggered.connect(lambda: self.mute_tab_requested.emit(tab_index))
        menu.addAction(mute_action)
        
        menu.addSeparator()
        
        # Close other tabs
        close_others_action = QAction("Close Other Tabs", menu)
        close_others_action.triggered.connect(lambda: self.close_other_tabs_requested.emit(tab_index))
        menu.addAction(close_others_action)
        
        # Close tabs to the right
        close_right_action = QAction("Close Tabs to the Right", menu)
        close_right_action.triggered.connect(lambda: self.close_tabs_right_requested.emit(tab_index))
        menu.addAction(close_right_action)
        
        menu.addSeparator()
        
        # Close tab
        close_action = QAction("Close Tab", menu)
        close_action.triggered.connect(lambda: self.close_tab_requested.emit(tab_index))
        menu.addAction(close_action)
        
        return menu
    
    def create_main_menu(self) -> QMenu:
        """Create main browser menu"""
        menu = QMenu()
        
        # New Tab
        new_tab_action = QAction("New Tab", menu)
        new_tab_action.setShortcut(QKeySequence("Ctrl+T"))
        new_tab_action.triggered.connect(self.new_tab_requested.emit)
        menu.addAction(new_tab_action)
        
        # New Window
        new_window_action = QAction("New Window", menu)
        new_window_action.setShortcut(QKeySequence("Ctrl+N"))
        new_window_action.triggered.connect(self.new_window_requested.emit)
        menu.addAction(new_window_action)
        
        # New Private Window
        new_private_action = QAction("New Private Window", menu)
        new_private_action.setShortcut(QKeySequence("Ctrl+Shift+N"))
        new_private_action.triggered.connect(self.new_private_window_requested.emit)
        menu.addAction(new_private_action)
        
        menu.addSeparator()
        
        # History
        history_action = QAction("History", menu)
        history_action.setShortcut(QKeySequence("Ctrl+H"))
        history_action.triggered.connect(self.history_requested.emit)
        menu.addAction(history_action)
        
        # Downloads
        downloads_action = QAction("Downloads", menu)
        downloads_action.setShortcut(QKeySequence("Ctrl+J"))
        downloads_action.triggered.connect(self.downloads_requested.emit)
        menu.addAction(downloads_action)
        
        # Bookmarks
        bookmarks_action = QAction("Bookmarks", menu)
        bookmarks_action.setShortcut(QKeySequence("Ctrl+Shift+O"))
        bookmarks_action.triggered.connect(self.bookmarks_requested.emit)
        menu.addAction(bookmarks_action)
        
        menu.addSeparator()
        
        # Zoom submenu
        zoom_menu = menu.addMenu("Zoom")
        
        zoom_in_action = QAction("Zoom In", zoom_menu)
        zoom_in_action.setShortcut(QKeySequence("Ctrl++"))
        zoom_in_action.triggered.connect(self.zoom_in_requested.emit)
        zoom_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("Zoom Out", zoom_menu)
        zoom_out_action.setShortcut(QKeySequence("Ctrl+-"))
        zoom_out_action.triggered.connect(self.zoom_out_requested.emit)
        zoom_menu.addAction(zoom_out_action)
        
        zoom_reset_action = QAction("Reset Zoom", zoom_menu)
        zoom_reset_action.setShortcut(QKeySequence("Ctrl+0"))
        zoom_reset_action.triggered.connect(self.zoom_reset_requested.emit)
        zoom_menu.addAction(zoom_reset_action)
        
        menu.addSeparator()
        
        # Find
        find_action = QAction("Find in Page", menu)
        find_action.setShortcut(QKeySequence("Ctrl+F"))
        find_action.triggered.connect(self.find_requested.emit)
        menu.addAction(find_action)
        
        # Print
        print_action = QAction("Print", menu)
        print_action.setShortcut(QKeySequence("Ctrl+P"))
        print_action.triggered.connect(self.print_requested.emit)
        menu.addAction(print_action)
        
        menu.addSeparator()
        
        # Extensions
        extensions_action = QAction("Extensions", menu)
        extensions_action.triggered.connect(self.extensions_requested.emit)
        menu.addAction(extensions_action)
        
        # Developer Tools
        dev_tools_action = QAction("Developer Tools", menu)
        dev_tools_action.setShortcut(QKeySequence("F12"))
        dev_tools_action.triggered.connect(self.developer_tools_requested.emit)
        menu.addAction(dev_tools_action)
        
        menu.addSeparator()
        
        # Settings
        settings_action = QAction("Settings", menu)
        settings_action.triggered.connect(self.settings_requested.emit)
        menu.addAction(settings_action)
        
        # About
        about_action = QAction("About Aether", menu)
        about_action.triggered.connect(self.about_requested.emit)
        menu.addAction(about_action)
        
        menu.addSeparator()
        
        # Quit
        quit_action = QAction("Quit", menu)
        quit_action.setShortcut(QKeySequence("Ctrl+Q"))
        quit_action.triggered.connect(self.quit_requested.emit)
        menu.addAction(quit_action)
        
        return menu
