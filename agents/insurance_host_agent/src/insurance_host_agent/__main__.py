import uvicorn
from fastapi import FastAPI

from insurance_host_agent.a2a.a2a import a2a_app
from insurance_host_agent.api.api import api


def main():

    app = FastAPI(
        title="Insurance Host Agent API",
        description="API for the Insurance Host Agent",
        version="1.0.0",
    )

    app.mount("/a2a", a2a_app, name="a2a")
    app.mount("/api", api, name="api")

    uvicorn.run(app, host="0.0.0.0")

if __name__ == "__main__":
    main()
