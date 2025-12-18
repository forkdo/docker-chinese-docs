---
title: 为你的 PHP 应用配置 CI/CD
linkTitle: 配置 CI/CD
weight: 40
keywords: php, CI/CD
description: 了解如何为你的 PHP 应用配置 CI/CD
aliases:
  - /language/php/configure-ci-cd/
  - /guides/language/php/configure-ci-cd/
---

## 前置条件

完成本指南之前的所有章节，从 [容器化 PHP 应用](containerize.md) 开始。你需要拥有 [GitHub](https://github.com/signup) 账户和 [Docker](https://hub.docker.com/signup) 账户才能完成本节内容。

## 概述

在本节中，你将学习如何使用 GitHub Actions 来构建、测试你的 Docker 镜像并将其推送到 Docker Hub。你需要完成以下步骤：

1. 在 GitHub 上创建新仓库。
2. 定义 GitHub Actions 工作流。
3. 运行工作流。

## 步骤一：创建仓库

创建 GitHub 仓库，配置 Docker Hub 凭据，并推送源代码。

1. 在 GitHub 上 [创建新仓库](https://github.com/new)。

2. 打开仓库的 **Settings**，进入 **Secrets and variables** > **Actions**。

3. 创建一个名为 `DOCKER_USERNAME` 的新 **仓库变量**，值为你的 Docker ID。

4. 为 Docker Hub 创建一个新的 [个人访问令牌 (PAT)](/manuals/security/access-tokens.md#create-an-access-token)。你可以将此令牌命名为 `docker-tutorial`。确保访问权限包含读取和写入。

5. 将 PAT 作为 **仓库密钥** 添加到你的 GitHub 仓库中，名称为 `DOCKERHUB_TOKEN`。

6. 在你本地机器上的仓库中，运行以下命令将 origin 更改为刚才创建的仓库。确保将 `your-username` 替换为你的 GitHub 用户名，将 `your-repository` 替换为你创建的仓库名称。

   ```console
   $ git remote set-url origin https://github.com/your-username/your-repository.git
   ```

7. 在你本地机器上的仓库中，运行以下命令将分支重命名为 main。

   ```console
   $ git branch -M main
   ```

8. 运行以下命令暂存、提交，然后将本地仓库推送到 GitHub。

   ```console
   $ git add -A
   $ git commit -m "my first commit"
   $ git push -u origin main
   ```

## 步骤二：设置工作流

为构建、测试和将镜像推送到 Docker Hub 设置 GitHub Actions 工作流。

1. 前往 GitHub 上的仓库，然后选择 **Actions** 标签页。

2. 选择 **set up a workflow yourself**。

   这将带你进入创建新 GitHub Actions 工作流文件的页面，该文件默认位于 `.github/workflows/main.yml`。

3. 在编辑器窗口中，复制并粘贴以下 YAML 配置。

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

   有关 `docker/build-push-action` 的 YAML 语法详细信息，请参考 [GitHub Action README](https://github.com/docker/build-push-action/blob/master/README.md)。

## 步骤三：运行工作流

保存工作流文件并运行任务。

1. 选择 **Commit changes...** 并将更改推送到 `main` 分支。

   推送提交后，工作流会自动启动。

2. 前往 **Actions** 标签页。它会显示工作流。

   选择工作流可以查看所有步骤的详细信息。

3. 当工作流完成后，前往你的 [Docker Hub 仓库页面](https://hub.docker.com/repositories)。

   如果在列表中看到新仓库，说明 GitHub Actions 已成功将镜像推送到 Docker Hub。

## 总结

在本节中，你学习了如何为应用设置 GitHub Actions 工作流。

相关信息：

- [GitHub Actions 介绍](/guides/gha.md)
- [Docker Build GitHub Actions](/manuals/build/ci/github-actions/_index.md)
- [GitHub Actions 工作流语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## 下一步

接下来，了解如何在部署前于 Kubernetes 上本地测试和调试你的工作负载。