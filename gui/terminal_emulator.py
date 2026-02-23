"""
CyberGuard UI - Terminal Emulator
Displays command output with syntax highlighting
"""

import subprocess
import threading
from queue import Queue, Empty

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QPushButton, QLabel, QLineEdit, QMenu
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QTextCursor, QColor, QTextCharFormat, QFont

from gui.styles import get_colors


class TerminalWidget(QWidget):
    """Terminal output panel with command execution"""
    
    command_finished = pyqtSignal(int, str)  # return code, output
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.colors = get_colors()
        self.current_process = None
        self.output_queue = Queue()
        self.setup_ui()
        
        # Timer for updating output
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_output)
        self.update_timer.start(50)  # 50ms refresh
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Header
        header = QHBoxLayout()
        
        title = QLabel("🖥️ Terminal Output")
        title.setStyleSheet(f"""
            color: {self.colors['text_primary']};
            font-weight: bold;
        """)
        header.addWidget(title)
        
        header.addStretch()
        
        # Status indicator
        self.status_label = QLabel("● Idle")
        self.status_label.setStyleSheet(f"color: {self.colors['success']};")
        header.addWidget(self.status_label)
        
        # Control buttons
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_output)
        header.addWidget(self.clear_btn)
        
        self.stop_btn = QPushButton("⏹ Stop")
        self.stop_btn.setEnabled(False)
        self.stop_btn.setObjectName("dangerButton")
        self.stop_btn.clicked.connect(self.stop_command)
        header.addWidget(self.stop_btn)
        
        layout.addLayout(header)
        
        # Output display
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Consolas", 10))
        self.output.setStyleSheet(f"""
            QTextEdit {{
                background-color: {self.colors['background']};
                color: {self.colors['text_primary']};
                border: 1px solid {self.colors['border']};
                border-radius: 6px;
                padding: 10px;
            }}
        """)
        
        # Setup ANSI color support
        self.setup_ansi_colors()
        
        layout.addWidget(self.output)
        
        # Quick command bar
        quick_bar = QHBoxLayout()
        
        quick_label = QLabel("Quick:")
        quick_label.setStyleSheet(f"color: {self.colors['text_secondary']};")
        quick_bar.addWidget(quick_label)
        
        self.quick_cmd = QLineEdit()
        self.quick_cmd.setPlaceholderText("Type command and press Enter...")
        self.quick_cmd.returnPressed.connect(self.run_quick_command)
        quick_bar.addWidget(self.quick_cmd)
        
        layout.addLayout(quick_bar)
        
        # Context menu
        self.output.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.output.customContextMenuRequested.connect(self.show_context_menu)
    
    def setup_ansi_colors(self):
        """Setup ANSI color code parsing"""
        self.ansi_colors = {
            '30': QColor('#000000'),  # Black
            '31': QColor(self.colors['danger']),    # Red
            '32': QColor(self.colors['success']),   # Green
            '33': QColor(self.colors['warning']),   # Yellow
            '34': QColor(self.colors['accent']),    # Blue
            '35': QColor(self.colors['info']),      # Magenta
            '36': QColor('#39c5cf'),   # Cyan
            '37': QColor(self.colors['text_primary']),  # White
        }
    
    def execute_command(self, command: str, working_dir: str = None):
        """Execute a command and display output"""
        self.append_output(f"\n$ {command}\n", 'command')
        
        self.status_label.setText("● Running")
        self.status_label.setStyleSheet(f"color: {self.colors['warning']};")
        self.stop_btn.setEnabled(True)
        
        def run_in_thread():
            try:
                self.current_process = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    cwd=working_dir
                )
                
                for line in iter(self.current_process.stdout.readline, ''):
                    if line:
                        self.output_queue.put(('output', line))
                
                self.current_process.wait()
                return_code = self.current_process.returncode
                
                self.output_queue.put(('finished', return_code))
                
            except Exception as e:
                self.output_queue.put(('error', str(e)))
        
        thread = threading.Thread(target=run_in_thread, daemon=True)
        thread.start()
    
    def update_output(self):
        """Update output display from queue"""
        try:
            while True:
                msg_type, data = self.output_queue.get_nowait()
                
                if msg_type == 'output':
                    self.append_output(data, 'output')
                elif msg_type == 'finished':
                    self.on_command_finished(data)
                elif msg_type == 'error':
                    self.append_output(f"\nError: {data}\n", 'error')
                    
        except Empty:
            pass
    
    def append_output(self, text: str, style: str = 'output'):
        """Append text to output with styling"""
        cursor = self.output.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        format = QTextCharFormat()
        
        if style == 'command':
            format.setForeground(QColor(self.colors['accent']))
            format.setFontWeight(QFont.Weight.Bold)
        elif style == 'error':
            format.setForeground(QColor(self.colors['danger']))
        elif style == 'success':
            format.setForeground(QColor(self.colors['success']))
        else:
            format.setForeground(QColor(self.colors['text_primary']))
        
        cursor.setCharFormat(format)
        cursor.insertText(text)
        
        # Auto-scroll to bottom
        self.output.setTextCursor(cursor)
        self.output.ensureCursorVisible()
    
    def on_command_finished(self, return_code: int):
        """Handle command completion"""
        self.status_label.setText("● Idle")
        self.status_label.setStyleSheet(f"color: {self.colors['success']};")
        self.stop_btn.setEnabled(False)
        
        if return_code == 0:
            self.append_output(f"\n✓ Command completed successfully\n", 'success')
        else:
            self.append_output(f"\n✗ Command failed (exit code {return_code})\n", 'error')
        
        self.current_process = None
        self.command_finished.emit(return_code, self.output.toPlainText())
    
    def stop_command(self):
        """Terminate running command"""
        if self.current_process:
            self.current_process.terminate()
            self.append_output("\n⚠ Command terminated by user\n", 'warning')
    
    def run_quick_command(self):
        """Execute quick command from input bar"""
        cmd = self.quick_cmd.text().strip()
        if cmd:
            self.execute_command(cmd)
            self.quick_cmd.clear()
    
    def clear_output(self):
        """Clear terminal output"""
        self.output.clear()
    
    def show_context_menu(self, position):
        """Show right-click context menu"""
        menu = QMenu(self)
        
        copy_action = menu.addAction("Copy")
        copy_action.triggered.connect(self.output.copy)
        
        select_all = menu.addAction("Select All")
        select_all.triggered.connect(self.output.selectAll)
        
        menu.addSeparator()
        
        save_output = menu.addAction("Save Output...")
        save_output.triggered.connect(self.save_output)
        
        menu.exec(self.output.mapToGlobal(position))
    
    def save_output(self):
        """Save terminal output to file"""
        from PyQt6.QtWidgets import QFileDialog
        
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Output", "cyberguard_output.txt", "Text Files (*.txt)"
        )
        if path:
            with open(path, 'w') as f:
                f.write(self.output.toPlainText())
