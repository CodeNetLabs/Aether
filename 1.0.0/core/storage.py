"""
Aether Browser - Storage Management
Handles persistent local storage for browser data
"""

import json
import os
from typing import Any, Optional
from pathlib import Path


class Storage:
    """Manages persistent storage for browser data"""
    
    def __init__(self, storage_dir: str = None):
        """Initialize storage manager"""
        if storage_dir is None:
            # Default to user's home directory
            home = Path.home()
            storage_dir = home / ".aether_browser" / "storage"
        
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Storage files
        self.settings_file = self.storage_dir / "settings.json"
        self.history_file = self.storage_dir / "history.json"
        self.bookmarks_file = self.storage_dir / "bookmarks.json"
        
        # Initialize storage
        self._init_storage()
    
    def _init_storage(self):
        """Initialize storage files if they don't exist"""
        if not self.settings_file.exists():
            self.save_settings({
                "dark_mode": False,
                "accent_color": "#4285f4",
                "home_url": "https://www.google.com",
                "default_zoom": 1.0
            })
        
        if not self.history_file.exists():
            self.save_history([])
        
        if not self.bookmarks_file.exists():
            self.save_bookmarks([])
    
    def _read_json(self, file_path: Path) -> Any:
        """Read JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
    
    def _write_json(self, file_path: Path, data: Any):
        """Write JSON file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
    
    # Settings
    def load_settings(self) -> dict:
        """Load browser settings"""
        return self._read_json(self.settings_file) or {}
    
    def save_settings(self, settings: dict):
        """Save browser settings"""
        self._write_json(self.settings_file, settings)
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a specific setting"""
        settings = self.load_settings()
        return settings.get(key, default)
    
    def set_setting(self, key: str, value: Any):
        """Set a specific setting"""
        settings = self.load_settings()
        settings[key] = value
        self.save_settings(settings)
    
    # History
    def load_history(self) -> list:
        """Load browsing history"""
        return self._read_json(self.history_file) or []
    
    def save_history(self, history: list):
        """Save browsing history"""
        self._write_json(self.history_file, history)
    
    def add_history_entry(self, url: str, title: str):
        """Add entry to browsing history"""
        from datetime import datetime
        
        history = self.load_history()
        entry = {
            "url": url,
            "title": title,
            "timestamp": datetime.now().isoformat()
        }
        history.insert(0, entry)
        
        # Keep only last 1000 entries
        history = history[:1000]
        self.save_history(history)
    
    # Bookmarks
    def load_bookmarks(self) -> list:
        """Load bookmarks"""
        return self._read_json(self.bookmarks_file) or []
    
    def save_bookmarks(self, bookmarks: list):
        """Save bookmarks"""
        self._write_json(self.bookmarks_file, bookmarks)
    
    def add_bookmark(self, url: str, title: str):
        """Add a bookmark"""
        bookmarks = self.load_bookmarks()
        bookmark = {
            "url": url,
            "title": title
        }
        bookmarks.append(bookmark)
        self.save_bookmarks(bookmarks)
    
    def remove_bookmark(self, url: str):
        """Remove a bookmark"""
        bookmarks = self.load_bookmarks()
        bookmarks = [b for b in bookmarks if b["url"] != url]
        self.save_bookmarks(bookmarks)
