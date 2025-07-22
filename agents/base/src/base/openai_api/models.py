"""
Pydantic models for OpenAI API compatibility.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class Role(str, Enum):
    """Message roles in chat completion.

    Defines the different types of participants in a conversation:
    - SYSTEM: System-level instructions or context
    - USER: Messages from the human user
    - ASSISTANT: Responses from the AI assistant
    - FUNCTION: Deprecated function call responses (legacy)
    - TOOL: Tool call responses (current standard)
    """

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"
    TOOL = "tool"


class ChatMessage(BaseModel):
    """A chat message in the conversation.

    Used attributes:
        role: The role of the message sender (system, user, assistant)
        content: The text content of the message

    Compatibility attributes (unused but included for OpenAI API compatibility):
        name, function_call, tool_calls, tool_call_id
    """

    role: Role
    content: Optional[str] = None
    name: Optional[str] = None
    function_call: Optional[Dict[str, Any]] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_call_id: Optional[str] = None


class FunctionCall(BaseModel):
    """Function call details.

    Included for OpenAI API compatibility but not currently used.
    """

    name: str
    arguments: str


class ToolCall(BaseModel):
    """Tool call details.

    Included for OpenAI API compatibility but not currently used.
    """

    id: str
    type: str = "function"
    function: FunctionCall


class ChatCompletionRequest(BaseModel):
    """Request model for chat completions endpoint.

    Used attributes:
        model: Model identifier (defaults to gemini-2.0-flash-exp)
        messages: List of conversation messages

    Compatibility attributes (unused but included for OpenAI API compatibility):
        temperature, top_p, n, stream, stop, max_tokens, presence_penalty,
        frequency_penalty, logit_bias, user, functions, function_call, tools,
        tool_choice, response_format, seed
    """

    model: str = Field(default="gemini-2.0-flash-exp")
    messages: List[ChatMessage]
    temperature: Optional[float] = Field(default=1.0, ge=0.0, le=2.0)
    top_p: Optional[float] = Field(default=1.0, ge=0.0, le=1.0)
    n: Optional[int] = Field(default=1, ge=1, le=10)
    stream: Optional[bool] = False
    stop: Optional[Union[str, List[str]]] = None
    max_tokens: Optional[int] = Field(default=None, ge=1)
    presence_penalty: Optional[float] = Field(default=0.0, ge=-2.0, le=2.0)
    frequency_penalty: Optional[float] = Field(default=0.0, ge=-2.0, le=2.0)
    logit_bias: Optional[Dict[str, float]] = None
    user: Optional[str] = None
    functions: Optional[List[Dict[str, Any]]] = None
    function_call: Optional[Union[str, Dict[str, str]]] = None
    tools: Optional[List[Dict[str, Any]]] = None
    tool_choice: Optional[Union[str, Dict[str, Any]]] = None
    response_format: Optional[Dict[str, str]] = None
    seed: Optional[int] = None


class Usage(BaseModel):
    """Usage statistics for the completion.

    All attributes are used for token counting and billing information.
    """

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class Choice(BaseModel):
    """A completion choice.

    Used attributes:
        index: Choice index (always 0 in current implementation)
        message: The generated message
        finish_reason: Reason for completion ("stop")

    Compatibility attributes (unused but included for OpenAI API compatibility):
        logprobs
    """

    index: int
    message: ChatMessage
    finish_reason: Optional[str] = None
    logprobs: Optional[Dict[str, Any]] = None


class ChatCompletionResponse(BaseModel):
    """Response model for chat completions endpoint.

    Used attributes:
        id: Unique completion identifier
        created: Unix timestamp of creation
        model: Model used for completion
        choices: List of completion choices
        usage: Token usage statistics

    Compatibility attributes (unused but included for OpenAI API compatibility):
        object, system_fingerprint
    """

    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[Choice]
    usage: Optional[Usage] = None
    system_fingerprint: Optional[str] = None


class DeltaMessage(BaseModel):
    """Delta message for streaming responses.

    Used attributes:
        role: Message role (sent in first chunk)
        content: Incremental text content

    Compatibility attributes (unused but included for OpenAI API compatibility):
        function_call, tool_calls
    """

    role: Optional[Role] = None
    content: Optional[str] = None
    function_call: Optional[Dict[str, Any]] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None


class ChoiceDelta(BaseModel):
    """A streaming completion choice delta.

    Used attributes:
        index: Choice index (always 0)
        delta: The incremental message content
        finish_reason: Completion reason ("stop" in final chunk)

    Compatibility attributes (unused but included for OpenAI API compatibility):
        logprobs
    """

    index: int
    delta: DeltaMessage
    finish_reason: Optional[str] = None
    logprobs: Optional[Dict[str, Any]] = None


class ChatCompletionStreamResponse(BaseModel):
    """Response model for streaming chat completions.

    Used attributes:
        id: Unique completion identifier
        created: Unix timestamp of creation
        model: Model used for completion
        choices: List of delta choices

    Compatibility attributes (unused but included for OpenAI API compatibility):
        object, usage, system_fingerprint
    """

    id: str
    object: str = "chat.completion.chunk"
    created: int
    model: str
    choices: List[ChoiceDelta]
    usage: Optional[Usage] = None
    system_fingerprint: Optional[str] = None


class ModelInfo(BaseModel):
    """Information about an available model.

    Included for OpenAI API compatibility but not currently used.
    """

    id: str
    object: str = "model"
    created: int
    owned_by: str
    permission: Optional[List[Dict[str, Any]]] = None
    root: Optional[str] = None
    parent: Optional[str] = None


class ModelsResponse(BaseModel):
    """Response model for models endpoint.

    Included for OpenAI API compatibility but not currently used.
    """

    object: str = "list"
    data: List[ModelInfo]


class OpenAIError(BaseModel):
    """OpenAI API error structure.

    Included for OpenAI API compatibility but not currently used.
    """

    message: str
    type: str
    param: Optional[str] = None
    code: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response wrapper.

    Included for OpenAI API compatibility but not currently used.
    """

    error: OpenAIError
