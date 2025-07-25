import pytest
from unittest.mock import Mock, AsyncMock
from openai import OpenAI
from openai.types.chat.chat_completion_user_message_param import ChatCompletionUserMessageParam

from starlette.testclient import TestClient
from google.adk import Agent

from base.openai_api.openai_api import OpenAICompatibleAPI
from base.openai_api.models import ChatCompletionResponse, Choice, ChatMessage, Role, ChatCompletionStreamResponse, ChoiceDelta, DeltaMessage


@pytest.fixture
def dummy_agent() -> Agent:
    """Create a dummy agent for testing."""
    return Agent(
        model="gemini-2.0-flash-exp",
        name="Host_Agent",
        instruction="You are a test insurance agent.",
        description="Test agent for insurance host testing."
    )


@pytest.fixture
def mock_chat_completion_service():
    """Create a mock chat completion service."""
    mock_service = Mock()

    # Mock the create_chat_completion method
    mock_response = ChatCompletionResponse(
        id="test-completion-id",
        object="chat.completion",
        created=1234567890,
        model="Host_Agent",
        choices=[
            Choice(
                index=0,
                message=ChatMessage(
                    role=Role.ASSISTANT,
                    content="Hallo! Gerne helfe ich Ihnen bei Ihren Versicherungsfragen. Als Ihr Broker Success Partner kann ich Sie über unsere verschiedenen Versicherungsprodukte informieren."
                ),
                finish_reason="stop"
            )
        ]
    )

    mock_service.create_chat_completion = AsyncMock(return_value=mock_response)
    
    # Mock streaming response
    async def mock_stream_generator(request, user):
        """Generate mock streaming responses."""
        completion_id = "test-stream-id"
        created = 1234567890
        
        # Send initial chunk with role
        initial_chunk = ChatCompletionStreamResponse(
            id=completion_id,
            created=created,
            model='Host_Agent',
            choices=[
                ChoiceDelta(
                    index=0,
                    delta=DeltaMessage(role=Role.ASSISTANT),
                    finish_reason=None,
                )
            ],
        )
        yield initial_chunk.model_dump_json()
        
        # Send content chunks
        chunks = [
            "Hallo! ",
            "Gerne helfe ich Ihnen ",
            "bei Ihren Versicherungsfragen. ",
            "Als Ihr Broker Success Partner ",
            "kann ich Sie über unsere ",
            "verschiedenen Versicherungsprodukte ",
            "informieren."
        ]
        
        for chunk in chunks:
            stream_response = ChatCompletionStreamResponse(
                id=completion_id,
                created=created,
                model='Host_Agent',
                choices=[
                    ChoiceDelta(
                        index=0,
                        delta=DeltaMessage(content=chunk),
                        finish_reason=None
                    )
                ]
            )
            yield stream_response.model_dump_json()
            
        # Send final chunk
        final_chunk = ChatCompletionStreamResponse(
            id=completion_id,
            created=created,
            model='Host_Agent',
            choices=[
                ChoiceDelta(
                    index=0,
                    delta=DeltaMessage(),
                    finish_reason="stop"
                )
            ]
        )
        yield final_chunk.model_dump_json()
    
    mock_service.stream_chat_completion = mock_stream_generator

    return mock_service


@pytest.fixture
def client(dummy_agent: Agent, mock_chat_completion_service) -> TestClient:
    """Create test client with mocked OpenAI API."""
    api = OpenAICompatibleAPI(agent=dummy_agent)
    # Replace the chat completion service with our mock
    api.chat_completion_service = mock_chat_completion_service

    return TestClient(app=api.app)


@pytest.fixture
def openai_client(client: TestClient) -> OpenAI:
    return OpenAI(
        base_url="http://testserver/v1/Host_Agent",
        http_client=client,
        api_key="dummy-key",
    )


def test_openai_api_chat_completion(openai_client: OpenAI):
    """Test calling the insurance host agent API using the OpenAI library."""

    # Test a simple chat completion
    response = openai_client.chat.completions.create(
        model="insurance-host-agent",
        messages=[
            ChatCompletionUserMessageParam(
                role = "user",
                content = "Hallo, ich bin ein neuer Kunde und möchte mich über Versicherungen informieren."
            )
        ]
    )
    
    # Verify response structure
    assert response.choices is not None
    assert len(response.choices) > 0
    assert response.choices[0].message is not None
    assert response.choices[0].message.content is not None
    assert isinstance(response.choices[0].message.content, str)
    assert len(response.choices[0].message.content) > 0


def test_openai_api_streaming_chat_completion(openai_client: OpenAI):
    """Test streaming chat completion with the insurance host agent API."""
    
    # Test streaming chat completion
    stream = openai_client.chat.completions.create(
        model="Host_Agent",
        messages=[
            ChatCompletionUserMessageParam(
                role="user",
                content="Was sind die wichtigsten Versicherungsarten für Familien?"
            )
        ],
        stream=True
    )
    
    # Collect streaming chunks
    chunks = []
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            chunks.append(chunk.choices[0].delta.content)
    
    # Verify we received streaming data
    assert len(chunks) > 0
    full_response = "".join(chunks)
    assert len(full_response) > 0
    assert "Hallo!" in full_response
    assert "Versicherungsprodukte" in full_response
