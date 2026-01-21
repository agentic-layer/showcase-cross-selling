# Insurance Cross-Selling Agentic System

A multi-agent system for intelligent insurance cross-selling built with Google's Agent Development Kit (ADK), Model Context Protocol (MCP) servers, and agent-to-agent communication. This system orchestrates insurance cross-selling opportunities by analyzing customer data, identifying suitable products, and coordinating customer communications through specialized AI agents.

This showcase demonstrates the capabilities of the [Agentic Layer platform](http://agentic-layer.ai/) for building complex multi-agent AI systems.
Further information about the Agentic Layer can be found in our [documentation](https://docs.agentic-layer.ai/).

----

## Table of Contents

- [Intro](#introduction)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Development](#development)
- [End-to-End (E2E) Testing](#end-to-end-e2e-testing)
- [Testing Tools and Their Configuration](#testing-tools-and-their-configuration)
- [Sample Data](#sample-data)
- [Project Architecture](#project-architecture)

---

## Introduction

In this showcase, a host agent uses tools and calls other agents to facilitate user requests like so:

**Conversation 1:**

> Nutzer: Bitte bereite mir ein Kundengespräch mit der Kundin Anna Müller vor.
>
> Agent: Gern helfe ich dir, das Gespräch vorzubereiten. Hier sind Optionen für verschiedene Verkaufsstrategien: …
>
> Nutzer: Bitte verschicke eine E-Mail an die Kundin mit einer Agenda.
>
> Agent: Erledigt.

**Conversation 2:**

> Nutzer: Bitte bereite mir ein Kundengespräch mit dem Kunden Thomas Schmidt vor. Sende außerdem eine Erinnerungs-Mail an den Kunden, dass das Gespräch stattfindet.
>
> Agent: Hier ist die Vorbereitung für dein Gespräch. Die Erinnerungsmail habe ich verschickt: …


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
# Install Python dependencies for all MCP servers
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

# LiteLLM Api Key. Defaults to the master key (optional)
LITELLM_PROXY_API_KEY=sk-your-api-key
```

### 4. Start the Application

Launch all services using Tilt:

```bash
# Start all agents and MCP servers
tilt up
```
We recommend using the included Librechat instance (http://localhost:11003) to easily have conversations with the insurance host agent.

**Expected Results:**
- Grafana at http://localhost:11000
- AI Gateway at http://localhost:11001
- Agent Gateway at http://localhost:11002
- Librechat (chat interface) at http://localhost:11003
- Insurance Host Agent at http://localhost:11010
- Communications Agent at http://localhost:11011
- Cross-Selling Agent at http://localhost:11012
- Customer CRM MCP Server at http://localhost:11020
- Insurance Products MCP Server at http://localhost:11021

## Development

### Developer Setup
For detailed contributing guidelines, refer to the [global contributing guide](https://github.com/agentic-layer/.github?tab=contributing-ov-file).

**Mandatory first step for contributors:**
```bash
# Activate pre-commit hooks
pre-commit install
```

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

**Test Coverage:**
- Cross-selling strategy generation for customer `Anna Müller`
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
API_ENDPOINT="http://localhost:11002/api/v1/chat/completions"
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

**Sample Customer Record (Anna Müller):**
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
curl -X POST http://localhost:11002/insurance-host-agent \
    -H "Content-Type: application/json" \
    -d '{
      "jsonrpc": "2.0",
      "id": 1,
      "method": "message/send",
      "params": {
        "message": {
          "role": "user",
          "parts": [
            {
              "kind": "text",
              "text": "Welche Cross-Selling-Möglichkeiten gibt es für unsere Kundin Anna Müller?"
            }
          ],
          "messageId": "9229e770-767c-417b-a0b0-f0741243c589",
          "contextId": "abcd1234-5678-90ab-cdef-1234567890ab"
        },
        "metadata": {"conversationId": "9229e770-767c-417b-a0b0-f0741243c589"}
      }
    }'
```

**Database Seeding:**
Customer and product data is automatically initialized when MCP servers start. No manual seeding required.


## Project Architecture

```
mcp-servers/
├── customer_crm/        # Customer relationship management data
└── insurance_products/  # Insurance product catalog server
```
