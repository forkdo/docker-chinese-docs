---
title: 使用 GitHub Actions 自动化构建
linkTitle: 使用 GitHub Actions 自动化构建
weight: 60
keywords: CI/CD, GitHub Actions, Angular
description: 了解如何为你的 Angular 应用配置基于 GitHub Actions 的 CI/CD 流水线。

---

## 前置条件

完成本指南之前的所有章节，从 [容器化 Angular 应用](containerize.md) 开始。

你还必须具备：
- 一个 [GitHub](https://github.com/signup) 账号。
- 一个 [Docker Hub](https://hub.docker.com/signup) 账号。

---

## 概述

在本节中，你将使用 [GitHub Actions](https://docs.github.com/en/actions) 设置 CI/CD 流水线，自动完成以下任务：

- 在 Docker 容器内构建 Angular 应用。
- 在一致的环境中运行测试。
- 将生产就绪的镜像推送到 [Docker Hub](https://hub.docker.com)。

---

## 将 GitHub 仓库连接到 Docker Hub

为了使 GitHub Actions 能够构建和推送 Docker 镜像，你需要在 GitHub 仓库中安全地存储 Docker Hub 凭据。

### 步骤 1：生成 Docker Hub 凭据并设置 GitHub Secrets

1. 从 [Docker Hub](https://hub.docker.com) 创建个人访问令牌（PAT）
   1. 进入 **Docker Hub 账号 → Account Settings → Security**。
   2. 生成一个新的访问令牌，权限为 **Read/Write**。
   3. 将其命名为类似 `docker-angular-sample` 的名称。
   4. 复制并保存该令牌——你将在步骤 4 中用到它。

2. 在 [Docker Hub](https://hub.docker.com/repositories/) 创建仓库
   1. 进入 **Docker Hub 账号 → Create a repository**。
   2. 仓库名称使用描述性名称——例如：`angular-sample`。
   3. 创建后，复制并保存仓库名称——你将在步骤 4 中用到它。

3. 在 [GitHub](https://github.com/new) 创建新仓库用于 Angular 项目

4. 将 Docker Hub 凭据添加为 GitHub 仓库 Secrets

   在你新创建的 GitHub 仓库中：
   
   1. 导航至：
   **Settings → Secrets and variables → Actions → New repository secret**。

   2. 添加以下 Secrets：

   | 名称              | 值                          |
   |-------------------|--------------------------------|
   | `DOCKER_USERNAME` | 你的 Docker Hub 用户名       |
   | `DOCKERHUB_TOKEN` | 你的 Docker Hub 访问令牌（在步骤 1 中创建）   |
   | `DOCKERHUB_PROJECT_NAME` | 你的 Docker 项目名称（在步骤 2 中创建）   |

   这些 Secrets 允许 GitHub Actions 在自动化工作流期间安全地与 Docker Hub 进行身份验证。

5. 将本地项目连接到 GitHub

   从项目根目录运行以下命令，将本地项目 `docker-angular-sample` 连接到刚创建的 GitHub 仓库：

   ```console
      $ git remote set-url origin https://github.com/{your-username}/{your-repository-name}.git
   ```

   >[!IMPORTANT]
   >将 `{your-username}` 和 `{your-repository}` 替换为你的实际 GitHub 用户名和仓库名。

   为确认本地项目已正确连接到远程 GitHub 仓库，运行：

   ```console
   $ git remote -v
   ```

   你应该看到类似以下输出：

   ```console
   origin  https://github.com/{your-username}/{your-repository-name}.git (fetch)
   origin  https://github.com/{your-username}/{your-repository-name}.git (push)
   ```

   这确认了本地仓库已正确关联，准备将源代码推送到 GitHub。

6. 推送源代码到 GitHub

   按以下步骤提交并推送本地项目到 GitHub 仓库：

   1. 暂存所有文件以准备提交。

      ```console
      $ git add -A
      ```
      此命令暂存所有更改——包括新增、修改和删除的文件——为提交做准备。

   2. 使用描述性消息提交暂存的更改。

      ```console
      $ git commit -m "Initial commit"
      ```
      此命令创建一个提交，快照暂存的更改并附带描述性消息。

   3. 推送到 `main` 分支。

      ```console
      $ git push -u origin main
      ```
      此命令将本地提交推送到远程 GitHub 仓库的 `main` 分支，并设置上游分支。

完成后，你的代码将出现在 GitHub 上，任何配置的 GitHub Actions 工作流将自动运行。

> [!NOTE]  
> 了解本步骤中使用的 Git 命令：
> - [Git add](https://git-scm.com/docs/git-add) – 暂存更改（新增、修改、删除）以准备提交  
> - [Git commit](https://git-scm.com/docs/git-commit) – 保存暂存更改的快照  
> - [Git push](https://git-scm.com/docs/git-push) – 将本地提交上传到 GitHub 仓库  
> - [Git remote](https://git-scm.com/docs/git-remote) – 查看和管理远程仓库 URL

---

### 步骤 2：设置工作流

现在你将创建一个 GitHub Actions 工作流，用于构建 Docker 镜像、运行测试并将镜像推送到 Docker Hub。

1. 在 GitHub 仓库中，选择顶部菜单的 **Actions** 标签。

2. 出现提示时，选择 **Set up a workflow yourself**。

   这将打开一个内联编辑器以创建新的工作流文件。默认情况下，它将被保存到：
   `.github/workflows/main.yml`

   
3. 将以下工作流配置添加到新文件中：

```yaml
name: CI/CD – Angular Application with Docker

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

jobs:
  build-test-push:
    name: Build, Test, and Push Docker Image
    runs-on: ubuntu-latest

    steps:
      # 1. Checkout source code
      - name: Checkout source code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      # 2. Set up Docker Buildx
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      # 3. Cache Docker layers
      - name: Cache Docker layers
        uses: actions/cache@v4
        with:
          path: /tmp/.buildx-cache
          key: ${{ runner.os }}-buildx-${{ github.sha }}
          restore-keys: |
            ${{ runner.os }}-buildx-

      # 4. Cache npm dependencies
      - name: Cache npm dependencies
        uses: actions/cache@v4
        with:
          path: ~/.npm
          key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-npm-

      # 5. Extract metadata
      - name: Extract metadata
        id: meta
        run: |
          echo "REPO_NAME=${GITHUB_REPOSITORY##*/}" >> "$GITHUB_OUTPUT"
          echo "SHORT_SHA=${GITHUB_SHA::7}" >> "$GITHUB_OUTPUT"

      # 6. Build dev Docker image
      - name: Build Docker image for tests
        uses: docker/build-push-action@v6
        with:
          context: .
          file: Dockerfile.dev
          tags: ${{ steps.meta.outputs.REPO_NAME }}-dev:latest
          load: true
          cache-from: type=local,src=/tmp/.buildx-cache
          cache-to: type=local,dest=/tmp/.buildx-cache,mode=max

      # 7. Run Angular tests with Jasmine
      - name: Run Angular Jasmine tests inside container
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
      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      # 9. Build and push production image
      - name: Build and push production image
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

此工作流为你的 Angular 应用执行以下任务：
- 在每次推送到 `main` 分支或针对 `main` 分支的拉取请求时触发。
- 使用 `Dockerfile.dev` 构建开发 Docker 镜像，优化测试环境。
- 在干净、容器化的环境中使用 Vitest 执行单元测试，确保一致性。
- 如果任何测试失败，立即停止工作流——强制执行代码质量。
- 缓存 Docker 构建层和 npm 依赖以加快 CI 运行速度。
- 使用 GitHub 仓库 Secrets 安全地与 Docker Hub 进行身份验证。
- 使用 `Dockerfile` 的 `prod` 阶段构建生产就绪镜像。
- 使用 `latest` 和短 SHA 标签标记并推送到 Docker Hub，便于追踪。

> [!NOTE]
> 有关 `docker/build-push-action` 的更多信息，请参考 [GitHub Action README](https://github.com/docker/build-push-action/blob/master/README.md)。

---

### 步骤 3：运行工作流

添加工作流文件后，现在是时候触发并观察 CI/CD 过程的实际运行。

1. 提交并推送工作流文件

   - 在 GitHub 编辑器中选择“Commit changes…”。
   - 此推送将自动触发 GitHub Actions 流水线。

2. 监控工作流执行

   - 进入 GitHub 仓库的 Actions 标签页。
   - 点击工作流运行以查看每一步：**build**、**test** 和（如果成功）**push**。

3. 验证 Docker Hub 上的镜像

   - 工作流成功运行后，访问你的 [Docker Hub 仓库](https://hub.docker.com/repositories)。
   - 你应该在仓库中看到新镜像，包含：
      - 仓库名：`${your-repository-name}`
      - 标签包括：
         - `latest` – 代表最近一次成功的构建；适用于快速测试或部署。
         - `<short-sha>` – 基于提交哈希的唯一标识符，用于版本追踪、回滚和可追溯性。

> [!TIP] 保护你的主分支
> 为保持代码质量并防止意外的直接推送，启用分支保护规则：
>  - 导航到 **GitHub 仓库 → Settings → Branches**。
>  - 在 Branch protection rules 下，点击 **Add rule**。
>  - 指定 `main` 为分支名。
>  - 启用以下选项：
>     - *Require a pull request before merging*。
>     - *Require status checks to pass before merging*。
>
> 这确保只有经过测试和审查的代码才能合并到 `main` 分支。
---

## 总结

在本节中，你为容器化的 Angular 应用使用 GitHub Actions 设置了完整的 CI/CD 流水线。

你完成了以下工作：

- 为项目创建了新的 GitHub 仓库。
- 生成了安全的 Docker Hub 访问令牌并将其作为 Secret 添加到 GitHub。
- 定义了 GitHub Actions 工作流，包括：
   - 在 Docker 容器内构建应用。
   - 在一致的容器化环境中运行测试。
   - 如果测试通过，将生产就绪镜像推送到 Docker Hub。
- 触发并验证了 GitHub Actions 中的工作流执行。
- 确认镜像已成功发布到 Docker Hub。

有了这个设置，你的 Angular 应用现在已准备好进行自动化测试和跨环境部署——提高信心、一致性和团队效率。

---

## 相关资源

深入了解容器化应用的自动化和最佳实践：

- [GitHub Actions 介绍](/guides/gha.md) – 学习如何使用 GitHub Actions 自动化工作流  
- [Docker Build GitHub Actions](/manuals/build/ci/github-actions/_index.md) – 使用 GitHub Actions 设置容器构建  
- [GitHub Actions 工作流语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) – 编写 GitHub 工作流的完整参考  
- [Compose 文件参考](/compose/compose-file/) – `compose.yaml` 的完整配置参考  
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 优化镜像的性能和安全性  

---

## 下一步

接下来，了解如何在 Kubernetes 上本地测试和调试 Angular 工作负载，然后再进行部署。这有助于确保你的应用在类似生产的环境中按预期运行，减少部署时的意外情况。