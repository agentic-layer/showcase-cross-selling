# Tiltfile for cross-selling use case development

update_settings(max_parallel_updates=10)

# Load .env file for environment variables
load('ext://dotenv', 'dotenv')
dotenv()

v1alpha1.extension_repo(name='agentic-layer', url='https://github.com/agentic-layer/tilt-extensions', ref='v0.3.0')

v1alpha1.extension(name='cert-manager', repo_name='agentic-layer', repo_path='cert-manager')
load('ext://cert-manager', 'cert_manager_install')
cert_manager_install()

v1alpha1.extension(name='agent-runtime', repo_name='agentic-layer', repo_path='agent-runtime')
load('ext://agent-runtime', 'agent_runtime_install')
agent_runtime_install(version='0.9.0')

v1alpha1.extension(name='ai-gateway-litellm', repo_name='agentic-layer', repo_path='ai-gateway-litellm')
load('ext://ai-gateway-litellm', 'ai_gateway_litellm_install')
ai_gateway_litellm_install(version='0.2.0')

v1alpha1.extension(name='agent-gateway-krakend', repo_name='agentic-layer', repo_path='agent-gateway-krakend')
load('ext://agent-gateway-krakend', 'agent_gateway_krakend_install')
agent_gateway_krakend_install(version='0.1.4')

# Apply Kubernetes manifests
k8s_yaml(kustomize('deploy/local'))

# Helper function to convert snake_case to kebab-case
def snake_to_kebab(snake_str):
    return snake_str.replace('_', '-')

# Open ports and sync changes to MCP servers
mcp_servers = [
    {'name': 'customer_crm', 'port': '11020:8000'},
    {'name': 'insurance_products', 'port': '11021:8000'},
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

# Expose the Monitoring stack (Grafana)
k8s_resource('lgtm', port_forwards=['11000:3000'])

# Expose AI and Agent Gateways
k8s_resource('ai-gateway-litellm', port_forwards=['11001:4000'])
k8s_resource('agent-gateway-krakend', port_forwards=['11002:8080'])

k8s_resource('insurance-host-agent', port_forwards='11010:8000', labels=['agents'], resource_deps=['agent-runtime'])
k8s_resource('communications-agent', port_forwards='11011:8000', labels=['agents'], resource_deps=['agent-runtime', 'customer-crm'])
k8s_resource('cross-selling-agent', port_forwards='11012:8000', labels=['agents'], resource_deps=['agent-runtime', 'customer-crm', 'insurance-products'])


# Add flag to run tests
config.define_bool("run-tests")
cfg = config.parse()

local_resource(
    'test_e2e_openai_api',
    cmd='./test/e2e/openai-api.sh',
    resource_deps=[
        'insurance-host-agent',
        'cross-selling-agent',
        'communications-agent',
        'customer-crm',
        'insurance-products',
        'ai-gateway-litellm',
        'agent-gateway-krakend',
        'lgtm',
        ],
    auto_init=cfg.get('run-tests', False),
    trigger_mode=TRIGGER_MODE_MANUAL,
)
