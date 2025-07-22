# Agent card (metadata)
import uvicorn
from fastapi import FastAPI

from communications_agent.a2a.a2a import a2a_app


def main():
    app = FastAPI(
        title="Communications Agent API",
        description="API for the Communications Agent",
        version="1.0.0",
    )
    app.mount("/a2a", a2a_app, name="a2a")

    uvicorn.run(app, host="0.0.0.0")


if __name__ == "__main__":
    main()
