"""
Advanced Performance Profiling Service
Professional profiling with CPU, memory, and call graph analysis
"""

import asyncio
import logging
import os
import sys
import time
import psutil
import gc
import threading
import queue
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple, Union
from uuid import UUID, uuid4
from pathlib import Path
import json
import cProfile
import pstats
import io
import tracemalloc
try:
    import line_profiler  # type: ignore
except Exception:  # pragma: no cover
    line_profiler = None
try:
    import memory_profiler  # type: ignore
except Exception:  # pragma: no cover
    memory_profiler = None
from collections import defaultdict, Counter

from app.core.config import settings
from app.schemas.debugger import (
    ProfileSession, ProfileData, PerformanceAnalysis, MemoryUsage,
    ProfilerType
)

logger = logging.getLogger(__name__)


class CPUProfiler:
    """CPU profiling with detailed function analysis"""
    
    def __init__(self):
        self.profiler = cProfile.Profile()
        self.is_running = False
        self.start_time = None
        self.end_time = None
        
    def start(self):
        """Start CPU profiling"""
        try:
            self.profiler.enable()
            self.is_running = True
            self.start_time = datetime.utcnow()
            logger.info("CPU profiling started")
            
        except Exception as e:
            logger.error(f"Failed to start CPU profiling: {e}")
            raise
    
    def stop(self) -> Dict[str, Any]:
        """Stop CPU profiling and return results"""
        try:
            if not self.is_running:
                return {}
            
            self.profiler.disable()
            self.is_running = False
            self.end_time = datetime.utcnow()
            
            # Get profiling statistics
            s = io.StringIO()
            stats = pstats.Stats(self.profiler, stream=s)
            stats.sort_stats('cumulative')
            stats.print_stats(50)  # Top 50 functions
            
            # Parse statistics
            stats_data = self._parse_stats(stats)
            
            logger.info("CPU profiling stopped")
            return stats_data
            
        except Exception as e:
            logger.error(f"Failed to stop CPU profiling: {e}")
            return {}
    
    def _parse_stats(self, stats: pstats.Stats) -> Dict[str, Any]:
        """Parse profiling statistics"""
        try:
            # Get function statistics
            function_stats = []
            for func, (cc, nc, tt, ct, callers) in stats.stats.items():
                filename, line_number, function_name = func
                
                function_stats.append({
                    "function": function_name,
                    "filename": filename,
                    "line_number": line_number,
                    "call_count": nc,
                    "total_time": tt,
                    "cumulative_time": ct,
                    "time_per_call": tt / nc if nc > 0 else 0,
                    "cumulative_time_per_call": ct / nc if nc > 0 else 0
                })
            
            # Sort by cumulative time
            function_stats.sort(key=lambda x: x["cumulative_time"], reverse=True)
            
            # Calculate summary statistics
            total_calls = sum(f["call_count"] for f in function_stats)
            total_time = sum(f["total_time"] for f in function_stats)
            
            return {
                "function_stats": function_stats,
                "summary": {
                    "total_calls": total_calls,
                    "total_time": total_time,
                    "profiled_functions": len(function_stats),
                    "top_functions": function_stats[:10]
                },
                "bottlenecks": self._identify_bottlenecks(function_stats),
                "recommendations": self._generate_recommendations(function_stats)
            }
            
        except Exception as e:
            logger.error(f"Failed to parse stats: {e}")
            return {}


