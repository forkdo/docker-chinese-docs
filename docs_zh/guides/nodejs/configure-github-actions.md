---
title: 使用 GitHub Actions 自动化构建
linkTitle: 使用 GitHub Actions 自动化构建
weight: 50
keywords: CI/CD, GitHub Actions, Node.js, Docker
description: 了解如何为你的 Node.js 应用配置基于 GitHub Actions 的 CI/CD。
aliases:
  - /language/nodejs/configure-ci-cd/
  - /guides/language/nodejs/configure-ci-cd/
---

## 前置条件

完成本指南所有前置章节，从 [容器化 Node.js 应用](containerize.md) 开始。

你还必须具备：

- 一个 [GitHub](https://github.com/signup) 账号。
- 一个 [Docker Hub](https://hub.docker.com/signup) 账号。

---

## 概述

在本节中，你将使用 [GitHub Actions](https://docs.github.com/en/actions) 配置 **CI/CD 流水线**，实现以下自动化：

- 在 Docker 容器中构建你的 Node.js 应用。
- 运行单元测试和集成测试，确保你的应用符合良好的代码质量标准。
- 执行安全扫描和漏洞评估。
- 将生产就绪的镜像推送到 [Docker Hub](https://hub.docker.com)。

---

## 将 GitHub 仓库连接到 Docker Hub

为了让 GitHub Actions 能够构建并推送 Docker 镜像，你需要将 Docker Hub 凭据安全地存储到 GitHub 仓库中。

### 步骤 1：将 GitHub 仓库连接到 Docker Hub

1. 在 [Docker Hub](https://hub.docker.com) 创建一个个人访问令牌（PAT）。
   1. 在 Docker Hub 账号中，进入 **Account Settings → Security**。
   2. 生成一个新的访问令牌，权限选择 **Read/Write**。
   3. 将其命名为类似 `docker-nodejs-sample`。
   4. 复制并保存该令牌——稍后在步骤 4 中会用到。

2. 在 [Docker Hub](https://hub.docker.com/repositories/) 创建一个仓库。
   1. 在 Docker Hub 账号中，选择 **Create a repository**。
   2. 仓库名称使用一个有意义的名称——例如：`nodejs-sample`。
   3. 创建后，复制并保存仓库名称——稍后在步骤 4 中会用到。

3. 为你的 Node.js 项目创建一个新的 [GitHub 仓库](https://github.com/new)。

4. 将 Docker Hub 凭据添加为 GitHub 仓库密钥（Secret）。

   在你的新 GitHub 仓库中：
   1. 进入 **Settings**，选择 **Secrets and variables → Actions → New repository secret**。

   2. 添加以下密钥：

   | 名称                     | 值                                            |
   | ------------------------ | ------------------------------------------------ |
   | `DOCKER_USERNAME`        | 你的 Docker Hub 用户名                         |
   | `DOCKERHUB_TOKEN`        | 你的 Docker Hub 访问令牌（在步骤 1 中创建）     |
   | `DOCKERHUB_PROJECT_NAME` | 你的 Docker 项目名称（在步骤 2 中创建）     |

   这些密钥允许 GitHub Actions 在自动化流水线中安全地与 Docker Hub 进行身份验证。

5. 将本地项目连接到 GitHub。

   将本地项目 `docker-nodejs-sample` 链接到刚创建的 GitHub 仓库，从项目根目录运行以下命令：

   ```console
      $ git remote set-url origin https://github.com/{your-username}/{your-repository-name}.git
   ```

   > [!IMPORTANT]
   > 将 `{your-username}` 和 `{your-repository}` 替换为你的实际 GitHub 用户名和仓库名。

   为确认本地项目已正确连接到远程 GitHub 仓库，运行：

   ```console
   $ git remote -v
   ```

   你应该看到类似以下的输出：

   ```console
   origin  https://github.com/{your-username}/{your-repository-name}.git (fetch)
   origin  https://github.com/{your-username}/{your-repository-name}.git (push)
   ```

   这表明本地仓库已正确关联，准备将源代码推送到 GitHub。

6. 推送源代码到 GitHub。

   按以下步骤提交并推送本地项目到 GitHub 仓库：
   1. 暂存所有文件。

      ```console
      $ git add -A
      ```

      此命令将所有变更（新增、修改、删除的文件）加入暂存区，准备提交。

   2. 提交变更。

      ```console
      $ git commit -m "Initial commit with CI/CD pipeline"
      ```

      此命令创建一个提交，使用描述性消息保存暂存区的变更快照。

   3. 推送到 `main` 分支。

      ```console
      $ git push -u origin main
      ```

      此命令将本地提交推送到远程 GitHub 仓库的 `main` 分支，并设置上游分支。

完成后，你的代码将出现在 GitHub 上，所有配置的 GitHub Actions 流水线将自动运行。

> [!NOTE]  
> 了解更多本步骤中使用的 Git 命令：
>
> - [Git add](https://git-scm.com/docs/git-add) – 将变更（新增、修改、删除）加入暂存区
> - [Git commit](https://git-scm.com/docs/git-commit) – 保存暂存区变更的快照
> - [Git push](https://git-scm.com/docs/git-push) – 将本地提交上传到 GitHub 仓库
> - [Git remote](https://git-scm.com/docs/git-remote) – 查看和管理远程仓库 URL

---

### 步骤 2：配置流水线

现在你将创建一个 GitHub Actions 流水线，用于构建 Docker 镜像、运行测试，并将镜像推送到 Docker Hub。

1. 在 GitHub 仓库中，选择顶部菜单的 **Actions** 标签页。

2. 系统提示时，选择 **Set up a workflow yourself**。

   这将打开一个内联编辑器，创建新的流水线文件。默认保存路径为：
   `.github/workflows/main.yml`

3. 将以下流水线配置添加到新文件中：

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

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and push multi-arch production image
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

该流水线为你的 Node.js 应用执行以下任务：

- 在每次向 `main` 分支推送或发起 Pull Request 时触发。
- 使用 `test` 阶段构建测试 Docker 镜像。
- 在容器化环境中运行测试。
- 若测试失败则中止流水线。
- 缓存 Docker 构建层和 npm 依赖以加快执行速度。
- 使用 GitHub 密钥与 Docker Hub 进行身份验证。
- 使用 `production` 阶段构建镜像。
- 打上标签并推送到 Docker Hub，包含 `latest` 和短 SHA 标签。

> [!NOTE]
> 有关 `docker/build-push-action` 的更多信息，请参考 [GitHub Action README](https://github.com/docker/build-push-action/blob/master/README.md)。

---

### 步骤 3：运行流水线

添加流水线文件后，触发 CI/CD 流程。

1. 提交并推送流水线文件

   在 GitHub 编辑器中，选择 **Commit changes…**。
   - 此次推送将自动触发 GitHub Actions 流水线。

2. 监控流水线执行
   1. 在 GitHub 仓库中，进入 **Actions** 标签页。
   2. 选择流水线运行，查看每一步：**test**、**build**、**security**，以及（成功时）**push** 和 **deploy**。

3. 验证 Docker Hub 上的镜像
   - 流水线成功运行后，访问你的 [Docker Hub 仓库](https://hub.docker.com/repositories)。
   - 你应该看到仓库中新增了一个镜像，包含：
     - 仓库名：`${your-repository-name}`
     - 标签包括：
       - `latest` – 代表最近一次成功的构建；适用于快速测试或部署。
       - `<short-sha>` – 基于提交哈希的唯一标识符，用于版本追踪、回滚和可追溯性。

> [!TIP] 保护你的主分支
> 为保持代码质量并防止意外的直接推送，启用分支保护规则：
>
> - 在 GitHub 仓库中，进入 **Settings → Branches**。
> - 在 Branch protection rules 下，选择 **Add rule**。
> - 指定 `main` 为分支名。
> - 启用以下选项：
>   - _Require a pull request before merging_（合并前需 Pull Request）。
>   - _Require status checks to pass before merging_（合并前需状态检查通过）。
>
> 这确保只有经过测试和审查的代码才能合并到 `main` 分支。

---

## 小结

在本节中，你为容器化的 Node.js 应用使用 GitHub Actions 配置了完整的 CI/CD 流水线。

你的成果：

- 创建了一个新的 GitHub 仓库用于项目。
- 生成 Docker Hub 访问令牌并作为 GitHub 密钥添加。
- 创建 GitHub Actions 流水线，能够：
  - 在 Docker 容器中构建应用。
  - 在容器化环境中运行测试。
  - 测试通过后推送镜像到 Docker Hub。
- 验证流水线成功运行。

你的 Node.js 应用现已具备自动化测试和部署能力。

---

## 相关资源

深入理解容器化应用的自动化和最佳实践：

- [GitHub Actions 入门](/guides/gha.md) – 了解 GitHub Actions 如何自动化工作流
- [Docker Build GitHub Actions](/manuals/build/ci/github-actions/_index.md) – 使用 GitHub Actions 配置容器构建
- [GitHub Actions 工作流语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) – 编写 GitHub 工作流的完整参考
- [GitHub 容器注册表](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) – 了解 GHCR 功能和用法
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 优化镜像的性能和安全性

---

## 后续步骤

接下来，学习如何将你的容器化 Node.js 应用部署到 Kubernetes，使用生产就绪的配置。这将帮助你确保应用在生产环境中的行为符合预期，减少部署时的意外。