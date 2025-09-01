# CloudMind Architecture Overview

## Assistant
- Multi-provider LLM orchestration (OpenAI/Anthropic/Google/Ollama)
- Planned RAG: vector store + project ingestion + secure retrieval
- Guardrails: prompt-injection filters, secret redaction

## Scanner
- Provider interfaces (AWS/Azure/GCP) with retries/backoff and normalization
- Discovery → Metrics → Cost calculation → Recommendations → Report
- Phase 1 static price engine; Phase 2 billing integrations

## Cost Optimizer
- PriceEngine abstraction with tiered calculators (EC2/S3, more to come)
- What-if analysis and backtests planned

## Cross-cutting
- CI gates (lint/type/coverage/audit), link checking, dependabot
- Secrets management integration planned; Celery workers for long scans
