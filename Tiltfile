# Tiltfile for cross-selling use case development

update_settings(max_parallel_updates=10)

# Configure Tilt to work with Agent Runtime Operator's custom Agent CRDs
# Without these configurations, Tilt cannot properly manage Agent resources created by the operator:
# image_json_path: Required because Agent CRDs store image references in a custom field ({.spec.image})
#                  rather than standard Kubernetes image fields that Tilt knows about by default
# pod_readiness: Required because the operator creates pods asynchronously after Agent CRD creation,
#                and Tilt must wait for operator-managed pods rather than assuming immediate readiness
k8s_kind(
    'Agent',
    image_json_path='{.spec.image}',
    pod_readiness='wait'
)

# Check if Agent Runtime Operator is running before proceeding
def check_operator_running():
    result = local('kubectl get pods -n agent-runtime-operator-system -l control-plane=controller-manager -o jsonpath="{.items[*].status.phase}" 2>/dev/null || echo "NOT_FOUND"', quiet=True)
    result_str = str(result).strip()
    if result_str == 'NOT_FOUND' or 'Running' not in result_str:
        fail('Agent Runtime Operator is not running. Please install and deploy it first. See: https://github.com/agentic-layer/agent-runtime-operator?tab=readme-ov-file#getting-started')

check_operator_running()

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
    namespace = "llm-gateway",
    inputs = { "GOOGLE_API_KEY": google_api_key }
))

litellm_master_key = os.environ.get('LITELLM_MASTER_KEY', 'sk-admin')
k8s_yaml(secret_from_dict(
    name = "litellm-master-key-secrets",
    namespace = "llm-gateway",
    inputs = { "LITELLM_MASTER_KEY": litellm_master_key }
))
k8s_yaml(secret_from_dict(
    name = "litellm-proxy-api-key-secret",
    namespace = "use-case-cross-selling",
    inputs = { "LITELLM_PROXY_API_KEY": os.environ.get('LITELLM_PROXY_API_KEY', litellm_master_key) }
))

# Apply Kubernetes manifests
k8s_yaml(kustomize('deploy/local'))

# Live update configuration for faster development (note: this copies the whole project, not only the respective subfolder)
live_update_sync = sync('.', '/app')

# Helper function to convert snake_case to kebab-case
def snake_to_kebab(snake_str):
    return snake_str.replace('_', '-')

# Open ports and sync changes to agents
agents = [
    {'name': 'communications_agent', 'port': '10002:8000'},
    {'name': 'cross_selling_agent', 'port': '10003:8000'},
    {'name': 'insurance_host_agent', 'port': '8000:8000'},
    {'name': 'stats_analysis_agent', 'port': '10004:8000'},
]

for agent in agents:
    agent_name = agent['name']
    docker_build(
        agent_name,
        context='.',
        dockerfile='./agents/Dockerfile',
        build_args={'AGENT_NAME': agent_name},
        live_update=[live_update_sync],
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
        live_update=[live_update_sync],
    )
    k8s_resource(snake_to_kebab(server_name), port_forwards=server['port'], labels=['mcp-servers'])

# Expose the Monitoring stack (Grafana)
k8s_resource('lgtm', port_forwards=['3000:3000', '4318:4318', '4317:4317'])

# Expose LLM Gateway (LiteLLM)
k8s_resource('litellm', port_forwards='4000:4000')

# Add flag to run tests
config.define_bool("run-tests")
cfg = config.parse()

local_resource(
    'test_e2e_openai_api',
    cmd='./test/e2e/openai-api.sh',
    resource_deps=['insurance-host-agent', 'cross-selling-agent', 'customer-crm', 'insurance-products', 'litellm', 'lgtm', 'stats-analysis-agent', 'communications-agent'],
    auto_init=cfg.get('run-tests', False),
    trigger_mode=TRIGGER_MODE_MANUAL,
)
