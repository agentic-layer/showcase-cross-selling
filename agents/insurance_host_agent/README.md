# Insurance Host Agent

The main orchestration agent that coordinates customer support interactions and manages the flow between specialized agents in the insurance cross-selling ecosystem.

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `CROSS_SELLING_AGENT_URL` | URL for cross-selling agent | Yes |
| `COMMUNICATIONS_AGENT_URL` | URL for communications agent | Yes |
| `CUSTOMER_CRM_URL` | URL for customer CRM MCP server | Yes |
| `INSURANCE_PRODUCTS_URL` | URL for insurance products MCP server | Yes |
| `HOST_AGENT_PORT` | Port for the host agent server | No (default: 8000) |


### Running the Agent

```bash
# From agent
uv run insurance_host_agent

# From workspace root
uv run --package insurance_host_agent insurance_host_agent
```

### Local Development

```bash
# Install dependencies
uv sync
```