# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
For more detailed information, refer to the [README.md](./README.md) file.

## Project Overview

This repository contains an agentic playground with Google ADK (Agent Development Kit) agents and MCP (Model Context Protocol) servers. The main components are:

- **ADK Agents**: Located in `agents/`, these are Google ADK-based agents including a banking hotline agent
- **MCP Server**: Located in `mcp-servers/`, contains MCP servers, like one that provides banking product data via MCP protocol

## Development Setup

```shell
# Install dependencies
brew bundle

# Authenticate with Google Cloud (required for ADK)
gcloud auth application-default login
```

## Common Commands

### Running ADK Agents
```shell
cd adk-agents
uv run adk web
```
Navigate to `http://localhost:8080` to access the ADK Web UI with agent selection dropdown.

### Running MCP Server
```shell
cd mcp-server
```

## Architecture

### Agents Structure
- Each agent is a Python module in `agents/`
- Agents use Google ADK framework with `Agent` class from `google.adk.agents`
- Tools can be Python functions or MCP toolsets via `MCPToolset`
- Current agents include:
  - `base/`: Shared base components including A2A agent executor and OpenAI API integration
  - `communications_agent/`: Handles drafting professional communications
  - `cross_selling_agent/`: Identifies cross-selling opportunities from CRM data
  - `insurance_host_agent/`: Orchestrates customer support for insurance brokers (German language)
  - `stats_analysis_agent/`: Provides statistical analysis capabilities
- Each agent follows the structure: `agent_name/src/agent_name/agent.py`
- Each agent includes A2A (Agent-to-Agent) integration in `agent_name/src/agent_name/a2a/`
- For detailed instructions on creating new agents, see the "Adding a New Agent" section in [README.md](./README.md)

### MCP Server Structure
- MCP servers provide external tools/resources to agents
- Built using FastMCP framework (`mcp.server.fastmcp`)
- Resources are decorated functions that agents can call
- Example: `bank_products/main.py` provides banking product information

### Agents Network Architecture

The agents operate as a distributed network using the Agent-to-Agent (A2A) protocol:

#### Network Structure
- **Host Agent (`insurance_host_agent`)**: The central orchestrator that routes user requests to appropriate specialized agents
- **Specialized Agents**: Each agent exposes specific capabilities and skills through A2A cards
- **Communication Protocol**: Agents communicate via HTTP using A2A message format

#### Agent Deployment
Each agent must:
1. **Define Agent Card**: Create `AgentCard` with capabilities, skills, and metadata in `a2a/card.py`
2. **Setup A2A Application**: Configure `A2AStarletteApplication` with `DefaultRequestHandler` and `A2AAgentExecutor` in `a2a/a2a.py`
3. **Create Main Entry Point**: Implement `__main__.py` with FastAPI app that mounts A2A endpoint at `/a2a`
   - **Health Checking**: No manual health endpoint needed - health checking is handled by agent-runtime-operator via A2A endpoints
4. **Network Accessibility**: Run with `uvicorn` on `0.0.0.0:8000` for inter-agent communication
5. **Use Base Components**: Leverage shared `A2AAgentExecutor` from `base/` module for consistent behavior
6. **Register with Host Agent**: Add agent URL to the host agent's `subagent_urls` for routing
7. **Added to docker-compose**: Ensure `./cross-selling-use-case/compose.yml` includes your new agent
8. **Added to github workflows**: Ensure `./cross-selling-use-case/.github/workflows/build-and-check.yml` and `./cross-selling-use-case/.github/workflows/build-and-publish.yml` include your new agent and its Dockerfile under strategy matrix include

#### Orchestration Flow
1. User interacts with `insurance_host_agent` (the orchestrator)
2. Host agent analyzes the request and determines which specialized agent(s) to call
3. Host agent routes requests to appropriate agents via HTTP A2A protocol
4. Specialized agents process tasks and return results to the host agent
5. Host agent consolidates responses and presents final output to the user

#### Example Agent URLs
- `http://communications-agent:8000/` - Professional communication drafting
- `http://cross-selling-agent:8000/` - CRM analysis and cross-selling opportunities
- `http://insurance-host-agent:8000/` - Main orchestrator endpoint

### Integration Pattern
Agents can integrate with MCP servers using `MCPToolset` with `StdioServerParameters` to connect via subprocess communication.

## Dependencies
- Python 3.13+
- google-adk>=1.0.0
- mcp[cli]>=1.9.1
- uv for dependency management
