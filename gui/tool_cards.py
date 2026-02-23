"""
CyberGuard UI - Tool Cards and Widgets
Reusable components for tool configuration and execution
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QCheckBox, QSpinBox, QFileDialog,
    QFrame, QGridLayout, QGroupBox, QTextEdit, QMessageBox,
    QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from gui.styles import get_colors


class ToolCategoryCard(QFrame):
    """Clickable card for tool categories"""
    
    clicked = pyqtSignal()
    
    def __init__(self, data: dict, parent=None):
        super().__init__(parent)
        self.data = data
        self.colors = get_colors()
        self.setup_ui()
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
    def setup_ui(self):
        self.setObjectName("cardFrame")
        self.setFixedSize(280, 200)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Icon
        icon = QLabel(self.data['icon'])
        icon.setStyleSheet(f"font-size: 48px;")
        layout.addWidget(icon)
        
        # Title
        title = QLabel(self.data['title'])
        title.setStyleSheet(f"""
            color: {self.data['color']};
            font-size: 16px;
            font-weight: bold;
        """)
        layout.addWidget(title)
        
        # Description
        desc = QLabel(self.data['desc'])
        desc.setStyleSheet(f"color: {self.colors['text_secondary']}; font-size: 11px;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        layout.addStretch()
        
        # Tools list
        tools = QLabel("Tools: " + ", ".join(self.data['tools'][:3]) + "...")
        tools.setStyleSheet(f"color: {self.colors['text_secondary']}; font-size: 9px;")
        layout.addWidget(tools)
    
    def mousePressEvent(self, event):
        self.clicked.emit()


class ToolWidget(QGroupBox):
    """Configurable tool execution widget"""
    
    def __init__(self, name: str, description: str, 
                 fields: list, run_callback, parent=None):
        super().__init__(parent)
        self.name = name
        self.description = description
        self.fields_config = fields
        self.run_callback = run_callback
        self.field_widgets = {}
        self.colors = get_colors()
        
        self.setTitle(name)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Description
        desc = QLabel(self.description)
        desc.setStyleSheet(f"color: {self.colors['text_secondary']};")
        layout.addWidget(desc)
        
        # Form layout for parameters
        form = QGridLayout()
        form.setColumnStretch(1, 1)
        form.setSpacing(10)
        
        row = 0
        for field in self.fields_config:
            # Label
            label_text = field['label']
            if field.get('required'):
                label_text += " *"
            
            label = QLabel(label_text)
            label.setStyleSheet(f"""
                color: {self.colors['text_primary']};
                {'color: ' + self.colors['accent'] + '; font-weight: bold;' if field.get('required') else ''}
            """)
            form.addWidget(label, row, 0)
            
            # Input widget based on type
            widget = self.create_input_widget(field)
            self.field_widgets[field['name']] = widget
            form.addWidget(widget, row, 1)
            
            row += 1
        
        layout.addLayout(form)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.reset_btn = QPushButton("↺ Reset")
        self.reset_btn.clicked.connect(self.reset_fields)
        btn_layout.addWidget(self.reset_btn)
        
        self.preview_btn = QPushButton("👁 Preview Command")
        self.preview_btn.clicked.connect(self.preview_command)
        btn_layout.addWidget(self.preview_btn)
        
        self.run_btn = QPushButton(f"▶ Run {self.name}")
        self.run_btn.setObjectName("primaryButton")
        self.run_btn.clicked.connect(self.execute_tool)
        btn_layout.addWidget(self.run_btn)
        
        layout.addLayout(btn_layout)
        
        # Command preview area
        self.preview_area = QTextEdit()
        self.preview_area.setPlaceholderText("Command preview will appear here...")
        self.preview_area.setMaximumHeight(80)
        self.preview_area.setReadOnly(True)
        self.preview_area.setStyleSheet(f"""
            background-color: {self.colors['background']};
            color: {self.colors['success']};
            font-family: 'Consolas', 'Monaco', monospace;
        """)
        layout.addWidget(self.preview_area)
    
    def create_input_widget(self, field: dict) -> QWidget:
        """Create appropriate input widget for field type"""
        field_type = field.get('type', 'text')
        
        if field_type == 'text':
            widget = QLineEdit()
            widget.setPlaceholderText(field.get('placeholder', ''))
            if 'default' in field:
                widget.setText(str(field['default']))
        
        elif field_type == 'number':
            widget = QSpinBox()
            widget.setMinimum(field.get('min', 0))
            widget.setMaximum(field.get('max', 999999))
            widget.setValue(field.get('default', 0))
        
        elif field_type == 'select':
            widget = QComboBox()
            widget.addItems(field.get('options', []))
            widget.setEditable(False)
        
        elif field_type == 'multiselect':
            # Use text with comma separation for multiselect
            widget = QLineEdit()
            widget.setPlaceholderText("Select: " + ", ".join(field.get('options', [])))
        
        elif field_type == 'checkbox':
            widget = QCheckBox()
            widget.setChecked(field.get('default', False))
        
        elif field_type == 'file':
            widget = FileSelector(field.get('default', ''))
        
        else:
            widget = QLineEdit()
        
        return widget
    
    def get_field_values(self) -> dict:
        """Collect all field values"""
        values = {}
        for name, widget in self.field_widgets.items():
            if isinstance(widget, QLineEdit):
                values[name] = widget.text()
            elif isinstance(widget, QSpinBox):
                values[name] = widget.value()
            elif isinstance(widget, QComboBox):
                values[name] = widget.currentText()
            elif isinstance(widget, QCheckBox):
                values[name] = widget.isChecked()
            elif isinstance(widget, FileSelector):
                values[name] = widget.get_path()
        return values
    
    def reset_fields(self):
        """Reset all fields to defaults"""
        for field in self.fields_config:
            name = field['name']
            widget = self.field_widgets[name]
            
            if isinstance(widget, QLineEdit):
                widget.setText(field.get('default', ''))
            elif isinstance(widget, QSpinBox):
                widget.setValue(field.get('default', 0))
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)
            elif isinstance(widget, QCheckBox):
                widget.setChecked(field.get('default', False))
            elif isinstance(widget, FileSelector):
                widget.set_path(field.get('default', ''))
        
        self.preview_area.clear()
    
    def preview_command(self):
        """Generate and display command preview"""
        values = self.get_field_values()
        
        # Build preview based on tool type
        preview = self.build_command_preview(values)
        self.preview_area.setText(preview)
    
    def build_command_preview(self, values: dict) -> str:
        """Build command string for preview - override in subclasses"""
        # Generic preview - tools should provide specific implementation
        return f"{self.name.lower()} " + " ".join(f"--{k} {v}" for k, v in values.items() if v)
    
    def execute_tool(self):
        """Validate and execute the tool"""
        values = self.get_field_values()
        
        # Validate required fields
        for field in self.fields_config:
            if field.get('required') and not values.get(field['name']):
                QMessageBox.warning(self, "Validation Error",
                    f"Required field '{field['label']}' is empty.")
                return
        
        # Confirm execution for dangerous tools
        if self.name in ['Aircrack-ng', 'SQLMap', 'Metasploit Console']:
            reply = QMessageBox.question(self, "Confirm Execution",
                f"You are about to run {self.name}.\n\n"
                "This tool may cause system changes or network activity.\n"
                "Continue only if you have proper authorization.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No)
            
            if reply != QMessageBox.StandardButton.Yes:
                return
        
        # Execute
        self.run_callback(values)


class FileSelector(QWidget):
    """Combined file path input with browse button"""
    
    def __init__(self, default_path: str = "", parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        self.path_input = QLineEdit(default_path)
        layout.addWidget(self.path_input)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.setMaximumWidth(80)
        browse_btn.clicked.connect(self.browse_file)
        layout.addWidget(browse_btn)
    
    def browse_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if path:
            self.path_input.setText(path)
    
    def get_path(self) -> str:
        return self.path_input.text()
    
    def set_path(self, path: str):
        self.path_input.setText(path)
