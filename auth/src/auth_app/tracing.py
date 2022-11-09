from functools import wraps

from auth_app.config import config
from flask import request, current_app
from opentelemetry import trace as ot_trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter


def configure_tracer():
    resource = Resource(attributes={"service.name": "Auth-service"})
    ot_trace.set_tracer_provider(TracerProvider(resource=resource))

    ot_trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=config.jaeger_host,
                agent_port=config.jaeger_port,
            )
        )
    )
    if config.DEBUG:
        ot_trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))


def trace(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        tracer = ot_trace.get_tracer(__name__)
        with tracer.start_as_current_span(fn.__name__) as span:
            request_id = request.headers.get("X-Request-Id")
            span.set_attribute("http.request_id", request_id)
            return fn(*args, **kwargs)

    return decorator


def loging(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        current_app.logger.info(f"Access to {request.path}")
        return fn(*args, **kwargs)

    return decorator
