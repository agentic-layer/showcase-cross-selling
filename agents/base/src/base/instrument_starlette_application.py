from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry import trace
from starlette.applications import Starlette

_tracer_provider = trace_sdk.TracerProvider()
_tracer_provider.add_span_processor(
    SimpleSpanProcessor(OTLPSpanExporter())
)
trace.set_tracer_provider(_tracer_provider)

def instrument_starlette_application(app: Starlette) -> None:
    from opentelemetry.instrumentation.starlette import StarletteInstrumentor
    StarletteInstrumentor().instrument_app(app, tracer_provider=_tracer_provider)
