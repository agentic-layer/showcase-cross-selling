# Insurance Products MCP Server

A Model Context Protocol (MCP) server that provides comprehensive insurance product information and services to agents in the cross-selling ecosystem.

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `PRODUCT_DATABASE_URL` | Database connection for product data | No (uses mock data) |
| `PRICING_API_URL` | External pricing service URL | No |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARN, ERROR) | No (default: INFO) |
| `CACHE_TTL` | Cache time-to-live in seconds | No (default: 3600) |

## Running the Server

```bash
# From mcp server
uv run insurance_products

# From workspace root
uv run --package insurance_products insurance_products
```

### Local Development

```bash
# Install dependencies
uv sync
```