from os import getenv

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from starlette.applications import Starlette

observability_dashboard_endpoint = getenv("OBSERVABILITY_DASHBOARD_ENDPOINT")

_tracer_provider = trace_sdk.TracerProvider()
_tracer_provider.add_span_processor(
    SimpleSpanProcessor(OTLPSpanExporter())
)  # Tempo endpoint is set by default, doesn't need to be specified
if observability_dashboard_endpoint:
    _tracer_provider.add_span_processor(
        SimpleSpanProcessor(OTLPSpanExporter(endpoint=observability_dashboard_endpoint))
    )
trace.set_tracer_provider(_tracer_provider)


def instrument_starlette_application(app: Starlette) -> None:
    from opentelemetry.instrumentation.starlette import StarletteInstrumentor

    StarletteInstrumentor().instrument_app(app, tracer_provider=_tracer_provider)
