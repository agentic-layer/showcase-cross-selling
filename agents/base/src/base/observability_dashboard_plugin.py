from typing import Any, Optional

from google.adk.agents import BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from google.adk.plugins.base_plugin import BasePlugin
from google.adk.tools import BaseTool, ToolContext
from google.genai import types
from opentelemetry import trace

from .observability_dashboard_callbacks import (
    after_agent_callback_observability_dashboard,
    after_model_callback_observability_dashboard,
    after_tool_callback_observability_dashboard,
    before_agent_callback_observability_dashboard,
    before_model_callback_observability_dashboard,
    before_tool_callback_observability_dashboard,
    flatten_dict,
    set_span_attributes_for_tool,
    set_span_attributes_from_callback_context,
)


class ObservabilityDashboardPlugin(BasePlugin):
    """A custom plugin class for the Observability Dashboard."""

    def __init__(self):
        super().__init__("ObservabilityDashboardPlugin")

    async def before_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> Optional[types.Content]:
        return before_agent_callback_observability_dashboard(callback_context)

    async def after_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> Optional[types.Content]:
        return after_agent_callback_observability_dashboard(callback_context)

    async def before_model_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> Optional[LlmResponse]:
        return before_model_callback_observability_dashboard(callback_context, llm_request)

    async def after_model_callback(
        self, *, callback_context: CallbackContext, llm_response: LlmResponse
    ) -> Optional[LlmResponse]:
        return after_model_callback_observability_dashboard(callback_context, llm_response)

    async def before_tool_callback(
        self,
        *,
        tool: BaseTool,
        tool_args: dict[str, Any],
        tool_context: ToolContext,
    ) -> Optional[dict]:
        return before_tool_callback_observability_dashboard(tool, tool_args, tool_context)

    async def after_tool_callback(
        self,
        *,
        tool: BaseTool,
        tool_args: dict[str, Any],
        tool_context: ToolContext,
        result: dict,
    ) -> Optional[dict]:
        return after_tool_callback_observability_dashboard(tool, tool_args, tool_context, result)

    async def on_model_error_callback(
        self,
        *,
        callback_context: CallbackContext,
        llm_request: LlmRequest,
        error: Exception,
    ) -> Optional[LlmResponse]:
        # not yet tested
        with trace.get_tracer(__name__).start_as_current_span(
            "on_model_error_callback_observability_dashboard"
        ) as span:
            set_span_attributes_from_callback_context(span, callback_context)
            span.set_attribute("model", llm_request.model or "unknown")
            if llm_request.contents:
                span.set_attributes(
                    flatten_dict(llm_request.contents[-1].model_dump(), parent_key="llm_request.content")
                )  # only send the last content part (last user input)
            span.set_attribute("error", str(error))
        return None

    async def on_tool_error_callback(
        self,
        *,
        tool: BaseTool,
        tool_args: dict[str, Any],
        tool_context: ToolContext,
        error: Exception,
    ) -> Optional[dict]:
        # not yet tested
        with trace.get_tracer(__name__).start_as_current_span("on_tool_error_callback_observability_dashboard") as span:
            set_span_attributes_for_tool(span, tool, tool_args, tool_context)
            span.set_attribute("error", str(error))
        return None
