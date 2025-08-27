import uvicorn
from base.fastapi_health_endpoint import add_health_endpoint
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google.adk.cli.fast_api import get_fast_api_app
import os

from .a2a.a2a import a2a_app
from .api.api import api


def main():
    app = FastAPI(
        title="Insurance Host Agent API",
        description="API for the Insurance Host Agent",
        version="1.0.0",
    )

    # Configure CORS origins from environment variable or use defaults
    cors_origins = os.getenv("CORS_ORIGINS",
        "http://localhost:3000,http://localhost:8080,https://chat-iframe.k8s.agentic-layer.ai,https://cross-selling-agent.k8s.agentic-layer.ai"
    ).split(",")

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin.strip() for origin in cors_origins],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    add_health_endpoint(app)

    adk_web = get_fast_api_app(agents_dir="agents/insurance_host_agent/src", web=True)

    app.mount("/a2a", a2a_app, name="a2a")
    app.mount("/api", api, name="api")
    app.mount("/", adk_web, name="web")

    uvicorn.run(app, host="0.0.0.0")


if __name__ == "__main__":
    main()
