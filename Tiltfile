# Tiltfile for cross-selling use case development

# Load .env file for environment variables
load('ext://dotenv', 'dotenv')
dotenv()

# Create Kubernetes secrets from environment variables
load('ext://secret', 'secret_from_dict')

google_api_key = os.environ.get('GOOGLE_API_KEY', '')
if not google_api_key:
    fail('GOOGLE_API_KEY environment variable is required. Please set it in your shell or .env file.')

k8s_yaml(secret_from_dict(
    name = "api-key-secrets",
    namespace = "use-case-cross-selling",
    inputs = { "GOOGLE_API_KEY": google_api_key }
))

# Apply Kubernetes manifests
k8s_yaml(kustomize('deploy/local'))

# Live update configuration for faster development
live_update_sync = sync('.', '/app')
live_update_run = run('uv pip install -e .', trigger=['pyproject.toml', 'uv.lock'])

# Helper function to convert snake_case to kebab-case
def snake_to_kebab(snake_str):
    return snake_str.replace('_', '-')

# Open ports and sync changes to agents
agents = [
    {'name': 'communications_agent', 'port': '10002:8000'},
    {'name': 'cross_selling_agent', 'port': '10003:8000'},
    {'name': 'insurance_host_agent', 'port': '8000:8000'},
]

for agent in agents:
    agent_name = agent['name']
    docker_build(
        agent_name,
        context='.',
        dockerfile='./agents/Dockerfile',
        build_args={'AGENT_NAME': agent_name},
        live_update=[live_update_sync, live_update_run],
    )
    k8s_resource(snake_to_kebab(agent_name), port_forwards=agent['port'], labels=['agents'])

# Open ports and sync changes to MCP servers
mcp_servers = [
    {'name': 'customer_crm', 'port': '8002:8000'},
    {'name': 'insurance_products', 'port': '8003:8000'},
]

for server in mcp_servers:
    server_name = server['name']
    docker_build(
        server_name,
        context='.',
        dockerfile='./mcp-servers/Dockerfile',
        build_args={'MCP_SERVER_NAME': server_name},
        live_update=[live_update_sync, live_update_run],
    )
    k8s_resource(snake_to_kebab(server_name), port_forwards=server['port'], labels=['mcp-servers'])

config.define_bool("run-tests")
cfg = config.parse()

local_resource(
    'test_e2e_openai_api',
    cmd='./test/e2e/openai-api.sh',
    resource_deps=['insurance-host-agent'],
    auto_init=cfg.get('run-tests', False),
    trigger_mode=TRIGGER_MODE_MANUAL,
)
