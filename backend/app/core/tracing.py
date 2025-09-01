"""
Lightweight OpenTelemetry setup (no-op if OTEL not installed).

This module safely initializes tracing and instruments FastAPI/Requests when
opentelemetry packages are present. In environments without OTEL, all functions
become no-ops to avoid import errors.
"""

from typing import Any
import logging

logger = logging.getLogger(__name__)


def init_tracing() -> None:
    """Initialize global tracer provider; prefer OTLP if configured."""
    try:
        import os
        from opentelemetry import trace
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor

        # Decide exporter
        exporter = None
        endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
        if endpoint:
            try:
                # Prefer HTTP/proto exporter
                from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
                    OTLPSpanExporter,
                )

                exporter = OTLPSpanExporter(endpoint=endpoint.rstrip("/") + "/v1/traces")
                logger.info("OTLP HTTP tracing exporter configured", extra={"endpoint": endpoint})
            except Exception as e:  # Fallback to console
                logger.debug(f"OTLP exporter unavailable, falling back to console: {e}")
        if exporter is None:
            from opentelemetry.sdk.trace.export import ConsoleSpanExporter

            exporter = ConsoleSpanExporter()

        resource = Resource.create({
            "service.name": "cloudmind-backend",
            "service.version": "1.0.0",
        })
        provider = TracerProvider(resource=resource)
        provider.add_span_processor(BatchSpanProcessor(exporter))
        trace.set_tracer_provider(provider)
        logger.info("OpenTelemetry tracing initialized")
    except Exception as e:
        logger.debug(f"OTEL init skipped: {e}")


def instrument_fastapi(app: Any) -> None:
    """Instrument FastAPI and outbound HTTP if OTEL is available."""
    try:
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
        from opentelemetry.instrumentation.requests import RequestsInstrumentor

        FastAPIInstrumentor.instrument_app(app)
        try:
            RequestsInstrumentor().instrument()
        except Exception:
            pass
        logger.info("OpenTelemetry instrumentation enabled for FastAPI")
    except Exception as e:
        logger.debug(f"OTEL instrumentation skipped: {e}")


