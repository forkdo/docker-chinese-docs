---
title: 使用 GitHub Actions 自动化构建
linkTitle: 使用 GitHub Actions 自动化构建
weight: 40
keywords: ci/cd, github actions, python, flask
description: 了解如何为 Python 应用程序配置基于 GitHub Actions 的 CI/CD。
aliases:
- /language/python/configure-ci-cd/
- /guides/language/python/configure-ci-cd/
- /guides/python/configure-ci-cd/
---

## 先决条件

完成本指南的所有先前部分，从 [容器化 Python 应用程序](containerize.md) 开始。您必须拥有 [GitHub](https://github.com/signup) 账户和 [Docker](https://hub.docker.com/signup) 账户才能完成本部分。

如果您尚未为您的项目创建 [GitHub 仓库](https://github.com/new)，现在是时候创建了。创建仓库后，不要忘记 [添加远程仓库](https://docs.github.com/en/get-started/getting-started-with-git/managing-remote-repositories) 并确保您可以提交代码并 [推送代码](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository#about-git-push) 到 GitHub。

1. 在您的项目 GitHub 仓库中，打开 **Settings**，然后转到 **Secrets and variables** > **Actions**。

2. 在 **Variables** 选项卡下，创建一个新的 **Repository variable**，名称为 `DOCKER_USERNAME`，值为您的 Docker ID。

3. 为 Docker Hub 创建一个新的 [个人访问令牌 (PAT)](/manuals/security/access-tokens.md#create-an-access-token)。您可以将此令牌命名为 `docker-tutorial`。确保访问权限包括 Read 和 Write。

4. 将 PAT 作为 **Repository secret** 添加到您的 GitHub 仓库中，名称为 `DOCKERHUB_TOKEN`。

## 概述

GitHub Actions 是内置于 GitHub 中的 CI/CD（持续集成和持续部署）自动化工具。它允许您定义自定义工作流，以便在特定事件发生时（例如推送代码、创建拉取请求等）构建、测试和部署代码。工作流是一个基于 YAML 的自动化脚本，定义了触发时要执行的一系列步骤。工作流存储在仓库的 `.github/workflows/` 目录中。

在本部分中，您将学习如何设置和使用 GitHub Actions 来构建 Docker 镜像并将其推送到 Docker Hub。您将完成以下步骤：

1. 定义 GitHub Actions 工作流。
2. 运行工作流。

## 1. 定义 GitHub Actions 工作流

您可以通过在仓库的 `.github/workflows/` 目录中创建一个 YAML 文件来创建 GitHub Actions 工作流。为此，请使用您喜欢的文本编辑器或 GitHub Web 界面。以下步骤展示了如何使用 GitHub Web 界面创建工作流文件。

如果您更喜欢使用 GitHub Web 界面，请按照以下步骤操作：

1. 转到 GitHub 上的仓库，然后选择 **Actions** 选项卡。

2. 选择 **set up a workflow yourself**。

   这将带您进入一个页面，用于在仓库中创建新的 GitHub Actions 工作流文件。默认情况下，该文件创建在 `.github/workflows/main.yml` 下，让我们将其名称更改为 `build.yml`。

如果您更喜欢使用文本编辑器，请在仓库的 `.github/workflows/` 目录中创建一个名为 `build.yml` 的新文件。

将以下内容添加到文件中：

```yaml
name: Build and push Docker image

on:
  push:
    branches:
      - main

jobs:
  lint-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run pre-commit hooks
        run: pre-commit run --all-files

      - name: Run pyright
        run: pyright

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

每个 GitHub Actions 工作流包含一个或多个作业 (jobs)。每个作业由多个步骤 (steps) 组成。每个步骤可以运行一组命令或使用已 [存在的操作](https://github.com/marketplace?type=actions)。上面的操作包含三个步骤：

1. [**Login to Docker Hub**](https://github.com/docker/login-action)：该操作使用您之前创建的 Docker ID 和个人访问令牌 (PAT) 登录 Docker Hub。

2. [**Set up Docker Buildx**](https://github.com/docker/setup-buildx-action)：该操作设置 Docker [Buildx](https://github.com/docker/buildx)，这是一个扩展 Docker CLI 功能的 CLI 插件。

3. [**Build and push**](https://github.com/docker/build-push-action)：该操作构建 Docker 镜像并将其推送到 Docker Hub。`tags` 参数指定了镜像名称和标签。本示例中使用了 `latest` 标签。

## 2. 运行工作流

提交更改并将其推送到 `main` 分支。每次您将更改推送到 `main` 分支时，此工作流都会运行。您可以在 [GitHub 文档](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows) 中找到有关工作流触发器的更多信息。

转到您的 GitHub 仓库的 **Actions** 选项卡。它会显示工作流。选择工作流会显示所有步骤的详细信息。

当工作流完成后，转到您在 [Docker Hub 上的仓库](https://hub.docker.com/repositories)。如果您在该列表中看到新仓库，则表示 GitHub Actions 工作流已成功将镜像推送到 Docker Hub。

## 总结

在本部分中，您学习了如何为 Python 应用程序设置 GitHub Actions 工作流，其中包括：

- 运行 pre-commit 挂钩进行代码检查和格式化
- 使用 Pyright 进行静态类型检查
- 构建并推送 Docker 镜像

相关信息：

- [GitHub Actions 简介](/guides/gha.md)
- [Docker Build GitHub Actions](/manuals/build/ci/github-actions/_index.md)
- [GitHub Actions 的工作流语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## 下一步

在下一节中，您将学习如何使用 Kubernetes 进行本地开发。