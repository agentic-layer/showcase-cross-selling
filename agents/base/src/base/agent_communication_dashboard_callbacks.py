import re
from typing import Any, Dict, List, Optional, Union

from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from mcp.types import CallToolResult
from opentelemetry import trace

# Pattern to match any key containing 'structuredcontent' or 'structured_content', case-insensitive
STRUCTURED_CONTENT_PATTERN = re.compile(r"\.structured[_]?content", re.IGNORECASE)


def _span_attribute_item(key: str, data: Any) -> tuple[str, Any]:
    """Convert data to a span attribute-compatible type."""
    if isinstance(data, (str, bool, int, float)):  # only these types are supported by span attributes
        return (key, data)
    else:
        return (key, str(data))


def flatten_dict(data, parent_key="", sep=".", parent_key_lower=None) -> Dict[str, Any]:
    if parent_key_lower is None:
        parent_key_lower = parent_key.lower()

    if STRUCTURED_CONTENT_PATTERN.search(parent_key_lower):
        return {}  # skip structured content as it can add too many attributes

    items: list[tuple[str, Any]] = []
    if isinstance(data, dict):
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            new_key_lower = new_key.lower()
            items.extend(flatten_dict(v, new_key, sep=sep, parent_key_lower=new_key_lower).items())
    elif isinstance(data, list):
        for i, v in enumerate(data):
            new_key = f"{parent_key}{sep}{i}"
            new_key_lower = new_key.lower()
            items.extend(flatten_dict(v, new_key, sep=sep, parent_key_lower=new_key_lower).items())
    elif data is not None:
        items.append(_span_attribute_item(parent_key, data))
    return dict(items)


def set_span_attributes_from_callback_context(span, callback_context: CallbackContext):
    span.set_attribute("conversation_id", callback_context.state.to_dict().get("conversation_id"))
    span.set_attribute("agent_name", callback_context.agent_name)
    span.set_attribute("agent_communication_dashboard", True)

    if callback_context.user_content:
        span.set_attributes(flatten_dict(callback_context.user_content.model_dump(), parent_key="user_content"))
    span.set_attributes(callback_context.state.to_dict())
    span.set_attribute("invocation_id", callback_context.invocation_id)


def set_span_attributes_for_tool(span, tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext):
    set_span_attributes_from_callback_context(span, tool_context)
    span.set_attributes(flatten_dict(tool_context.actions.model_dump(), parent_key="tool_context.actions"))
    span.set_attribute("tool_name", tool.name)
    span.set_attributes(flatten_dict(args, parent_key="args"))


def before_agent_callback_agent_communications_dashboard(callback_context: CallbackContext) -> Optional[types.Content]:
    with trace.get_tracer(__name__).start_as_current_span(
        "before_agent_callback_agent_communications_dashboard"
    ) as span:
        set_span_attributes_from_callback_context(span, callback_context)
    return None


def after_agent_callback_agent_communications_dashboard(callback_context: CallbackContext) -> Optional[types.Content]:
    with trace.get_tracer(__name__).start_as_current_span(
        "after_agent_callback_agent_communications_dashboard"
    ) as span:
        set_span_attributes_from_callback_context(span, callback_context)
    return None


def before_model_callback_agent_communications_dashboard(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    with trace.get_tracer(__name__).start_as_current_span(
        "before_model_callback_agent_communications_dashboard"
    ) as span:
        set_span_attributes_from_callback_context(span, callback_context)
        span.set_attribute("model", llm_request.model or "unknown")
        if llm_request.contents:
            span.set_attributes(
                flatten_dict(llm_request.contents[-1].model_dump(), parent_key="llm_request.content")
            )  # only send the last content part (last user input)
    return None


def after_model_callback_agent_communications_dashboard(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> Optional[LlmResponse]:
    with trace.get_tracer(__name__).start_as_current_span(
        "after_model_callback_agent_communications_dashboard"
    ) as span:
        set_span_attributes_from_callback_context(span, callback_context)
        span.set_attributes(flatten_dict(llm_response.model_dump(), parent_key="llm_response"))
    return None


def before_tool_callback_agent_communications_dashboard(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext
) -> Optional[Dict]:
    with trace.get_tracer(__name__).start_as_current_span(
        "before_tool_callback_agent_communications_dashboard"
    ) as span:
        set_span_attributes_for_tool(span, tool, args, tool_context)
    return None


def after_tool_callback_agent_communications_dashboard(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Union[Dict, List, CallToolResult]
) -> Optional[Dict]:
    with trace.get_tracer(__name__).start_as_current_span("after_tool_callback_agent_communications_dashboard") as span:
        set_span_attributes_for_tool(span, tool, args, tool_context)
        if isinstance(tool_response, (dict, list)):
            span.set_attributes(flatten_dict(tool_response, parent_key="tool_response"))
        elif isinstance(tool_response, CallToolResult):
            span.set_attributes(flatten_dict(tool_response.model_dump(), parent_key="tool_response"))
    return None
