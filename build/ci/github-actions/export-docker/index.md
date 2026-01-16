---
title: Export to Docker with GitHub Actions
url: /build/ci/github-actions/export-docker/
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
  - title: Export to Docker with GitHub Actions
    url: /build/ci/github-actions/export-docker/
next:
  title: Copy image between registries with GitHub Actions
  url: /build/ci/github-actions/copy-image-registries/
prev:
  title: Local registry with GitHub Actions
  url: /build/ci/github-actions/local-registry/
---


You may want your build result to be available in the Docker client through
`docker images` to be able to use it in another step of your workflow:

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Build
        uses: docker/build-push-action@v6
        with:
          load: true
          tags: myimage:latest
      
      - name: Inspect
        run: |
          docker image inspect myimage:latest
```

