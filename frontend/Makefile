# Calculate VERSION once and reuse it
VERSION ?= $(shell echo "$$(git rev-parse --abbrev-ref HEAD)-$$(git rev-parse --short=7 HEAD)-$$(date +%s)")
IMAGE_TAG_BASE ?= ghcr.io/agentic-layer/showcase-cross-selling-frontend
IMG := $(IMAGE_TAG_BASE):$(VERSION)
PLATFORMS ?= linux/arm64,linux/amd64


.PHONY: all
all: build docker-build

.PHONY: build
build:
	npm run build

.PHONY: run
run: build
	npm run preview

.PHONY: dev
dev: build
	npm run dev


.PHONY: docker-build
docker-build:
	docker build -t $(IMG) .

.PHONY: docker-run
docker-run: docker-build
	docker run --rm -it -p 8000:80 -e BACKEND_URL=http://host.docker.internal:9009 $(IMG)

.PHONY: docker-push
docker-push:
	- docker buildx create --name agent-builder
	docker buildx use agent-builder
	docker buildx build --push --platform=$(PLATFORMS) --tag ${IMG} .
