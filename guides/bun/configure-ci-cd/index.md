# 为你的 Bun 应用程序配置 CI/CD

## 先决条件

完成本指南之前的所有章节，从[容器化 Bun 应用程序](containerize.md)开始。你必须拥有 [GitHub](https://github.com/signup) 账户和 [Docker](https://hub.docker.com/signup) 账户才能完成本节。

## 概述

在本节中，你将学习如何设置和使用 GitHub Actions 来构建和测试你的 Docker 镜像，并将其推送到 Docker Hub。你将完成以下步骤：

1. 在 GitHub 上创建一个新的仓库。
2. 定义 GitHub Actions 工作流。
3. 运行工作流。

## 步骤一：创建仓库

创建 GitHub 仓库，配置 Docker Hub 凭据，并推送你的源代码。

1. 在 GitHub 上[创建一个新仓库](https://github.com/new)。

2. 打开仓库的 **Settings**（设置），然后转到 **Secrets and variables**（密钥和变量）>
   **Actions**（操作）。

3. 创建一个名为 `DOCKER_USERNAME` 的新 **Repository variable**（仓库变量），值为你 Docker ID。

4. 为 Docker Hub 创建一个新的 [Personal Access Token (PAT)](/manuals/security/access-tokens.md#create-an-access-token)。你可以将此令牌命名为 `docker-tutorial`。确保访问权限包含读取和写入权限。

5. 在你的 GitHub 仓库中，将该 PAT 添加为名为
   `DOCKERHUB_TOKEN` 的 **Repository secret**（仓库密钥）。

6. 在你机器上的本地仓库中，运行以下命令以将
   origin 更改为你刚刚创建的仓库。确保将
   `your-username` 替换为你的 GitHub 用户名，将 `your-repository` 替换为
   你创建的仓库名称。

   ```console
   $ git remote set-url origin https://github.com/your-username/your-repository.git
   ```

7. 运行以下命令来暂存、提交并推送你的本地仓库到 GitHub。

   ```console
   $ git add -A
   $ git commit -m "my commit"
   $ git push -u origin main
   ```

## 步骤二：设置工作流

设置你的 GitHub Actions 工作流，用于构建、测试镜像
并将其推送到 Docker Hub。

1. 进入你在 GitHub 上的仓库，然后选择 **Actions**（操作）选项卡。

2. 选择 **set up a workflow yourself**（自己设置工作流）。

   这将带你进入一个页面，用于在你的仓库中创建一个新的 GitHub actions 工作流文件，
   默认路径为 `.github/workflows/main.yml`。

3. 在编辑器窗口中，复制并粘贴以下 YAML 配置，然后提交更改。

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

         - name: Build and push
           uses: docker/build-push-action@v6
           with:
             platforms: linux/amd64,linux/arm64
             push: true
             tags: ${{ vars.DOCKER_USERNAME }}/${{ github.event.repository.name }}:latest
   ```

   有关 `docker/build-push-action` 的 YAML 语法的更多信息，
   请参阅 [GitHub Action README](https://github.com/docker/build-push-action/blob/master/README.md)。

## 步骤三：运行工作流

保存工作流文件并运行作业。

1. 选择 **Commit changes...**（提交更改...）并将更改推送到 `main` 分支。

   推送提交后，工作流将自动开始。

2. 进入 **Actions**（操作）选项卡。那里会显示工作流。

   选择该工作流可以查看所有步骤的细分情况。

3. 工作流完成后，访问你在 [Docker Hub 上的仓库](https://hub.docker.com/repositories)。

   如果你在该列表中看到了新仓库，则意味着 GitHub Actions
   已成功将镜像推送到 Docker Hub。

## 总结

在本节中，你学习了如何为你的 Bun 应用程序设置 GitHub Actions 工作流。

相关信息：

- [GitHub Actions 简介](/guides/gha.md)
- [Docker Build GitHub Actions](/manuals/build/ci/github-actions/_index.md)
- [GitHub Actions 的工作流语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## 后续步骤

接下来，学习如何在部署之前于 Kubernetes 本地测试和调试你的工作负载。
