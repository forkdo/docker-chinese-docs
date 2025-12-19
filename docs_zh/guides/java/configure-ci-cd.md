---
title: 为 Java 应用程序配置 CI/CD
linkTitle: 配置 CI/CD
weight: 40
keywords: java, CI/CD, 本地, 开发
description: 了解如何为 Java 应用程序配置 CI/CD
aliases:
  - /language/java/configure-ci-cd/
  - /guides/language/java/configure-ci-cd/
---

## 先决条件

完成本指南前面的部分，从[容器化您的应用程序](containerize.md)开始。您必须拥有 [GitHub](https://github.com/signup) 账户和 [Docker](https://hub.docker.com/signup) 账户才能完成本部分。

## 概述

在本部分中，您将学习如何设置和使用 GitHub Actions 来构建并将 Docker 镜像推送到 Docker Hub。您将完成以下步骤：

1. 在 GitHub 上创建新仓库。
2. 定义 GitHub Actions 工作流。
3. 运行工作流。

## 第一步：创建仓库

创建 GitHub 仓库，配置 Docker Hub 凭据，并推送源代码。

1. 在 GitHub 上[创建新仓库](https://github.com/new)。

2. 打开仓库的 **Settings**（设置），然后转到 **Secrets and variables**（机密和变量）> **Actions**。

3. 创建一个名为 `DOCKER_USERNAME` 的新 **Repository variable**（仓库变量），并将您的 Docker ID 作为其值。

4. 为 Docker Hub 创建一个新的[个人访问令牌 (PAT)](/manuals/security/access-tokens.md#create-an-access-token)。您可以将此令牌命名为 `docker-tutorial`。确保访问权限包括读取和写入权限。

5. 将 PAT 作为 **Repository secret**（仓库机密）添加到您的 GitHub 仓库中，名称为 `DOCKERHUB_TOKEN`。

6. 在本地机器上的本地仓库中，运行以下命令将 origin 更改为刚刚创建的仓库。请确保将 `your-username` 替换为您的 GitHub 用户名，将 `your-repository` 替换为您创建的仓库名称。

   ```console
   $ git remote set-url origin https://github.com/your-username/your-repository.git
   ```

7. 运行以下命令将本地仓库暂存、提交并推送到 GitHub。

   ```console
   $ git add -A
   $ git commit -m "my commit"
   $ git push -u origin main
   ```

## 第二步：设置工作流

设置 GitHub Actions 工作流以构建、测试并将镜像推送到 Docker Hub。

1. 转到 GitHub 上的仓库，然后选择 **Actions** 选项卡。
   该项目已经有一个 `maven-build` 工作流，用于使用 Maven 构建和测试您的 Java 应用程序。如果需要，您可以选择禁用此工作流，因为本指南中不会使用它。您将创建一个新的替代工作流来构建、测试并推送镜像。

2. 选择 **New workflow**（新建工作流）。

3. 选择 **set up a workflow yourself**（自行设置工作流）。

   这会将您带到一个页面，用于在仓库中创建新的 GitHub Actions 工作流文件，默认位于 `.github/workflows/main.yml`。

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

   有关 `docker/build-push-action` 的 YAML 语法的更多信息，请参阅 [GitHub Action README](https://github.com/docker/build-push-action/blob/master/README.md)。

## 第三步：运行工作流

保存工作流文件并运行作业。

1. 选择 **Commit changes...**（提交更改...）并将更改推送到 `main` 分支。

   推送提交后，工作流会自动启动。

2. 转到 **Actions** 选项卡。它会显示工作流。

   选择工作流可以查看其所有步骤的细分。

3. 工作流完成后，转到 [Docker Hub 上的仓库](https://hub.docker.com/repositories)。

   如果您在该列表中看到新仓库，则表示 GitHub Actions 已成功将镜像推送到 Docker Hub。

## 总结

在本部分中，您学习了如何为应用程序设置 GitHub Actions 工作流。

相关信息：

- [GitHub Actions 简介](/guides/gha.md)
- [Docker Build GitHub Actions](/manuals/build/ci/github-actions/_index.md)
- [GitHub Actions 工作流语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## 下一步

接下来，了解如何在部署之前在 Kubernetes 上本地测试和调试工作负载。