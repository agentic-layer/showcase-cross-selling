import uvicorn
from fastapi import FastAPI

from cross_selling_agent.a2a.a2a import a2a_app


def main():
    app = FastAPI(
        title="Cross Selling Agent API",
        description="API for the Cross Selling Agent",
        version="1.0.0",
    )

    app.mount("/a2a", a2a_app, name="a2a")

    uvicorn.run(app, host="0.0.0.0")


if __name__ == "__main__":
    main()
