"""OpenTelemetry setup for MCP servers."""

import logging
import os

from opentelemetry import metrics, trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

_logger = logging.getLogger(__name__)


def setup_otel() -> None:
    """Set up OpenTelemetry tracing, logging and metrics."""
    # Set log level for urllib to WARNING to reduce noise (like sending logs to OTLP)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    # Traces
    trace_provider = TracerProvider()
    if os.environ.get("OTEL_EXPORTER_OTLP_PROTOCOL", "grpc") == "grpc":
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter as OTLPSpanExporterGrpc

        trace_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporterGrpc()))
    else:
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter as OTLPSpanExporterHttp

        trace_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporterHttp()))
    trace.set_tracer_provider(trace_provider)

    # Logs
    logger_provider = LoggerProvider()
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter()))
    # Sets the global default logger provider
    set_logger_provider(logger_provider)

    # Attach OTLP handler to root logger
    logging.getLogger().addHandler(LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider))

    # Sets the global default meter provider
    metrics.set_meter_provider(
        MeterProvider(
            metric_readers=[PeriodicExportingMetricReader(OTLPMetricExporter())],
        )
    )
