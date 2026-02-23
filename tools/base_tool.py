"""
CyberGuard UI - Base Tool Class
Abstract foundation for all security tools
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Optional, Callable
import subprocess
import threading
import json
import os


@dataclass
class ToolParameter:
    """Definition of a tool parameter"""
    name: str
    label: str
    param_type: str  # 'string', 'integer', 'boolean', 'choice', 'file', 'list'
    required: bool = False
    default: any = None
    description: str = ""
    choices: List[str] = None
    validation_regex: str = None
    sensitive: bool = False  # Mask in logs (passwords, keys)


@dataclass
class ToolResult:
    """Result of tool execution"""
    success: bool
    return_code: int
    stdout: str
    stderr: str
    parsed_output: Dict = None
    output_files: List[str] = None
    execution_time: float = 0.0


class BaseSecurityTool(ABC):
    """Abstract base class for all security tools"""
    
    def __init__(self):
        self.name = self.__class__.__name__
        self.description = ""
        self.version = "unknown"
        self.category = "Uncategorized"
        self.risk_level = "low"  # low, medium, high, critical
        self.requires_root = False
        self.parameters: List[ToolParameter] = []
        self._callbacks: List[Callable] = []
    
    @abstractmethod
    def build_command(self, params: Dict) -> List[str]:
        """Build command-line arguments from parameters"""
        pass
    
    @abstractmethod
    def parse_output(self, stdout: str, stderr: str) -> Dict:
        """Parse tool output into structured data"""
        pass
    
    def validate_parameters(self, params: Dict) -> tuple[bool, str]:
        """Validate input parameters"""
        for param in self.parameters:
            if param.required and not params.get(param.name):
                return False, f"Required parameter '{param.label}' is missing"
            
            value = params.get(param.name)
            if value and param.validation_regex:
                import re
                if not re.match(param.validation_regex, str(value)):
                    return False, f"Invalid format for '{param.label}'"
        
        return True, ""
    
    def execute(self, params: Dict, 
                output_callback: Callable[[str], None] = None,
                progress_callback: Callable[[int], None] = None) -> ToolResult:
        """
        Execute the tool with given parameters
        
        Args:
            params: Parameter dictionary
            output_callback: Called with each line of output
            progress_callback: Called with progress percentage
        
        Returns:
            ToolResult with execution results
        """
        import time
        
        # Validate
        valid, error = self.validate_parameters(params)
        if not valid:
            return ToolResult(False, -1, "", error)
        
        # Build command
        cmd = self.build_command(params)
        
        # Check root requirement
        if self.requires_root and os.geteuid() != 0:
            cmd = ['sudo'] + cmd
        
        # Execute
        start_time = time.time()
        
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            stdout_lines = []
            stderr_lines = []
            
            # Stream output
            while True:
                stdout_line = process.stdout.readline()
                stderr_line = process.stderr.readline()
                
                if stdout_line:
                    stdout_lines.append(stdout_line)
                    if output_callback:
                        output_callback(stdout_line)
                
                if stderr_line:
                    stderr_lines.append(stderr_line)
                    if output_callback:
                        output_callback(f"[stderr] {stderr_line}")
                
                if process.poll() is not None and not stdout_line and not stderr_line:
                    break
            
            process.wait()
            execution_time = time.time() - start_time
            
            stdout = ''.join(stdout_lines)
            stderr = ''.join(stderr_lines)
            
            # Parse structured output
            parsed = self.parse_output(stdout, stderr)
            
            return ToolResult(
                success=process.returncode == 0,
                return_code=process.returncode,
                stdout=stdout,
                stderr=stderr,
                parsed_output=parsed,
                execution_time=execution_time
            )
            
        except Exception as e:
            return ToolResult(False, -1, "", str(e))
    
    def get_documentation(self) -> str:
        """Get tool documentation"""
        docs = f"""
# {self.name}

{self.description}

**Category:** {self.category}
**Risk Level:** {self.risk_level}
**Requires Root:** {'Yes' if self.requires_root else 'No'}

## Parameters
"""
        for param in self.parameters:
            req = " (required)" if param.required else ""
            default = f" [default: {param.default}]" if param.default is not None else ""
            docs += f"\n- **{param.label}** (`{param.param_type}`){req}{default}\n"
            docs += f"  {param.description}\n"
        
        return docs
    
    def to_dict(self) -> Dict:
        """Serialize tool definition"""
        return {
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'risk_level': self.risk_level,
            'requires_root': self.requires_root,
            'parameters': [
                {
                    'name': p.name,
                    'label': p.label,
                    'type': p.param_type,
                    'required': p.required,
                    'default': p.default,
                    'description': p.description,
                    'choices': p.choices
                }
                for p in self.parameters
            ]
        }
