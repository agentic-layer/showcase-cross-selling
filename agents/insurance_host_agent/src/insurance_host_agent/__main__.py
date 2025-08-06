import uvicorn
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app
from base import add_health_endpoint

from insurance_host_agent.a2a.a2a import a2a_app
from insurance_host_agent.api.api import api


def main():
    app = FastAPI(
        title="Insurance Host Agent API",
        description="API for the Insurance Host Agent",
        version="1.0.0",
    )

    add_health_endpoint(app)
    
    adk_web = get_fast_api_app(agents_dir="agents/insurance_host_agent/src", web=True)

    app.mount("/a2a", a2a_app, name="a2a")
    app.mount("/api", api, name="api")
    app.mount("/", adk_web, name="web")

    uvicorn.run(app, host="0.0.0.0")


if __name__ == "__main__":
    main()
