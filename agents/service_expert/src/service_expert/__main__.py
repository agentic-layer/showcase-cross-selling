import uvicorn
from fastapi import FastAPI

from service_expert.a2a.a2a import a2a_app


def main():
    app = FastAPI(
        title="Service Expert Agent API",
        description="API for the Service Expert Agent",
        version="1.0.0",
    )

    app.mount("/a2a", a2a_app, name="a2a")

    uvicorn.run(app, host="0.0.0.0")


if __name__ == "__main__":
    main()
