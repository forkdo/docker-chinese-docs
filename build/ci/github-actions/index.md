---
title: Docker Build GitHub Actions
url: /build/ci/github-actions/
parent:
  title: Continuous integration with Docker
  url: /build/ci/
breadcrumbs:
  - title: 手册
    url: /manuals/
  - title: Docker Build
    url: /build/
  - title: Continuous integration with Docker
    url: /build/ci/
  - title: Docker Build GitHub Actions
    url: /build/ci/github-actions/
children:
  - title: Add image annotations with GitHub Actions
    url: /build/ci/github-actions/annotations/
    description: Add OCI annotations to image components using GitHub Actions
  - title: Add SBOM and provenance attestations with GitHub Actions
    url: /build/ci/github-actions/attestations/
    description: Add SBOM and provenance attestations to your images with GitHub Actions
  - title: Validating build configuration with GitHub Actions
    url: /build/ci/github-actions/checks/
    description: Discover how to validate your build configuration and identify best practice violations using build checks in GitHub Actions.
  - title: Using secrets with GitHub Actions
    url: /build/ci/github-actions/secrets/
    description: Example using secret mounts with GitHub Actions
  - title: GitHub Actions build summary
    url: /build/ci/github-actions/build-summary/
    description: Get an overview of your Docker Builds with GitHub Actions
  - title: Configuring your GitHub Actions builder
    url: /build/ci/github-actions/configure-builder/
    description: Configuring BuildKit instances for building in CI with GitHub Actions
  - title: Cache management with GitHub Actions
    url: /build/ci/github-actions/cache/
  - title: Copy image between registries with GitHub Actions
    url: /build/ci/github-actions/copy-image-registries/
    description: Build multi-platform images and copy them between registries with GitHub Actions
  - title: Export to Docker with GitHub Actions
    url: /build/ci/github-actions/export-docker/
    description: Load the build results to the image store with GitHub Actions
  - title: Local registry with GitHub Actions
    url: /build/ci/github-actions/local-registry/
    description: Create and use a local OCI registry with GitHub Actions
  - title: Multi-platform image with GitHub Actions
    url: /build/ci/github-actions/multi-platform/
    description: Build for multiple architectures with GitHub Actions using QEMU emulation or multiple native builders
  - title: Named contexts with GitHub Actions
    url: /build/ci/github-actions/named-contexts/
    description: Use additional contexts in multi-stage builds with GitHub Actions
  - title: Push to multiple registries with GitHub Actions
    url: /build/ci/github-actions/push-multi-registries/
    description: Push to multiple registries with GitHub Actions
  - title: Reproducible builds with GitHub Actions
    url: /build/ci/github-actions/reproducible-builds/
    description: How to create reproducible builds in GitHub Actions using the SOURCE_EPOCH environment variable
  - title: Share built image between jobs with GitHub Actions
    url: /build/ci/github-actions/share-image-jobs/
    description: Share an image between runners without pushing to a registry
  - title: Manage tags and labels with GitHub Actions
    url: /build/ci/github-actions/manage-tags-labels/
    description: Assign tags and labels to images automatically with GitHub Actions
  - title: Test before push with GitHub Actions
    url: /build/ci/github-actions/test-before-push/
    description: Here's how you can validate an image, before pushing it to a registry
  - title: Update Docker Hub description with GitHub Actions
    url: /build/ci/github-actions/update-dockerhub-desc/
    description: How to update the repository README in Docker Hub using with GitHub Actions
---


GitHub Actions is a popular CI/CD platform for automating your build, test, and
deployment pipeline. Docker provides a set of official GitHub Actions for you to
use in your workflows. These official actions are reusable, easy-to-use
components for building, annotating, and pushing images.

The following GitHub Actions are available:

- [Build and push Docker images](https://github.com/marketplace/actions/build-and-push-docker-images):
  build and push Docker images with BuildKit.
- [Docker Buildx Bake](https://github.com/marketplace/actions/docker-buildx-bake):
  enables using high-level builds with [Bake](../../bake/_index.md).
- [Docker Login](https://github.com/marketplace/actions/docker-login):
  sign in to a Docker registry.
- [Docker Setup Buildx](https://github.com/marketplace/actions/docker-setup-buildx):
  creates and boots a BuildKit builder.
- [Docker Metadata action](https://github.com/marketplace/actions/docker-metadata-action):
  extracts metadata from Git reference and GitHub events to generate tags,
  labels, and annotations.
- [Docker Setup Compose](https://github.com/marketplace/actions/docker-setup-compose):
  installs and sets up [Compose](../../../compose).
- [Docker Setup Docker](https://github.com/marketplace/actions/docker-setup-docker):
  installs Docker Engine.
- [Docker Setup QEMU](https://github.com/marketplace/actions/docker-setup-qemu):
  installs [QEMU](https://github.com/qemu/qemu) static binaries for
  multi-platform builds.
- [Docker Scout](https://github.com/docker/scout-action):
  analyze Docker images for security vulnerabilities.

Using Docker's actions provides an easy-to-use interface, while still allowing
flexibility for customizing build parameters.

## Examples

If you're looking for examples on how to use the Docker GitHub Actions,
refer to the following sections:


- [Add image annotations with GitHub Actions](/build/ci/github-actions/annotations/)

- [Add SBOM and provenance attestations with GitHub Actions](/build/ci/github-actions/attestations/)

- [Validating build configuration with GitHub Actions](/build/ci/github-actions/checks/)

- [Using secrets with GitHub Actions](/build/ci/github-actions/secrets/)

- [GitHub Actions build summary](/build/ci/github-actions/build-summary/)

- [Configuring your GitHub Actions builder](/build/ci/github-actions/configure-builder/)

- [Cache management with GitHub Actions](/build/ci/github-actions/cache/)

- [Copy image between registries with GitHub Actions](/build/ci/github-actions/copy-image-registries/)

- [Export to Docker with GitHub Actions](/build/ci/github-actions/export-docker/)

- [Local registry with GitHub Actions](/build/ci/github-actions/local-registry/)

- [Multi-platform image with GitHub Actions](/build/ci/github-actions/multi-platform/)

- [Named contexts with GitHub Actions](/build/ci/github-actions/named-contexts/)

- [Push to multiple registries with GitHub Actions](/build/ci/github-actions/push-multi-registries/)

- [Reproducible builds with GitHub Actions](/build/ci/github-actions/reproducible-builds/)

- [Share built image between jobs with GitHub Actions](/build/ci/github-actions/share-image-jobs/)

- [Manage tags and labels with GitHub Actions](/build/ci/github-actions/manage-tags-labels/)

- [Test before push with GitHub Actions](/build/ci/github-actions/test-before-push/)

- [Update Docker Hub description with GitHub Actions](/build/ci/github-actions/update-dockerhub-desc/)



## Get started with GitHub Actions

The [Introduction to GitHub Actions with Docker](/guides/gha.md) guide walks
you through the process of setting up and using Docker GitHub Actions for
building Docker images, and pushing images to Docker Hub.

