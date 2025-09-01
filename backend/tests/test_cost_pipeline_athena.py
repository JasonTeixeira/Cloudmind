import pytest
import sys
import types
from unittest.mock import MagicMock

from app.services.cost_pipeline import CostIngestionPipeline
from app.core.config import settings


@pytest.fixture(autouse=True)
def enable_cost_ingestion_env(monkeypatch):
	# Set both env and live settings object (since settings loads early)
	monkeypatch.setenv("ENABLE_COST_INGESTION", "true")
	monkeypatch.setenv("AWS_ATHENA_WORKGROUP", "primary")
	monkeypatch.setenv("AWS_ATHENA_DATABASE", "cur_db")
	monkeypatch.setenv("AWS_ATHENA_OUTPUT_LOCATION", "s3://bucket/path/")
	monkeypatch.setenv("AWS_CUR_TABLE", "cur_db.cur_table")
	monkeypatch.setattr(settings, "ENABLE_COST_INGESTION", True, raising=False)
	monkeypatch.setattr(settings, "AWS_ATHENA_WORKGROUP", "primary", raising=False)
	monkeypatch.setattr(settings, "AWS_ATHENA_DATABASE", "cur_db", raising=False)
	monkeypatch.setattr(settings, "AWS_ATHENA_OUTPUT_LOCATION", "s3://bucket/path/", raising=False)
	monkeypatch.setattr(settings, "AWS_CUR_TABLE", "cur_db.cur_table", raising=False)
	yield


def _mock_boto3_client_success():
	client = MagicMock()
	client.start_query_execution.return_value = {"QueryExecutionId": "q-123"}
	client.get_query_execution.return_value = {
		"QueryExecution": {"Status": {"State": "SUCCEEDED"}}
	}
	# Simulate header + one data row
	page = {
		"ResultSet": {
			"ResultSetMetadata": {
				"ColumnInfo": [
					{"Name": "service"},
					{"Name": "region"},
					{"Name": "usage_amount"},
					{"Name": "cost"},
					{"Name": "ts"},
				]
			},
			"Rows": [
				{"Data": [{"VarCharValue": "service"}]},
				{"Data": [
					{"VarCharValue": "AmazonEC2"},
					{"VarCharValue": "us-east-1"},
					{"VarCharValue": "10"},
					{"VarCharValue": "2.5"},
					{"VarCharValue": "2025-01-01T00:00:00Z"},
				]},
			],
		},
	}
	paginator = MagicMock()
	paginator.paginate.return_value = [page]
	client.get_paginator.return_value = paginator
	return client


def test_ingest_aws_cur_via_athena_parsing(monkeypatch):
	pipeline = CostIngestionPipeline()
	client = _mock_boto3_client_success()
	mock_boto3 = types.SimpleNamespace(client=lambda service: client)
	# Inject synthetic boto3 module prior to import usage in pipeline
	monkeypatch.setitem(sys.modules, "boto3", mock_boto3)
	rows = pipeline._ingest_aws_cur_via_athena()
	assert isinstance(rows, list)
	assert len(rows) == 1
	row = rows[0]
	assert row["provider"] == "aws"
	assert row["service"] == "AmazonEC2"
	assert row["region"] == "us-east-1"
	assert row["usage_amount"] == 10.0
	assert row["cost"] == 2.5
