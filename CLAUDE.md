# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains an agentic playground with Google ADK (Agent Development Kit) agents and MCP (Model Context Protocol) servers. The main components are:

- **ADK Agents**: Located in `adk-agents/`, these are Google ADK-based agents including a banking hotline agent
- **MCP Server**: Located in `mcp-server/`, contains MCP servers, like one that provides banking product data via MCP protocol

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
uv run mcp dev bank_products/main.py
```

## Architecture

### ADK Agents Structure
- Each agent is a Python module in `adk-agents/`
- Agents use Google ADK framework with `Agent` class from `google.adk.agents`
- Tools can be Python functions or MCP toolsets via `MCPToolset`
- Example agent: `bank_hotline_agent/agent.py` defines a German-language banking assistant

### MCP Server Structure
- MCP servers provide external tools/resources to agents
- Built using FastMCP framework (`mcp.server.fastmcp`)
- Resources are decorated functions that agents can call
- Example: `bank_products/main.py` provides banking product information

### Integration Pattern
Agents can integrate with MCP servers using `MCPToolset` with `StdioServerParameters` to connect via subprocess communication.

## Dependencies
- Python 3.13+
- google-adk>=1.0.0
- mcp[cli]>=1.9.1
- uv for dependency management