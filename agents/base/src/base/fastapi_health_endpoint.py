import logging

from fastapi import FastAPI

from .log_filters import EndpointFilter


def add_health_endpoint(app: FastAPI) -> None:
    """Add a standard health check endpoint to the FastAPI app.

    Args:
        app: The FastAPI application instance to add the health endpoint to.
    """

    excluded_endpoints = ["/health"]
    logging.getLogger("uvicorn.access").addFilter(EndpointFilter(excluded_endpoints))

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}
