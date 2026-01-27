---
title: 使用 GitHub Actions 自动化构建
linkTitle: 使用 GitHub Actions 自动化构建
weight: 50
keywords: CI/CD, GitHub Actions, Node.js, Docker
description: 了解如何为你的 Node.js 应用程序配置使用 GitHub Actions 的 CI/CD 流程。
aliases:
  - /language/nodejs/configure-ci-cd/
  - /guides/language/nodejs/configure-ci-cd/
---

## 先决条件

完成本指南从[容器化 Node.js 应用程序](containerize.md)开始的所有先前章节。

你还必须拥有：

- 一个 [GitHub](https://github.com/signup) 账户。
- 一个经过验证的 [Docker Hub](https://hub.docker.com/signup) 账户。

---

## 概述

在本节中，你将使用 [GitHub Actions](https://docs.github.com/en/actions) 设置一个 **CI/CD 流水线**，以自动执行以下操作：

- 在 Docker 容器内构建你的 Node.js 应用程序。
- 运行单元测试和集成测试，并确保你的应用程序符合可靠的代码质量标准。
- 执行安全扫描和漏洞评估。
- 将生产就绪的镜像推送到 [Docker Hub](https://hub.docker.com)。

---

## 将你的 GitHub 仓库连接到 Docker Hub

为了启用 GitHub Actions 构建和推送 Docker 镜像，你需要将 Docker Hub 凭据安全地存储在新的 GitHub 仓库中。

### 步骤 1：将你的 GitHub 仓库连接到 Docker Hub

1. 从 [Docker Hub](https://hub.docker.com) 创建一个个人访问令牌 (PAT)。
   1. 从你的 Docker Hub 账户，进入 **账户设置 → 安全**。
   2. 生成一个具有 **读/写** 权限的新访问令牌。
   3. 将其命名为类似 `docker-nodejs-sample` 的名称。
   4. 复制并保存该令牌 —— 你将在步骤 4 中需要它。

2. 在 [Docker Hub](https://hub.docker.com/repositories/) 中创建一个仓库。
   1. 从你的 Docker Hub 账户，选择 **创建仓库**。
   2. 对于仓库名称，请使用具有描述性的名称 —— 例如：`nodejs-sample`。
   3. 创建完成后，复制并保存仓库名称 —— 你将在步骤 4 中需要它。

3. 为你的 Node.js 项目创建一个新的 [GitHub 仓库](https://github.com/new)。

4. 将 Docker Hub 凭据添加为 GitHub 仓库机密。

   在你新创建的 GitHub 仓库中：
   1. 从 **设置**，进入 **机密和变量 → 操作 → 新建仓库机密**。

   2. 添加以下机密：

   | 名称                     | 值                                            |
   | ------------------------ | ------------------------------------------------ |
   | `DOCKER_USERNAME`        | 你的 Docker Hub 用户名                         |
   | `DOCKERHUB_TOKEN`        | 你的 Docker Hub 访问令牌（在步骤 1 中创建）     |
   | `DOCKERHUB_PROJECT_NAME` | 你的 Docker 项目名称（在步骤 2 中创建）         |

   这些机密让 GitHub Actions 在自动化工作流期间能够安全地与 Docker Hub 进行身份验证。

5. 将你的本地项目连接到 GitHub。

   通过从项目根目录运行以下命令，将你的本地项目 `docker-nodejs-sample` 链接到你刚创建的 GitHub 仓库：

   ```console
      $ git remote set-url origin https://github.com/{your-username}/{your-repository-name}.git
   ```

   > [!重要]
   > 将 `{your-username}` 和 `{your-repository}` 替换为你的实际 GitHub 用户名和仓库名称。

   要确认你的本地项目已正确连接到远程 GitHub 仓库，请运行：

   ```console
   $ git remote -v
   ```

   你应该看到类似以下的输出：

   ```console
   origin  https://github.com/{your-username}/{your-repository-name}.git (fetch)
   origin  https://github.com/{your-username}/{your-repository-name}.git (push)
   ```

   这确认了你的本地仓库已正确链接，并准备好将源代码推送到 GitHub。

6. 将源代码推送到 GitHub。

   按照以下步骤将本地项目提交并推送到你的 GitHub 仓库：
   1. 暂存所有文件以进行提交。

      ```console
      $ git add -A
      ```

      此命令暂存所有更改 —— 包括新建、修改和删除的文件 —— 为提交做准备。

   2. 提交你的更改。

      ```console
      $ git commit -m "Initial commit with CI/CD pipeline"
      ```

      此命令创建一个提交，快照暂存的更改并附带描述性消息。

   3. 将代码推送到 `main` 分支。

      ```console
      $ git push -u origin main
      ```

      此命令将本地提交推送到远程 GitHub 仓库的 `main` 分支，并设置上游分支。

完成后，你的代码将在 GitHub 上可用，并且你配置的任何 GitHub Actions 工作流都将自动运行。

> [!注意]  
> 了解本步骤中使用的 Git 命令的更多信息：
>
> - [Git add](https://git-scm.com/docs/git-add) – 暂存更改（新建、修改、删除）以进行提交
> - [Git commit](https://git-scm.com/docs/git-commit) – 保存暂存更改的快照
> - [Git push](https://git-scm.com/docs/git-push) – 将本地提交上传到你的 GitHub 仓库
> - [Git remote](https://git-scm.com/docs/git-remote) – 查看和管理远程仓库 URL

---

### 步骤 2：设置工作流

现在，你将创建一个 GitHub Actions 工作流，用于构建 Docker 镜像、运行测试并将镜像推送到 Docker Hub。

1. 在 GitHub 上的仓库中，选择顶部菜单中的 **Actions** 选项卡。

2. 出现提示时，选择 **Set up a workflow yourself**。

   这将打开一个内联编辑器来创建新的工作流文件。默认情况下，它将保存到：
   `.github/workflows/main.yml`

3. 将以下工作流配置添加到新文件中：

```yaml
name: CI/CD – Node.js Application with Docker

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

jobs:
  test:
    name: Run Node.js Tests
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:18-alpine
        env:
          POSTGRES_DB: todoapp_test
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Cache npm dependencies
        uses: actions/cache@v4
        with:
          path: ~/.npm
          key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
          restore-keys: ${{ runner.os }}-npm-

      - name: Build test image
        uses: docker/build-push-action@v6
        with:
          context: .
          target: test
          tags: nodejs-app-test:latest
          platforms: linux/amd64
          load: true
          cache-from: type=local,src=/tmp/.buildx-cache
          cache-to: type=local,dest=/tmp/.buildx-cache,mode=max

      - name: Run tests inside container
        run: |
          docker run --rm \
            --network host \
            -e NODE_ENV=test \
            -e POSTGRES_HOST=localhost \
            -e POSTGRES_PORT=5432 \
            -e POSTGRES_DB=todoapp_test \
            -e POSTGRES_USER=postgres \
            -e POSTGRES_PASSWORD=postgres \
            nodejs-app-test:latest
        env:
          CI: true
        timeout-minutes: 10

  build-and-push:
    name: Build and Push Docker Image
    runs-on: ubuntu-latest
    needs: test

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Cache Docker layers
        uses: actions/cache@v4
        with:
          path: /tmp/.buildx-cache
          key: ${{ runner.os }}-buildx-${{ github.sha }}
          restore-keys: ${{ runner.os }}-buildx-

      - name: Extract metadata
        id: meta
        run: |
          echo "REPO_NAME=${GITHUB_REPOSITORY##*/}" >> "$GITHUB_OUTPUT"
          echo "SHORT_SHA=${GITHUB_SHA::7}" >> "$GITHUB_OUTPUT"

- name: 登录到 Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: 构建并推送多架构生产镜像
        uses: docker/build-push-action@v6
        with:
          context: .
          target: production
          push: true
          platforms: linux/amd64,linux/arm64
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/${{ secrets.DOCKERHUB_PROJECT_NAME }}:latest
            ${{ secrets.DOCKER_USERNAME }}/${{ secrets.DOCKERHUB_PROJECT_NAME }}:${{ steps.meta.outputs.SHORT_SHA }}
          cache-from: type=local,src=/tmp/.buildx-cache
          cache-to: type=local,dest=/tmp/.buildx-cache,mode=max
```

此工作流为您的 Node.js 应用程序执行以下任务：

- 在每次向 `main` 分支推送（`push`）或创建拉取请求（`pull request`）时触发。
- 使用 `test` 阶段构建测试 Docker 镜像。
- 在容器化环境中运行测试。
- 如果任何测试失败，则停止工作流。
- 缓存 Docker 构建层和 npm 依赖项，以加快后续运行速度。
- 使用 GitHub Secrets 进行 Docker Hub 身份验证。
- 使用 `production` 阶段构建镜像。
- 使用 `latest` 和短 SHA 标签将镜像标记并推送到 Docker Hub。

> [!NOTE]
> 有关 `docker/build-push-action` 的更多信息，请参阅 [GitHub Action README](https://github.com/docker/build-push-action/blob/master/README.md)。

---

### 步骤 3：运行工作流

添加工作流文件后，触发 CI/CD 流程。

1. 提交并推送您的工作流文件

   在 GitHub 编辑器中，选择 **Commit changes…**（提交更改…）。
   - 此次推送将自动触发 GitHub Actions 流水线。

2. 监控工作流执行
   1. 在您的 GitHub 仓库中，转到 **Actions**（操作）选项卡。
   2. 选择工作流运行，以跟踪每个步骤：**test**（测试）、**build**（构建）、**security**（安全），以及（如果成功）**push**（推送）和 **deploy**（部署）。

3. 在 Docker Hub 上验证 Docker 镜像
   - 工作流运行成功后，访问您的 [Docker Hub 仓库](https://hub.docker.com/repositories)。
   - 您应该会在仓库中看到一个新镜像，包含：
     - 仓库名称：`${your-repository-name}`
     - 标签包括：
       - `latest` – 代表最近一次成功的构建；非常适合快速测试或部署。
       - `<short-sha>` – 基于提交哈希的唯一标识符，可用于版本跟踪、回滚和可追溯性。

> [!TIP] 保护您的主分支
> 为了维护代码质量并防止意外直接推送，请启用分支保护规则：
>
> - 在您的 GitHub 仓库中，转到 **Settings → Branches**（设置 → 分支）。
> - 在“Branch protection rules”（分支保护规则）下，选择 **Add rule**（添加规则）。
> - 将 `main` 指定为分支名称。
> - 启用以下选项：
>   - _Require a pull request before merging_（合并前需要拉取请求）。
>   - _Require status checks to pass before merging_（合并前需要状态检查通过）。
>
> 这可以确保只有经过测试和审查的代码才能合并到 `main` 分支。

---

## 总结

在本节中，您使用 GitHub Actions 为您的容器化 Node.js 应用程序设置了完整的 CI/CD 流水线。

您已完成的工作：

- 为您的项目创建了一个新的 GitHub 仓库。
- 生成了一个 Docker Hub 访问令牌，并将其添加为 GitHub Secret。
- 创建了一个 GitHub Actions 工作流，该工作流：
  - 在 Docker 容器中构建您的应用程序。
  - 在容器化环境中运行测试。
  - 如果测试通过，则将镜像推送到 Docker Hub。
- 验证了工作流成功运行。

您的 Node.js 应用程序现已实现自动化测试和部署。

---

## 相关资源

深入了解容器化应用程序的自动化和最佳实践：

- [GitHub Actions 简介](/guides/gha.md) – 了解 GitHub Actions 如何自动化您的工作流
- [Docker Build GitHub Actions](/manuals/build/ci/github-actions/_index.md) – 使用 GitHub Actions 设置容器构建
- [GitHub Actions 的工作流语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) – 编写 GitHub 工作流的完整参考
- [GitHub 容器注册表](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) – 了解 GHCR 功能和使用方法
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 优化您的镜像以获得性能和安全性

---

## 后续步骤

接下来，学习如何将容器化的 Node.js 应用程序部署到 Kubernetes，并使用生产就绪的配置。这有助于确保您的应用程序在类似生产的环境中按预期运行，从而减少部署过程中的意外情况。