from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class PriceInput:
    resource_type: str
    region: str
    attributes: Dict[str, Any]


@dataclass
class PriceResult:
    monthly_cost: float
    currency: str = "USD"
    details: Dict[str, Any] = None  # type: ignore[assignment]


class PriceEngine:
    """Simple tiered price calculators.

    NOTE: Backed by static tables for Phase 1. Replace with provider billing later.
    """

    def __init__(self) -> None:
        self._ec2_hourly_fallback = {
            "t3.micro": 0.0104,
            "t3.small": 0.0208,
            "t3.medium": 0.0416,
            "m5.large": 0.096,
        }

    def price_ec2_instance(self, inp: PriceInput) -> PriceResult:
        instance_type = inp.attributes.get("instance_type", "t3.micro")
        state = inp.attributes.get("state", "running")
        hourly_rate = self._ec2_hourly_fallback.get(instance_type, 0.05)
        monthly = hourly_rate * 730 if state == "running" else 0.0
        return PriceResult(monthly_cost=monthly, details={"hourly_rate": hourly_rate})

    def price_s3_bucket(self, inp: PriceInput) -> PriceResult:
        storage_gb = float(inp.attributes.get("storage_gb", 100))
        requests = int(inp.attributes.get("requests", 10000))
        storage_cost = storage_gb * 0.023
        request_cost = (requests / 1000.0) * 0.0004
        return PriceResult(monthly_cost=storage_cost + request_cost, details={
            "storage_gb": storage_gb,
            "requests": requests,
        })

    def price_rds_instance(self, inp: PriceInput) -> PriceResult:
        instance_class = inp.attributes.get("instance_class", "db.t3.micro")
        storage_gb = int(inp.attributes.get("storage_gb", 20))
        multi_az = bool(inp.attributes.get("multi_az", False))
        instance_costs = {
            "db.t3.micro": 12.41,
            "db.t3.small": 24.82,
            "db.t3.medium": 49.64,
            "db.r5.large": 228.00,
            "db.r5.xlarge": 456.00,
        }
        base_cost = instance_costs.get(instance_class, 50.0)
        storage_cost = storage_gb * 0.115
        multi_az_cost = base_cost if multi_az else 0.0
        monthly = base_cost + storage_cost + multi_az_cost
        return PriceResult(monthly_cost=monthly, details={
            "instance_class": instance_class,
            "storage_gb": storage_gb,
            "multi_az": multi_az,
        })

    def price_elasticache_cluster(self, inp: PriceInput) -> PriceResult:
        node_type = inp.attributes.get("node_type", "cache.t3.micro")
        num_nodes = int(inp.attributes.get("num_nodes", 1))
        node_costs = {
            "cache.t3.micro": 13.68,
            "cache.t3.small": 27.36,
            "cache.t3.medium": 54.72,
            "cache.r5.large": 252.00,
        }
        per_node = node_costs.get(node_type, 50.0)
        monthly = per_node * num_nodes
        return PriceResult(monthly_cost=monthly, details={
            "node_type": node_type,
            "num_nodes": num_nodes,
        })

    def price_load_balancer(self, inp: PriceInput) -> PriceResult:
        lb_type = inp.attributes.get("lb_type", "application")
        monthly = 16.20 if lb_type == "application" else 22.25 if lb_type == "network" else 16.20
        return PriceResult(monthly_cost=monthly, details={"lb_type": lb_type})

    def calculate_ec2_optimization_potential(self, instance_type: str, current_utilization: float) -> dict:
        """Calculate EC2 optimization potential"""
        try:
            optimization = {
                'current_instance': instance_type,
                'current_utilization': current_utilization,
                'recommendations': [],
                'potential_savings': 0.0
            }
            
            # Define instance families and their characteristics
            instance_families = {
                't3': {'type': 'burstable', 'min_cores': 1, 'max_cores': 8},
                'm5': {'type': 'general', 'min_cores': 2, 'max_cores': 96},
                'c5': {'type': 'compute', 'min_cores': 2, 'max_cores': 96},
                'r5': {'type': 'memory', 'min_cores': 2, 'max_cores': 96}
            }
            
            # Extract family from instance type
            family = instance_type.split('.')[0]
            current_cores = self._get_instance_cores(instance_type)
            
            if current_utilization < 20:
                # Underutilized - recommend smaller instance
                if family in instance_families:
                    smaller_instances = self._get_smaller_instances(family, current_cores)
                    for smaller in smaller_instances:
                        optimization['recommendations'].append({
                            'action': 'downsize',
                            'from': instance_type,
                            'to': smaller,
                            'reason': f'Low utilization ({current_utilization:.1f}%)',
                            'savings_percent': 30
                        })
                        
            elif current_utilization > 80:
                # Overutilized - recommend larger instance
                if family in instance_families:
                    larger_instances = self._get_larger_instances(family, current_cores)
                    for larger in larger_instances:
                        optimization['recommendations'].append({
                            'action': 'upsize',
                            'from': instance_type,
                            'to': larger,
                            'reason': f'High utilization ({current_utilization:.1f}%)',
                            'savings_percent': -20  # Cost increase
                        })
            
            # Calculate potential savings
            if optimization['recommendations']:
                current_cost = self.price_ec2_instance(PriceInput(
                    resource_type="ec2",
                    region="us-east-1",
                    attributes={"instance_type": instance_type, "state": "running"}
                )).monthly_cost
                
                for rec in optimization['recommendations']:
                    if rec['action'] == 'downsize':
                        new_cost = self.price_ec2_instance(PriceInput(
                            resource_type="ec2",
                            region="us-east-1",
                            attributes={"instance_type": rec['to'], "state": "running"}
                        )).monthly_cost
                        savings = current_cost - new_cost
                        optimization['potential_savings'] += savings
            
            return optimization
            
        except Exception as e:
            return {'current_instance': instance_type, 'recommendations': [], 'potential_savings': 0.0}

    def _get_instance_cores(self, instance_type: str) -> int:
        """Get number of cores for instance type"""
        core_mapping = {
            'micro': 1, 'small': 1, 'medium': 1,
            'large': 2, 'xlarge': 4, '2xlarge': 8,
            '4xlarge': 16, '8xlarge': 32, '16xlarge': 64
        }
        
        size = instance_type.split('.')[-1]
        return core_mapping.get(size, 2)

    def _get_smaller_instances(self, family: str, current_cores: int) -> list:
        """Get smaller instances in the same family"""
        smaller = []
        if current_cores > 1:
            if current_cores == 4:  # xlarge
                smaller.append(f'{family}.large')
            elif current_cores == 2:  # large
                smaller.append(f'{family}.medium')
        return smaller

    def _get_larger_instances(self, family: str, current_cores: int) -> list:
        """Get larger instances in the same family"""
        larger = []
        if current_cores < 32:
            if current_cores == 1:  # medium/small/micro
                larger.append(f'{family}.large')
            elif current_cores == 2:  # large
                larger.append(f'{family}.xlarge')
            elif current_cores == 4:  # xlarge
                larger.append(f'{family}.2xlarge')
        return larger


