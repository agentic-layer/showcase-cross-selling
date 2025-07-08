# agentic-playground

## Requirements

* Google ADK: https://google.github.io/adk-docs/get-started/quickstart/#set-up-the-model

## Setup

```shell
# Install brew bundle
brew bundle

# Authenticate with Google Cloud
gcloud auth application-default login
```

Add .env file with the following content to `adk-agents` directory:

```dotenv
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your-project-id
# Note: Some models are only available in certain regions, like `us-central1`.
GOOGLE_CLOUD_LOCATION=us-central1
# Required the communications agent's Slack capabilities:
SLACK_BOT_TOKEN=...
```

## ADK Agents

See [adk-agents](adk-agents/README.md).

## MCP Server

See [mcp-server](mcp-server/README.md).

## Evaluation

Run DeepEval tests (just example code currently):

```shell
export OPENAI_API_KEY=...
deepeval test run deepeval/test_chatbot.py
```

## k8s platform

```shell
# create the Kubernetes cluster in GCP
task gke-cluster-create

# bootstrap AI platform components and services using Flux2
# make sure you have set a valid GITHUB_TOKEN environment variable
task flux-bootstrap

# required to configure Config Connector with Google Cloud ProjectID
kubectl annotate namespace default cnrm.cloud.google.com/project-id=qaware-paal

# Create secret
task create-secrets

# the Kube Prometheus Stack is accessible via
kubectl port-forward -n monitoring pod/kube-prometheus-stack-grafana-7c5cd8bd69-lpm5z 3000:3000
# Login: admin:prom-operator
open http://localhost:3000
```