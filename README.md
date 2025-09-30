# Insurance Cross-Selling Agentic System

> **🔒 Private Repository** - This is a private repository containing proprietary demo showcases.


A sophisticated multi-agent system for intelligent insurance cross-selling built with Google's Agent Development Kit (ADK), Model Context Protocol (MCP) servers, and agent-to-agent communication. This system orchestrates insurance cross-selling opportunities by analyzing customer data, identifying suitable products, and coordinating customer communications through specialized AI agents.

----

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Development](#development)
- [End-to-End (E2E) Testing](#end-to-end-e2e-testing)
- [Testing Tools and Their Configuration](#testing-tools-and-their-configuration)
- [Sample Data](#sample-data)
- [Project Architecture](#project-architecture)

----

## Prerequisites

The following tools and dependencies are required to run this project:

- **Python 3.13+**: Required for all agent components and MCP servers
- **Google Cloud SDK**: For ADK and Vertex AI integration
- **uv 0.5.0+**: Python package manager for dependency management
- **Tilt**: Kubernetes development environment orchestration
- **Docker**: For containerization and local Kubernetes
- **Google Cloud Account**: With access to Vertex AI or Google AI APIs
- **Slack Bot Token** (optional): For communications agent integration

----

## Getting Started

### 1. Install Dependencies

```bash
# Install system dependencies via Homebrew
brew bundle
```
```bash
# Install Python dependencies for all agents and MCP servers
uv sync --all-packages
```

### 2. Authentication Setup

```bash
# Authenticate with Google Cloud for AI model access
gcloud auth application-default login
```


### 3. Environment Configuration

Create a `.env` file in the root directory with the following content:

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

### 4. Agent Runtime Operator Setup

The Agent Runtime Operator is required for agent deployment and management. For detailed setup instructions, please refer to the [Agent Runtime Operator Getting Started guide](https://github.com/agentic-layer/agent-runtime-operator?tab=readme-ov-file#getting-started).

**Note:** Ensure the operator is installed and running in your Kubernetes cluster before proceeding to step 5.

### 5. Start the Application

Launch all services using Tilt:

```bash
# Start all agents and MCP servers
tilt up
```
```bash
# View real-time logs
tilt logs
```

**Expected Results:**
- ADK Web UI available at http://localhost:8000/
- OpenAI-compatible API available at http://localhost:8000/api
- API documentation at http://localhost:8000/api/docs
- Grafana observability dashboard at http://localhost:3000

## Development

### Developer Setup
For detailed contributing guidelines, refer to the [global contributing guide](https://github.com/agentic-layer/.github?tab=contributing-ov-file).

**Mandatory first step for contributors:**
```bash
# Activate pre-commit hooks
pre-commit install
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

**Agent Development Guidelines:**
- Follow the existing agent structure in `agents/`
- Implement A2A (Agent-to-Agent) communication protocols
- Use the shared `base` package for common utilities
- Create comprehensive agent cards for capability description
- Ensure Kubernetes deployment compatibility

### Code Quality Standards

**Code Style:**
- **Linting**: Ruff with 120 character line limit
- **Type Checking**: mypy for static type analysis
- **Security**: Bandit for security vulnerability detection
- **Import Organization**: import-linter for dependency management

**Development Commands:**
```bash
# Run all quality checks
uv run poe check

# Individual checks
uv run poe mypy          # Type checking
uv run poe ruff          # Linting and formatting
uv run poe bandit        # Security analysis
uv run poe lint-imports  # Import dependency validation
uv run poe test          # Execute test suite

# Auto-formatting
uv run poe format        # Code formatting
uv run poe lint          # Auto-fix linting issues
```


## End-to-End (E2E) Testing

### Running E2E Tests

Execute the end-to-end test suite to validate the complete agent workflow:

```bash
# Run the cross-selling conversation test
./test/e2e/openai-api.sh
```

**Prerequisites for E2E Tests:**
- All services must be running (`tilt up`)
- Insurance Host Agent accessible at `http://localhost:8000`
- Customer CRM and Insurance Products MCP servers operational
- Network connectivity between all agent components

**Test Coverage:**
- Cross-selling strategy generation for customer `cust001`
- Agent-to-agent communication validation
- OpenAI-compatible API endpoint functionality
- Response content validation for German language interactions

## Testing Tools and Their Configuration

### Testing Framework

**Primary Tool: Bash/cURL Integration Tests**
- **Location**: `test/e2e/openai-api.sh`
- **Configuration**: Tests use OpenAI-compatible API endpoints
- **Validation**: Response content matching using `grep` with German keywords

**Example Test Configuration:**
```bash
# API endpoint configuration
API_ENDPOINT="http://localhost:8000/api/v1/chat/completions"
MODEL_NAME="insurance_host_agent"
TIMEOUT="90"  # seconds
```
```bash
# Content validation patterns
EXPECTED_PATTERNS="cust001\|cross.sell\|strategie\|kunde"
```


## Sample Data

### Customer CRM Data

The system includes mock customer data accessible through the Customer CRM MCP server:

**Sample Customer Record (cust001):**
```json
{
  "customer_id": "cust001",
  "name": "Anna Müller",
  "current_policies": ["auto_insurance", "home_insurance"],
  "demographics": {
    "age": 35,
    "location": "Munich",
    "income_level": "middle"
  }
}
```

**Sample API Request:**
```bash
# Test cross-selling recommendation
curl -X POST http://localhost:8000/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "insurance_host_agent",
    "messages": [
      {
        "role": "user",
        "content": "Welche Cross-Selling-Möglichkeiten gibt es für unsere Kundin Anna Müller mit der Kundennummer cust001?"
      }
    ]
  }'
```

**Database Seeding:**
Customer and product data is automatically initialized when MCP servers start. No manual seeding required.



## Project Architecture

```
agents/
├── base/                 # Shared utilities and A2A framework
├── insurance_host_agent/ # Main orchestration agent
├── cross_selling_agent/  # Cross-selling logic implementation
└── communications_agent/ # External communication handling

mcp-servers/
├── customer_crm/        # Customer relationship management data
└── insurance_products/  # Insurance product catalog server
```
