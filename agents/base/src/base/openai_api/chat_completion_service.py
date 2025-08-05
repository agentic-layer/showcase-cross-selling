import time
import uuid
from typing import AsyncGenerator, List

from google.adk.agents import Agent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from base.openai_api.models import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionStreamResponse,
    ChatMessage,
    Choice,
    ChoiceDelta,
    DeltaMessage,
    Role,
    Usage,
)


class ChatCompletionService:
    def __init__(self, agent: Agent):
        self.runner = Runner(
            app_name=agent.name,
            agent=agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )

    async def create_chat_completion(self, request: ChatCompletionRequest, user: str) -> ChatCompletionResponse:
        """Create a non-streaming chat completion."""
        completion_id = await self._create_completion_id()
        created = int(time.time())

        session = await self.runner.session_service.create_session(
            app_name=self.runner.agent.name,
            user_id=user,
            state={},
            session_id=str(uuid.uuid4()),
        )

        # Convert messages to a single query string
        query = self._messages_to_query(request.messages)

        content = types.Content(role="user", parts=[types.Part.from_text(text=query)])

        response_text = ""
        prompt_tokens = 0
        completion_tokens = 0
        async for event in self.runner.run_async(user_id=user, session_id=session.id, new_message=content):
            if event.is_final_response() and event.content and event.content.parts:
                if event.usage_metadata:
                    prompt_tokens = event.usage_metadata.prompt_token_count or 0
                    completion_tokens = event.usage_metadata.candidates_token_count or 0
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text and not part.thought:
                        response_text += part.text

        return ChatCompletionResponse(
            id=completion_id,
            created=created,
            model=request.model,
            choices=[
                Choice(
                    index=0,
                    message=ChatMessage(role=Role.ASSISTANT, content=response_text),
                    finish_reason="stop",
                )
            ],
            usage=Usage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens,
            ),
        )

    async def stream_chat_completion(self, request: ChatCompletionRequest, user: str) -> AsyncGenerator[str, None]:
        """Create a non-streaming chat completion."""
        completion_id = await self._create_completion_id()
        created = int(time.time())

        session = await self.runner.session_service.create_session(
            app_name=self.runner.agent.name,
            user_id=user,
            state={},
            session_id=str(uuid.uuid4()),
        )

        # Convert messages to a single query string
        query = self._messages_to_query(request.messages)

        content = types.Content(role="user", parts=[types.Part.from_text(text=query)])

        try:
            # Send initial chunk
            initial_chunk = ChatCompletionStreamResponse(
                id=completion_id,
                created=created,
                model=request.model,
                choices=[
                    ChoiceDelta(
                        index=0,
                        delta=DeltaMessage(role=Role.ASSISTANT),
                        finish_reason=None,
                    )
                ],
            )

            yield initial_chunk.model_dump_json()

            # Stream agent response
            async for event in self.runner.run_async(user_id=user, session_id=session.id, new_message=content):
                print(f"Event received: {event}")
                print(event)
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, "text") and part.text and not part.thought:
                            chunk = ChatCompletionStreamResponse(
                                id=completion_id,
                                created=created,
                                model=request.model,
                                choices=[
                                    ChoiceDelta(
                                        index=0,
                                        delta=DeltaMessage(content=part.text),
                                        finish_reason=None,
                                    )
                                ],
                            )

                            yield chunk.model_dump_json()

            # Send final chunk
            final_chunk = ChatCompletionStreamResponse(
                id=completion_id,
                created=created,
                model=request.model,
                choices=[
                    ChoiceDelta(
                        index=0,
                        delta=DeltaMessage(),
                        finish_reason="stop",
                    )
                ],
            )

            yield final_chunk.model_dump_json()

        except Exception as e:
            error_chunk = ChatCompletionStreamResponse(
                id=completion_id,
                created=created,
                model=request.model,
                choices=[
                    ChoiceDelta(
                        index=0,
                        delta=DeltaMessage(content=f"Error: {str(e)}"),
                        finish_reason="stop",
                    )
                ],
            )

            yield error_chunk.model_dump_json()

    async def _create_completion_id(self):
        completion_id = f"chatcmpl-{uuid.uuid4().hex}"
        return completion_id

    def _messages_to_query(self, messages: List[ChatMessage]) -> str:
        """Convert chat messages to a single query string."""
        query_parts = []

        for message in messages:
            if message.role == Role.SYSTEM and message.content:
                query_parts.append(f"System: {message.content}")
            elif message.role == Role.USER and message.content:
                query_parts.append(message.content)
            elif message.role == Role.ASSISTANT and message.content:
                query_parts.append(f"Assistant: {message.content}")

        return "\n\n".join(query_parts)
