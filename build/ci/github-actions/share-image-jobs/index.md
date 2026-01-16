---
title: Share built image between jobs with GitHub Actions
url: /build/ci/github-actions/share-image-jobs/
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
  - title: Share built image between jobs with GitHub Actions
    url: /build/ci/github-actions/share-image-jobs/
next:
  title: Reproducible builds with GitHub Actions
  url: /build/ci/github-actions/reproducible-builds/
prev:
  title: Manage tags and labels with GitHub Actions
  url: /build/ci/github-actions/manage-tags-labels/
---


As each job is isolated in its own runner, you can't use your built image
between jobs, except if you're using [self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners)
or [Docker Build Cloud](/build-cloud).
However, you can [pass data between jobs](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts#passing-data-between-jobs-in-a-workflow)
in a workflow using the [actions/upload-artifact](https://github.com/actions/upload-artifact)
and [actions/download-artifact](https://github.com/actions/download-artifact)
actions:

```yaml
name: ci

on:
  push:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and export
        uses: docker/build-push-action@v6
        with:
          tags: myimage:latest
          outputs: type=docker,dest=${{ runner.temp }}/myimage.tar

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: myimage
          path: ${{ runner.temp }}/myimage.tar

  use:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Download artifact
        uses: actions/download-artifact@v4
        with:
          name: myimage
          path: ${{ runner.temp }}

      - name: Load image
        run: |
          docker load --input ${{ runner.temp }}/myimage.tar
          docker image ls -a
```

