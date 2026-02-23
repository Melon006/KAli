```python
#!/usr/bin/env python3
"""
CyberGuard UI - Kali Linux Tools GUI Suite
A beginner-friendly interface for cybersecurity tools
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from gui.main_window import CyberGuardMainWindow
from gui.styles import apply_dark_theme


def main():
    """Initialize and run CyberGuard UI"""
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("CyberGuard UI")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("CyberGuard")
    
    # Apply professional dark theme
    apply_dark_theme(app)
    
    # Create and show main window
    window = CyberGuardMainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
```
