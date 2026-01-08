---
title: 使用 GitHub Actions 自动化构建
linkTitle: 使用 GitHub Actions 自动化构建
weight: 20
keywords: ci/cd, github actions, ruby, flask
description: 了解如何为 Ruby on Rails 应用程序配置使用 GitHub Actions 的 CI/CD 流程。
aliases:
- /language/ruby/configure-ci-cd/
- /guides/language/ruby/configure-ci-cd/
- /guides/ruby/configure-ci-cd/
---

## 先决条件

请完成本指南中从[容器化 Ruby on Rails 应用程序](containerize.md)开始的所有先前章节。要完成本节内容，您必须拥有 [GitHub](https://github.com/signup) 账户和 [Docker](https://hub.docker.com/signup) 账户。

如果您尚未为您的项目创建 [GitHub 仓库](https://github.com/new)，现在可以开始创建了。创建仓库后，请记得[添加远程仓库](https://docs.github.com/en/get-started/getting-started-with-git/managing-remote-repositories)，并确保您可以提交代码并[将代码推送到 GitHub](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository#about-git-push)。

1. 在您的项目 GitHub 仓库中，打开 **Settings**（设置），然后进入 **Secrets and variables**（机密和变量）> **Actions**。

2. 在 **Variables**（变量）选项卡下，创建一个名为 `DOCKER_USERNAME` 的新 **Repository variable**（仓库变量），并将您的 Docker ID 作为其值。

3. 为 Docker Hub 创建一个新的[个人访问令牌 (PAT)](/manuals/security/access-tokens.md#create-an-access-token)。您可以将此令牌命名为 `docker-tutorial`。请确保访问权限包含读取和写入权限。

4. 将 PAT 作为 **Repository secret**（仓库机密）添加到您的 GitHub 仓库中，名称为 `DOCKERHUB_TOKEN`。

## 概述

GitHub Actions 是 GitHub 内置的 CI/CD（持续集成和持续部署）自动化工具。它允许您定义自定义工作流，以便在特定事件发生时（例如推送代码、创建拉取请求等）构建、测试和部署代码。工作流是基于 YAML 的自动化脚本，用于定义触发时要执行的一系列步骤。工作流存储在仓库的 `.github/workflows/` 目录中。

在本节中，您将学习如何设置和使用 GitHub Actions 来构建 Docker 镜像并将其推送到 Docker Hub。您将完成以下步骤：

1. 定义 GitHub Actions 工作流。
2. 运行工作流。

## 1. 定义 GitHub Actions 工作流

您可以通过在仓库的 `.github/workflows/` 目录中创建 YAML 文件来创建 GitHub Actions 工作流。您可以使用自己喜欢的文本编辑器或 GitHub 网页界面来完成此操作。以下步骤展示了如何使用 GitHub 网页界面创建工作流文件。

如果您更喜欢使用 GitHub 网页界面，请按照以下步骤操作：

1. 转到 GitHub 上的仓库，然后选择 **Actions** 选项卡。

2. 选择 **set up a workflow yourself**（自行设置工作流）。

   这将带您进入一个页面，用于在仓库中创建新的 GitHub Actions 工作流文件。默认情况下，文件创建在 `.github/workflows/main.yml` 路径下，让我们将其名称更改为 `build.yml`。

如果您更喜欢使用文本编辑器，请在仓库的 `.github/workflows/` 目录中创建一个名为 `build.yml` 的新文件。

将以下内容添加到文件中：

```yaml
name: Build and push Docker image

on:
  push:
    branches:
      - main

jobs:
  build_and_push:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: ${{ vars.DOCKER_USERNAME }}/${{ github.event.repository.name }}:latest
```

每个 GitHub Actions 工作流包含一个或多个作业。每个作业由多个步骤组成。每个步骤可以运行一组命令或使用[现有操作](https://github.com/marketplace?type=actions)。上述操作包含三个步骤：

1. [**Login to Docker Hub**](https://github.com/docker/login-action)：此操作使用您之前创建的 Docker ID 和个人访问令牌 (PAT) 登录到 Docker Hub。

2. [**Set up Docker Buildx**](https://github.com/docker/setup-buildx-action)：此操作设置 Docker [Buildx](https://github.com/docker/buildx)，这是一个扩展 Docker CLI 功能的 CLI 插件。

3. [**Build and push**](https://github.com/docker/build-push-action)：此操作构建 Docker 镜像并将其推送到 Docker Hub。`tags` 参数指定镜像名称和标签。本示例中使用的是 `latest` 标签。

## 2. 运行工作流

提交更改并将其推送到 `main` 分支。此工作流会在您每次向 `main` 分支推送更改时运行。您可以在 [GitHub 文档](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows) 中找到有关工作流触发器的更多信息。

转到 GitHub 仓库的 **Actions** 选项卡。它会显示工作流。选择工作流可以查看其所有步骤的详细信息。

工作流完成后，转到 [Docker Hub 上的仓库页面](https://hub.docker.com/repositories)。如果您在该列表中看到新仓库，则表示 GitHub Actions 工作流已成功将镜像推送到 Docker Hub。

## 总结

在本节中，您学习了如何为 Ruby on Rails 应用程序设置 GitHub Actions 工作流。

相关信息：

- [GitHub Actions 简介](/guides/gha.md)
- [Docker Build GitHub Actions](/manuals/build/ci/github-actions/_index.md)
- [GitHub Actions 工作流语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## 后续步骤

在下一节中，您将学习如何使用容器开发应用程序。