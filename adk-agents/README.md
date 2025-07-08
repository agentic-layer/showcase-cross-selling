# Google ADK Agents

## Run the local ADK Web Server

```shell
uv run adk web
```

Navigate to `http://localhost:8080` to access the ADK Web UI.

It has a drop-down menu to select the agent.

For example question for the bank_hotline_agent, see [examples.md](bank_hotline_agent/examples.md).

## Run the tests

### Using pytest

```shell
uv run pytest
```

This will run all tests.
The tests currently

### Using adk eval

```shell
adk eval bank_hotline_agent bank_hotline_agent/general_information.evalset.json
```

### Using adk web

You can also select the Evalset in the ADK Web UI and run the evals from there.
