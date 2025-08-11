import uvicorn
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app
from insurance_host_agent.api.api import api


def main():
    app = FastAPI(
        title="Stats Analysis Agent API",
        description="API for the Stats Analysis Agent",
        version="1.0.0",
    )

    adk_web = get_fast_api_app(agents_dir="agents/stats_analysis_agent/src", web=True)

    app.mount("/api", api, name="api")
    app.mount("/", adk_web, name="web")

    uvicorn.run(app, host="0.0.0.0")


if __name__ == "__main__":
    main()
