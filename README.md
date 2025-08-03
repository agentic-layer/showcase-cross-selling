# Insurance Cross-Selling Use Case

An agentic system for intelligent insurance cross-selling using Google's Agent Development Kit (ADK), Model Context Protocol (MCP) servers, and agent-to-agent communication.

## Overview

This project demonstrates a multi-agent system that orchestrates insurance cross-selling opportunities by analyzing customer data, identifying suitable products, and coordinating customer communications. The system is built using modern agentic architecture principles with clear separation of concerns.

## Architecture

### Components

The system consists of several specialized agents and MCP servers:

#### 🤖 **Agents**
- **[Insurance Host Agent](agents/insurance_host_agent/README.md)**: Main orchestration agent that coordinates customer interactions
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
```

## Development

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

## Deployment

### Docker Compose

```bash
# Start all services
docker compose up

# View logs
docker compose logs -f
```