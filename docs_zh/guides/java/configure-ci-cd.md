---
title: 为你的 Java 应用配置 CI/CD
linkTitle: 配置 CI/CD
weight: 40
keywords: java, CI/CD, local, development
description: 了解如何为你的 Java 应用配置 CI/CD
aliases:
  - /language/java/configure-ci-cd/
  - /guides/language/java/configure-ci-cd/
---

## 先决条件

完成本指南的前面部分，从 [容器化你的应用](containerize.md) 开始。你必须拥有 [GitHub](https://github.com/signup) 账户和已验证的 [Docker](https://hub.docker.com/signup) 账户才能完成本部分。

## 概述

在本部分中，你将学习如何设置和使用 GitHub Actions 来构建并将你的 Docker 镜像推送到 Docker Hub。你将完成以下步骤：

1. 在 GitHub 上创建一个新仓库。
2. 定义 GitHub Actions 工作流。
3. 运行工作流。

## 步骤一：创建仓库

创建一个 GitHub 仓库，配置 Docker Hub 凭据，并推送你的源代码。

1. 在 GitHub 上 [创建一个新仓库](https://github.com/new)。

2. 打开仓库的 **Settings**，然后转到 **Secrets and variables** >
   **Actions**。

3. 创建一个名为 `DOCKER_USERNAME` 的新 **Repository variable**，并使用你的 Docker ID 作为值。

4. 为 Docker Hub 创建一个新的 [Personal Access Token (PAT)](/manuals/security/access-tokens.md#create-an-access-token)。你可以将此令牌命名为 `docker-tutorial`。确保访问权限包括读取和写入。

5. 将 PAT 作为 **Repository secret** 添加到你的 GitHub 仓库中，命名为
   `DOCKERHUB_TOKEN`。

6. 在你机器上的本地仓库中，运行以下命令来更改
   origin 为你刚刚创建的仓库。确保你将
   `your-username` 更改为你的 GitHub 用户名，将 `your-repository` 更改为
   你创建的仓库名称。

   ```console
   $ git remote set-url origin https://github.com/your-username/your-repository.git
   ```

7. 运行以下命令来暂存、提交并将你的本地仓库推送到 GitHub。

   ```console
   $ git add -A
   $ git commit -m "my commit"
   $ git push -u origin main
   ```

## 步骤二：设置工作流

为构建、测试并将镜像推送到 Docker Hub 设置你的 GitHub Actions 工作流。

1. 转到 GitHub 上的你的仓库，然后选择 **Actions** 选项卡。
   项目已经有一个 `maven-build` 工作流，使用 Maven 构建和测试你的 Java 应用。如果需要，你可以选择性地禁用此工作流，因为你在本指南中不会使用它。你将创建一个新的替代工作流来构建、测试并推送你的镜像。

2. 选择 **New workflow**。

3. 选择 **set up a workflow yourself**。

   这会带你到一个页面，在你的仓库中创建一个新的 GitHub actions 工作流文件，默认在 `.github/workflows/main.yml` 下。

4. 在编辑器窗口中，复制并粘贴以下 YAML 配置。

   ```yaml
   name: ci

   on:
     push:
       branches:
         - main

   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         - name: Login to Docker Hub
           uses: docker/login-action@v3
           with:
             username: ${{ vars.DOCKER_USERNAME }}
             password: ${{ secrets.DOCKERHUB_TOKEN }}

         - name: Set up Docker Buildx
           uses: docker/setup-buildx-action@v3

         - name: Build and test
           uses: docker/build-push-action@v6
           with:
             target: test
             load: true

         - name: Build and push
           uses: docker/build-push-action@v6
           with:
             platforms: linux/amd64,linux/arm64
             push: true
             target: final
             tags: ${{ vars.DOCKER_USERNAME }}/${{ github.event.repository.name }}:latest
   ```

   有关 `docker/build-push-action` 的 YAML 语法的更多信息，
   请参阅 [GitHub Action README](https://github.com/docker/build-push-action/blob/master/README.md)。

## 步骤三：运行工作流

保存工作流文件并运行作业。

1. 选择 **Commit changes...** 并将更改推送到 `main` 分支。

   推送提交后，工作流会自动启动。

2. 转到 **Actions** 选项卡。它会显示工作流。

   选择工作流会显示所有步骤的详细信息。

3. 当工作流完成后，转到你的
   [Docker Hub 上的仓库](https://hub.docker.com/repositories)。

   如果你在该列表中看到新仓库，这意味着 GitHub Actions
   已成功将镜像推送到 Docker Hub。

## 总结

在本部分中，你学习了如何为你的应用设置 GitHub Actions 工作流。

相关信息：

- [GitHub Actions 介绍](/guides/gha.md)
- [Docker Build GitHub Actions](/manuals/build/ci/github-actions/_index.md)
- [GitHub Actions 的工作流语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## 下一步

接下来，了解如何在部署前在 Kubernetes 上本地测试和调试你的工作负载。