# Tiltfile for cross-selling use case development

update_settings(max_parallel_updates=10, k8s_upsert_timeout_secs=600)

# Load .env file for environment variables
load('ext://dotenv', 'dotenv')
dotenv()

v1alpha1.extension_repo(name='agentic-layer', url='https://github.com/agentic-layer/tilt-extensions', ref='v0.9.2')

v1alpha1.extension(name='cert-manager', repo_name='agentic-layer', repo_path='cert-manager')
load('ext://cert-manager', 'cert_manager_install')
cert_manager_install()

v1alpha1.extension(name='agent-runtime', repo_name='agentic-layer', repo_path='agent-runtime')
load('ext://agent-runtime', 'agent_runtime_install')
agent_runtime_install(version='0.17.2')

v1alpha1.extension(name='ai-gateway-litellm', repo_name='agentic-layer', repo_path='ai-gateway-litellm')
load('ext://ai-gateway-litellm', 'ai_gateway_litellm_install')
ai_gateway_litellm_install(version='0.4.1')

v1alpha1.extension(name='agent-gateway-krakend', repo_name='agentic-layer', repo_path='agent-gateway-krakend')
load('ext://agent-gateway-krakend', 'agent_gateway_krakend_install')
agent_gateway_krakend_install(version='0.5.3')

v1alpha1.extension(name='librechat', repo_name='agentic-layer', repo_path='librechat')
load('ext://librechat', 'librechat_install')
librechat_install()

v1alpha1.extension(name='testbench', repo_name='agentic-layer', repo_path='testbench')
load('ext://testbench', 'testbench_install')
testbench_install(version='0.4.1')

# Apply local Kubernetes manifests
k8s_yaml(kustomize('deploy/local'))

# Deploy showcase using Helm chart with local image overrides
k8s_yaml(helm(
    'chart',
    name='showcase-cross-selling',
    namespace='showcase-cross-selling',
    values=[
        'chart/values.yaml'
    ],
    set=[
        # Override tool server images to use local Tilt builds
        'images.toolServers.customerCrm.repository=customer_crm',
        'images.toolServers.customerCrm.tag=latest',
        'images.toolServers.insuranceProducts.repository=insurance_products',
        'images.toolServers.insuranceProducts.tag=latest',
        'frontend.backendUrl=http://agent-gateway.agent-gateway.svc.cluster.local:10000',
    ]
))


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
    k8s_resource(snake_to_kebab(server_name), port_forwards=server['port'], labels=['showcase'], resource_deps=['agent-runtime'])

# Monitoring
k8s_resource('lgtm', labels=['monitoring'], resource_deps=['testbench'], port_forwards=['11000:3000'])

# Observability Dashboard
k8s_resource('observability-dashboard', labels=['monitoring'], port_forwards=['11004:8000'])

# Expose AI and Agent Gateways
k8s_resource('ai-gateway', port_forwards=['11001:4000'])
k8s_resource('agent-gateway', port_forwards=['11002:8080'])

k8s_resource('cross-selling-workforce', labels=['showcase'], resource_deps=['agent-runtime'], pod_readiness='ignore')
k8s_resource('insurance-host-agent', labels=['showcase'], resource_deps=['agent-runtime'], port_forwards='11010:8000')
k8s_resource('communications-agent', labels=['showcase'], resource_deps=['agent-runtime', 'customer-crm'], port_forwards='11011:8000')
k8s_resource('cross-selling-agent', labels=['showcase'], resource_deps=['agent-runtime', 'customer-crm', 'insurance-products'], port_forwards='11012:8000')
k8s_resource('frontend', labels=['showcase'], resource_deps=['agent-gateway'], port_forwards='11013:80')

k8s_resource('insurance-host-ragas-evaluation', labels=['testing'], resource_deps=['testkube'])
k8s_resource('insurance-host-ragas-evaluation-trigger', labels=['testing'], resource_deps=['testkube'])
k8s_resource('cross-selling-ragas-evaluation', labels=['testing'], resource_deps=['testkube'])
k8s_resource('cross-selling-ragas-evaluation-trigger', labels=['testing'], resource_deps=['testkube'])
k8s_resource(
    objects=['metrics-config:configmap:testkube'],
    new_name='metrics-config',
    labels=['testing'],
    resource_deps=['testkube']
)
k8s_resource(
    objects=['datasets:configmap:testkube'],
    new_name='datasets',
    labels=['testing'],
    resource_deps=['testkube']
)
