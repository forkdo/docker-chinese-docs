---
title: 使用 GitHub Actions 自动化构建
linkTitle: 使用 GitHub Actions 自动化构建
weight: 20
keywords: ci/cd, github actions, ruby, flask
description: 了解如何为 Ruby on Rails 应用配置基于 GitHub Actions 的 CI/CD。
aliases:
  - /language/ruby/configure-ci-cd/
  - /guides/language/ruby/configure-ci-cd/
  - /guides/ruby/configure-ci-cd/
---

## 前置条件

完成本指南之前的所有章节，从 [容器化 Ruby on Rails 应用](containerize.md) 开始。你需要拥有 [GitHub](https://github.com/signup) 账号和 [Docker](https://hub.docker.com/signup) 账号才能完成本章节。

如果你还没有为项目创建 [GitHub 仓库](https://github.com/new)，现在就去创建。创建仓库后，别忘了[添加远程仓库](https://docs.github.com/en/get-started/getting-started-with-git/managing-remote-repositories)，并确保可以提交和[推送代码](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository#about-git-push)到 GitHub。

1. 在项目的 GitHub 仓库中，打开 **Settings**，进入 **Secrets and variables** > **Actions**。

2. 在 **Variables** 标签下，创建一个名为 `DOCKER_USERNAME` 的 **Repository variable**，值为你的 Docker ID。

3. 为 Docker Hub 创建一个新的 [Personal Access Token (PAT)](/manuals/security/access-tokens.md#create-an-access-token)。你可以将此令牌命名为 `docker-tutorial`。确保访问权限包含读取和写入。

4. 将 PAT 作为 **Repository secret** 添加到 GitHub 仓库中，命名为
   `DOCKERHUB_TOKEN`。

## 概述

GitHub Actions 是 GitHub 内置的 CI/CD（持续集成和持续部署）自动化工具。它允许你定义自定义工作流，在特定事件发生时（例如推送代码、创建拉取请求等）自动构建、测试和部署代码。工作流是基于 YAML 的自动化脚本，定义了触发时要执行的步骤序列。工作流文件存储在仓库的 `.github/workflows/` 目录中。

在本章节中，你将学习如何设置和使用 GitHub Actions 来构建 Docker 镜像并推送到 Docker Hub。你需要完成以下步骤：

1. 定义 GitHub Actions 工作流。
2. 运行工作流。

## 1. 定义 GitHub Actions 工作流

你可以通过在仓库的 `.github/workflows/` 目录中创建 YAML 文件来定义 GitHub Actions 工作流。你可以使用喜欢的文本编辑器或 GitHub Web 界面完成此操作。以下步骤展示如何使用 GitHub Web 界面创建工作流文件。

如果选择使用 GitHub Web 界面，请遵循以下步骤：

1. 访问 GitHub 上的仓库，然后选择 **Actions** 标签页。

2. 选择 **set up a workflow yourself**。

   这将带你进入创建新 GitHub Actions 工作流文件的页面。默认情况下，文件会创建在 `.github/workflows/main.yml`，让我们将其重命名为 `build.yml`。

如果你更喜欢使用文本编辑器，请在仓库的 `.github/workflows/` 目录中创建一个名为 `build.yml` 的新文件。

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

每个 GitHub Actions 工作流包含一个或多个任务。每个任务由多个步骤组成。每个步骤可以运行一组命令或使用已有的[现有 Actions](https://github.com/marketplace?type=actions)。上述工作流包含三个步骤：

1. [**登录到 Docker Hub**](https://github.com/docker/login-action)：使用之前创建的 Docker ID 和 Personal Access Token (PAT) 登录 Docker Hub。

2. [**设置 Docker Buildx**](https://github.com/docker/setup-buildx-action)：设置 Docker [Buildx](https://github.com/docker/buildx)，这是一个扩展 Docker CLI 功能的 CLI 插件。

3. [**构建并推送**](https://github.com/docker/build-push-action)：构建并推送 Docker 镜像到 Docker Hub。`tags` 参数指定镜像名称和标签。本示例使用 `latest` 标签。

## 2. 运行工作流

提交更改并推送到 `main` 分支。此工作流会在你推送到 `main` 分支时自动运行。你可以在 [GitHub 文档](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows) 中找到更多关于工作流触发器的信息。

前往 GitHub 仓库的 **Actions** 标签页。它会显示工作流。选择工作流可以查看所有步骤的详细信息。

当工作流完成后，前往你的 [Docker Hub 仓库列表](https://hub.docker.com/repositories)。如果在列表中看到新仓库，说明 GitHub Actions 工作流已成功将镜像推送到 Docker Hub。

## 总结

在本章节中，你学习了如何为 Ruby on Rails 应用设置 GitHub Actions 工作流。

相关信息：

- [GitHub Actions 介绍](/guides/gha.md)
- [Docker Build GitHub Actions](/manuals/build/ci/github-actions/_index.md)
- [GitHub Actions 工作流语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## 下一步

在下一章节中，你将学习如何使用容器开发应用。