# Customer CRM MCP Server

A Model Context Protocol (MCP) server that provides customer relationship management data and services to agents in the insurance cross-selling ecosystem.

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | Database connection string | No (uses mock data) |
| `CRM_API_KEY` | API key for external CRM system | No |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARN, ERROR) | No (default: INFO) |


## Running the Server

```bash
# From mcp server
uv run customer_crm

# From workspace root
uv run --package customer_crm customer_crm
```

### Local Development

```bash
# Install dependencies
uv sync
```