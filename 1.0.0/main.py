"""
Aether Browser - Main Entry Point
Version 1.0.0
"""

import sys
import os

# Add the ui directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ui'))

from window import main

if __name__ == "__main__":
    main()
