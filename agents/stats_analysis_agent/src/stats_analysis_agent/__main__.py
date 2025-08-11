import uvicorn
from base.fastapi_health_endpoint import add_health_endpoint
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app

from .api.api import api


def main():
    app = FastAPI(
        title="Stats Analysis Agent API",
        description="API for the Stats Analysis Agent",
        version="1.0.0",
    )

    add_health_endpoint(app)

    adk_web = get_fast_api_app(agents_dir="agents/stats_analysis_agent/src", web=True)

    app.mount("/api", api, name="api")
    app.mount("/", adk_web, name="web")

    uvicorn.run(app, host="0.0.0.0")


if __name__ == "__main__":
    main()
