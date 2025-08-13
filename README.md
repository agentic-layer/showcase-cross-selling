# Insurance Cross-Selling Use Case

An agentic system for intelligent insurance cross-selling using Google's Agent Development Kit (ADK), Model Context
Protocol (MCP) servers, and agent-to-agent communication.

## Overview

This project demonstrates a multi-agent system that orchestrates insurance cross-selling opportunities by analyzing
customer data, identifying suitable products, and coordinating customer communications. The system is built using modern
agentic architecture principles with clear separation of concerns.

## Architecture

### Components

The system consists of several specialized agents and MCP servers:

#### 🤖 **Agents**

- **[Insurance Host Agent](agents/insurance_host_agent/README.md)**: Main orchestration agent that coordinates customer
  interactions
- **[Cross-Selling Agent](agents/cross_selling_agent/README.md)**: Identifies and presents cross-selling opportunities
- **[Communications Agent](agents/communications_agent/README.md)**: Handles external communications (Slack, email)
- **[Base Agent](agents/base/README.md)**: Shared utilities and execution framework

#### 🔌 **MCP Servers**

- **[Customer CRM](mcp-servers/customer_crm/README.md)**: Customer relationship management data and services
- **[Insurance Products](mcp-servers/insurance_products/README.md)**: Insurance product catalog and information

## Prerequisites

- **Python 3.13+**: Required for all components
- **Google Cloud Account**: For ADK and Vertex AI integration
- **Slack Bot Token**: For communications agent (optional)
- **uv**: Package manager for Python projects

## Setup

### 1. Install Dependencies

```bash
# Install system dependencies
brew bundle

# Install Python dependencies for all agents and MCP servers
uv sync --all-packages
```

### 2. Google Cloud Authentication

A connection to Google Cloud is required to use Gemini models.

```bash
# Authenticate with Google Cloud
gcloud auth application-default login
```

### 3. Environment Configuration

Create a `.env` file in the [agents](./agents) directory with the following content:

```dotenv
# Google Cloud Configuration
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_CLOUD_PROJECT=qaware-paal
GOOGLE_CLOUD_LOCATION=europe-west3
GOOGLE_API_KEY=your-google-api-key

# Slack Integration (optional)
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token

# LiteLLM Api Key. Defaults to the master key (optional)
LITELLM_PROXY_API_KEY=sk-your-api-key
```

### 4. Local Kubernetes Setup

For local development, you need a Kubernetes cluster.
Use your preferred method to set up a local Kubernetes cluster. Docker Desktop, Ranger Desktop and Colima all provide standard Kubernetes clusters. Those are recommended.

Alternatively, use `k3d` for a lightweight solution.

Hint: Ensure Docker can use **at least** 8GB of memory. For Colima users: `colima start --memory 8`

Using `k3d`, create a local registry and cluster:
```
brew install k3d
k3d registry create local-paal-registry --port 6169
# Currently required for Colima users. See https://github.com/k3d-io/k3d/pull/1584
export K3D_FIX_DNS=0
k3d cluster create local-paal --registry-use k3d-local-paal-registry
```

## Development

### Local Deployment

```bash
# Start all services
tilt up

# View logs
tilt logs
```

Visit http://localhost:8000/ to access the ADK Web UI or access the OpenAI API at http://localhost:8000/api.

API specifications can be found at http://localhost:8000/api/docs.

You'll have access to the insurance host agent. Example questions:

- "Welche Cross-Selling-Möglichkeiten gibt es für unsere Kundin Anna Müller mit der Kundennummer cust001?"
- "Verfasse eine E-Mail an Anna Müller, um ihr unsere neuen Versicherungsprodukte vorzustellen."

The traces can be viewed
in [Grafana](http://localhost:3000/a/grafana-exploretraces-app/explore?from=now-30m&to=now&timezone=browser&var-ds=Tempo&var-primarySignal=nestedSetParent%3C0&var-filters=&var-metric=rate&var-groupBy=resource.service.name&var-spanListColumns=&var-latencyThreshold=&var-partialLatencyThreshold=&actionView=traceList).

### Code Quality

The project includes comprehensive code quality tools:

```bash
# Run all checks
uv run poe check

# Individual checks
uv run poe mypy          # Type checking
uv run poe ruff          # Linting and formatting
uv run poe bandit        # Security analysis
uv run poe lint-imports  # Import linting
uv run poe test          # Run tests
```

### Workspace Structure

The project uses uv workspace for dependency management:

```
├── agents/                    # Agent implementations
│   ├── base/                 # Shared agent utilities
│   ├── communications_agent/ # Communication handling
│   ├── cross_selling_agent/  # Cross-selling logic
│   └── insurance_host_agent/ # Main orchestration
├── mcp-servers/              # MCP server implementations
│   ├── customer_crm/        # Customer data server
│   └── insurance_products/  # Product catalog server
├── pyproject.toml           # Workspace configuration
└── uv.lock                  # Dependency lock file
```

### Adding a New Agent

To add a new agent to the project, follow these steps:

#### 1. Create the Agent Package

```bash
# Create a new agent package
uv init --package agents/<NEW_AGENT_NAME>

# Example: Creating a fraud detection agent
uv init --package agents/any_insurance_agent
```

#### 2. Configure Dependencies

Edit the new agent's `pyproject.toml` file as follows:

- Add the base dependency
- Point the project.script to the main function of the new agent
- Name the project.script the same as the agent package name

```toml
[project]
name = "any-insurance-agent"
version = "0.1.0"
description = "An agent used for any insurance use case"
readme = "README.md"
requires-python = ">=3.13"
dependencies = [
    "base",
    # Add other specific dependencies here
]

[tool.uv.sources]
base = { workspace = true }

[project.scripts]
any_insurance_agent = "any_insurance_agent.__main__:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

#### 3. Install and Test

```bash
# Install dependencies
uv sync

# Test the new agent
uv run --package <NEW_AGENT_NAME> <NEW_AGENT_NAME>
```
