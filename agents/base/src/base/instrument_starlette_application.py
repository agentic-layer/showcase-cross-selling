from os import getenv

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from starlette.applications import Starlette

agent_communication_dashboard_backend_endpoint = getenv(
    "AGENT_COMMUNICATION_DASHBOARD_BACKEND_ENDPOINT",
    "http://agent-communications-dashboard-backend.monitoring.svc.cluster.local:8000/v1/traces",
)

_tracer_provider = trace_sdk.TracerProvider()
_tracer_provider.add_span_processor(
    SimpleSpanProcessor(OTLPSpanExporter())
)  # Tempo endpoint is set by default, doesn't need to be specified
_tracer_provider.add_span_processor(
    SimpleSpanProcessor(OTLPSpanExporter(endpoint=agent_communication_dashboard_backend_endpoint))
)
trace.set_tracer_provider(_tracer_provider)


def instrument_starlette_application(app: Starlette) -> None:
    from opentelemetry.instrumentation.starlette import StarletteInstrumentor

    StarletteInstrumentor().instrument_app(app, tracer_provider=_tracer_provider)
