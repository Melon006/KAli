
```python
"""
CyberGuard UI - Theme and Styling
Modern dark theme optimized for long security work sessions
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor, QFont


def apply_dark_theme(app: QApplication):
    """Apply professional cybersecurity dark theme"""
    
    # Color scheme - Cyberpunk-inspired security colors
    COLORS = {
        'background': '#0d1117',
        'surface': '#161b22',
        'surface_hover': '#1c2128',
        'border': '#30363d',
        'text_primary': '#c9d1d9',
        'text_secondary': '#8b949e',
        'accent': '#58a6ff',      # Blue for info/actions
        'success': '#3fb950',      # Green for success
        'warning': '#d29922',      # Orange for warnings
        'danger': '#f85149',       # Red for critical/danger
        'info': '#a371f7',         # Purple for special features
    }
    
    app.setStyle('Fusion')
    
    palette = QPalette()
    
    # Base colors
    palette.setColor(QPalette.ColorRole.Window, QColor(COLORS['background']))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(COLORS['text_primary']))
    palette.setColor(QPalette.ColorRole.Base, QColor(COLORS['surface']))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(COLORS['surface_hover']))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(COLORS['surface']))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(COLORS['text_primary']))
    palette.setColor(QPalette.ColorRole.Text, QColor(COLORS['text_primary']))
    palette.setColor(QPalette.ColorRole.Button, QColor(COLORS['surface']))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(COLORS['text_primary']))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(COLORS['danger']))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(COLORS['accent']))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(COLORS['background']))
    
    app.setPalette(palette)
    
    # Global stylesheet
    app.setStyleSheet(f"""
        QMainWindow {{
            background-color: {COLORS['background']};
        }}
        
        QWidget {{
            font-family: 'Segoe UI', 'Ubuntu', sans-serif;
            font-size: 10pt;
        }}
        
        QPushButton {{
            background-color: {COLORS['surface']};
            color: {COLORS['text_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: 6px;
            padding: 8px 16px;
            min-width: 80px;
        }}
        
        QPushButton:hover {{
            background-color: {COLORS['surface_hover']};
            border-color: {COLORS['accent']};
        }}
        
        QPushButton:pressed {{
            background-color: {COLORS['accent']};
            color: {COLORS['background']};
        }}
        
        QPushButton#primaryButton {{
            background-color: {COLORS['accent']};
            color: {COLORS['background']};
            font-weight: bold;
        }}
        
        QPushButton#primaryButton:hover {{
            background-color: #79c0ff;
        }}
        
        QPushButton#dangerButton {{
            background-color: {COLORS['danger']};
            color: white;
        }}
        
        QPushButton#successButton {{
            background-color: {COLORS['success']};
            color: {COLORS['background']};
        }}
        
        QLineEdit, QTextEdit, QPlainTextEdit {{
            background-color: {COLORS['surface']};
            color: {COLORS['text_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: 6px;
            padding: 8px;
            selection-background-color: {COLORS['accent']};
        }}
        
        QLineEdit:focus, QTextEdit:focus {{
            border-color: {COLORS['accent']};
        }}
        
        QComboBox {{
            background-color: {COLORS['surface']};
            color: {COLORS['text_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: 6px;
            padding: 8px;
            min-width: 120px;
        }}
        
        QComboBox:hover {{
            border-color: {COLORS['accent']};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 30px;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {COLORS['surface']};
            color: {COLORS['text_primary']};
            selection-background-color: {COLORS['accent']};
            border: 1px solid {COLORS['border']};
        }}
        
        QTabWidget::pane {{
            border: 1px solid {COLORS['border']};
            border-radius: 6px;
            background-color: {COLORS['surface']};
        }}
        
        QTabBar::tab {{
            background-color: {COLORS['background']};
            color: {COLORS['text_secondary']};
            padding: 10px 20px;
            border: none;
            border-bottom: 2px solid transparent;
        }}
        
        QTabBar::tab:selected {{
            color: {COLORS['accent']};
            border-bottom: 2px solid {COLORS['accent']};
        }}
        
        QTabBar::tab:hover {{
            color: {COLORS['text_primary']};
            background-color: {COLORS['surface_hover']};
        }}
        
        QGroupBox {{
            color: {COLORS['text_secondary']};
            border: 1px solid {COLORS['border']};
            border-radius: 6px;
            margin-top: 12px;
            font-weight: bold;
            padding-top: 10px;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }}
        
        QProgressBar {{
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
            text-align: center;
            color: {COLORS['text_primary']};
        }}
        
        QProgressBar::chunk {{
            background-color: {COLORS['accent']};
            border-radius: 3px;
        }}
        
        QScrollBar:vertical {{
            background-color: {COLORS['background']};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {COLORS['border']};
            border-radius: 6px;
            min-height: 30px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {COLORS['text_secondary']};
        }}
        
        QTreeWidget, QTableWidget {{
            background-color: {COLORS['surface']};
            color: {COLORS['text_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: 6px;
            outline: none;
        }}
        
        QTreeWidget::item:selected, QTableWidget::item:selected {{
            background-color: {COLORS['accent']};
            color: {COLORS['background']};
        }}
        
        QTreeWidget::item:hover, QTableWidget::item:hover {{
            background-color: {COLORS['surface_hover']};
        }}
        
        QHeaderView::section {{
            background-color: {COLORS['background']};
            color: {COLORS['text_secondary']};
            padding: 8px;
            border: none;
            border-bottom: 1px solid {COLORS['border']};
        }}
        
        QLabel#titleLabel {{
            color: {COLORS['accent']};
            font-size: 18pt;
            font-weight: bold;
        }}
        
        QLabel#descriptionLabel {{
            color: {COLORS['text_secondary']};
            font-size: 10pt;
        }}
        
        QFrame#cardFrame {{
            background-color: {COLORS['surface']};
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
        }}
        
        QFrame#cardFrame:hover {{
            border-color: {COLORS['accent']};
        }}
        
        QMenuBar {{
            background-color: {COLORS['background']};
            color: {COLORS['text_primary']};
        }}
        
        QMenuBar::item:selected {{
            background-color: {COLORS['surface_hover']};
        }}
        
        QMenu {{
            background-color: {COLORS['surface']};
            color: {COLORS['text_primary']};
            border: 1px solid {COLORS['border']};
        }}
        
        QMenu::item:selected {{
            background-color: {COLORS['accent']};
            color: {COLORS['background']};
        }}
        
        QToolTip {{
            background-color: {COLORS['surface']};
            color: {COLORS['text_primary']};
            border: 1px solid {COLORS['border']};
            padding: 5px;
        }}
    """)
    
    # Set default font
    font = QFont('Segoe UI', 10)
    if not QFont(font).exactMatch():
        font = QFont('Ubuntu', 10)
    app.setFont(font)
    
    return COLORS


# Export colors for use in other modules
THEME_COLORS = None

def get_colors():
    """Get current theme colors"""
    global THEME_COLORS
    if THEME_COLORS is None:
        THEME_COLORS = {
            'background': '#0d1117',
            'surface': '#161b22',
            'surface_hover': '#1c2128',
            'border': '#30363d',
            'text_primary': '#c9d1d9',
            'text_secondary': '#8b949e',
            'accent': '#58a6ff',
            'success': '#3fb950',
            'warning': '#d29922',
            'danger': '#f85149',
            'info': '#a371f7',
        }
    return THEME_COLORS
```
