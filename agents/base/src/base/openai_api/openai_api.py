"""
OpenAI-compatible REST API implementation using FastAPI.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.adk.agents import Agent
from sse_starlette.sse import EventSourceResponse

from .chat_completion_service import ChatCompletionService
from .models import (
    ChatCompletionRequest,
)


class OpenAICompatibleAPI:
    """OpenAI-compatible API server using FastAPI."""

    def __init__(self, agent: Agent):
        self.app = FastAPI(
            title="OpenAI Compatible API",
            description=f"OpenAI-compatible REST API for {agent.name}",
            version="1.0.0",
        )

        # Setup CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Register routes
        self._register_routes()

        self.agent_name = agent.name
        self.chat_completion_service = ChatCompletionService(agent)

    def _register_routes(self):
        """Register all API routes."""

        @self.app.post("/v1/chat/completions")
        async def chat_completions(request: ChatCompletionRequest, user: str = "anonymous"):
            """Create a chat completion."""
            try:
                if request.stream:
                    return EventSourceResponse(
                        self.chat_completion_service.stream_chat_completion(request, user),
                        media_type="text/event-stream",
                    )
                else:
                    return await self.chat_completion_service.create_chat_completion(request, user)

            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": {
                            "message": f"Internal server error: {str(e)}",
                            "type": "internal_server_error",
                            "code": "internal_error",
                        }
                    },
                )


def create_openai_api(agent: Agent) -> FastAPI:
    """Create an OpenAI-compatible FastAPI application."""
    api = OpenAICompatibleAPI(agent=agent)
    return api.app
