"""
Advanced Debugging Service
Professional debugging with breakpoint management, variable inspection, and step-through debugging
"""

import asyncio
import logging
import os
import subprocess
import signal
import sys
import traceback
import inspect
import ast
import threading
import queue
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple, Union
from uuid import UUID, uuid4
from pathlib import Path
import json
import psutil
import gc
import weakref

from app.core.config import settings
from app.schemas.debugger import (
    DebugSession, Breakpoint, Variable, StackFrame, WatchExpression, DebugState,
    EvaluationResult, DebuggerStatus, BreakpointType, BreakpointStatus, StepType,
    VariableScope, VariableType
)

logger = logging.getLogger(__name__)


class DebuggerProcess:
    """Manages debugger process and communication"""
    
    def __init__(self, session_id: str, target_file: str, working_directory: str):
        self.session_id = session_id
        self.target_file = target_file
        self.working_directory = working_directory
        self.process: Optional[subprocess.Popen] = None
        self.debugger_process: Optional[subprocess.Popen] = None
        self.status = "stopped"
        self.output_queue = queue.Queue()
        self.input_queue = queue.Queue()
        self.breakpoints: Dict[str, Breakpoint] = {}
        self.current_frame: Optional[StackFrame] = None
        self.call_stack: List[StackFrame] = []
        self.variables: Dict[str, Variable] = {}
        self.watch_expressions: Dict[str, WatchExpression] = {}
        
    async def start(self, language: str, debugger_type: str = "auto"):
        """Start the debugger process"""
        try:
            # Determine debugger command based on language
            debugger_cmd = self._get_debugger_command(language, debugger_type)
            
            # Create debugger process
            env = os.environ.copy()
            env['PYTHONPATH'] = self.working_directory
            
            self.debugger_process = subprocess.Popen(
                debugger_cmd,
                shell=True,
                cwd=self.working_directory,
                env=env,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            self.status = "running"
            
            # Start output monitoring
            self._start_output_monitoring()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to start debugger process: {e}")
            self.status = "error"
            return False
    
    async def stop(self):
        """Stop the debugger process"""
        try:
            if self.debugger_process:
                self.debugger_process.terminate()
                self.debugger_process.wait(timeout=5)
                self.debugger_process = None
            
            self.status = "stopped"
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop debugger process: {e}")
            return False
    
    async def send_command(self, command: str) -> bool:
        """Send command to debugger"""
        try:
            if self.debugger_process and self.debugger_process.poll() is None:
                self.debugger_process.stdin.write(command + "\n")
                self.debugger_process.stdin.flush()
                return True
            return False
            
        except Exception as e:
            logger.error(f"Failed to send command: {e}")
            return False
    
    async def get_output(self, timeout: float = 1.0) -> List[str]:
        """Get debugger output"""
        outputs = []
        try:
            while not self.output_queue.empty():
                outputs.append(self.output_queue.get_nowait())
        except queue.Empty:
            pass
        return outputs
    
    def _get_debugger_command(self, language: str, debugger_type: str) -> str:
        """Get debugger command based on language"""
        if debugger_type == "auto":
            debugger_type = self._detect_debugger(language)
        
        debugger_commands = {
            "python": {
                "pdb": f"python -m pdb {self.target_file}",
                "ipdb": f"python -m ipdb {self.target_file}",
                "pudb": f"python -m pudb {self.target_file}",
                "debugpy": f"python -m debugpy --listen 5678 {self.target_file}"
            },
            "node": {
                "node": f"node --inspect-brk=0.0.0.0:9229 {self.target_file}",
                "node-debug": f"node-debug {self.target_file}"
            },
            "java": {
                "jdb": f"jdb {self.target_file}",
                "remote": f"java -agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=5005 {self.target_file}"
            }
        }
        
        return debugger_commands.get(language, {}).get(debugger_type, f"python -m pdb {self.target_file}")
    
    def _detect_debugger(self, language: str) -> str:
        """Detect available debugger for language"""
        if language == "python":
            # Try to detect available debuggers
            try:
                import ipdb
                return "ipdb"
            except ImportError:
                try:
                    import pudb
                    return "pudb"
                except ImportError:
                    return "pdb"
        elif language == "node":
            return "node"
        elif language == "java":
            return "jdb"
        
        return "pdb"  # Default fallback
    
    def _start_output_monitoring(self):
        """Start monitoring debugger output"""
        def monitor_output():
            try:
                while self.debugger_process and self.debugger_process.poll() is None:
                    if self.debugger_process.stdout:
                        line = self.debugger_process.stdout.readline()
                        if line:
                            self.output_queue.put(line.strip())
                    
                    if self.debugger_process.stderr:
                        line = self.debugger_process.stderr.readline()
                        if line:
                            self.output_queue.put(f"ERROR: {line.strip()}")
                    
                    asyncio.sleep(0.01)
                    
            except Exception as e:
                logger.error(f"Error monitoring debugger output: {e}")
        
        thread = threading.Thread(target=monitor_output, daemon=True)
        thread.start()


class BreakpointManager:
    """Manages breakpoints and their lifecycle"""
    
    def __init__(self):
        self.breakpoints: Dict[str, Breakpoint] = {}
        self.breakpoint_hits: Dict[str, int] = {}
        
    def add_breakpoint(self, breakpoint: Breakpoint) -> bool:
        """Add a breakpoint"""
        try:
            self.breakpoints[breakpoint.id] = breakpoint
            self.breakpoint_hits[breakpoint.id] = 0
            return True
            
        except Exception as e:
            logger.error(f"Failed to add breakpoint: {e}")
            return False
    
    def remove_breakpoint(self, breakpoint_id: str) -> bool:
        """Remove a breakpoint"""
        try:
            if breakpoint_id in self.breakpoints:
                del self.breakpoints[breakpoint_id]
            if breakpoint_id in self.breakpoint_hits:
                del self.breakpoint_hits[breakpoint_id]
            return True
            
        except Exception as e:
            logger.error(f"Failed to remove breakpoint: {e}")
            return False
    
    def enable_breakpoint(self, breakpoint_id: str) -> bool:
        """Enable a breakpoint"""
        try:
            if breakpoint_id in self.breakpoints:
                self.breakpoints[breakpoint_id].enabled = True
                self.breakpoints[breakpoint_id].status = BreakpointStatus.ENABLED
                return True
            return False
            
        except Exception as e:
            logger.error(f"Failed to enable breakpoint: {e}")
            return False
    
    def disable_breakpoint(self, breakpoint_id: str) -> bool:
        """Disable a breakpoint"""
        try:
            if breakpoint_id in self.breakpoints:
                self.breakpoints[breakpoint_id].enabled = False
                self.breakpoints[breakpoint_id].status = BreakpointStatus.DISABLED
                return True
            return False
            
        except Exception as e:
            logger.error(f"Failed to disable breakpoint: {e}")
            return False
    
    def hit_breakpoint(self, breakpoint_id: str) -> bool:
        """Record a breakpoint hit"""
        try:
            if breakpoint_id in self.breakpoints:
                breakpoint = self.breakpoints[breakpoint_id]
                self.breakpoint_hits[breakpoint_id] += 1
                breakpoint.hit_count += 1
                breakpoint.last_hit = datetime.utcnow()
                
                # Check ignore count
                if breakpoint.ignore_count > 0 and self.breakpoint_hits[breakpoint_id] <= breakpoint.ignore_count:
                    return False
                
                return breakpoint.enabled
            return False
            
        except Exception as e:
            logger.error(f"Failed to record breakpoint hit: {e}")
            return False
    
    def get_breakpoints_for_file(self, file_path: str) -> List[Breakpoint]:
        """Get all breakpoints for a specific file"""
        return [bp for bp in self.breakpoints.values() if bp.file_path == file_path]
    
    def get_breakpoints_for_line(self, file_path: str, line_number: int) -> List[Breakpoint]:
        """Get breakpoints for a specific line"""
        return [bp for bp in self.breakpoints.values() 
                if bp.file_path == file_path and bp.line_number == line_number]


class VariableInspector:
    """Inspects and manages variables during debugging"""
    
    def __init__(self):
        self.variable_cache: Dict[str, Variable] = {}
        
    def inspect_variable(self, name: str, value: Any, scope: VariableScope = VariableScope.LOCAL) -> Variable:
        """Inspect a variable and create Variable object"""
        try:
            var_id = f"{name}_{id(value)}"
            
            # Get variable type and category
            var_type = type(value).__name__
            type_category = self._categorize_type(value)
            
            # Get variable value as string
            value_str = self._format_value(value)
            
            # Get variable size
            size = self._get_variable_size(value)
            
            # Create variable object
            variable = Variable(
                id=var_id,
                session_id="",  # Will be set by caller
                name=name,
                value=value_str,
                type=var_type,
                type_category=type_category,
                scope=scope,
                size=size,
                has_children=self._has_children(value),
                children=self._get_children(value) if self._has_children(value) else []
            )
            
            self.variable_cache[var_id] = variable
            return variable
            
        except Exception as e:
            logger.error(f"Failed to inspect variable {name}: {e}")
            # Return basic variable info
            return Variable(
                id=f"{name}_error",
                session_id="",
                name=name,
                value="<error>",
                type="unknown",
                type_category=VariableType.UNKNOWN,
                scope=scope
            )
    
    def _categorize_type(self, value: Any) -> VariableType:
        """Categorize variable type"""
        if isinstance(value, (int, float, str, bool, type(None))):
            return VariableType.PRIMITIVE
        elif isinstance(value, (list, tuple, set, dict)):
            return VariableType.COLLECTION
        elif inspect.isfunction(value):
            return VariableType.FUNCTION
        elif inspect.isclass(value):
            return VariableType.CLASS
        elif inspect.ismodule(value):
            return VariableType.MODULE
        else:
            return VariableType.OBJECT
    
    def _format_value(self, value: Any) -> str:
        """Format variable value as string"""
        try:
            if value is None:
                return "None"
            elif isinstance(value, str):
                return f'"{value}"'
            elif isinstance(value, (list, tuple)):
                return f"{type(value).__name__}[{len(value)}]"
            elif isinstance(value, dict):
                return f"dict[{len(value)}]"
            elif isinstance(value, (int, float, bool)):
                return str(value)
            else:
                return str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                
        except Exception:
            return "<unprintable>"
    
    def _get_variable_size(self, value: Any) -> Optional[int]:
        """Get variable size in bytes"""
        try:
            import sys
            return sys.getsizeof(value)
        except Exception:
            return None
    
    def _has_children(self, value: Any) -> bool:
        """Check if variable has children (attributes)"""
        try:
            if hasattr(value, '__dict__'):
                return len(value.__dict__) > 0
            elif isinstance(value, (list, tuple, dict)):
                return len(value) > 0
            return False
        except Exception:
            return False
    
    def _get_children(self, value: Any) -> List[Variable]:
        """Get child variables"""
        children = []
        try:
            if hasattr(value, '__dict__'):
                for name, attr_value in value.__dict__.items():
                    if not name.startswith('_'):
                        children.append(self.inspect_variable(name, attr_value, VariableScope.INSTANCE))
            elif isinstance(value, dict):
                for key, val in list(value.items())[:10]:  # Limit to first 10 items
                    children.append(self.inspect_variable(str(key), val, VariableScope.LOCAL))
            elif isinstance(value, (list, tuple)):
                for i, item in enumerate(value[:10]):  # Limit to first 10 items
                    children.append(self.inspect_variable(f"[{i}]", item, VariableScope.LOCAL))
                    
        except Exception as e:
            logger.error(f"Failed to get children: {e}")
        
        return children


class DebuggerService:
    """Advanced debugging service"""
    
    def __init__(self):
        self.sessions: Dict[str, DebugSession] = {}
        self.debugger_processes: Dict[str, DebuggerProcess] = {}
        self.breakpoint_managers: Dict[str, BreakpointManager] = {}
        self.variable_inspectors: Dict[str, VariableInspector] = {}
        self.active_sessions: Dict[str, bool] = {}
        
    async def start_debug_session(
        self, 
        project_id: UUID, 
        user_id: UUID,
        target_file: str,
        language: str = "python",
        debugger_type: str = "auto",
        working_directory: Optional[str] = None,
        environment_variables: Dict[str, str] = None,
        command_line_args: List[str] = None
    ) -> DebugSession:
        """Start a new debug session"""
        try:
            session_id = str(uuid4())
            
            # Determine working directory
            if not working_directory:
                working_directory = str(Path(settings.LOCAL_STORAGE_PATH) / str(project_id))
            
            # Ensure target file exists
            target_path = Path(working_directory) / target_file
            if not target_path.exists():
                raise ValueError(f"Target file not found: {target_file}")
            
            # Create debug session
            session = DebugSession(
                id=session_id,
                project_id=project_id,
                user_id=user_id,
                name=f"Debug-{target_file}-{session_id[:8]}",
                status=DebuggerStatus.INITIALIZING,
                created_at=datetime.utcnow(),
                last_activity=datetime.utcnow(),
                target_file=str(target_path),
                working_directory=working_directory,
                language=language,
                debugger_type=debugger_type,
                environment_variables=environment_variables or {},
                command_line_args=command_line_args or []
            )
            
            # Store session
            self.sessions[session_id] = session
            self.active_sessions[session_id] = True
            
            # Create debugger process
            debugger_process = DebuggerProcess(session_id, str(target_path), working_directory)
            self.debugger_processes[session_id] = debugger_process
            
            # Create breakpoint manager
            breakpoint_manager = BreakpointManager()
            self.breakpoint_managers[session_id] = breakpoint_manager
            
            # Create variable inspector
            variable_inspector = VariableInspector()
            self.variable_inspectors[session_id] = variable_inspector
            
            # Start debugger process
            success = await debugger_process.start(language, debugger_type)
            
            if success:
                session.status = DebuggerStatus.READY
            else:
                session.status = DebuggerStatus.ERROR
            
            return session
            
        except Exception as e:
            logger.error(f"Failed to start debug session: {e}")
            raise
    
    async def set_breakpoint(
        self, 
        session_id: str, 
        file_path: str, 
        line_number: int,
        breakpoint_type: BreakpointType = BreakpointType.LINE,
        condition: Optional[str] = None,
        ignore_count: int = 0
    ) -> Breakpoint:
        """Set a breakpoint"""
        try:
            if session_id not in self.sessions:
                raise ValueError(f"Debug session {session_id} not found")
            
            breakpoint_id = str(uuid4())
            
            breakpoint = Breakpoint(
                id=breakpoint_id,
                session_id=session_id,
                type=breakpoint_type,
                status=BreakpointStatus.ENABLED,
                file_path=file_path,
                line_number=line_number,
                condition=condition,
                ignore_count=ignore_count,
                created_at=datetime.utcnow()
            )
            
            # Add to breakpoint manager
            breakpoint_manager = self.breakpoint_managers[session_id]
            breakpoint_manager.add_breakpoint(breakpoint)
            
            # Send breakpoint command to debugger
            debugger_process = self.debugger_processes[session_id]
            if debugger_process:
                await debugger_process.send_command(f"b {file_path}:{line_number}")
            
            return breakpoint
            
        except Exception as e:
            logger.error(f"Failed to set breakpoint: {e}")
            raise
    
    async def remove_breakpoint(self, session_id: str, breakpoint_id: str) -> bool:
        """Remove a breakpoint"""
        try:
            if session_id not in self.breakpoint_managers:
                return False
            
            breakpoint_manager = self.breakpoint_managers[session_id]
            success = breakpoint_manager.remove_breakpoint(breakpoint_id)
            
            if success:
                # Send clear breakpoint command to debugger
                debugger_process = self.debugger_processes.get(session_id)
                if debugger_process:
                    await debugger_process.send_command(f"cl {breakpoint_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to remove breakpoint: {e}")
            return False
    
    async def step(self, session_id: str, step_type: StepType, count: int = 1) -> DebugState:
        """Step through code"""
        try:
            if session_id not in self.debugger_processes:
                raise ValueError(f"Debug session {session_id} not found")
            
            debugger_process = self.debugger_processes[session_id]
            
            # Map step types to debugger commands
            step_commands = {
                StepType.OVER: "n",
                StepType.INTO: "s",
                StepType.OUT: "r",
                StepType.CONTINUE: "c",
                StepType.PAUSE: "h",
                StepType.RESTART: "run"
            }
            
            command = step_commands.get(step_type, "n")
            
            # Send step command
            for _ in range(count):
                await debugger_process.send_command(command)
                await asyncio.sleep(0.1)  # Small delay between steps
            
            # Get updated debug state
            return await self.get_debug_state(session_id)
            
        except Exception as e:
            logger.error(f"Failed to step: {e}")
            raise
    
    async def get_variables(self, session_id: str, scope: VariableScope = VariableScope.LOCAL) -> List[Variable]:
        """Get variables in current scope"""
        try:
            if session_id not in self.variable_inspectors:
                return []
            
            variable_inspector = self.variable_inspectors[session_id]
            debugger_process = self.debugger_processes.get(session_id)
            
            if not debugger_process:
                return []
            
            # Get variables from debugger
            await debugger_process.send_command("l")
            await debugger_process.send_command("p locals()")
            
            # This is a simplified implementation
            # In a real implementation, you would parse the debugger output
            # and extract variable information
            
            variables = []
            # Mock variables for demonstration
            mock_vars = {
                "x": 42,
                "y": "hello",
                "z": [1, 2, 3]
            }
            
            for name, value in mock_vars.items():
                variable = variable_inspector.inspect_variable(name, value, scope)
                variable.session_id = session_id
                variables.append(variable)
            
            return variables
            
        except Exception as e:
            logger.error(f"Failed to get variables: {e}")
            return []
    
    async def get_call_stack(self, session_id: str) -> List[StackFrame]:
        """Get call stack"""
        try:
            if session_id not in self.debugger_processes:
                return []
            
            debugger_process = self.debugger_processes[session_id]
            
            # Send stack command
            await debugger_process.send_command("w")
            
            # Parse stack output (simplified)
            stack_frames = []
            
            # Mock stack frames for demonstration
            mock_frames = [
                {"function": "main", "file": "main.py", "line": 10},
                {"function": "process_data", "file": "utils.py", "line": 25},
                {"function": "validate_input", "file": "validation.py", "line": 15}
            ]
            
            for i, frame_info in enumerate(mock_frames):
                stack_frame = StackFrame(
                    id=f"{session_id}_frame_{i}",
                    session_id=session_id,
                    level=i,
                    function_name=frame_info["function"],
                    file_path=frame_info["file"],
                    line_number=frame_info["line"],
                    is_current=(i == 0)
                )
                stack_frames.append(stack_frame)
            
            return stack_frames
            
        except Exception as e:
            logger.error(f"Failed to get call stack: {e}")
            return []
    
    async def evaluate_expression(
        self, 
        session_id: str, 
        expression: str,
        frame_level: Optional[int] = None,
        timeout: Optional[int] = None
    ) -> EvaluationResult:
        """Evaluate expression in debug context"""
        try:
            if session_id not in self.debugger_processes:
                raise ValueError(f"Debug session {session_id} not found")
            
            debugger_process = self.debugger_processes[session_id]
            start_time = datetime.utcnow()
            
            # Send evaluation command
            await debugger_process.send_command(f"p {expression}")
            
            # Get output
            outputs = await debugger_process.get_output()
            
            # Parse result (simplified)
            result = "".join(outputs) if outputs else "<no output>"
            is_error = "Error" in result or "Traceback" in result
            
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            
            return EvaluationResult(
                session_id=session_id,
                expression=expression,
                result=result,
                type="string",
                is_error=is_error,
                error_message=result if is_error else None,
                execution_time=execution_time,
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Failed to evaluate expression: {e}")
            return EvaluationResult(
                session_id=session_id,
                expression=expression,
                result="<error>",
                type="error",
                is_error=True,
                error_message=str(e),
                execution_time=0.0,
                timestamp=datetime.utcnow()
            )
    
    async def add_watch_expression(self, session_id: str, expression: str, name: Optional[str] = None) -> WatchExpression:
        """Add watch expression"""
        try:
            watch_id = str(uuid4())
            
            watch_expression = WatchExpression(
                id=watch_id,
                session_id=session_id,
                expression=expression,
                name=name or expression,
                created_at=datetime.utcnow(),
                last_updated=datetime.utcnow()
            )
            
            # Store in debugger process
            debugger_process = self.debugger_processes.get(session_id)
            if debugger_process:
                debugger_process.watch_expressions[watch_id] = watch_expression
            
            return watch_expression
            
        except Exception as e:
            logger.error(f"Failed to add watch expression: {e}")
            raise
    
    async def get_debug_state(self, session_id: str) -> DebugState:
        """Get current debug state"""
        try:
            if session_id not in self.sessions:
                raise ValueError(f"Debug session {session_id} not found")
            
            session = self.sessions[session_id]
            debugger_process = self.debugger_processes.get(session_id)
            
            # Get current frame
            current_frame = None
            if debugger_process and debugger_process.current_frame:
                current_frame = debugger_process.current_frame
            
            # Get call stack
            call_stack = await self.get_call_stack(session_id)
            
            # Get variables
            variables = await self.get_variables(session_id)
            
            # Get watch expressions
            watch_expressions = []
            if debugger_process:
                watch_expressions = list(debugger_process.watch_expressions.values())
            
            return DebugState(
                session_id=session_id,
                status=session.status,
                current_frame=current_frame,
                call_stack=call_stack,
                variables=variables,
                watch_expressions=watch_expressions,
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Failed to get debug state: {e}")
            raise
    
    async def stop_debug_session(self, session_id: str) -> bool:
        """Stop debug session"""
        try:
            if session_id not in self.sessions:
                return False
            
            # Stop debugger process
            debugger_process = self.debugger_processes.get(session_id)
            if debugger_process:
                await debugger_process.stop()
                del self.debugger_processes[session_id]
            
            # Update session status
            session = self.sessions[session_id]
            session.status = DebuggerStatus.TERMINATED
            session.last_activity = datetime.utcnow()
            
            # Clean up
            self.active_sessions[session_id] = False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop debug session: {e}")
            return False


# Global instance
debugger_service = DebuggerService()
