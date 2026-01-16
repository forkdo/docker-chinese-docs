---
title: Local registry with GitHub Actions
url: /build/ci/github-actions/local-registry/
parent:
  title: Docker Build GitHub Actions
  url: /build/ci/github-actions/
breadcrumbs:
  - title: 手册
    url: /manuals/
  - title: Docker Build
    url: /build/
  - title: Continuous integration with Docker
    url: /build/ci/
  - title: Docker Build GitHub Actions
    url: /build/ci/github-actions/
  - title: Local registry with GitHub Actions
    url: /build/ci/github-actions/local-registry/
next:
  title: Export to Docker with GitHub Actions
  url: /build/ci/github-actions/export-docker/
prev:
  title: Multi-platform image with GitHub Actions
  url: /build/ci/github-actions/multi-platform/
---


For testing purposes you may need to create a [local registry](https://hub.docker.com/_/registry)
to push images into:

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    services:
      registry:
        image: registry:3
        ports:
          - 5000:5000
    steps:
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        with:
          driver-opts: network=host
      
      - name: Build and push to local registry
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: localhost:5000/name/app:latest
      
      - name: Inspect
        run: |
          docker buildx imagetools inspect localhost:5000/name/app:latest
```

