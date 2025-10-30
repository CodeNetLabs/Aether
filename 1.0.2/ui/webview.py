"""
Aether Browser - Web View Management
Handles displaying website contents
"""

from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from PyQt6.QtCore import pyqtSignal, QUrl

class WebView(QWebEngineView):
    """Custom web view with additional functionality"""
    
    # Signals
    title_changed_signal = pyqtSignal(str)
    icon_changed_signal = pyqtSignal()
    loading_changed_signal = pyqtSignal(bool)
    url_changed_signal = pyqtSignal(QUrl)
    
    def __init__(self, profile=None, parent=None):
        super().__init__(parent)
        
        if profile:
            page = QWebEnginePage(profile, self)
            self.setPage(page)
        
        # Connect signals
        self.titleChanged.connect(self._on_title_changed)
        self.iconChanged.connect(self._on_icon_changed)
        self.loadStarted.connect(lambda: self.loading_changed_signal.emit(True))
        self.loadFinished.connect(lambda: self.loading_changed_signal.emit(False))
        self.urlChanged.connect(self._on_url_changed)
        
    def _on_title_changed(self, title):
        """Handle title changes"""
        if not title:
            title = "New Tab"
        self.title_changed_signal.emit(title)
    
    def _on_icon_changed(self):
        """Handle icon changes"""
        self.icon_changed_signal.emit()
    
    def _on_url_changed(self, url):
        """Handle URL changes"""
        self.url_changed_signal.emit(url)
    
    def load_url(self, url_string: str):
        """Load a URL from string"""
        if not url_string:
            return
        
        # Add https:// if no protocol specified
        if not url_string.startswith(('http://', 'https://', 'file://', 'about:')):
            # Check if it looks like a URL or a search query
            if '.' in url_string and ' ' not in url_string:
                url_string = 'https://' + url_string
            else:
                # Treat as search query
                url_string = f'https://www.google.com/search?q={url_string}'
        
        self.setUrl(QUrl(url_string))
    
    def get_title(self) -> str:
        """Get current page title"""
        title = self.title()
        return title if title else "New Tab"
    
    def get_url(self) -> str:
        """Get current URL"""
        return self.url().toString()
    
    def zoom_in(self):
        """Zoom in"""
        current_zoom = self.zoomFactor()
        self.setZoomFactor(min(current_zoom + 0.1, 3.0))
    
    def zoom_out(self):
        """Zoom out"""
        current_zoom = self.zoomFactor()
        self.setZoomFactor(max(current_zoom - 0.1, 0.25))
    
    def zoom_reset(self):
        """Reset zoom to 100%"""
        self.setZoomFactor(1.0)


class WebViewManager:
    """Manages web view profiles and settings"""
    
    def __init__(self):
        self.default_profile = QWebEngineProfile.defaultProfile()
        self.private_profile = QWebEngineProfile()
        
        # Configure profiles
        self._configure_profile(self.default_profile, False)
        self._configure_profile(self.private_profile, True)
    
    def _configure_profile(self, profile: QWebEngineProfile, is_private: bool):
        """Configure a web engine profile"""
        if is_private:
            profile.setPersistentCookiesPolicy(
                QWebEngineProfile.PersistentCookiesPolicy.NoPersistentCookies
            )
        
        # Set user agent
        profile.setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Aether/1.0"
        )
    
    def create_web_view(self, is_private: bool = False, parent=None) -> WebView:
        """Create a new web view"""
        profile = self.private_profile if is_private else self.default_profile
        return WebView(profile, parent)
