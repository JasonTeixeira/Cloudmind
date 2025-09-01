"""
Automation Engine for CloudMind
Advanced automation workflows and decision making for cloud optimization
"""

import logging
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union, Callable
from dataclasses import dataclass
from enum import Enum
import json
import uuid

from app.core.config import settings
from app.services.optimization.ml_optimizer import ml_optimizer, OptimizationType, OptimizationRecommendation
from app.services.ai_engine.ensemble_ai import ensemble_ai, ConsensusMethod
from app.services.ai_engine.god_tier_ai_service import AnalysisType
from app.utils.retry import async_with_retries, TransientError

logger = logging.getLogger(__name__)


class AutomationTrigger(Enum):
    """Types of automation triggers"""
    SCHEDULED = "scheduled"
    THRESHOLD_BREACH = "threshold_breach"
    MANUAL = "manual"
    AI_RECOMMENDATION = "ai_recommendation"
    COST_ALERT = "cost_alert"
    PERFORMANCE_ALERT = "performance_alert"


class AutomationStatus(Enum):
    """Automation workflow status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AutomationPriority(Enum):
    """Automation priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AutomationWorkflow:
    """Automation workflow definition"""
    workflow_id: str
    name: str
    description: str
    trigger: AutomationTrigger
    priority: AutomationPriority
    steps: List[Dict[str, Any]]
    conditions: Dict[str, Any]
    schedule: Optional[str] = None  # Cron expression for scheduled triggers
    enabled: bool = True
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)


@dataclass
class AutomationExecution:
    """Automation execution instance"""
    execution_id: str
    workflow_id: str
    status: AutomationStatus
    trigger_data: Dict[str, Any]
    results: Dict[str, Any]
    error_message: Optional[str] = None
    started_at: datetime = None
    completed_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.started_at is None:
            self.started_at = datetime.now(timezone.utc)


@dataclass
class AutomationDecision:
    """Automation decision result"""
    decision_id: str
    workflow_id: str
    decision_type: str
    decision: str  # "approve", "reject", "require_manual_review"
    confidence_score: float
    reasoning: str
    recommendations: List[str]
    risk_assessment: Dict[str, Any]
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)


