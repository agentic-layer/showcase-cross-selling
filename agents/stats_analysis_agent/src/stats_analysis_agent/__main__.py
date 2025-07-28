import uvicorn
from fastapi import FastAPI

from stats_analysis_agent import a2a_app


def main():
    app = FastAPI(
        title="Stats Analysis Agent API",
        description="API for the Stats Analysis Agent",
        version="1.0.0",
    )

    app.mount("/a2a", a2a_app.build(), name="a2a")

    uvicorn.run(app, host="0.0.0.0")


if __name__ == "__main__":
    main()
