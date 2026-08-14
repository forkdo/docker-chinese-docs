---
title: Docker Build GitHub Actions
linkTitle: GitHub Actions
description: Docker 维护了一组用于构建 Docker 镜像的官方 GitHub Actions。
keywords: ci, github actions, gha,  build, introduction, tutorial
aliases:
  - /ci-cd/github-actions/
  - /build/ci/github-actions/examples/
---

GitHub Actions 是一个流行的 CI/CD 平台，用于自动化你的构建、测试和部署流水线。Docker 提供了一组
官方 GitHub Actions 供你在工作流中使用。这些官方 action 是用于构建、注解和推送镜像的可复用、
易用的组件。

目前提供以下 GitHub Actions：

- [Build and push Docker images](https://github.com/marketplace/actions/build-and-push-docker-images)：
  使用 BuildKit 构建并推送 Docker 镜像。
- [Docker Buildx Bake](https://github.com/marketplace/actions/docker-buildx-bake)：
  支持使用 [Bake](../../bake/_index.md) 进行高层构建。
- [Docker Login](https://github.com/marketplace/actions/docker-login)：
  登录到 Docker 注册表。
- [Docker Setup Buildx](https://github.com/marketplace/actions/docker-setup-buildx)：
  创建并启动一个 BuildKit 构建器。
- [Docker Metadata action](https://github.com/marketplace/actions/docker-metadata-action)：
  从 Git reference 和 GitHub 事件中提取元数据，以生成标签、标注和注解。
- [Docker Setup Compose](https://github.com/marketplace/actions/docker-setup-compose)：
  安装并设置 [Compose](../../../compose)。
- [Docker Setup Docker](https://github.com/marketplace/actions/docker-setup-docker)：
  安装 Docker Engine。
- [Docker Setup QEMU](https://github.com/marketplace/actions/docker-setup-qemu)：
  为多平台构建安装 [QEMU](https://github.com/qemu/qemu) 静态二进制文件。
- [Docker Scout](https://github.com/docker/scout-action)：
  分析 Docker 镜像以发现安全漏洞。

使用 Docker 的 action 既提供了易用的接口，同时也保留了自定义构建参数的灵活性。

## Examples

如果你正在寻找如何使用 Docker GitHub Actions 的示例，请参阅以下章节：

{{% sectionlinks %}}

## Get started with GitHub Actions

[Introduction to GitHub Actions with Docker](/guides/gha.md) 指南将带你完成为构建 Docker 镜像
以及向 Docker Hub 推送镜像而设置并使用 Docker GitHub Actions 的全过程。