class AutomationEngine:
    """Advanced automation engine for cloud optimization"""
    
    def __init__(self):
        self.workflows: Dict[str, AutomationWorkflow] = {}
        self.executions: List[AutomationExecution] = []
        self.decisions: List[AutomationDecision] = []
        self.running_executions: Dict[str, asyncio.Task] = {}
        
        # Initialize default workflows
        self._initialize_default_workflows()
        
        logger.info("🤖 Automation Engine initialized")
    
    def _initialize_default_workflows(self):
        """Initialize default automation workflows"""
        try:
            # Cost optimization workflow
            cost_workflow = AutomationWorkflow(
                workflow_id="cost_optimization_auto",
                name="Automated Cost Optimization",
                description="Automatically optimize costs when thresholds are breached",
                trigger=AutomationTrigger.THRESHOLD_BREACH,
                priority=AutomationPriority.HIGH,
                steps=[
                    {
                        "step_id": "analyze_costs",
                        "name": "Analyze Current Costs",
                        "action": "analyze_costs",
                        "parameters": {"timeframe": "7d"}
                    },
                    {
                        "step_id": "generate_recommendations",
                        "name": "Generate Optimization Recommendations",
                        "action": "generate_recommendations",
                        "parameters": {"optimization_type": "cost_optimization"}
                    },
                    {
                        "step_id": "ai_decision",
                        "name": "AI Decision Making",
                        "action": "ai_decision",
                        "parameters": {"confidence_threshold": 0.8}
                    },
                    {
                        "step_id": "apply_optimizations",
                        "name": "Apply Optimizations",
                        "action": "apply_optimizations",
                        "parameters": {"auto_apply": True}
                    }
                ],
                conditions={
                    "cost_increase_threshold": 0.2,  # 20% increase
                    "utilization_threshold": 0.3,    # 30% utilization
                    "min_savings_threshold": 0.1     # 10% minimum savings
                }
            )
            
            # Performance optimization workflow
            performance_workflow = AutomationWorkflow(
                workflow_id="performance_optimization_auto",
                name="Automated Performance Optimization",
                description="Automatically optimize performance when issues are detected",
                trigger=AutomationTrigger.PERFORMANCE_ALERT,
                priority=AutomationPriority.MEDIUM,
                steps=[
                    {
                        "step_id": "analyze_performance",
                        "name": "Analyze Performance Metrics",
                        "action": "analyze_performance",
                        "parameters": {"metrics": ["cpu", "memory", "response_time"]}
                    },
                    {
                        "step_id": "generate_recommendations",
                        "name": "Generate Performance Recommendations",
                        "action": "generate_recommendations",
                        "parameters": {"optimization_type": "performance_optimization"}
                    },
                    {
                        "step_id": "ai_decision",
                        "name": "AI Decision Making",
                        "action": "ai_decision",
                        "parameters": {"confidence_threshold": 0.75}
                    }
                ],
                conditions={
                    "cpu_threshold": 0.8,           # 80% CPU utilization
                    "memory_threshold": 0.8,        # 80% memory utilization
                    "response_time_threshold": 1000  # 1 second response time
                }
            }
            
            # Scheduled optimization workflow
            scheduled_workflow = AutomationWorkflow(
                workflow_id="scheduled_optimization",
                name="Scheduled Optimization Review",
                description="Weekly automated optimization review and recommendations",
                trigger=AutomationTrigger.SCHEDULED,
                priority=AutomationPriority.LOW,
                schedule="0 2 * * 1",  # Every Monday at 2 AM
                steps=[
                    {
                        "step_id": "comprehensive_analysis",
                        "name": "Comprehensive Resource Analysis",
                        "action": "comprehensive_analysis",
                        "parameters": {"timeframe": "30d"}
                    },
                    {
                        "step_id": "generate_recommendations",
                        "name": "Generate All Recommendations",
                        "action": "generate_recommendations",
                        "parameters": {"optimization_types": ["cost", "performance", "rightsizing"]}
                    },
                    {
                        "step_id": "ai_decision",
                        "name": "AI Decision Making",
                        "action": "ai_decision",
                        "parameters": {"confidence_threshold": 0.7}
                    },
                    {
                        "step_id": "notify_results",
                        "name": "Notify Results",
                        "action": "notify_results",
                        "parameters": {"channels": ["email", "slack"]}
                    }
                ],
                conditions={}
            )
            
            # Add workflows to registry
            self.workflows[cost_workflow.workflow_id] = cost_workflow
            self.workflows[performance_workflow.workflow_id] = performance_workflow
            self.workflows[scheduled_workflow.workflow_id] = scheduled_workflow
            
            logger.info(f"✅ Initialized {len(self.workflows)} default workflows")
            
        except Exception as e:
            logger.error(f"Failed to initialize default workflows: {e}")
    
    async def trigger_workflow(
        self,
        workflow_id: str,
        trigger_data: Dict[str, Any],
        manual_trigger: bool = False
    ) -> Optional[AutomationExecution]:
        """Trigger an automation workflow"""
        try:
            if workflow_id not in self.workflows:
                logger.error(f"Workflow {workflow_id} not found")
                return None
            
            workflow = self.workflows[workflow_id]
            
            if not workflow.enabled:
                logger.warning(f"Workflow {workflow_id} is disabled")
                return None
            
            # Check if workflow is already running
            if workflow_id in self.running_executions:
                logger.warning(f"Workflow {workflow_id} is already running")
                return None
            
            # Create execution instance
            execution = AutomationExecution(
                execution_id=str(uuid.uuid4()),
                workflow_id=workflow_id,
                status=AutomationStatus.PENDING,
                trigger_data=trigger_data,
                results={}
            )
            
            # Add to executions list
            self.executions.append(execution)
            
            # Start execution
            task = asyncio.create_task(self._execute_workflow(execution))
            self.running_executions[workflow_id] = task
            
            logger.info(f"🚀 Triggered workflow {workflow_id} (execution: {execution.execution_id})")
            return execution
            
        except Exception as e:
            logger.error(f"Failed to trigger workflow {workflow_id}: {e}")
            return None
    
    async def _execute_workflow(self, execution: AutomationExecution):
        """Execute an automation workflow"""
        try:
            workflow = self.workflows[execution.workflow_id]
            execution.status = AutomationStatus.RUNNING
            
            logger.info(f"🔄 Executing workflow {workflow.name}")
            
            # Execute each step
            for step in workflow.steps:
                try:
                    step_result = await self._execute_step(step, execution)
                    execution.results[step["step_id"]] = step_result
                    
                    # Check if step failed
                    if step_result.get("status") == "failed":
                        execution.status = AutomationStatus.FAILED
                        execution.error_message = step_result.get("error", "Step execution failed")
                        break
                        
                except Exception as e:
                    logger.error(f"Step {step['step_id']} failed: {e}")
                    execution.status = AutomationStatus.FAILED
                    execution.error_message = str(e)
                    break
            
            # Mark as completed if not failed
            if execution.status != AutomationStatus.FAILED:
                execution.status = AutomationStatus.COMPLETED
                execution.completed_at = datetime.now(timezone.utc)
            
            # Remove from running executions
            if execution.workflow_id in self.running_executions:
                del self.running_executions[execution.workflow_id]
            
            logger.info(f"✅ Workflow {workflow.name} completed with status: {execution.status.value}")
            
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            execution.status = AutomationStatus.FAILED
            execution.error_message = str(e)
            execution.completed_at = datetime.now(timezone.utc)
            
            # Remove from running executions
            if execution.workflow_id in self.running_executions:
                del self.running_executions[execution.workflow_id]
    
    async def _execute_step(self, step: Dict[str, Any], execution: AutomationExecution) -> Dict[str, Any]:
        """Execute a single workflow step"""
        try:
            action = step["action"]
            parameters = step.get("parameters", {})
            
            logger.info(f"🔧 Executing step: {step['name']} ({action})")
            
            if action == "analyze_costs":
                return await self._analyze_costs(parameters)
            elif action == "generate_recommendations":
                return await self._generate_recommendations(parameters)
            elif action == "ai_decision":
                return await self._ai_decision(parameters, execution)
            elif action == "apply_optimizations":
                return await self._apply_optimizations(parameters, execution)
            elif action == "analyze_performance":
                return await self._analyze_performance(parameters)
            elif action == "comprehensive_analysis":
                return await self._comprehensive_analysis(parameters)
            elif action == "notify_results":
                return await self._notify_results(parameters, execution)
            else:
                return {
                    "status": "failed",
                    "error": f"Unknown action: {action}"
                }
                
        except Exception as e:
            logger.error(f"Step execution failed: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }
    
    async def _analyze_costs(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze current costs"""
        try:
            timeframe = parameters.get("timeframe", "7d")
            
            # Mock cost analysis
            analysis_result = {
                "status": "success",
                "timeframe": timeframe,
                "total_cost": 1250.50,
                "cost_trend": "increasing",
                "cost_increase_percentage": 15.5,
                "top_cost_drivers": [
                    {"resource": "ec2-instances", "cost": 800.00, "percentage": 64.0},
                    {"resource": "rds-databases", "cost": 300.00, "percentage": 24.0},
                    {"resource": "s3-storage", "cost": 150.50, "percentage": 12.0}
                ],
                "optimization_opportunities": [
                    {"type": "rightsizing", "potential_savings": 200.00},
                    {"type": "reserved_instances", "potential_savings": 150.00},
                    {"type": "storage_optimization", "potential_savings": 50.00}
                ]
            }
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Cost analysis failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def _generate_recommendations(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate optimization recommendations"""
        try:
            optimization_type = parameters.get("optimization_type", "cost_optimization")
            
            # Mock resources for recommendation generation
            mock_resources = [
                {
                    'id': 'ec2-001',
                    'type': 'ec2',
                    'cost_per_hour': 0.50,
                    'utilization_rate': 0.25,
                    'instance_size': 'm5.large'
                },
                {
                    'id': 'rds-001',
                    'type': 'rds',
                    'cost_per_hour': 0.75,
                    'utilization_rate': 0.60,
                    'instance_size': 'db.r5.large'
                }
            ]
            
            # Generate recommendations using ML optimizer
            recommendations = await ml_optimizer.generate_optimization_recommendations(
                mock_resources,
                OptimizationType(optimization_type),
                include_ai_analysis=True
            )
            
            return {
                "status": "success",
                "optimization_type": optimization_type,
                "recommendations_count": len(recommendations),
                "total_potential_savings": sum(rec.expected_savings for rec in recommendations),
                "recommendations": [
                    {
                        "id": rec.recommendation_id,
                        "type": rec.optimization_type.value,
                        "resource_id": rec.resource_id,
                        "expected_savings": rec.expected_savings,
                        "confidence_score": rec.confidence_score,
                        "implementation_effort": rec.implementation_effort,
                        "risk_level": rec.risk_level
                    }
                    for rec in recommendations
                ]
            }
            
        except Exception as e:
            logger.error(f"Recommendation generation failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def _ai_decision(self, parameters: Dict[str, Any], execution: AutomationExecution) -> Dict[str, Any]:
        """Make AI-powered decision"""
        try:
            confidence_threshold = parameters.get("confidence_threshold", 0.8)
            
            # Get recommendations from previous step
            recommendations_result = execution.results.get("generate_recommendations", {})
            recommendations = recommendations_result.get("recommendations", [])
            
            if not recommendations:
                return {
                    "status": "success",
                    "decision": "no_action",
                    "reasoning": "No recommendations available for decision making"
                }
            
            # Analyze recommendations using AI
            total_savings = sum(rec["expected_savings"] for rec in recommendations)
            avg_confidence = sum(rec["confidence_score"] for rec in recommendations) / len(recommendations)
            
            # Create AI prompt for decision making
            prompt = f"""
            Analyze these optimization recommendations and make a decision:
            
            Total potential savings: ${total_savings:.2f}
            Average confidence score: {avg_confidence:.2f}
            Number of recommendations: {len(recommendations)}
            
            Recommendations:
            {json.dumps(recommendations, indent=2)}
            
            Make a decision (approve/reject/require_manual_review) based on:
            1. Potential savings vs risk
            2. Confidence scores
            3. Implementation effort
            4. Business impact
            
            Provide reasoning for your decision.
            """
            
            # Get AI decision
            ai_response = await ensemble_ai.generate_ensemble_response(
                prompt=prompt,
                analysis_type=AnalysisType.COMPREHENSIVE,
                consensus_method=ConsensusMethod.EXPERT_VOTE
            )
            
            # Parse AI decision
            decision = self._parse_ai_decision(ai_response.final_response, avg_confidence, confidence_threshold)
            
            # Create decision record
            automation_decision = AutomationDecision(
                decision_id=str(uuid.uuid4()),
                workflow_id=execution.workflow_id,
                decision_type="optimization_approval",
                decision=decision["decision"],
                confidence_score=ai_response.confidence_score,
                reasoning=ai_response.final_response,
                recommendations=[f"Apply {len(recommendations)} optimization recommendations"],
                risk_assessment={
                    "total_savings": total_savings,
                    "average_confidence": avg_confidence,
                    "risk_level": "medium" if avg_confidence < 0.9 else "low"
                }
            )
            
            self.decisions.append(automation_decision)
            
            return {
                "status": "success",
                "decision": decision["decision"],
                "confidence_score": ai_response.confidence_score,
                "reasoning": ai_response.final_response,
                "decision_id": automation_decision.decision_id
            }
            
        except Exception as e:
            logger.error(f"AI decision failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    def _parse_ai_decision(self, ai_response: str, avg_confidence: float, confidence_threshold: float) -> Dict[str, Any]:
        """Parse AI response to extract decision"""
        try:
            response_lower = ai_response.lower()
            
            if "approve" in response_lower and avg_confidence >= confidence_threshold:
                return {"decision": "approve", "reasoning": "High confidence and clear approval"}
            elif "reject" in response_lower:
                return {"decision": "reject", "reasoning": "AI recommended rejection"}
            elif "manual" in response_lower or "review" in response_lower:
                return {"decision": "require_manual_review", "reasoning": "Requires human review"}
            else:
                # Default decision based on confidence
                if avg_confidence >= confidence_threshold:
                    return {"decision": "approve", "reasoning": "High confidence threshold met"}
                else:
                    return {"decision": "require_manual_review", "reasoning": "Below confidence threshold"}
                    
        except Exception as e:
            logger.error(f"Failed to parse AI decision: {e}")
            return {"decision": "require_manual_review", "reasoning": "Failed to parse AI response"}
    
    async def _apply_optimizations(self, parameters: Dict[str, Any], execution: AutomationExecution) -> Dict[str, Any]:
        """Apply optimization recommendations"""
        try:
            auto_apply = parameters.get("auto_apply", False)
            
            # Get decision from previous step
            decision_result = execution.results.get("ai_decision", {})
            decision = decision_result.get("decision", "require_manual_review")
            
            if decision != "approve":
                return {
                    "status": "success",
                    "action": "skipped",
                    "reason": f"Decision was {decision}, not approved for auto-application"
                }
            
            if not auto_apply:
                return {
                    "status": "success",
                    "action": "manual_application_required",
                    "reason": "Auto-apply is disabled"
                }
            
            # Mock optimization application
            applied_optimizations = [
                {"resource_id": "ec2-001", "action": "rightsized", "savings": 0.20},
                {"resource_id": "rds-001", "action": "optimized", "savings": 0.15}
            ]
            
            return {
                "status": "success",
                "action": "applied",
                "applied_optimizations": applied_optimizations,
                "total_applied_savings": sum(opt["savings"] for opt in applied_optimizations)
            }
            
        except Exception as e:
            logger.error(f"Optimization application failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def _analyze_performance(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance metrics"""
        try:
            metrics = parameters.get("metrics", ["cpu", "memory", "response_time"])
            
            # Mock performance analysis
            analysis_result = {
                "status": "success",
                "metrics_analyzed": metrics,
                "performance_score": 0.75,
                "issues_detected": [
                    {"metric": "cpu", "value": 0.85, "threshold": 0.8, "severity": "high"},
                    {"metric": "response_time", "value": 1200, "threshold": 1000, "severity": "medium"}
                ],
                "recommendations": [
                    "Scale up CPU resources",
                    "Optimize database queries",
                    "Add caching layer"
                ]
            }
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Performance analysis failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def _comprehensive_analysis(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive resource analysis"""
        try:
            timeframe = parameters.get("timeframe", "30d")
            
            # Mock comprehensive analysis
            analysis_result = {
                "status": "success",
                "timeframe": timeframe,
                "resources_analyzed": 25,
                "cost_analysis": {
                    "total_cost": 2500.00,
                    "cost_trend": "stable",
                    "optimization_potential": 400.00
                },
                "performance_analysis": {
                    "average_performance_score": 0.78,
                    "performance_issues": 3,
                    "optimization_opportunities": 5
                },
                "security_analysis": {
                    "security_score": 0.85,
                    "vulnerabilities": 2,
                    "compliance_status": "compliant"
                }
            }
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Comprehensive analysis failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def _notify_results(self, parameters: Dict[str, Any], execution: AutomationExecution) -> Dict[str, Any]:
        """Notify workflow results"""
        try:
            channels = parameters.get("channels", ["email"])
            
            # Mock notification
            notification_result = {
                "status": "success",
                "channels": channels,
                "message": f"Workflow {execution.workflow_id} completed with status: {execution.status.value}",
                "recipients": ["admin@company.com"],
                "sent_at": datetime.now(timezone.utc).isoformat()
            }
            
            return notification_result
            
        except Exception as e:
            logger.error(f"Notification failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def get_workflow_summary(self) -> Dict[str, Any]:
        """Get automation workflow summary"""
        try:
            total_workflows = len(self.workflows)
            enabled_workflows = sum(1 for w in self.workflows.values() if w.enabled)
            total_executions = len(self.executions)
            
            # Calculate execution statistics
            completed_executions = sum(1 for e in self.executions if e.status == AutomationStatus.COMPLETED)
            failed_executions = sum(1 for e in self.executions if e.status == AutomationStatus.FAILED)
            running_executions = len(self.running_executions)
            
            # Get recent executions
            recent_executions = [
                {
                    "execution_id": e.execution_id,
                    "workflow_id": e.workflow_id,
                    "status": e.status.value,
                    "started_at": e.started_at.isoformat(),
                    "completed_at": e.completed_at.isoformat() if e.completed_at else None
                }
                for e in sorted(self.executions, key=lambda x: x.started_at, reverse=True)[:10]
            ]
            
            return {
                "total_workflows": total_workflows,
                "enabled_workflows": enabled_workflows,
                "total_executions": total_executions,
                "completed_executions": completed_executions,
                "failed_executions": failed_executions,
                "running_executions": running_executions,
                "success_rate": completed_executions / total_executions if total_executions > 0 else 0,
                "recent_executions": recent_executions
            }
            
        except Exception as e:
            logger.error(f"Failed to get workflow summary: {e}")
            return {}
    
    async def get_decision_summary(self) -> Dict[str, Any]:
        """Get automation decision summary"""
        try:
            total_decisions = len(self.decisions)
            
            # Group decisions by type
            decisions_by_type = {}
            for decision in self.decisions:
                decision_type = decision.decision_type
                if decision_type not in decisions_by_type:
                    decisions_by_type[decision_type] = []
                decisions_by_type[decision_type].append(decision)
            
            # Calculate approval rate
            approved_decisions = sum(1 for d in self.decisions if d.decision == "approve")
            approval_rate = approved_decisions / total_decisions if total_decisions > 0 else 0
            
            # Get recent decisions
            recent_decisions = [
                {
                    "decision_id": d.decision_id,
                    "workflow_id": d.workflow_id,
                    "decision": d.decision,
                    "confidence_score": d.confidence_score,
                    "created_at": d.created_at.isoformat()
                }
                for d in sorted(self.decisions, key=lambda x: x.created_at, reverse=True)[:10]
            ]
            
            return {
                "total_decisions": total_decisions,
                "approved_decisions": approved_decisions,
                "approval_rate": approval_rate,
                "decisions_by_type": {
                    decision_type: len(decisions) for decision_type, decisions in decisions_by_type.items()
                },
                "recent_decisions": recent_decisions
            }
            
        except Exception as e:
            logger.error(f"Failed to get decision summary: {e}")
            return {}


# Global automation engine instance
automation_engine = AutomationEngine()
