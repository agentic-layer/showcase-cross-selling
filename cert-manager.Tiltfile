# -*- mode: Python -*-

version_settings(constraint='>=0.23.0')


def cert_manager_install(version="1.3.1"):
    """
    Installs the cert-manager into your cluster.
    """

    install_url = "https://github.com/cert-manager/cert-manager/releases/download/v%s/cert-manager.yaml"

    wait_cmd = """
kubectl wait --for=condition=Available --timeout=300s -n cert-manager deployment/cert-manager 1>&2
kubectl wait --for=condition=Available --timeout=300s -n cert-manager deployment/cert-manager-cainjector 1>&2
kubectl wait --for=condition=Available --timeout=300s -n cert-manager deployment/cert-manager-webhook 1>&2
kubectl wait \
  --for=jsonpath='{.webhooks[0].clientConfig.caBundle}' \
  --timeout=300s \
  -n cert-manager \
  validatingwebhookconfiguration cert-manager-webhook 1>&2
"""

    delete_cmd = [
        "kubectl", "delete", "--ignore-not-found", "-f", install_url % version
    ]

    k8s_custom_deploy(
        'cert-manager',
        deps=[],
        apply_cmd="""
set -ex
kubectl apply -f %s -o yaml
set +e
""" % (install_url % version) + wait_cmd,
        delete_cmd=delete_cmd,
    )

    k8s_resource(
        'cert-manager',
        labels=['cert-manager'],
        resource_deps=[],
    )
