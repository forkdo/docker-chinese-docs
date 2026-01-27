# 使用 GitHub Actions 自动化构建


## 先决条件

完成本指南的所有前面部分，从 [容器化 Vue.js 应用程序](containerize.md) 开始。

您还必须拥有：
- 一个 [GitHub](https://github.com/signup) 账户。
- 一个已验证的 [Docker Hub](https://hub.docker.com/signup) 账户。

---

## 概述

在本节中，您将使用 [GitHub Actions](https://docs.github.com/en/actions) 设置一个 CI/CD 流水线，以自动：

- 在 Docker 容器内构建您的 Vue.js 应用程序。
- 在一致的环境中运行测试。
- 将生产就绪的镜像推送到 [Docker Hub](https://hub.docker.com)。

---

## 将您的 GitHub 仓库连接到 Docker Hub

为了使 GitHub Actions 能够构建和推送 Docker 镜像，您将在新的 GitHub 仓库中安全地存储您的 Docker Hub 凭据。

### 步骤 1：生成 Docker Hub 凭据并设置 GitHub 机密

1. 从 [Docker Hub](https://hub.docker.com) 创建个人访问令牌 (PAT)
   1. 前往您的 **Docker Hub 账户 → 账户设置 → 安全**。
   2. 生成一个具有 **读/写** 权限的新访问令牌。
   3. 将其命名为类似 `docker-vuejs-sample` 的名称。
   4. 复制并保存该令牌 — 您将在步骤 4 中需要它。

2. 在 [Docker Hub](https://hub.docker.com/repositories/) 中创建一个仓库
   1. 前往您的 **Docker Hub 账户 → 创建仓库**。
   2. 对于仓库名称，使用描述性的名称 — 例如：`vuejs-sample`。
   3. 创建后，复制并保存仓库名称 — 您将在步骤 4 中需要它。

3. 为您的 Vue.js 项目创建一个新的 [GitHub 仓库](https://github.com/new)

4. 将 Docker Hub 凭据添加为 GitHub 仓库机密

   在您新创建的 GitHub 仓库中：
   
   1. 导航到：
   **Settings → Secrets and variables → Actions → New repository secret**。

   2. 添加以下机密：

   | Name              | Value                          |
   |-------------------|--------------------------------|
   | `DOCKER_USERNAME` | 您的 Docker Hub 用户名       |
   | `DOCKERHUB_TOKEN` | 您的 Docker Hub 访问令牌（在步骤 1 中创建）   |
   | `DOCKERHUB_PROJECT_NAME` | 您的 Docker 项目名称（在步骤 2 中创建）   |

   这些机密允许 GitHub Actions 在自动化工作流程期间安全地与 Docker Hub 进行身份验证。

5. 将您的本地项目连接到 GitHub

   通过从项目根目录运行以下命令，将您的本地项目 `docker-vuejs-sample` 链接到您刚刚创建的 GitHub 仓库：

   ```console
      $ git remote set-url origin https://github.com/{your-username}/{your-repository-name}.git
   ```

   >[!IMPORTANT]
   >将 `{your-username}` 和 `{your-repository}` 替换为您实际的 GitHub 用户名和仓库名称。

   为确认您的本地项目已正确连接到远程 GitHub 仓库，请运行：

   ```console
   $ git remote -v
   ```

   您应该看到类似以下的输出：

   ```console
   origin  https://github.com/{your-username}/{your-repository-name}.git (fetch)
   origin  https://github.com/{your-username}/{your-repository-name}.git (push)
   ```

   这确认了您的本地仓库已正确链接并准备好将源代码推送到 GitHub。

6. 将您的源代码推送到 GitHub

   按照这些步骤提交并将您的本地项目推送到 GitHub 仓库：

   1. 将所有文件暂存以进行提交。

      ```console
      $ git add -A
      ```
      此命令将暂存所有更改 — 包括新文件、修改文件和删除文件 — 为提交做准备。


   2. 使用描述性消息提交暂存的更改。

      ```console
      $ git commit -m "Initial commit"
      ```
      此命令创建一个提交，以描述性消息快照暂存的更改。  

   3. 将代码推送到 `main` 分支。

      ```console
      $ git push -u origin main
      ```
      此命令将您的本地提交推送到远程 GitHub 仓库的 `main` 分支并设置上游分支。

完成后，您的代码将在 GitHub 上可用，您配置的任何 GitHub Actions 工作流程都将自动运行。

> [!NOTE]  
> 了解更多关于此步骤中使用的 Git 命令：
> - [Git add](https://git-scm.com/docs/git-add) – 暂存更改（新、修改、删除）以进行提交  
> - [Git commit](https://git-scm.com/docs/git-commit) – 保存暂存更改的快照  
> - [Git push](https://git-scm.com/docs/git-push) – 将本地提交上传到您的 GitHub 仓库  
> - [Git remote](https://git-scm.com/docs/git-remote) – 查看和管理远程仓库 URL

---

### 步骤 2：设置工作流程

现在您将创建一个 GitHub Actions 工作流程，该工作流程构建您的 Docker 镜像，运行测试，并将镜像推送到 Docker Hub。

1. 前往 GitHub 上的您的仓库并选择顶部菜单中的 **Actions** 选项卡。

2. 出现提示时选择 **Set up a workflow yourself**。

    这将打开一个内联编辑器以创建新的工作流程文件。默认情况下，它将保存到：
   `.github/workflows/main.yml`

   
3. 将以下工作流程配置添加到新文件：

```yaml
name: CI/CD – Vue.js App with Docker

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

jobs:
  build-test-deploy:
    name: Build, Test & Deploy
    runs-on: ubuntu-latest

    steps:
      # 1. Checkout the codebase
      - name: Checkout Code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      # 2. Set up Docker Buildx
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      # 3. Cache Docker layers
      - name: Cache Docker Layers
        uses: actions/cache@v4
        with:
          path: /tmp/.buildx-cache
          key: ${{ runner.os }}-buildx-${{ github.sha }}
          restore-keys: |
            ${{ runner.os }}-buildx-

      # 4. Cache npm dependencies
      - name: Cache npm Dependencies
        uses: actions/cache@v4
        with:
          path: ~/.npm
          key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-npm-

      # 5. Generate build metadata
      - name: Generate Build Metadata
        id: meta
        run: |
          echo "REPO_NAME=${GITHUB_REPOSITORY##*/}" >> "$GITHUB_OUTPUT"
          echo "SHORT_SHA=${GITHUB_SHA::7}" >> "$GITHUB_OUTPUT"

      # 6. Build Docker image for testing
      - name: Build Dev Docker Image
        uses: docker/build-push-action@v6
        with:
          context: .
          file: Dockerfile.dev
          tags: ${{ steps.meta.outputs.REPO_NAME }}-dev:latest
          load: true
          cache-from: type=local,src=/tmp/.buildx-cache
          cache-to: type=local,dest=/tmp/.buildx-cache,mode=max

      # 7. Run unit tests inside container
      - name: Run Vue.js Tests
        run: |
          docker run --rm \
            --workdir /app \
            --entrypoint "" \
            ${{ steps.meta.outputs.REPO_NAME }}-dev:latest \
            sh -c "npm ci && npm run test -- --ci --runInBand"
        env:
          CI: true
          NODE_ENV: test
        timeout-minutes: 10

      # 8. Log in to Docker Hub
      - name: Docker Hub Login
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      # 9. Build and push production image
      - name: Build and Push Production Image
        uses: docker/build-push-action@v6
        with:
          context: .
          file: Dockerfile
          push: true
          platforms: linux/amd64,linux/arm64
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/${{ secrets.DOCKERHUB_PROJECT_NAME }}:latest
            ${{ secrets.DOCKER_USERNAME }}/${{ secrets.DOCKERHUB_PROJECT_NAME }}:${{ steps.meta.outputs.SHORT_SHA }}
          cache-from: type=local,src=/tmp/.buildx-cache
```

---
title: "第 3 部分：使用 GitHub Actions 设置 CI/CD"
description: "学习如何为容器化的 Vue.js 应用程序设置 CI/CD 管道，使用 GitHub Actions 自动化构建、测试和部署流程。"
keywords: ["Docker", "GitHub Actions", "CI/CD", "Vue.js", "容器化", "自动化部署"]
tags: ["docker", "github-actions", "ci-cd", "vuejs", "containerization"]
---

## 第 3 部分：使用 GitHub Actions 设置 CI/CD

本节将指导您使用 GitHub Actions 为容器化的 Vue.js 应用程序设置完整的 CI/CD 管道。您将学习如何自动化构建、测试和部署流程，确保代码质量和部署的一致性。

---

### 步骤 1：创建 GitHub 仓库

首先，您需要创建一个新的 GitHub 仓库来托管您的 Vue.js 应用程序。

1. 登录到 GitHub 并创建一个新的仓库
   - 点击 "New repository" 按钮
   - 输入仓库名称（例如 `vuejs-docker-cicd`）
   - 选择 "Public" 或 "Private"（根据您的偏好）
   - **不要** 初始化仓库（不添加 README、.gitignore 或 license）

2. 将本地项目推送到 GitHub
   ```bash
   git remote add origin https://github.com/<your-username>/<your-repo-name>.git
   git branch -M main
   git push -u origin main
   ```

---

### 步骤 2：配置 Docker Hub 访问令牌

为了能够将 Docker 镜像推送到 Docker Hub，您需要配置访问令牌。

1. 生成 Docker Hub 访问令牌
   - 登录到 [Docker Hub](https://hub.docker.com/)
   - 导航到 Account Settings → Security
   - 点击 "New Access Token"
   - 输入令牌描述（例如 "GitHub Actions CI/CD"）
   - 点击 "Generate" 并复制生成的令牌

2. 将令牌添加到 GitHub 仓库
   - 转到您的 GitHub 仓库 → Settings → Secrets and variables → Actions
   - 点击 "New repository secret"
   - Name: `DOCKERHUB_TOKEN`
   - Secret: 粘贴您复制的访问令牌
   - 点击 "Add secret"

---

### 步骤 3：创建 GitHub Actions 工作流

在您的项目根目录中创建 `.github/workflows/ci-cd.yml` 文件：

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

env:
  REGISTRY: docker.io
  IMAGE_NAME: ${{ secrets.DOCKERHUB_USERNAME }}/${{ github.event.repository.name }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Cache Docker layers
        uses: actions/cache@v4
        with:
          path: /tmp/.buildx-cache
          key: ${{ runner.os }}-buildx-${{ github.sha }}
          restore-keys: |
            ${{ runner.os }}-buildx-

      - name: Build and run tests
        uses: docker/build-push-action@v6
        with:
          context: .
          file: ./Dockerfile.dev
          target: test
          load: true
          cache-from: type=local,src=/tmp/.buildx-cache
          cache-to: type=local,dest=/tmp/.buildx-cache-new
        env:
          DOCKER_BUILDKIT: 1

      - name: Run tests
        run: |
          docker run --rm $(docker images -q | head -n 1) npm test

      - name: Move cache
        run: |
          rm -rf /tmp/.buildx-cache
          mv /tmp/.buildx-cache-new /tmp/.buildx-cache

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    permissions:
      contents: read
      packages: write
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Extract metadata (tags, labels)
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=raw,value=latest
            type=sha,prefix=,suffix=,format=short

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: .
          file: ./Dockerfile
          target: prod
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

此工作流为您的 Vue.js 应用程序执行以下任务：
- 在每次针对 `main` 分支的 `push` 或 `pull request` 时触发。
- 使用 `Dockerfile.dev` 构建开发 Docker 镜像，针对测试进行优化。
- 在干净的容器化环境中使用 Vitest 执行单元测试以确保一致性。
- 如果任何测试失败，立即停止工作流——强制执行代码质量。
- 缓存 Docker 构建层和 npm 依赖项以加快 CI 运行速度。
- 使用 GitHub 仓库密钥安全地与 Docker Hub 进行身份验证。
- 使用 `Dockerfile` 中的 `prod` 阶段构建生产就绪镜像。
- 使用 `latest` 和短 SHA 标签将最终镜像标记并推送到 Docker Hub 以实现可追溯性。

> [!NOTE]
>  有关 `docker/build-push-action` 的更多信息，请参阅 [GitHub Action README](https://github.com/docker/build-push-action/blob/master/README.md)。

---

### 步骤 3：运行工作流

在您添加了工作流文件后，是时候触发并观察 CI/CD 过程的实际运行了。

1. 提交并推送您的工作流文件
   - 在 GitHub 编辑器中选择 "Commit changes…"
   - 此推送将自动触发 GitHub Actions 管道。

2. 监控工作流执行
   - 转到 GitHub 仓库中的 Actions 选项卡。
   - 点击进入工作流运行以跟踪每个步骤：**build**、**test** 和（如果成功）**push**。

3. 在 Docker Hub 上验证 Docker 镜像

   - 工作流成功运行后，访问您的 [Docker Hub 仓库](https://hub.docker.com/repositories)。
   - 您应该在您的仓库下看到一个新镜像，包含：
      - 仓库名称：`${your-repository-name}`
      - 标签包括：
         - `latest` – 代表最新的成功构建；适合快速测试或部署。
         - `<short-sha>` – 基于提交哈希的唯一标识符，用于版本跟踪、回滚和可追溯性。

> [!TIP] 保护您的主分支
> 为了保持代码质量并防止意外的直接推送，启用分支保护规则：
>  - 导航到您的 **GitHub 仓库 → Settings → Branches**。
>  - 在分支保护规则下，点击 **Add rule**。
>  - 指定 `main` 作为分支名称。
>  - 启用以下选项：
>     - *Require a pull request before merging*。
>     - *Require status checks to pass before merging*。
>
>  这确保只有经过测试和审查的代码才能合并到 `main` 分支。
---

## 总结

在本节中，您使用 GitHub Actions 为容器化的 Vue.js 应用程序设置了完整的 CI/CD 管道。

以下是您完成的内容：

- 为您的项目专门创建了一个新的 GitHub 仓库。
- 生成了一个安全的 Docker Hub 访问令牌并将其作为密钥添加到 GitHub。
- 定义了一个 GitHub Actions 工作流，该工作流：
   - 在 Docker 容器内构建您的应用程序。
   - 在一致的容器化环境中运行测试。
   - 如果测试通过，将生产就绪镜像推送到 Docker Hub。
- 通过 GitHub Actions 触发并验证了工作流执行。
- 确认您的镜像已成功发布到 Docker Hub。

通过此设置，您的 Vue.js 应用程序现在已准备好在不同环境中进行自动化测试和部署——提高信心、一致性和团队生产力。

---

## 相关资源

深入了解自动化和容器化应用程序的最佳实践：

- [GitHub Actions 简介](/guides/gha.md) – 了解 GitHub Actions 如何自动化您的工作流  
- [Docker Build GitHub Actions](/manuals/build/ci/github-actions/_index.md) – 使用 GitHub Actions 设置容器构建  
- [GitHub Actions 的工作流语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) – 编写 GitHub 工作流的完整参考  
- [Compose 文件参考](/compose/compose-file/) – `compose.yaml` 的完整配置参考  
- [编写 Dockerfiles 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 优化您的镜像以获得性能和安全性  

---

## 下一步

接下来，了解如何在部署之前在 Kubernetes 上本地测试和调试您的 Vue.js 工作负载。这有助于您确保应用程序在类似生产的环境中按预期运行，减少部署期间的意外情况。