class MemoryProfiler:
    """Memory profiling with leak detection"""
    
    def __init__(self):
        self.tracemalloc = tracemalloc
        self.snapshots = []
        self.is_running = False
        self.start_time = None
        self.end_time = None
        
    def start(self):
        """Start memory profiling"""
        try:
            self.tracemalloc.start()
            self.is_running = True
            self.start_time = datetime.utcnow()
            
            # Take initial snapshot
            self.snapshots.append({
                "timestamp": self.start_time,
                "snapshot": self.tracemalloc.take_snapshot()
            })
            
            logger.info("Memory profiling started")
            
        except Exception as e:
            logger.error(f"Failed to start memory profiling: {e}")
            raise
    
    def take_snapshot(self):
        """Take a memory snapshot"""
        try:
            if self.is_running:
                snapshot_data = {
                    "timestamp": datetime.utcnow(),
                    "snapshot": self.tracemalloc.take_snapshot()
                }
                self.snapshots.append(snapshot_data)
                
        except Exception as e:
            logger.error(f"Failed to take memory snapshot: {e}")
    
    def stop(self) -> Dict[str, Any]:
        """Stop memory profiling and return results"""
        try:
            if not self.is_running:
                return {}
            
            self.end_time = datetime.utcnow()
            self.is_running = False
            
            # Take final snapshot
            final_snapshot = self.tracemalloc.take_snapshot()
            self.snapshots.append({
                "timestamp": self.end_time,
                "snapshot": final_snapshot
            })
            
            # Analyze memory usage
            memory_data = self._analyze_memory_usage()
            
            self.tracemalloc.stop()
            logger.info("Memory profiling stopped")
            
            return memory_data
            
        except Exception as e:
            logger.error(f"Failed to stop memory profiling: {e}")
            return {}
    
    def _analyze_memory_usage(self) -> Dict[str, Any]:
        """Analyze memory usage patterns"""
        try:
            if len(self.snapshots) < 2:
                return {}
            
            # Compare first and last snapshots
            first_snapshot = self.snapshots[0]["snapshot"]
            last_snapshot = self.snapshots[-1]["snapshot"]
            
            # Get top memory allocations
            top_stats = last_snapshot.statistics('filename')
            
            # Calculate memory growth
            memory_growth = []
            for i in range(1, len(self.snapshots)):
                prev_snapshot = self.snapshots[i-1]["snapshot"]
                curr_snapshot = self.snapshots[i]["snapshot"]
                
                stats = curr_snapshot.compare_to(prev_snapshot, 'filename')
                memory_growth.extend(stats)
            
            # Detect potential memory leaks
            memory_leaks = self._detect_memory_leaks(memory_growth)
            
            # Get current memory usage
            current_memory = psutil.Process().memory_info()
            
            return {
                "current_memory": {
                    "rss": current_memory.rss,
                    "vms": current_memory.vms,
                    "percent": psutil.Process().memory_percent()
                },
                "top_allocations": [
                    {
                        "filename": stat.traceback.format()[-1],
                        "size": stat.size,
                        "count": stat.count
                    }
                    for stat in top_stats[:20]
                ],
                "memory_growth": [
                    {
                        "filename": stat.traceback.format()[-1],
                        "size_diff": stat.size_diff,
                        "count_diff": stat.count_diff
                    }
                    for stat in memory_growth[:20]
                ],
                "memory_leaks": memory_leaks,
                "snapshots": len(self.snapshots),
                "duration": (self.end_time - self.start_time).total_seconds()
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze memory usage: {e}")
            return {}
    
    def _detect_memory_leaks(self, memory_growth: List) -> List[Dict[str, Any]]:
        """Detect potential memory leaks"""
        leaks = []
        
        try:
            for stat in memory_growth:
                # Consider it a potential leak if memory grew significantly
                if stat.size_diff > 1024 * 1024:  # 1MB threshold
                    leaks.append({
                        "filename": stat.traceback.format()[-1],
                        "size_growth": stat.size_diff,
                        "count_growth": stat.count_diff,
                        "severity": "high" if stat.size_diff > 10 * 1024 * 1024 else "medium"
                    })
            
            return leaks
            
        except Exception as e:
            logger.error(f"Failed to detect memory leaks: {e}")
            return leaks


class CallGraphProfiler:
    """Call graph profiling with function relationships"""
    
    def __init__(self):
        self.call_graph = defaultdict(list)
        self.function_stats = defaultdict(lambda: {
            "call_count": 0,
            "total_time": 0.0,
            "callers": set(),
            "callees": set()
        })
        self.is_running = False
        
    def start(self):
        """Start call graph profiling"""
        try:
            self.is_running = True
            logger.info("Call graph profiling started")
            
        except Exception as e:
            logger.error(f"Failed to start call graph profiling: {e}")
            raise
    
    def record_call(self, caller: str, callee: str, duration: float):
        """Record a function call"""
        try:
            if not self.is_running:
                return
            
            # Record call relationship
            self.call_graph[caller].append(callee)
            
            # Update statistics
            self.function_stats[caller]["call_count"] += 1
            self.function_stats[caller]["callees"].add(callee)
            
            self.function_stats[callee]["call_count"] += 1
            self.function_stats[callee]["total_time"] += duration
            self.function_stats[callee]["callers"].add(caller)
            
        except Exception as e:
            logger.error(f"Failed to record call: {e}")
    
    def stop(self) -> Dict[str, Any]:
        """Stop call graph profiling and return results"""
        try:
            if not self.is_running:
                return {}
            
            self.is_running = False
            
            # Analyze call graph
            analysis = self._analyze_call_graph()
            
            logger.info("Call graph profiling stopped")
            return analysis
            
        except Exception as e:
            logger.error(f"Failed to stop call graph profiling: {e}")
            return {}
    
    def _analyze_call_graph(self) -> Dict[str, Any]:
        """Analyze call graph structure"""
        try:
            # Find most called functions
            most_called = sorted(
                self.function_stats.items(),
                key=lambda x: x[1]["call_count"],
                reverse=True
            )[:20]
            
            # Find functions with highest execution time
            slowest_functions = sorted(
                self.function_stats.items(),
                key=lambda x: x[1]["total_time"],
                reverse=True
            )[:20]
            
            # Find functions with most callers (bottlenecks)
            bottleneck_functions = sorted(
                self.function_stats.items(),
                key=lambda x: len(x[1]["callers"]),
                reverse=True
            )[:20]
            
            # Calculate call graph metrics
            total_functions = len(self.function_stats)
            total_calls = sum(stats["call_count"] for stats in self.function_stats.values())
            
            return {
                "summary": {
                    "total_functions": total_functions,
                    "total_calls": total_calls,
                    "average_calls_per_function": total_calls / total_functions if total_functions > 0 else 0
                },
                "most_called_functions": [
                    {
                        "function": func,
                        "call_count": stats["call_count"],
                        "total_time": stats["total_time"],
                        "callers": list(stats["callers"]),
                        "callees": list(stats["callees"])
                    }
                    for func, stats in most_called
                ],
                "slowest_functions": [
                    {
                        "function": func,
                        "total_time": stats["total_time"],
                        "call_count": stats["call_count"],
                        "average_time": stats["total_time"] / stats["call_count"] if stats["call_count"] > 0 else 0
                    }
                    for func, stats in slowest_functions
                ],
                "bottleneck_functions": [
                    {
                        "function": func,
                        "caller_count": len(stats["callers"]),
                        "callers": list(stats["callers"]),
                        "total_time": stats["total_time"]
                    }
                    for func, stats in bottleneck_functions
                ],
                "call_graph": dict(self.call_graph)
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze call graph: {e}")
            return {}


class LineProfiler:
    """Line-by-line profiling"""
    
    def __init__(self):
        if line_profiler is None:
            raise ImportError("line_profiler is not installed")
        self.profiler = line_profiler.LineProfiler()
        self.is_running = False
        self.profiled_functions = []
        
    def add_function(self, function):
        """Add function to line profiler"""
        try:
            self.profiler.add_function(function)
            self.profiled_functions.append(function.__name__)
            
        except Exception as e:
            logger.error(f"Failed to add function to line profiler: {e}")
    
    def start(self):
        """Start line profiling"""
        try:
            self.profiler.enable_by_count()
            self.is_running = True
            logger.info("Line profiling started")
            
        except Exception as e:
            logger.error(f"Failed to start line profiling: {e}")
            raise
    
    def stop(self) -> Dict[str, Any]:
        """Stop line profiling and return results"""
        try:
            if not self.is_running:
                return {}
            
            self.profiler.disable_by_count()
            self.is_running = False
            
            # Get line-by-line statistics
            stats = self.profiler.get_stats()
            
            # Parse line statistics
            line_stats = self._parse_line_stats(stats)
            
            logger.info("Line profiling stopped")
            return line_stats
            
        except Exception as e:
            logger.error(f"Failed to stop line profiling: {e}")
            return {}
    
    def _parse_line_stats(self, stats) -> Dict[str, Any]:
        """Parse line-by-line statistics"""
        try:
            line_data = {}
            
            for func_name, (filename, first_lineno, func) in stats.timings.items():
                if func_name in stats.timings:
                    timings = stats.timings[func_name]
                    
                    line_stats = []
                    for line_no, (nhits, total_time) in timings.items():
                        line_stats.append({
                            "line_number": line_no,
                            "hits": nhits,
                            "total_time": total_time,
                            "time_per_hit": total_time / nhits if nhits > 0 else 0
                        })
                    
                    # Sort by total time
                    line_stats.sort(key=lambda x: x["total_time"], reverse=True)
                    
                    line_data[func_name] = {
                        "filename": filename,
                        "first_line": first_lineno,
                        "line_stats": line_stats,
                        "total_lines": len(line_stats),
                        "slowest_lines": line_stats[:10]
                    }
            
            return {
                "functions": line_data,
                "summary": {
                    "profiled_functions": len(line_data),
                    "total_lines": sum(data["total_lines"] for data in line_data.values())
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to parse line stats: {e}")
            return {}


class PerformanceProfiler:
    """Main performance profiling service"""
    
    def __init__(self):
        self.profiling_sessions: Dict[str, ProfileSession] = {}
        self.active_profilers: Dict[str, Dict[str, Any]] = {}
        self.profiler_results: Dict[str, Dict[str, Any]] = {}
        
    async def start_profiling(
        self, 
        debug_session_id: str,
        profiler_type: ProfilerType,
        configuration: Dict[str, Any] = None
    ) -> ProfileSession:
        """Start a profiling session"""
        try:
            session_id = str(uuid4())
            configuration = configuration or {}
            
            # Create profiling session
            session = ProfileSession(
                id=session_id,
                debug_session_id=debug_session_id,
                profiler_type=profiler_type,
                status="starting",
                created_at=datetime.utcnow(),
                configuration=configuration
            )
            
            # Initialize profilers based on type
            profilers = {}
            
            if profiler_type in [ProfilerType.CPU, ProfilerType.CALL_GRAPH]:
                profilers["cpu"] = CPUProfiler()
                profilers["call_graph"] = CallGraphProfiler()
            
            if profiler_type in [ProfilerType.MEMORY, ProfilerType.MEMORY_PROFILER]:
                profilers["memory"] = MemoryProfiler()
            
            if profiler_type == ProfilerType.LINE_PROFILER:
                profilers["line"] = LineProfiler()
            
            # Start profilers
            for profiler_name, profiler in profilers.items():
                try:
                    profiler.start()
                except Exception as e:
                    logger.error(f"Failed to start {profiler_name} profiler: {e}")
            
            # Store session and profilers
            self.profiling_sessions[session_id] = session
            self.active_profilers[session_id] = profilers
            
            session.status = "running"
            session.started_at = datetime.utcnow()
            
            return session
            
        except Exception as e:
            logger.error(f"Failed to start profiling: {e}")
            raise
    
    async def stop_profiling(self, session_id: str) -> ProfileData:
        """Stop profiling session and return results"""
        try:
            if session_id not in self.profiling_sessions:
                raise ValueError(f"Profiling session {session_id} not found")
            
            session = self.profiling_sessions[session_id]
            profilers = self.active_profilers.get(session_id, {})
            
            # Stop all profilers
            results = {}
            for profiler_name, profiler in profilers.items():
                try:
                    if hasattr(profiler, 'stop'):
                        results[profiler_name] = profiler.stop()
                except Exception as e:
                    logger.error(f"Failed to stop {profiler_name} profiler: {e}")
                    results[profiler_name] = {}
            
            # Update session
            session.status = "completed"
            session.stopped_at = datetime.utcnow()
            if session.started_at:
                session.duration = (session.stopped_at - session.started_at).total_seconds()
            
            # Create profile data
            profile_data = ProfileData(
                session_id=session_id,
                profiler_type=session.profiler_type,
                data=results,
                summary=self._generate_summary(results),
                timestamp=datetime.utcnow()
            )
            
            # Store results
            self.profiler_results[session_id] = results
            
            # Clean up
            del self.active_profilers[session_id]
            
            return profile_data
            
        except Exception as e:
            logger.error(f"Failed to stop profiling: {e}")
            raise
    
    async def get_profiling_results(self, session_id: str) -> Optional[ProfileData]:
        """Get profiling results for a session"""
        try:
            if session_id not in self.profiler_results:
                return None
            
            results = self.profiler_results[session_id]
            session = self.profiling_sessions.get(session_id)
            
            if not session:
                return None
            
            return ProfileData(
                session_id=session_id,
                profiler_type=session.profiler_type,
                data=results,
                summary=self._generate_summary(results),
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Failed to get profiling results: {e}")
            return None
    
    async def analyze_performance(self, session_id: str) -> PerformanceAnalysis:
        """Analyze performance and generate recommendations"""
        try:
            profile_data = await self.get_profiling_results(session_id)
            if not profile_data:
                raise ValueError(f"No profiling data found for session {session_id}")
            
            # Analyze bottlenecks
            bottlenecks = self._identify_bottlenecks(profile_data.data)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(profile_data.data)
            
            # Calculate metrics
            metrics = self._calculate_metrics(profile_data.data)
            
            return PerformanceAnalysis(
                session_id=session_id,
                analysis_type="comprehensive",
                bottlenecks=bottlenecks,
                recommendations=recommendations,
                metrics=metrics,
                generated_at=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Failed to analyze performance: {e}")
            raise
    
    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary from profiling results"""
        try:
            summary = {
                "profiler_count": len(results),
                "profiler_types": list(results.keys()),
                "total_data_points": 0
            }
            
            for profiler_name, profiler_data in results.items():
                if "summary" in profiler_data:
                    summary[f"{profiler_name}_summary"] = profiler_data["summary"]
                
                if "function_stats" in profiler_data:
                    summary["total_data_points"] += len(profiler_data["function_stats"])
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to generate summary: {e}")
            return {}
    
    def _identify_bottlenecks(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify performance bottlenecks"""
        bottlenecks = []
        
        try:
            # CPU bottlenecks
            if "cpu" in results and "function_stats" in results["cpu"]:
                cpu_stats = results["cpu"]["function_stats"]
                for func in cpu_stats[:5]:  # Top 5 slowest functions
                    bottlenecks.append({
                        "type": "cpu",
                        "function": func["function"],
                        "filename": func["filename"],
                        "line_number": func["line_number"],
                        "total_time": func["total_time"],
                        "call_count": func["call_count"],
                        "severity": "high" if func["total_time"] > 1.0 else "medium"
                    })
            
            # Memory bottlenecks
            if "memory" in results and "memory_leaks" in results["memory"]:
                for leak in results["memory"]["memory_leaks"]:
                    bottlenecks.append({
                        "type": "memory",
                        "filename": leak["filename"],
                        "size_growth": leak["size_growth"],
                        "severity": leak["severity"],
                        "description": "Potential memory leak detected"
                    })
            
            return bottlenecks
            
        except Exception as e:
            logger.error(f"Failed to identify bottlenecks: {e}")
            return bottlenecks
    
    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []
        
        try:
            # CPU optimization recommendations
            if "cpu" in results and "function_stats" in results["cpu"]:
                cpu_stats = results["cpu"]["function_stats"]
                if cpu_stats:
                    slowest_func = cpu_stats[0]
                    if slowest_func["total_time"] > 1.0:
                        recommendations.append(
                            f"Optimize function '{slowest_func['function']}' - "
                            f"takes {slowest_func['total_time']:.2f}s total time"
                        )
            
            # Memory optimization recommendations
            if "memory" in results and "memory_leaks" in results["memory"]:
                leak_count = len(results["memory"]["memory_leaks"])
                if leak_count > 0:
                    recommendations.append(
                        f"Investigate {leak_count} potential memory leaks detected"
                    )
            
            # General recommendations
            if not recommendations:
                recommendations.append("Performance appears to be within acceptable limits")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Failed to generate recommendations: {e}")
            return ["Unable to generate recommendations due to error"]
    
    def _calculate_metrics(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate performance metrics"""
        try:
            metrics = {
                "total_profiling_time": 0,
                "functions_profiled": 0,
                "memory_usage": 0,
                "cpu_usage": 0
            }
            
            # Calculate metrics from results
            for profiler_name, profiler_data in results.items():
                if "summary" in profiler_data:
                    summary = profiler_data["summary"]
                    if "total_time" in summary:
                        metrics["cpu_usage"] += summary["total_time"]
                    if "profiled_functions" in summary:
                        metrics["functions_profiled"] += summary["profiled_functions"]
                
                if "current_memory" in profiler_data:
                    memory_info = profiler_data["current_memory"]
                    metrics["memory_usage"] = memory_info.get("rss", 0)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to calculate metrics: {e}")
            return {}


# Global instance
performance_profiler = PerformanceProfiler()
