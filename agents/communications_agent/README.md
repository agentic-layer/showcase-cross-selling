# Communications Agent

A specialized agent for handling communication workflows, including email and Slack integration, within the insurance cross-selling use case.

## Configuration

### Slack Setup

1. **Bot Token**: Set your Slack bot token as an environment variable:
   ```bash
   export SLACK_BOT_TOKEN=xoxb-your-bot-token-here
   ```

2. **Bot Permissions**: Ensure your Slack bot has the following scopes:
   - `chat:write`: Send messages
   - `channels:read`: Read channel information
   - `users:read`: Read user information

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SLACK_BOT_TOKEN` | Slack bot token for API access | Yes |

## Usage

### Running the Agent

```bash
# From agent
uv run communications_agent

# From workspace root
uv run --package communications_agent communications_agent
```

## Development

### Local Development

```bash
# Install dependencies
uv sync
```