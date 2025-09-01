from app.services.pricing.price_engine import PriceEngine, PriceInput


def test_price_ec2_running_instance():
    engine = PriceEngine()
    result = engine.price_ec2_instance(PriceInput(
        resource_type="ec2_instance",
        region="us-east-1",
        attributes={"instance_type": "t3.micro", "state": "running"},
    ))
    assert result.monthly_cost > 0


def test_price_s3_bucket_defaults():
    engine = PriceEngine()
    result = engine.price_s3_bucket(PriceInput(
        resource_type="s3_bucket",
        region="us-east-1",
        attributes={},
    ))
    assert result.monthly_cost > 0


def test_price_rds_instance():
    engine = PriceEngine()
    result = engine.price_rds_instance(PriceInput(
        resource_type="rds_instance",
        region="us-east-1",
        attributes={"instance_class": "db.t3.micro", "storage_gb": 20, "multi_az": True},
    ))
    assert result.monthly_cost > 0


def test_price_elasticache_cluster():
    engine = PriceEngine()
    result = engine.price_elasticache_cluster(PriceInput(
        resource_type="elasticache_cluster",
        region="us-east-1",
        attributes={"node_type": "cache.t3.small", "num_nodes": 2},
    ))
    assert result.monthly_cost > 0


def test_price_load_balancer():
    engine = PriceEngine()
    result = engine.price_load_balancer(PriceInput(
        resource_type="load_balancer",
        region="us-east-1",
        attributes={"lb_type": "application"},
    ))
    assert result.monthly_cost == 16.20

