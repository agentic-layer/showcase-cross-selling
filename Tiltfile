# Tiltfile for cross-selling use case development

"""Deploy monitoring stack with Tempo and kube-prometheus-stack"""
load('ext://helm_remote', 'helm_remote')

# Deploy Tempo
helm_remote('tempo',
    repo_name='grafana',
    repo_url='https://grafana.github.io/helm-charts',
    version='1.23.2',
    namespace='monitoring',
    create_namespace=True,
    set=['mode=monolithic', 'tempo.service.type=ClusterIP', 'tempo.service.port=3200']
)

# Deploy kube-prometheus-stack
helm_remote('kube-prometheus-stack',
    repo_name='prometheus-community',
    repo_url='https://prometheus-community.github.io/helm-charts',
    version='66.3.0',
    namespace='monitoring',
    set=[
        'grafana.additionalDataSources[0].name=Tempo',
        'grafana.additionalDataSources[0].type=tempo',
        'grafana.additionalDataSources[0].access=proxy',
        'grafana.additionalDataSources[0].url=http://tempo.monitoring.svc.cluster.local:3200'
    ]
)

# Add labels to monitoring resources
k8s_resource('tempo', labels=['monitoring'])
k8s_resource('kube-prometheus-stack-grafana', port_forwards='3000:3000', labels=['monitoring'])


"""Create Kubernetes secrets from environment variables"""
load('ext://secret', 'secret_from_dict')

google_api_key = os.environ.get('GEMINI_API_KEY', '')
if not google_api_key:
    fail('GEMINI_API_KEY environment variable is required. Please set it in your shell or .env file.')

k8s_yaml(secret_from_dict(
    name = "api-key-secrets",
    namespace = "use-case-cross-selling",
    inputs = { "GOOGLE_API_KEY": google_api_key }
))

# Apply Kubernetes manifests
k8s_yaml(kustomize('../infrastructure/platform/applications/use-case-cross-selling/local'))

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
    {'name': 'insurance_host_agent', 'port': '8000:8000'}
]

for agent in agents:
    agent_name = agent['name']
    docker_build(
        agent_name,
        context='.',
        dockerfile='./agents/Dockerfile',
        build_args={'AGENT_NAME': agent_name},
        live_update=[live_update_sync, live_update_run]
    )
    k8s_resource(snake_to_kebab(agent_name), port_forwards=agent['port'], labels=['agents'])

# Open ports and sync changes to MCP servers
mcp_servers = [
    {'name': 'customer_crm', 'port': '8002:8000'},
    {'name': 'insurance_products', 'port': '8003:8000'}
]

for server in mcp_servers:
    server_name = server['name']
    docker_build(
        server_name,
        context='.',
        dockerfile='./mcp-servers/Dockerfile',
        build_args={'MCP_SERVER_NAME': server_name},
        live_update=[live_update_sync, live_update_run]
    )
    k8s_resource(snake_to_kebab(server_name), port_forwards=server['port'], labels=['mcp-servers'])
