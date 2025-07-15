# Base Agent Package

This package provides shared functionality and utilities for all agents in the cross-selling use case.

## Development

This package is part of the uv workspace and is automatically installed when working with other agents.

```bash
# Install dependencies
uv sync
```

## Integration

Other agents can import and use components from this package:

```python
from base.agent_executor import ADKAgentExecutor
# Use shared functionality
```
