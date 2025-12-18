---
title: 使用 GitHub Actions 自动化构建
linkTitle: 使用 GitHub Actions 自动化构建
weight: 60
keywords: CI/CD, GitHub Actions, Vue.js
description: 了解如何为你的 Vue.js 应用配置基于 GitHub Actions 的 CI/CD。

---

## 前置条件

完成本指南的所有前置章节，从 [容器化 Vue.js 应用](containerize.md) 开始。

你还需要：
- 一个 [GitHub](https://github.com/signup) 账号。
- 一个 [Docker Hub](https://hub.docker.com/signup) 账号。

---

## 概述

在本节中，你将使用 [GitHub Actions](https://docs.github.com/en/actions) 设置 CI/CD 流水线，自动完成以下任务：

- 在 Docker 容器中构建你的 Vue.js 应用。
- 在一致的环境中运行测试。
- 将生产就绪的镜像推送到 [Docker Hub](https://hub.docker.com)。

---

## 将 GitHub 仓库连接到 Docker Hub

为了让 GitHub Actions 能够构建并推送 Docker 镜像，你需要将 Docker Hub 凭据安全地存储在 GitHub 仓库中。

### 步骤 1：生成 Docker Hub 凭据并设置 GitHub Secrets

1. 从 [Docker Hub](https://hub.docker.com) 创建个人访问令牌 (PAT)
   1. 进入 **Docker Hub 账号 → Account Settings → Security**。
   2. 生成一个新的访问令牌，权限为 **Read/Write**。
   3. 将其命名为类似 `docker-vuejs-sample` 的名称。
   4. 复制并保存该令牌 —— 你将在步骤 4 中用到它。

2. 在 [Docker Hub](https://hub.docker.com/repositories/) 创建仓库
   1. 进入 **Docker Hub 账号 → Create a repository**。
   2. 仓库名称使用一个有意义的名称 —— 例如：`vuejs-sample`。
   3. 创建后，复制并保存仓库名称 —— 你将在步骤 4 中用到它。

3. 为你的 Vue.js 项目创建一个新的 [GitHub 仓库](https://github.com/new)

4. 将 Docker Hub 凭据添加为 GitHub 仓库 Secrets

   在你刚创建的 GitHub 仓库中：
   
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

   从项目根目录运行以下命令，将本地项目 `docker-vuejs-sample` 链接到刚创建的 GitHub 仓库：

   ```console
      $ git remote set-url origin https://github.com/{your-username}/{your-repository-name}.git
   ```

   >[!IMPORTANT]
   >将 `{your-username}` 和 `{your-repository}` 替换为你的实际 GitHub 用户名和仓库名。

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

6. 将源代码推送到 GitHub

   按以下步骤提交并推送本地项目到 GitHub 仓库：

   1. 将所有文件加入暂存区。

      ```console
      $ git add -A
      ```
      此命令将所有变更（新增、修改、删除的文件）加入暂存区，为提交做准备。

   2. 提交暂存的变更并附上描述性消息。

      ```console
      $ git commit -m "Initial commit"
      ```
      此命令创建一次提交，将暂存的变更以描述性消息保存快照。

   3. 将代码推送到 `main` 分支。

      ```console
      $ git push -u origin main
      ```
      此命令将本地提交推送到远程 GitHub 仓库的 `main` 分支，并设置上游分支。

完成后，你的代码将出现在 GitHub 上，任何已配置的 GitHub Actions 工作流将自动运行。

> [!NOTE]  
> 了解更多本步骤中使用的 Git 命令：
> - [Git add](https://git-scm.com/docs/git-add) – 将变更加入暂存区（新增、修改、删除）  
> - [Git commit](https://git-scm.com/docs/git-commit) – 保存暂存变更的快照  
> - [Git push](https://git-scm.com/docs/git-push) – 将本地提交上传到 GitHub 仓库  
> - [Git remote](https://git-scm.com/docs/git-remote) – 查看和管理远程仓库 URL

---

### 步骤 2：设置工作流

现在你将创建一个 GitHub Actions 工作流，用于构建 Docker 镜像、运行测试并将镜像推送到 Docker Hub。

1. 访问 GitHub 上的仓库，点击顶部菜单中的 **Actions** 标签。

2. 提示时选择 **Set up a workflow yourself**。

    这将打开一个内联编辑器，创建新的工作流文件。默认保存路径为：
   `.github/workflows/main.yml`

   
3. 将以下工作流配置添加到新文件中：

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
      # 1. 检出代码
      - name: Checkout Code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      # 2. 设置 Docker Buildx
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      # 3. 缓存 Docker 层
      - name: Cache Docker Layers
        uses: actions/cache@v4
        with:
          path: /tmp/.buildx-cache
          key: ${{ runner.os }}-buildx-${{ github.sha }}
          restore-keys: |
            ${{ runner.os }}-buildx-

      # 4. 缓存 npm 依赖
      - name: Cache npm Dependencies
        uses: actions/cache@v4
        with:
          path: ~/.npm
          key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-npm-

      # 5. 生成构建元数据
      - name: Generate Build Metadata
        id: meta
        run: |
          echo "REPO_NAME=${GITHUB_REPOSITORY##*/}" >> "$GITHUB_OUTPUT"
          echo "SHORT_SHA=${GITHUB_SHA::7}" >> "$GITHUB_OUTPUT"

      # 6. 为测试构建 Docker 镜像
      - name: Build Dev Docker Image
        uses: docker/build-push-action@v6
        with:
          context: .
          file: Dockerfile.dev
          tags: ${{ steps.meta.outputs.REPO_NAME }}-dev:latest
          load: true
          cache-from: type=local,src=/tmp/.buildx-cache
          cache-to: type=local,dest=/tmp/.buildx-cache,mode=max

      # 7. 在容器内运行单元测试
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

      # 8. 登录 Docker Hub
      - name: Docker Hub Login
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      # 9. 构建并推送生产镜像
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

此工作流为你的 Vue.js 应用执行以下任务：
- 在每次推送到 `main` 分支或针对 `main` 分支的 `pull request` 时触发。
- 使用 `Dockerfile.dev` 构建开发 Docker 镜像，针对测试优化。
- 在干净、容器化的环境中使用 Vitest 执行单元测试，确保一致性。
- 如果任何测试失败，立即中止工作流 —— 强制执行代码质量。
- 缓存 Docker 构建层和 npm 依赖，加快 CI 运行速度。
- 使用 GitHub 仓库 Secrets 安全地与 Docker Hub 进行身份验证。
- 使用 `Dockerfile` 的 `prod` 阶段构建生产就绪镜像。
- 将最终镜像标记并推送到 Docker Hub，包含 `latest` 和短 SHA 标签，便于追踪。

> [!NOTE]
>  有关 `docker/build-push-action` 的更多信息，请参考 [GitHub Action README](https://github.com/docker/build-push-action/blob/master/README.md)。

---

### 步骤 3：运行工作流

添加工作流文件后，现在开始触发并观察 CI/CD 流程的实际运行。

1. 提交并推送工作流文件
   - 在 GitHub 编辑器中选择 "Commit changes…"。
   - 此次推送将自动触发 GitHub Actions 流水线。

2. 监控工作流执行
   - 进入 GitHub 仓库的 Actions 标签页。
   - 点击工作流运行，查看每一步：**build**、**test** 和（如果成功）**push**。

3. 在 Docker Hub 验证 Docker 镜像

   - 工作流成功运行后，访问你的 [Docker Hub 仓库](https://hub.docker.com/repositories)。
   - 你应该在仓库中看到一个新镜像，包含：
      - 仓库名：`${your-repository-name}`
      - 标签包括：
         - `latest` – 代表最近一次成功的构建；适合快速测试或部署。
         - `<short-sha>` – 基于提交哈希的唯一标识符，用于版本追踪、回滚和可追溯性。

> [!TIP] 保护你的主分支
> 为保持代码质量并防止意外的直接推送，启用分支保护规则：
>  - 导航至你的 **GitHub 仓库 → Settings → Branches**。
>  - 在 Branch protection rules 下，点击 **Add rule**。
>  - 将 `main` 指定为分支名。
>  - 启用以下选项：
>     - *Require a pull request before merging*（合并前需要拉取请求）。
>     - *Require status checks to pass before merging*（合并前需要状态检查通过）。
>
>  这确保只有经过测试和审查的代码才能合并到 `main` 分支。
---

## 总结

在本节中，你为容器化的 Vue.js 应用使用 GitHub Actions 设置了完整的 CI/CD 流水线。

你完成了以下工作：

- 创建了一个专门用于项目的 GitHub 仓库。
- 生成了安全的 Docker Hub 访问令牌，并将其作为 Secret 添加到 GitHub。
- 定义了 GitHub Actions 工作流，能够：
   - 在 Docker 容器中构建应用。
   - 在一致的容器化环境中运行测试。
   - 如果测试通过，将生产就绪镜像推送到 Docker Hub。
- 触发并验证了工作流通过 GitHub Actions 的执行。
- 确认镜像已成功发布到 Docker Hub。

有了这个设置，你的 Vue.js 应用现在已准备好进行自动化的测试和跨环境部署 —— 提高信心、一致性和团队效率。

---

## 相关资源

深入理解容器化应用的自动化和最佳实践：

- [GitHub Actions 入门](/guides/gha.md) – 了解 GitHub Actions 如何自动化工作流  
- [Docker Build GitHub Actions](/manuals/build/ci/github-actions/_index.md) – 使用 GitHub Actions 设置容器构建  
- [GitHub Actions 工作流语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) – 编写 GitHub 工作流的完整参考  
- [Compose 文件参考](/compose/compose-file/) – `compose.yaml` 的完整配置参考  
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 优化镜像的性能和安全性  

---

## 后续步骤

接下来，了解如何在 Kubernetes 上本地测试和调试你的 Vue.js 工作负载，然后再进行部署。这有助于确保你的应用在类似生产的环境中按预期运行，减少部署时的意外情况。