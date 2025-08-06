"""FastAPI utilities for shared functionality across agents."""

from fastapi import FastAPI


def add_health_endpoint(app: FastAPI) -> None:
    """Add a standard health check endpoint to the FastAPI app.
    
    Args:
        app: The FastAPI application instance to add the health endpoint to.
    """
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}