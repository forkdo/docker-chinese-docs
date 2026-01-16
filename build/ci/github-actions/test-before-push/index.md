---
title: Test before push with GitHub Actions
url: /build/ci/github-actions/test-before-push/
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
  - title: Test before push with GitHub Actions
    url: /build/ci/github-actions/test-before-push/
next:
  title: Manage tags and labels with GitHub Actions
  url: /build/ci/github-actions/manage-tags-labels/
prev:
  title: Update Docker Hub description with GitHub Actions
  url: /build/ci/github-actions/update-dockerhub-desc/
---


In some cases, you might want to validate that the image works as expected
before pushing it. The following workflow implements several steps to achieve
this:

1. Build and export the image to Docker
2. Test your image
3. Multi-platform build and push the image

```yaml
name: ci

on:
  push:

env:
  TEST_TAG: user/app:test
  LATEST_TAG: user/app:latest

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and export to Docker
        uses: docker/build-push-action@v6
        with:
          load: true
          tags: ${{ env.TEST_TAG }}

      - name: Test
        run: |
          docker run --rm ${{ env.TEST_TAG }}

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ env.LATEST_TAG }}
```

> [!NOTE]
>
> The `linux/amd64` image is only built once in this workflow. The image is
> built once, and the following steps use the internal cache from the first
> `Build and push` step. The second `Build and push` step only builds
> `linux/arm64`.

