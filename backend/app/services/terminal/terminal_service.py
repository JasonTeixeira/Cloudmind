"""
Integrated Terminal Service
Professional terminal system with session management and command execution
"""

import asyncio
import logging
import os
import subprocess
import signal
import shlex
import tempfile
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple
from uuid import UUID, uuid4
from pathlib import Path
import json
import psutil
import threading
import queue

from app.core.config import settings
from app.schemas.terminal import (
    TerminalSession, TerminalTab, TerminalPane, Command, CommandResult,
    TerminalOutput, TerminalStatus, TerminalType, CommandStatus, OutputType
)

logger = logging.getLogger(__name__)


class ProcessManager:
    """Manages terminal processes and their lifecycle"""
    
    def __init__(self):
        self.processes: Dict[str, subprocess.Popen] = {}
        self.process_metadata: Dict[str, Dict[str, Any]] = {}
        self.output_queues: Dict[str, queue.Queue] = {}
        
    def create_process(
        self, 
        session_id: str, 
        command: str, 
        working_directory: str,
        environment_variables: Dict[str, str] = None
    ) -> subprocess.Popen:
        """Create a new terminal process"""
        try:
            # Prepare environment
            env = os.environ.copy()
            if environment_variables:
                env.update(environment_variables)
            
            # Create process
            process = subprocess.Popen(
                command,
                shell=True,
                cwd=working_directory,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Store process
            self.processes[session_id] = process
            self.process_metadata[session_id] = {
                "command": command,
                "working_directory": working_directory,
                "environment_variables": environment_variables or {},
                "created_at": datetime.utcnow(),
                "status": "running"
            }
            
            # Create output queue
            self.output_queues[session_id] = queue.Queue()
            
            # Start output monitoring
            self._start_output_monitoring(session_id, process)
            
            return process
            
        except Exception as e:
            logger.error(f"Failed to create process for session {session_id}: {e}")
            raise
    
    def kill_process(self, session_id: str) -> bool:
        """Kill a terminal process"""
        try:
            if session_id in self.processes:
                process = self.processes[session_id]
                
                # Try graceful termination first
                process.terminate()
                
                # Wait for termination
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Force kill if needed
                    process.kill()
                    process.wait()
                
                # Cleanup
                del self.processes[session_id]
                if session_id in self.process_metadata:
                    del self.process_metadata[session_id]
                if session_id in self.output_queues:
                    del self.output_queues[session_id]
                
                return True
                
        except Exception as e:
            logger.error(f"Failed to kill process for session {session_id}: {e}")
            return False
    
    def send_input(self, session_id: str, input_data: str) -> bool:
        """Send input to a terminal process"""
        try:
            if session_id in self.processes:
                process = self.processes[session_id]
                process.stdin.write(input_data)
                process.stdin.flush()
                return True
                
        except Exception as e:
            logger.error(f"Failed to send input to session {session_id}: {e}")
            return False
    
    def get_process_status(self, session_id: str) -> Optional[str]:
        """Get process status"""
        if session_id in self.processes:
            process = self.processes[session_id]
            if process.poll() is None:
                return "running"
            else:
                return "stopped"
        return None
    
    def _start_output_monitoring(self, session_id: str, process: subprocess.Popen):
        """Start monitoring process output"""
        def monitor_output():
            try:
                while process.poll() is None:
                    # Read stdout
                    if process.stdout:
                        line = process.stdout.readline()
                        if line:
                            self.output_queues[session_id].put({
                                "type": "stdout",
                                "content": line,
                                "timestamp": datetime.utcnow()
                            })
                    
                    # Read stderr
                    if process.stderr:
                        line = process.stderr.readline()
                        if line:
                            self.output_queues[session_id].put({
                                "type": "stderr",
                                "content": line,
                                "timestamp": datetime.utcnow()
                            })
                    
                    # Small delay to prevent busy waiting
                    asyncio.sleep(0.01)
                    
            except Exception as e:
                logger.error(f"Error monitoring output for session {session_id}: {e}")
        
        # Start monitoring in a separate thread
        thread = threading.Thread(target=monitor_output, daemon=True)
        thread.start()


class TerminalService:
    """Integrated terminal service"""
    
    def __init__(self):
        self.sessions: Dict[str, TerminalSession] = {}
        self.tabs: Dict[str, List[TerminalTab]] = {}
        self.panes: Dict[str, List[TerminalPane]] = {}
        self.commands: Dict[str, List[Command]] = {}
        self.process_manager = ProcessManager()
        self.active_sessions: Dict[str, bool] = {}
        
    async def create_terminal(
        self, 
        project_id: UUID, 
        user_id: UUID,
        name: Optional[str] = None,
        terminal_type: TerminalType = TerminalType.BASH,
        working_directory: Optional[str] = None,
        environment_variables: Dict[str, str] = None,
        custom_shell: Optional[str] = None,
        theme: str = "default",
        columns: int = 80,
        rows: int = 24
    ) -> TerminalSession:
        """Create a new terminal session"""
        try:
            session_id = str(uuid4())
            
            # Determine working directory
            if not working_directory:
                working_directory = str(Path(settings.LOCAL_STORAGE_PATH) / str(project_id))
            
            # Ensure working directory exists
            Path(working_directory).mkdir(parents=True, exist_ok=True)
            
            # Determine shell command
            shell_command = self._get_shell_command(terminal_type, custom_shell)
            
            # Create terminal session
            session = TerminalSession(
                id=session_id,
                project_id=project_id,
                user_id=user_id,
                name=name or f"Terminal-{session_id[:8]}",
                type=terminal_type,
                status=TerminalStatus.CREATED,
                created_at=datetime.utcnow(),
                last_activity=datetime.utcnow(),
                working_directory=working_directory,
                environment_variables=environment_variables or {},
                custom_shell=custom_shell,
                theme=theme,
                columns=columns,
                rows=rows
            )
            
            # Store session
            self.sessions[session_id] = session
            self.tabs[session_id] = []
            self.panes[session_id] = []
            self.commands[session_id] = []
            self.active_sessions[session_id] = True
            
            # Create initial process
            try:
                self.process_manager.create_process(
                    session_id=session_id,
                    command=shell_command,
                    working_directory=working_directory,
                    environment_variables=environment_variables
                )
                session.status = TerminalStatus.RUNNING
            except Exception as e:
                session.status = TerminalStatus.ERROR
                logger.error(f"Failed to create terminal process: {e}")
            
            return session
            
        except Exception as e:
            logger.error(f"Failed to create terminal session: {e}")
            raise
    
    async def execute_command(
        self, 
        session_id: str, 
        command: str,
        working_directory: Optional[str] = None,
        environment_variables: Dict[str, str] = None,
        timeout: Optional[int] = None
    ) -> CommandResult:
        """Execute a command in a terminal session"""
        try:
            if session_id not in self.sessions:
                raise ValueError(f"Terminal session {session_id} not found")
            
            session = self.sessions[session_id]
            command_id = str(uuid4())
            
            # Use session working directory if not specified
            if not working_directory:
                working_directory = session.working_directory
            
            # Merge environment variables
            env_vars = session.environment_variables.copy()
            if environment_variables:
                env_vars.update(environment_variables)
            
            # Create command record
            cmd_record = Command(
                id=command_id,
                session_id=session_id,
                command=command,
                status=CommandStatus.PENDING,
                started_at=datetime.utcnow(),
                working_directory=working_directory,
                environment_variables=env_vars,
                user_id=session.user_id
            )
            
            # Store command
            self.commands[session_id].append(cmd_record)
            
            # Execute command
            start_time = datetime.utcnow()
            
            try:
                # Prepare environment
                env = os.environ.copy()
                env.update(env_vars)
                
                # Execute command
                result = subprocess.run(
                    command,
                    shell=True,
                    cwd=working_directory,
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                
                end_time = datetime.utcnow()
                execution_time = (end_time - start_time).total_seconds()
                
                # Update command record
                cmd_record.status = CommandStatus.COMPLETED
                cmd_record.completed_at = end_time
                cmd_record.exit_code = result.returncode
                
                # Create command result
                command_result = CommandResult(
                    command_id=command_id,
                    success=result.returncode == 0,
                    exit_code=result.returncode,
                    stdout=result.stdout,
                    stderr=result.stderr,
                    execution_time=execution_time,
                    started_at=start_time,
                    completed_at=end_time,
                    working_directory=working_directory
                )
                
                # Update session activity
                session.last_activity = datetime.utcnow()
                
                return command_result
                
            except subprocess.TimeoutExpired:
                cmd_record.status = CommandStatus.TIMEOUT
                cmd_record.completed_at = datetime.utcnow()
                
                return CommandResult(
                    command_id=command_id,
                    success=False,
                    exit_code=-1,
                    stdout="",
                    stderr="Command timed out",
                    execution_time=timeout or 0,
                    started_at=start_time,
                    completed_at=datetime.utcnow(),
                    working_directory=working_directory
                )
                
            except Exception as e:
                cmd_record.status = CommandStatus.FAILED
                cmd_record.completed_at = datetime.utcnow()
                
                return CommandResult(
                    command_id=command_id,
                    success=False,
                    exit_code=-1,
                    stdout="",
                    stderr=str(e),
                    execution_time=(datetime.utcnow() - start_time).total_seconds(),
                    started_at=start_time,
                    completed_at=datetime.utcnow(),
                    working_directory=working_directory
                )
                
        except Exception as e:
            logger.error(f"Failed to execute command: {e}")
            raise
    
    async def send_input(self, session_id: str, input_data: str) -> bool:
        """Send input to a terminal session"""
        try:
            if session_id not in self.sessions:
                return False
            
            # Send input to process
            success = self.process_manager.send_input(session_id, input_data)
            
            if success:
                # Update session activity
                self.sessions[session_id].last_activity = datetime.utcnow()
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to send input: {e}")
            return False
    
    async def get_output(self, session_id: str, limit: int = 100) -> List[TerminalOutput]:
        """Get terminal output"""
        try:
            if session_id not in self.process_manager.output_queues:
                return []
            
            outputs = []
            queue = self.process_manager.output_queues[session_id]
            
            # Get available output
            while not queue.empty() and len(outputs) < limit:
                try:
                    output_data = queue.get_nowait()
                    
                    output = TerminalOutput(
                        session_id=session_id,
                        output_type=OutputType.STDOUT if output_data["type"] == "stdout" else OutputType.STDERR,
                        content=output_data["content"],
                        timestamp=output_data["timestamp"],
                        is_error=output_data["type"] == "stderr"
                    )
                    
                    outputs.append(output)
                    
                except queue.Empty:
                    break
            
            return outputs
            
        except Exception as e:
            logger.error(f"Failed to get output: {e}")
            return []
    
    async def resize_terminal(self, session_id: str, columns: int, rows: int) -> bool:
        """Resize terminal window"""
        try:
            if session_id not in self.sessions:
                return False
            
            session = self.sessions[session_id]
            session.columns = columns
            session.rows = rows
            session.last_activity = datetime.utcnow()
            
            # Send resize signal to process if supported
            if session_id in self.process_manager.processes:
                process = self.process_manager.processes[session_id]
                try:
                    # Send SIGWINCH signal for terminal resize
                    process.send_signal(signal.SIGWINCH)
                except:
                    pass  # Ignore if signal not supported
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to resize terminal: {e}")
            return False
    
    async def kill_process(self, session_id: str) -> bool:
        """Kill terminal process"""
        try:
            success = self.process_manager.kill_process(session_id)
            
            if success and session_id in self.sessions:
                self.sessions[session_id].status = TerminalStatus.KILLED
                self.active_sessions[session_id] = False
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to kill process: {e}")
            return False
    
    async def get_terminal_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get terminal session information"""
        try:
            if session_id not in self.sessions:
                return None
            
            session = self.sessions[session_id]
            session_commands = self.commands.get(session_id, [])
            session_tabs = self.tabs.get(session_id, [])
            
            # Calculate statistics
            total_commands = len(session_commands)
            successful_commands = len([c for c in session_commands if c.status == CommandStatus.COMPLETED])
            failed_commands = total_commands - successful_commands
            
            # Get process status
            process_status = self.process_manager.get_process_status(session_id)
            
            return {
                "session": session,
                "tabs": session_tabs,
                "active_tab": next((tab for tab in session_tabs if tab.is_active), None),
                "recent_commands": session_commands[-10:],  # Last 10 commands
                "statistics": {
                    "total_commands": total_commands,
                    "successful_commands": successful_commands,
                    "failed_commands": failed_commands,
                    "process_status": process_status,
                    "session_duration": (datetime.utcnow() - session.created_at).total_seconds()
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to get terminal info: {e}")
            return None
    
    async def create_tab(self, session_id: str, name: Optional[str] = None) -> Optional[TerminalTab]:
        """Create a new terminal tab"""
        try:
            if session_id not in self.sessions:
                return None
            
            tab_id = str(uuid4())
            session = self.sessions[session_id]
            
            tab = TerminalTab(
                id=tab_id,
                session_id=session_id,
                name=name or f"Tab-{len(self.tabs[session_id]) + 1}",
                status=TerminalStatus.CREATED,
                created_at=datetime.utcnow(),
                last_activity=datetime.utcnow(),
                working_directory=session.working_directory,
                order=len(self.tabs[session_id])
            )
            
            self.tabs[session_id].append(tab)
            return tab
            
        except Exception as e:
            logger.error(f"Failed to create tab: {e}")
            return None
    
    async def switch_tab(self, session_id: str, tab_id: str) -> bool:
        """Switch to a different terminal tab"""
        try:
            if session_id not in self.tabs:
                return False
            
            # Deactivate all tabs
            for tab in self.tabs[session_id]:
                tab.is_active = False
            
            # Activate target tab
            for tab in self.tabs[session_id]:
                if tab.id == tab_id:
                    tab.is_active = True
                    tab.last_activity = datetime.utcnow()
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to switch tab: {e}")
            return False
    
    def _get_shell_command(self, terminal_type: TerminalType, custom_shell: Optional[str] = None) -> str:
        """Get shell command based on terminal type"""
        if custom_shell:
            return custom_shell
        
        shell_commands = {
            TerminalType.BASH: "bash",
            TerminalType.ZSH: "zsh",
            TerminalType.FISH: "fish",
            TerminalType.POWERSHELL: "powershell",
            TerminalType.CMD: "cmd",
        }
        
        return shell_commands.get(terminal_type, "bash")


# Global instance
terminal_service = TerminalService()
