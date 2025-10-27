"""
Aether Browser - Main Window
Creates the browser window and manages the overall layout
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtCore import Qt, QUrl

# Import UI components
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ui.theme import Theme
from ui.menus import MenuManager
from ui.toolbar import NavigationToolbar, TabWidget
from ui.webview import WebView, WebViewManager
from ui.settings_dialog import SettingsDialog
from core.storage import Storage


class BrowserWindow(QMainWindow):
    """Main browser window"""
    
    def __init__(self):
        super().__init__()

        # Set icon directory for IconLoader
        icon_dir = os.path.join(os.path.dirname(__file__), "..", "utils", "icons")
        icon_dir = os.path.abspath(icon_dir)
        from ui.toolbar import IconLoader
        IconLoader.set_icon_directory(icon_dir)
        
        # Initialize storage
        self.storage = Storage()
        
        # Initialize managers
        self.theme = Theme()
        self.menu_manager = MenuManager()
        self.webview_manager = WebViewManager()
        
        # Load saved settings
        self._load_settings()
        
        # Setup window
        self._setup_window()
        self._setup_ui()
        self._connect_signals()
        self._apply_theme()
        
        # Create first tab
        self.create_new_tab()
        self.toolbar.new_tab_clicked.connect(self.create_new_tab)
    
    def _load_settings(self):
        """Load settings from storage"""
        settings = self.storage.load_settings()
        
        # Apply dark mode
        self.theme.dark_mode = settings.get('dark_mode', False)
        
        # Apply accent color
        accent_color_hex = settings.get('accent_color', '#4285f4')
        self.theme.accent_color = QColor(accent_color_hex)
    
    def _save_settings(self):
        """Save current settings to storage"""
        settings = {
            'dark_mode': self.theme.dark_mode,
            'accent_color': self.theme.accent_color.name(),
            'home_url': 'https://www.google.com',
            'default_zoom': 1.0
        }
        self.storage.save_settings(settings)
    
    def _setup_window(self):
        """Configure main window"""
        self.setWindowTitle("Aether Browser")
        self.setMinimumSize(1000, 600)
        self.resize(1200, 800)
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(__file__), "..", "utils", "icons", "50.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
    
    def _setup_ui(self):
        """Setup user interface"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Navigation toolbar
        self.toolbar = NavigationToolbar()
        layout.addWidget(self.toolbar)
        
        # Tab widget
        self.tab_widget = TabWidget()
        layout.addWidget(self.tab_widget)
    
    def _connect_signals(self):
        """Connect all signals"""
        # Toolbar signals
        self.toolbar.back_clicked.connect(self._on_back_clicked)
        self.toolbar.forward_clicked.connect(self._on_forward_clicked)
        self.toolbar.reload_clicked.connect(self._on_reload_clicked)
        self.toolbar.home_clicked.connect(self._on_home_clicked)
        self.toolbar.menu_clicked.connect(self._on_menu_clicked)
        self.toolbar.navigate_to_url.connect(self._on_navigate_to_url)
        
        # Tab widget signals
        self.tab_widget.new_tab_requested.connect(lambda: self.create_new_tab())
        self.tab_widget.tab_changed.connect(self._on_tab_changed)
        self.tab_widget.tab_close_requested.connect(self._on_tab_close_requested)
        self.tab_widget.tab_context_menu_requested.connect(self._on_tab_context_menu)
        
        # Menu signals
        self.menu_manager.new_tab_requested.connect(lambda: self.create_new_tab())
        self.menu_manager.new_window_requested.connect(self._on_new_window)
        self.menu_manager.settings_requested.connect(self._on_settings)
        self.menu_manager.quit_requested.connect(self.close)
        self.menu_manager.close_tab_requested.connect(self._on_tab_close_requested)
        self.menu_manager.reload_tab_requested.connect(self._on_reload_tab)
        self.menu_manager.duplicate_tab_requested.connect(self._on_duplicate_tab)
        self.menu_manager.zoom_in_requested.connect(self._on_zoom_in)
        self.menu_manager.zoom_out_requested.connect(self._on_zoom_out)
        self.menu_manager.zoom_reset_requested.connect(self._on_zoom_reset)
        
        # Theme signals
        self.theme.theme_changed.connect(self._apply_theme)
        self.theme.theme_changed.connect(self._save_settings)
    
    def _apply_theme(self):
        """Apply current theme"""
        self.setStyleSheet(self.theme.get_stylesheet())
    
    def _get_new_tab_url(self) -> str:
        """Get the URL for new tab page"""
        new_tab_path = os.path.join(
            os.path.dirname(__file__), 
            "..", 
            "utils", 
            "browser_websites", 
            "newtab.html"
        )
        new_tab_path = os.path.abspath(new_tab_path)
        return f"file:///{new_tab_path.replace(os.sep, '/')}"
    
    def create_new_tab(self, url: str = None) -> int:
        """Create a new browser tab"""
        if url is None:
            url = self._get_new_tab_url()
        
        webview = self.webview_manager.create_web_view()
        
        # Connect webview signals
        webview.title_changed_signal.connect(
            lambda title: self._on_webview_title_changed(webview, title)
        )
        webview.url_changed_signal.connect(
            lambda url: self._on_webview_url_changed(webview, url)
        )
        webview.loading_changed_signal.connect(
            lambda loading: self._on_webview_loading_changed(webview, loading)
        )
        
        # Add tab
        index = self.tab_widget.add_tab(webview, "New Tab")
        
        # Load URL
        webview.load_url(url)
        
        return index
    
    def _get_current_webview(self) -> WebView:
        """Get currently active webview"""
        return self.tab_widget.currentWidget()
    
    def _get_webview_at(self, index: int) -> WebView:
        """Get webview at specific index"""
        return self.tab_widget.widget(index)
    
    # Toolbar action handlers
    def _on_back_clicked(self):
        """Handle back button click"""
        webview = self._get_current_webview()
        if webview:
            webview.back()
    
    def _on_forward_clicked(self):
        """Handle forward button click"""
        webview = self._get_current_webview()
        if webview:
            webview.forward()
    
    def _on_reload_clicked(self):
        """Handle reload button click"""
        webview = self._get_current_webview()
        if webview:
            if webview.page().isLoading():
                webview.stop()
            else:
                webview.reload()
    
    def _on_home_clicked(self):
        """Handle home button click"""
        webview = self._get_current_webview()
        if webview:
            webview.load_url(self._get_new_tab_url())
    
    def _on_menu_clicked(self):
        """Handle menu button click"""
        menu = self.menu_manager.create_main_menu()
        menu.exec(self.toolbar.menu_btn.mapToGlobal(
            self.toolbar.menu_btn.rect().bottomLeft()
        ))
    
    def _on_navigate_to_url(self, url: str):
        """Handle URL navigation"""
        webview = self._get_current_webview()
        if webview:
            webview.load_url(url)
            # Add to history if it's a real URL
            if url and not url.startswith('file://'):
                self.storage.add_history_entry(url, webview.get_title())
    
    # Tab action handlers
    def _on_tab_changed(self, index: int):
        """Handle tab change"""
        webview = self._get_webview_at(index)
        if webview:
            # Update address bar
            self.toolbar.set_address(webview.get_url())
            
            # Update navigation buttons
            self.toolbar.update_buttons(
                webview.page().history().canGoBack(),
                webview.page().history().canGoForward()
            )
            
            # Update window title
            self.setWindowTitle(f"{webview.get_title()} - Aether Browser")
    
    def _on_tab_close_requested(self, index: int):
        """Handle tab close request"""
        if self.tab_widget.count() > 1:
            self.tab_widget.close_tab(index)
        else:
            # Don't close last tab, just navigate to new tab
            webview = self._get_webview_at(index)
            if webview:
                webview.load_url(self._get_new_tab_url())
    
    def _on_tab_context_menu(self, index: int, position):
        """Handle tab context menu request"""
        menu = self.menu_manager.create_tab_context_menu(index)
        menu.exec(position)
    
    # WebView event handlers
    def _on_webview_title_changed(self, webview: WebView, title: str):
        """Handle webview title change"""
        index = self.tab_widget.indexOf(webview)
        if index >= 0:
            self.tab_widget.update_tab_title(index, title)
            
            # Update window title if it's the current tab
            if index == self.tab_widget.currentIndex():
                self.setWindowTitle(f"{title} - Aether Browser")
    
    def _on_webview_url_changed(self, webview: WebView, url: QUrl):
        """Handle webview URL change"""
        if webview == self._get_current_webview():
            url_string = url.toString()
            self.toolbar.set_address(url_string)
            
            # Update navigation buttons
            self.toolbar.update_buttons(
                webview.page().history().canGoBack(),
                webview.page().history().canGoForward()
            )
            
            # Add to history if it's a real URL
            if url_string and not url_string.startswith('file://'):
                self.storage.add_history_entry(url_string, webview.get_title())
    
    def _on_webview_loading_changed(self, webview: WebView, loading: bool):
        """Handle webview loading state change"""
        if webview == self._get_current_webview():
            # Update toolbar loading state
            self.toolbar.set_loading(loading)
    
    # Menu action handlers
    def _on_new_window(self):
        """Create new browser window"""
        new_window = BrowserWindow()
        new_window.show()
    
    def _on_settings(self):
        """Open settings dialog"""
        dialog = SettingsDialog(self.theme, self)
        dialog.exec()
    
    def _on_reload_tab(self, index: int):
        """Reload specific tab"""
        webview = self._get_webview_at(index)
        if webview:
            webview.reload()
    
    def _on_duplicate_tab(self, index: int):
        """Duplicate specific tab"""
        webview = self._get_webview_at(index)
        if webview:
            url = webview.get_url()
            if url.startswith('file://'):
                url = self._get_new_tab_url()
            self.create_new_tab(url)
    
    def _on_zoom_in(self):
        """Zoom in current page"""
        webview = self._get_current_webview()
        if webview:
            webview.zoom_in()
    
    def _on_zoom_out(self):
        """Zoom out current page"""
        webview = self._get_current_webview()
        if webview:
            webview.zoom_out()
    
    def _on_zoom_reset(self):
        """Reset zoom for current page"""
        webview = self._get_current_webview()
        if webview:
            webview.zoom_reset()
    
    def closeEvent(self, event):
        """Handle window close event"""
        self._save_settings()
        event.accept()


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    # Set application details
    app.setApplicationName("Aether Browser")
    app.setApplicationDisplayName("Aether")
    app.setOrganizationName("Aether")
    
    # Create and show main window
    window = BrowserWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
