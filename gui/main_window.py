
```python
"""
CyberGuard UI - Main Window
Central hub for all cybersecurity tools
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QPushButton, QLabel, QFrame,
    QScrollArea, QSizePolicy, QMessageBox, QMenuBar,
    QMenu, QStatusBar, QProgressBar, QSplitter
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QAction, QIcon, QFont

from gui.styles import get_colors
from gui.tool_cards import ToolCategoryCard, ToolWidget
from gui.terminal_emulator import TerminalWidget
from tools.reconnaissance import ReconnaissanceTools
from tools.scanning import ScanningTools
from tools.wireless import WirelessTools
from tools.exploitation import ExploitationTools
from tools.forensics import ForensicsTools


class CyberGuardMainWindow(QMainWindow):
    """Main application window with category navigation"""
    
    def __init__(self):
        super().__init__()
        self.colors = get_colors()
        self.current_tool = None
        self.setup_ui()
        self.setup_menu()
        self.setup_status_bar()
        
    def setup_ui(self):
        """Initialize main user interface"""
        self.setWindowTitle("CyberGuard UI - Kali Linux Tools Suite")
        self.setMinimumSize(1400, 900)
        
        # Central widget with horizontal splitter
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Left sidebar - Category navigation
        self.sidebar = self.create_sidebar()
        layout.addWidget(self.sidebar)
        
        # Main content area with splitter
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Tool workspace (center)
        self.workspace = QStackedWidget()
        self.workspace.setMinimumWidth(600)
        
        # Category overview page
        self.overview_page = self.create_overview_page()
        self.workspace.addWidget(self.overview_page)
        
        # Tool pages will be added dynamically
        self.tool_pages = {}
        
        self.splitter.addWidget(self.workspace)
        
        # Right panel - Terminal output
        self.terminal = TerminalWidget()
        self.terminal.setMinimumWidth(400)
        self.splitter.addWidget(self.terminal)
        
        # Set splitter proportions (60% workspace, 40% terminal)
        self.splitter.setSizes([800, 500])
        
        layout.addWidget(self.splitter)
        
    def create_sidebar(self) -> QWidget:
        """Create left navigation sidebar"""
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['surface']};
                border-right: 1px solid {self.colors['border']};
            }}
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(16, 20, 16, 20)
        layout.setSpacing(8)
        
        # Logo/Title
        title = QLabel("🔒 CyberGuard")
        title.setStyleSheet(f"""
            color: {self.colors['accent']};
            font-size: 18px;
            font-weight: bold;
        """)
        layout.addWidget(title)
        
        subtitle = QLabel("Kali Linux GUI Suite")
        subtitle.setStyleSheet(f"color: {self.colors['text_secondary']};")
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # Navigation buttons
        self.nav_buttons = {}
        
        categories = [
            ("🏠", "Overview", "overview"),
            ("🔍", "Reconnaissance", "recon"),
            ("📡", "Network Scanning", "scan"),
            ("📶", "Wireless Attacks", "wireless"),
            ("💥", "Exploitation", "exploit"),
            ("🔬", "Forensics", "forensics"),
        ]
        
        for icon, text, key in categories:
            btn = QPushButton(f"{icon}  {text}")
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    text-align: left;
                    padding: 12px 16px;
                    border: none;
                    border-radius: 8px;
                    color: {self.colors['text_secondary']};
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background-color: {self.colors['surface_hover']};
                    color: {self.colors['text_primary']};
                }}
                QPushButton:checked {{
                    background-color: {self.colors['accent']};
                    color: {self.colors['background']};
                    font-weight: bold;
                }}
            """)
            btn.clicked.connect(lambda checked, k=key: self.navigate_to(k))
            self.nav_buttons[key] = btn
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # Help button at bottom
        help_btn = QPushButton("❓  Help & Documentation")
        help_btn.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding: 12px 16px;
                border: 1px solid {self.colors['border']};
                border-radius: 8px;
                color: {self.colors['text_secondary']};
            }}
            QPushButton:hover {{
                border-color: {self.colors['accent']};
                color: {self.colors['text_primary']};
            }}
        """)
        help_btn.clicked.connect(self.show_help)
        layout.addWidget(help_btn)
        
        return sidebar
    
    def create_overview_page(self) -> QWidget:
        """Create main dashboard/overview page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Welcome header
        header = QLabel("Welcome to CyberGuard UI")
        header.setStyleSheet(f"""
            color: {self.colors['text_primary']};
            font-size: 28px;
            font-weight: bold;
        """)
        layout.addWidget(header)
        
        desc = QLabel("Select a category below to start using Kali Linux security tools with an intuitive interface.")
        desc.setStyleSheet(f"color: {self.colors['text_secondary']}; font-size: 12px;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        layout.addSpacing(20)
        
        # Category grid
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        container = QWidget()
        grid = QHBoxLayout(container)
        grid.setSpacing(20)
        
        # Tool category cards
        categories = [
            {
                'key': 'recon',
                'icon': '🔍',
                'title': 'Reconnaissance',
                'desc': 'Information gathering and footprinting',
                'tools': ['theHarvester', 'Maltego', 'Recon-ng', 'OSINT Framework'],
                'color': self.colors['accent']
            },
            {
                'key': 'scan',
                'icon': '📡',
                'title': 'Network Scanning',
                'desc': 'Port scanning and vulnerability detection',
                'tools': ['Nmap', 'Masscan', 'OpenVAS', 'Nessus'],
                'color': self.colors['success']
            },
            {
                'key': 'wireless',
                'icon': '📶',
                'title': 'Wireless Attacks',
                'desc': 'WiFi security testing and analysis',
                'tools': ['Aircrack-ng', 'Wifite', 'Fern WiFi Cracker', 'Kismet'],
                'color': self.colors['warning']
            },
            {
                'key': 'exploit',
                'icon': '💥',
                'title': 'Exploitation',
                'desc': 'Penetration testing frameworks',
                'tools': ['Metasploit', 'BeEF', 'SQLMap', 'Commix'],
                'color': self.colors['danger']
            },
            {
                'key': 'forensics',
                'icon': '🔬',
                'title': 'Digital Forensics',
                'desc': 'Evidence collection and analysis',
                'tools': ['Autopsy', 'Sleuth Kit', 'Volatility', 'Binwalk'],
                'color': self.colors['info']
            },
        ]
        
        for cat in categories:
            card = ToolCategoryCard(cat, self)
            card.clicked.connect(lambda k=cat['key']: self.navigate_to(k))
            grid.addWidget(card)
        
        grid.addStretch()
        scroll.setWidget(container)
        layout.addWidget(scroll)
        
        # Quick start section
        layout.addSpacing(30)
        quick_label = QLabel("⚡ Quick Start")
        quick_label.setStyleSheet(f"""
            color: {self.colors['text_primary']};
            font-size: 16px;
            font-weight: bold;
        """)
        layout.addWidget(quick_label)
        
        quick_desc = QLabel("New to penetration testing? Start with a basic network scan to learn the workflow.")
        quick_desc.setStyleSheet(f"color: {self.colors['text_secondary']};")
        layout.addWidget(quick_desc)
        
        quick_btn = QPushButton("🚀  Run Quick Network Scan")
        quick_btn.setObjectName("primaryButton")
        quick_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        quick_btn.setFixedWidth(250)
        quick_btn.clicked.connect(lambda: self.navigate_to('scan'))
        layout.addWidget(quick_btn)
        
        layout.addStretch()
        
        return page
    
    def setup_menu(self):
        """Create application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_session = QAction("New Session", self)
        new_session.setShortcut("Ctrl+N")
        file_menu.addAction(new_session)
        
        save_report = QAction("Save Report...", self)
        save_report.setShortcut("Ctrl+S")
        file_menu.addAction(save_report)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        
        update_tools = QAction("Update Kali Tools", self)
        update_tools.triggered.connect(self.update_kali_tools)
        tools_menu.addAction(update_tools)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        docs = QAction("Documentation", self)
        docs.setShortcut("F1")
        docs.triggered.connect(self.show_help)
        help_menu.addAction(docs)
        
        about = QAction("About", self)
        about.triggered.connect(self.show_about)
        help_menu.addAction(about)
    
    def setup_status_bar(self):
        """Create status bar with system info"""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        
        # System status
        self.status_label = QLabel("✓ System Ready")
        self.statusbar.addWidget(self.status_label)
        
        self.statusbar.addStretch()
        
        # Progress indicator
        self.progress = QProgressBar()
        self.progress.setMaximumWidth(150)
        self.progress.setVisible(False)
        self.statusbar.addWidget(self.progress)
        
        # Tool status
        self.tool_status = QLabel("No tool running")
        self.statusbar.addWidget(self.tool_status)
    
    def navigate_to(self, category: str):
        """Navigate to specific category or tool page"""
        # Update sidebar selection
        for key, btn in self.nav_buttons.items():
            btn.setChecked(key == category)
        
        if category == 'overview':
            self.workspace.setCurrentWidget(self.overview_page)
            return
        
        # Create tool page if not exists
        if category not in self.tool_pages:
            page = self.create_tool_page(category)
            self.tool_pages[category] = page
            self.workspace.addWidget(page)
        
        self.workspace.setCurrentWidget(self.tool_pages[category])
    
    def create_tool_page(self, category: str) -> QWidget:
        """Create tool page for specific category"""
        pages = {
            'recon': ReconnaissancePage,
            'scan': ScanningPage,
            'wireless': WirelessPage,
            'exploit': ExploitationPage,
            'forensics': ForensicsPage,
        }
        
        page_class = pages.get(category, QWidget)
        return page_class(self.terminal, self)
    
    def show_help(self):
        """Show help documentation"""
        QMessageBox.information(self, "Help", 
            "CyberGuard UI Help\n\n"
            "1. Select a tool category from the sidebar\n"
            "2. Configure tool parameters in the form\n"
            "3. Click Run to execute the tool\n"
            "4. View output in the terminal panel\n\n"
            "For detailed documentation, visit: https://github.com/cyberguard/ui")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About CyberGuard UI",
            "<h2>CyberGuard UI 1.0</h2>"
            "<p>A beginner-friendly graphical interface for Kali Linux security tools.</p>"
            "<p>Built with PyQt6 for modern Linux distributions.</p>"
            "<p><b>Warning:</b> Only use on systems you own or have explicit permission to test.</p>")
    
    def update_kali_tools(self):
        """Update Kali Linux tools via apt"""
        self.terminal.execute_command("sudo apt update && sudo apt upgrade -y")


# ============== Individual Tool Pages ==============

class ReconnaissancePage(QWidget):
    """Reconnaissance and information gathering tools"""
    
    def __init__(self, terminal, parent=None):
        super().__init__(parent)
        self.terminal = terminal
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = QLabel("🔍 Reconnaissance Tools")
        header.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(header)
        
        desc = QLabel("Gather information about targets without direct interaction")
        desc.setStyleSheet(f"color: {get_colors()['text_secondary']};")
        layout.addWidget(desc)
        
        layout.addSpacing(20)
        
        # Tool: theHarvester
        harvester = ToolWidget(
            "theHarvester",
            "Email harvesting and subdomain discovery",
            [
                {'name': 'domain', 'label': 'Target Domain', 'type': 'text', 
                 'placeholder': 'example.com', 'required': True},
                {'name': 'limit', 'label': 'Result Limit', 'type': 'number', 
                 'default': 500},
                {'name': 'source', 'label': 'Data Sources', 'type': 'multiselect',
                 'options': ['baidu', 'bing', 'google', 'linkedin', 'twitter', 
                           'virustotal', 'threatcrowd', 'crtsh']},
            ],
            self.run_harvester
        )
        layout.addWidget(harvester)
        
        # Tool: Recon-ng
        reconng = ToolWidget(
            "Recon-ng",
            "Web reconnaissance framework with modules",
            [
                {'name': 'workspace', 'label': 'Workspace Name', 'type': 'text',
                 'placeholder': 'my_target'},
                {'name': 'module', 'label': 'Module', 'type': 'select',
                 'options': ['recon/domains-hosts/brute_hosts',
                           'recon/domains-hosts/google_site_web',
                           'recon/hosts-hosts/resolve']},
            ],
            self.run_reconng
        )
        layout.addWidget(reconng)
        
        layout.addStretch()


class ScanningPage(QWidget):
    """Network scanning and vulnerability assessment"""
    
    def __init__(self, terminal, parent=None):
        super().__init__(parent)
        self.terminal = terminal
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        
        header = QLabel("📡 Network Scanning")
        header.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(header)
        
        desc = QLabel("Discover hosts, services, and vulnerabilities on networks")
        desc.setStyleSheet(f"color: {get_colors()['text_secondary']};")
        layout.addWidget(desc)
        
        layout.addSpacing(20)
        
        # Tool: Nmap
        nmap = ToolWidget(
            "Nmap",
            "Network discovery and security auditing",
            [
                {'name': 'target', 'label': 'Target Host/IP', 'type': 'text',
                 'placeholder': '192.168.1.1 or scanme.nmap.org', 'required': True},
                {'name': 'scan_type', 'label': 'Scan Type', 'type': 'select',
                 'options': ['Quick Scan (-F)', 'Intense Scan (-A)', 
                           'Intense Scan + UDP (-sS -sU -A)',
                           'Quick Scan Plus (-sV -T4 -O -F --version-light)',
                           'Ping Scan (-sn)', 'Regular Scan']},
                {'name': 'ports', 'label': 'Port Range', 'type': 'text',
                 'placeholder': '80,443,8080 or 1-1000'},
                {'name': 'timing', 'label': 'Timing Template', 'type': 'select',
                 'options': ['T0 (Paranoid)', 'T1 (Sneaky)', 'T2 (Polite)',
                           'T3 (Normal)', 'T4 (Aggressive)', 'T5 (Insane)']},
                {'name': 'save_output', 'label': 'Save Output', 'type': 'checkbox'},
            ],
            self.run_nmap
        )
        layout.addWidget(nmap)
        
        # Tool: Masscan
        masscan = ToolWidget(
            "Masscan",
            "Internet-scale port scanner (ASYNC)",
            [
                {'name': 'target', 'label': 'Target Range', 'type': 'text',
                 'placeholder': '10.0.0.0/8', 'required': True},
                {'name': 'ports', 'label': 'Ports', 'type': 'text',
                 'placeholder': '0-65535', 'default': '80,443'},
                {'name': 'rate', 'label': 'Packets/Second', 'type': 'number',
                 'default': 1000},
            ],
            self.run_masscan
        )
        layout.addWidget(masscan)
        
        layout.addStretch()
    
    def run_nmap(self, params: dict):
        """Execute nmap with GUI parameters"""
        target = params['target']
        
        scan_types = {
            'Quick Scan (-F)': '-F',
            'Intense Scan (-A)': '-A',
            'Intense Scan + UDP (-sS -sU -A)': '-sS -sU -A',
            'Quick Scan Plus (-sV -T4 -O -F --version-light)': '-sV -T4 -O -F --version-light',
            'Ping Scan (-sn)': '-sn',
            'Regular Scan': ''
        }
        
        cmd = ['nmap']
        cmd.append(scan_types.get(params['scan_type'], ''))
        
        if params.get('ports'):
            cmd.extend(['-p', params['ports']])
        
        if params.get('timing'):
            timing = params['timing'].split()[0]
            cmd.append(f'-{timing.lower()}')
        
        cmd.append(target)
        
        if params.get('save_output'):
            cmd.extend(['-oX', f'nmap_{target.replace("/", "_")}.xml'])
        
        self.terminal.execute_command(' '.join(filter(None, cmd)))


class WirelessPage(QWidget):
    """Wireless security testing tools"""
    
    def __init__(self, terminal, parent=None):
        super().__init__(parent)
        self.terminal = terminal
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        
        header = QLabel("📶 Wireless Security")
        header.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(header)
        
        # Warning banner
        warning = QFrame()
        warning.setStyleSheet(f"""
            background-color: {get_colors()['warning']}20;
            border: 1px solid {get_colors()['warning']};
            border-radius: 8px;
            padding: 15px;
        """)
        warn_layout = QHBoxLayout(warning)
        warn_icon = QLabel("⚠️")
        warn_icon.setStyleSheet("font-size: 24px;")
        warn_layout.addWidget(warn_icon)
        warn_text = QLabel("Wireless testing requires a compatible USB adapter in monitor mode. "
                          "Only test networks you own or have written permission to test.")
        warn_text.setWordWrap(True)
        warn_text.setStyleSheet(f"color: {get_colors()['warning']};")
        warn_layout.addWidget(warn_text, 1)
        layout.addWidget(warning)
        
        layout.addSpacing(20)
        
        # Tool: Aircrack-ng suite
        aircrack = ToolWidget(
            "Aircrack-ng",
            "WEP and WPA/WPA2-PSK key cracking",
            [
                {'name': 'bssid', 'label': 'Target BSSID', 'type': 'text',
                 'placeholder': 'AA:BB:CC:DD:EE:FF'},
                {'name': 'essid', 'label': 'Network Name (ESSID)', 'type': 'text'},
                {'name': 'wordlist', 'label': 'Wordlist Path', 'type': 'file',
                 'default': '/usr/share/wordlists/rockyou.txt'},
                {'name': 'capture', 'label': 'Capture File (.cap)', 'type': 'file'},
            ],
            self.run_aircrack
        )
        layout.addWidget(aircrack)
        
        # Tool: Wifite
        wifite = ToolWidget(
            "Wifite",
            "Automated wireless auditor",
            [
                {'name': 'interface', 'label': 'Wireless Interface', 'type': 'text',
                 'default': 'wlan0mon'},
                {'name': 'wpa', 'label': 'Target WPA only', 'type': 'checkbox',
                 'default': True},
                {'name': 'dict', 'label': 'Dictionary Attack', 'type': 'checkbox'},
                {'name': 'pixie', 'label': 'WPS Pixie Dust Attack', 'type': 'checkbox'},
            ],
            self.run_wifite
        )
        layout.addWidget(wifite)
        
        layout.addStretch()


class ExploitationPage(QWidget):
    """Penetration testing and exploitation frameworks"""
    
    def __init__(self, terminal, parent=None):
        super().__init__(parent)
        self.terminal = terminal
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        
        header = QLabel("💥 Exploitation Frameworks")
        header.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(header)
        
        # Critical warning
        warning = QFrame()
        warning.setStyleSheet(f"""
            background-color: {get_colors()['danger']}20;
            border: 1px solid {get_colors()['danger']};
            border-radius: 8px;
            padding: 15px;
        """)
        warn_layout = QHBoxLayout(warning)
        warn_icon = QLabel("🚨")
        warn_icon.setStyleSheet("font-size: 24px;")
        warn_layout.addWidget(warn_icon)
        warn_text = QLabel("EXPLOITATION TOOLS: These can cause system damage and legal consequences. "
                          "Only use on authorized test systems with proper documentation.")
        warn_text.setWordWrap(True)
        warn_text.setStyleSheet(f"color: {get_colors()['danger']}; font-weight: bold;")
        warn_layout.addWidget(warn_text, 1)
        layout.addWidget(warning)
        
        layout.addSpacing(20)
        
        # Tool: SQLMap
        sqlmap = ToolWidget(
            "SQLMap",
            "Automatic SQL injection and database takeover",
            [
                {'name': 'url', 'label': 'Target URL', 'type': 'text',
                 'placeholder': 'http://target.com/page.php?id=1', 'required': True},
                {'name': 'level', 'label': 'Test Level (1-5)', 'type': 'number',
                 'default': 1, 'min': 1, 'max': 5},
                {'name': 'risk', 'label': 'Risk Level (1-3)', 'type': 'number',
                 'default': 1, 'min': 1, 'max': 3},
                {'name': 'dbs', 'label': 'Enumerate Databases', 'type': 'checkbox'},
                {'name': 'tables', 'label': 'Enumerate Tables', 'type': 'checkbox'},
                {'name': 'dump', 'label': 'Dump Data', 'type': 'checkbox'},
                {'name': 'tor', 'label': 'Use Tor Proxy', 'type': 'checkbox'},
            ],
            self.run_sqlmap
        )
        layout.addWidget(sqlmap)
        
        # Tool: Metasploit quick launcher
        msf = ToolWidget(
            "Metasploit Console",
            "Launch Metasploit Framework console",
            [
                {'name': 'resource', 'label': 'Resource Script (optional)', 'type': 'file'},
                {'name': 'quiet', 'label': 'Quiet Mode', 'type': 'checkbox'},
            ],
            self.run_msfconsole
        )
        layout.addWidget(msf)
        
        layout.addStretch()


class ForensicsPage(QWidget):
    """Digital forensics and incident response"""
    
    def __init__(self, terminal, parent=None):
        super().__init__(parent)
        self.terminal = terminal
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        
        header = QLabel("🔬 Digital Forensics")
        header.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(header)
        
        desc = QLabel("Evidence collection, analysis, and incident response")
        desc.setStyleSheet(f"color: {get_colors()['text_secondary']};")
        layout.addWidget(desc)
        
        layout.addSpacing(20)
        
        # Tool: Autopsy
        autopsy = ToolWidget(
            "Autopsy",
            "Digital forensics platform and GUI for Sleuth Kit",
            [
                {'name': 'case', 'label': 'Case Name', 'type': 'text',
                 'default': 'Case_001'},
                {'name': 'image', 'label': 'Disk Image (optional)', 'type': 'file'},
            ],
            self.run_autopsy
        )
        layout.addWidget(autopsy)
        
        # Tool: Binwalk
        binwalk = ToolWidget(
            "Binwalk",
            "Firmware analysis and extraction",
            [
                {'name': 'file', 'label': 'Target File', 'type': 'file',
                 'required': True},
                {'name': 'extract', 'label': 'Auto-extract Files', 'type': 'checkbox',
                 'default': True},
                {'name': 'depth', 'label': 'Recursion Depth', 'type': 'number',
                 'default': 8},
            ],
            self.run_binwalk
        )
        layout.addWidget(binwalk)
        
        layout.addStretch()
```

