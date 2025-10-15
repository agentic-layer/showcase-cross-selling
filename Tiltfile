# Tiltfile for cross-selling use case development

update_settings(max_parallel_updates=10)

v1alpha1.extension_repo(name='agentic-layer', url='https://github.com/agentic-layer/tilt-extensions')

v1alpha1.extension(name='cert-manager', repo_name='agentic-layer', repo_path='cert-manager')
load('ext://cert-manager', 'cert_manager_install')
cert_manager_install()

v1alpha1.extension(name='agent-runtime', repo_name='agentic-layer', repo_path='agent-runtime')
load('ext://agent-runtime', 'agent_runtime_install')
agent_runtime_install(version='0.7.0')

# Configure Tilt to work with Agent Runtime Operator's (ARO) custom CRDs
# Without these configurations, Tilt cannot properly manage Agent resources created by the operator:
# image_json_path: Required because ARO CRDs store image references in a custom field ({.spec.image})
#                  rather than standard Kubernetes image fields that Tilt knows about by default
# pod_readiness: Required because the operator creates pods asynchronously after ARO CRD creation,
#                and Tilt must wait for operator-managed pods rather than assuming immediate readiness
k8s_kind(
    'Agent',
    pod_readiness='wait',
)

k8s_kind(
    'ToolServer',
    image_json_path='{.spec.image}',
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
    namespace = "showcase-cross-selling",
    inputs = { "LITELLM_PROXY_API_KEY": os.environ.get('LITELLM_PROXY_API_KEY', litellm_master_key) }
))

# Apply Kubernetes manifests
k8s_yaml(kustomize('deploy/local'))

# Helper function to convert snake_case to kebab-case
def snake_to_kebab(snake_str):
    return snake_str.replace('_', '-')

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
    )
    k8s_resource(snake_to_kebab(server_name), port_forwards=server['port'], labels=['mcp-servers'], resource_deps=['agent-runtime'])

k8s_resource('communications-agent', port_forwards='10002:8000', labels=['agents'], resource_deps=['agent-runtime', 'customer-crm'])
k8s_resource('cross-selling-agent', port_forwards='10003:8000', labels=['agents'], resource_deps=['agent-runtime', 'customer-crm', 'insurance-products'])
k8s_resource('insurance-host-agent', port_forwards='8000:8000', labels=['agents'], resource_deps=['agent-runtime'])

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
