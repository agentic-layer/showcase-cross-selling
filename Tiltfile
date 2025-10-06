# Tiltfile for cross-selling use case development

update_settings(max_parallel_updates=10)

# Cert manager is required for Agent Runtime Operator to support webhooks
load('ext://cert_manager', 'deploy_cert_manager')
deploy_cert_manager()

print("Installing agent-runtime-operator")
local("kubectl apply -f https://github.com/agentic-layer/agent-runtime-operator/releases/download/v0.5.0/install.yaml")

print("Waiting for agent-runtime-operator to start")
local("kubectl wait --for=condition=Available --timeout=60s -n agent-runtime-operator-system deployment/agent-runtime-operator-controller-manager")

# Configure Tilt to work with Agent Runtime Operator's custom Agent CRDs
# Without these configurations, Tilt cannot properly manage Agent resources created by the operator:
# image_json_path: Required because Agent CRDs store image references in a custom field ({.spec.image})
#                  rather than standard Kubernetes image fields that Tilt knows about by default
# pod_readiness: Required because the operator creates pods asynchronously after Agent CRD creation,
#                and Tilt must wait for operator-managed pods rather than assuming immediate readiness
k8s_kind(
    'Agent',
    pod_readiness='wait',
)

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

k8s_resource('communications-agent', port_forwards='10002:8000', labels=['agents'])
k8s_resource('cross-selling-agent', port_forwards='10003:8000', labels=['agents'])
k8s_resource('insurance-host-agent', port_forwards='8000:8000', labels=['agents'])

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
    resource_deps=['insurance-host-agent', 'cross-selling-agent', 'customer-crm', 'insurance-products', 'litellm', 'lgtm', 'communications-agent'],
    auto_init=cfg.get('run-tests', False),
    trigger_mode=TRIGGER_MODE_MANUAL,
)
