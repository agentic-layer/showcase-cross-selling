# -*- mode: Python -*-

version_settings(constraint='>=0.23.0')

# Increase the default k8s upsert timeout to accommodate CRD installations
update_settings(k8s_upsert_timeout_secs=300)

# Configure Tilt to work with Agent Runtime Operator's custom Agent CRDs
k8s_kind(
    'Agent',
    # Operator creates pods asynchronously after Agent CRD creation and Tilt
    # must wait for operator-managed pods rather than assuming immediate readiness
    pod_readiness='wait',
)


def agent_runtime_install(version="0.5.0"):
    """
    Installs the agent-runtime operators into your cluster.
    """

    install_url = "https://github.com/agentic-layer/agent-runtime-operator/releases/download/v%s/install.yaml"

    wait_cmd = """
kubectl wait --for=condition=Available --timeout=300s -n agent-runtime-operator-system deployment/agent-runtime-operator-controller-manager 1>&2
"""

    delete_cmd = [
        "kubectl", "delete", "--ignore-not-found",

        # Kubernetes is prone to deadlocks when you delete CRDs and namespaces at the same time:
        # - The Namespace controller thinks it's responsible for deleting all resources in its namespace.
        # - The CRD controller deletes the API routes for deleting resources.
        # So the namespace controller blocks and eventually times out.
        #
        # To prevent this from slowing down 'tilt down', we do a --wait=false when deleting
        # CRDs+Namespaces together.
        "--wait=false",
        "-f", install_url % version
    ]

    k8s_custom_deploy(
        'agent-runtime',
        deps=[],
        apply_cmd="""
set -ex
kubectl apply -f %s -o yaml
set +e
""" % (install_url % version) + wait_cmd,
        delete_cmd=delete_cmd,
    )

    k8s_resource(
        'agent-runtime',
        labels=['agent-runtime'],
        resource_deps=['cert-manager'],
    )
