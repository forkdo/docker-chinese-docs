# 为您的 PHP 应用程序配置 CI/CD

## 先决条件

完成本指南的所有先前部分，从[容器化 PHP 应用程序](containerize.md)开始。要完成本节内容，您必须拥有 [GitHub](https://github.com/signup) 账户和 [Docker](https://hub.docker.com/signup) 账户。

## 概述

在本节中，您将学习如何设置和使用 GitHub Actions 来构建和测试您的 Docker 镜像，并将其推送到 Docker Hub。您将完成以下步骤：

1. 在 GitHub 上创建一个新仓库。
2. 定义 GitHub Actions 工作流。
3. 运行工作流。

## 第一步：创建仓库

创建一个 GitHub 仓库，配置 Docker Hub 凭据，并推送您的源代码。

1. 在 GitHub 上[创建一个新仓库](https://github.com/new)。

2. 打开仓库的 **Settings**（设置），然后转到 **Secrets and variables**（机密和变量）>
   **Actions**。

3. 创建一个新的 **Repository variable**（仓库变量），名称为 `DOCKER_USERNAME`，值为您的 Docker ID。

4. 为 Docker Hub 创建一个新的[个人访问令牌 (PAT)](/manuals/security/access-tokens.md#create-an-access-token)。您可以将此令牌命名为 `docker-tutorial`。确保访问权限包括 Read and Write（读取和写入）。

5. 将 PAT 作为 **Repository secret**（仓库机密）添加到您的 GitHub 仓库中，名称为
   `DOCKERHUB_TOKEN`。

6. 在您机器上的本地仓库中，运行以下命令将 origin 更改为刚刚创建的仓库。请确保将 `your-username` 更改为您自己的 GitHub 用户名，将 `your-repository` 更改为您创建的仓库名称。

   ```console
   $ git remote set-url origin https://github.com/your-username/your-repository.git
   ```

7. 在您机器上的本地仓库中，运行以下命令将分支重命名为 main。

   ```console
   $ git branch -M main
   ```

8. 运行以下命令暂存、提交，然后将您的本地仓库推送到 GitHub。

   ```console
   $ git add -A
   $ git commit -m "my first commit"
   $ git push -u origin main
   ```

## 第二步：设置工作流

设置您的 GitHub Actions 工作流，用于构建、测试镜像并将其推送到 Docker Hub。

1. 转到您在 GitHub 上的仓库，然后选择 **Actions** 标签页。

2. 选择 **set up a workflow yourself**（自己设置工作流）。

   这将带您到一个页面，用于在您的仓库中创建一个新的 GitHub actions 工作流文件，默认路径为 `.github/workflows/main.yml`。

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

   有关 `docker/build-push-action` 的 YAML 语法的更多信息，请参阅 [GitHub Action README](https://github.com/docker/build-push-action/blob/master/README.md)。

## 第三步：运行工作流

保存工作流文件并运行作业。

1. 选择 **Commit changes...**（提交更改...）并将更改推送到 `main` 分支。

   推送提交后，工作流会自动开始。

2. 转到 **Actions** 标签页。它会显示工作流。

   选择工作流会显示所有步骤的详细分解。

3. 当工作流完成后，转到您的
   [Docker Hub 上的仓库](https://hub.docker.com/repositories)。

   如果您在该列表中看到新仓库，则表示 GitHub Actions 已成功将镜像推送到 Docker Hub。

## 总结

在本节中，您学习了如何为您的应用程序设置 GitHub Actions 工作流。

相关信息：

- [GitHub Actions 简介](/guides/gha.md)
- [Docker Build GitHub Actions](/manuals/build/ci/github-actions/_index.md)
- [GitHub Actions 的工作流语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## 下一步

接下来，学习如何在部署之前在本地测试和调试 Kubernetes 上的工作负载。
