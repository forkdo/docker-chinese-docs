---
title: 使用 GitHub Actions 自动化构建
linkTitle: 使用 GitHub Actions 自动化构建
weight: 60
keywords: CI/CD, GitHub( Actions), Vue.js
description: 了解如何使用 GitHub Actions 为您的 Vue.js 应用程序配置 CI/CD。

---

## 前提条件

完成本指南的所有先前部分，从 [容器化 Vue.js 应用程序](containerize.md) 开始。

您还必须拥有：
- 一个 [GitHub](https://github.com/signup) 账户。
- 一个 [Docker Hub](https://hub.docker.com/signup) 账户。

---

## 概述

在本节中，您将使用 [GitHub Actions](https://docs.github.com/en/actions) 设置一个 CI/CD 管道，以自动执行以下操作：

- 在 Docker 容器中构建您的 Vue.js 应用程序。
- 在一致的环境中运行测试。
- 将生产就绪的镜像推送到 [Docker Hub](https://hub.docker.com)。

---

## 将您的 GitHub 仓库连接到 Docker Hub

为了使 GitHub Actions 能够构建和推送 Docker 镜像，您需要将 Docker Hub 凭证安全地存储在新的 GitHub 仓库中。

### 第 1 步：生成 Docker Hub 凭证并设置 GitHub 密钥

1. 从 [Docker Hub](https://hub.docker.com) 创建个人访问令牌 (PAT)
   1. 转到您的 **Docker Hub 账户 → 账户设置 → 安全性**。
   2. 生成一个新的访问令牌，权限为 **Read/Write**（读/写）。
   3. 将其命名为类似 `docker-vuejs-sample` 的名称。
   4. 复制并保存该令牌 — 您将在第 4 步中用到它。

2. 在 [Docker Hub](https://hub.docker.com/repositories/) 上创建一个仓库
   1. 转到您的 **Docker Hub 账户 → 创建仓库**。
   2. 对于仓库名称，请使用具有描述性的名称 — 例如：`vuejs-sample`。
   3. 创建后，复制并保存仓库名称 — 您将在第 4 步中用到它。

3. 为您的 Vue.js 项目创建一个新的 [GitHub 仓库](https://github.com/new)

4. 将 Docker Hub 凭证添加为 GitHub 仓库密钥

   在您新创建的 GitHub 仓库中：
   
   1. 导航至：
   **Settings（设置） → Secrets and variables（密钥和变量） → Actions → New repository secret（新建仓库密钥）**。

   2. 添加以下密钥：

   | 名称              | 值                          |
   |-------------------|--------------------------------|
   | `DOCKER_USERNAME` | 您的 Docker Hub 用户名       |
   | `DOCKERHUB_TOKEN` | 您的 Docker Hub 访问令牌（在第 1 步中创建）   |
   | `DOCKERHUB_PROJECT_NAME` | 您的 Docker 项目名称（在第 2 步中创建）   |

   这些密钥允许 GitHub Actions 在自动化工作流期间安全地向 Docker Hub 进行身份验证。

5. 将您的本地项目连接到 GitHub

   通过从项目根目录运行以下命令，将您的本地项目 `docker-vuejs-sample` 链接到您刚刚创建的 GitHub 仓库：

   ```console
      $ git remote set-url origin https://github.com/{your-username}/{your-repository-name}.git
   ```

   >[!IMPORTANT]
   >将 `{your-username}` 和 `{your-repository}` 替换为您实际的 GitHub 用户名和仓库名称。

   要确认您的本地项目已正确连接到远程 GitHub 仓库，请运行：

   ```console
   $ git remote -v
   ```

   您应该会看到类似以下的输出：

   ```console
   origin  https://github.com/{your-username}/{your-repository-name}.git (fetch)
   origin  https://github.com/{your-username}/{your-repository-name}.git (push)
   ```

   这确认了您的本地仓库已正确链接，并准备好将源代码推送到 GitHub。

6. 将您的源代码推送到 GitHub

   按照以下步骤提交并推送您的本地项目到 GitHub 仓库：

   1. 将所有文件暂存以供提交。

      ```console
      $ git add -A
      ```
      此命令暂存所有更改 — 包括新的、修改过的和已删除的文件 — 为提交做准备。


   2. 使用描述性消息提交已暂存的更改。

      ```console
      $ git commit -m "Initial commit"
      ```
      此命令创建一个提交，以描述性消息快照暂存的更改。  

   3. 将代码推送到 `main` 分支。

      ```console
      $ git push -u origin main
      ```
      此命令将您的本地提交推送到远程 GitHub 仓库的 `main` 分支，并设置上游分支。

完成后，您的代码将在 GitHub 上可用，并且您配置的任何 GitHub Actions 工作流都将自动运行。

> [!NOTE]  
> 了解更多关于本步骤中使用的 Git 命令的信息：
> - [Git add](https://git-scm.com/docs/git-add) – 暂存更改（新的、修改的、删除的）以供提交  
> - [Git commit](https://git-scm.com/docs/git-commit) – 保存已暂存更改的快照  
> - [Git push](https://git-scm.com/docs/git-push) – 将本地提交上传到您的 GitHub 仓库  
> - [Git remote](https://git-scm.com/docs/git-remote) – 查看和管理远程仓库 URL

---

### 第 2 步：设置工作流

现在您将创建一个 GitHub Actions 工作流，该工作流将构建您的 Docker 镜像，运行测试，并将镜像推送到 Docker Hub。

1. 转到 GitHub 上的仓库，并在顶部菜单中选择 **Actions** 选项卡。

2. 在提示时选择 **Set up a workflow yourself**（自行设置工作流）。

    这将打开一个内联编辑器以创建新的工作流文件。默认情况下，它将保存到：
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
      # 1. 签出代码库
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

      # 4. 缓存 npm 依赖项
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

此工作流为您的 Vue.js 应用程序执行以下任务：
- 在每次针对 `main` 分支的 `push` 或 `pull request` 时触发。
- 使用 `Dockerfile.dev` 构建一个开发 Docker 镜像，针对测试进行了优化。
- 在干净的容器化环境中使用 Vitest 执行单元测试，以确保一致性。
- 如果任何测试失败，立即停止工作流 — 强制执行代码质量。
- 缓存 Docker 构建层和 npm 依赖项，以加快 CI 运行速度。
- 使用 GitHub 仓库密钥安全地向 Docker Hub 进行身份验证。
- 使用 `Dockerfile` 中的 `prod` 阶段构建生产就绪的镜像。
- 使用 `latest` 和短 SHA 标记最终镜像并将其推送到 Docker Hub，以便进行跟踪。

> [!NOTE]
>  有关 `docker/build-push-action` 的更多信息，请参阅 [GitHub Action README](https://github.com/docker/build-push-action/blob/master/README.md)。

---

### 第 3 步：运行工作流

添加工作流文件后，是时候触发并观察 CI/CD 过程的运行了。

1. 提交并推送您的工作流文件
   - 在 GitHub 编辑器中选择 "Commit changes…"（提交更改…）。
   - 此推送将自动触发 GitHub Actions 管道。

2. 监控工作流执行
   - 转到 GitHub 仓库中的 Actions 选项卡。
   - 点击进入工作流运行，以跟踪每个步骤：**build**、**test** 和（如果成功）**push**。

3. 在 Docker Hub 上验证 Docker 镜像

   - 工作流成功运行后，访问您的 [Docker Hub 仓库](https://hub.docker.com/repositories)。
   - 您应该会在您的仓库下看到一个新的镜像，包含：
      - 仓库名称：`${your-repository-name}`
      - 标签包括：
         - `latest` – 代表最近的成功构建；非常适合快速测试或部署。
         - `<short-sha>` – 基于提交哈希的唯一标识符，对于版本跟踪、回滚和可追溯性非常有用。

> [!TIP] 保护您的 main 分支
> 要维护代码质量并防止意外直接推送，请启用分支保护规则：
>  - 导航到您的 **GitHub 仓库 → Settings（设置） → Branches（分支）**。
>  - 在分支保护规则下，点击 **Add rule（添加规则）**。
>  - 指定 `main` 作为分支名称。
>  - 启用以下选项：
>     - *Require a pull request before merging（在合并前需要拉取请求）*。
>     - *Require status checks to pass before merging（在合并前需要状态检查通过）*。
>
>  这确保只有经过测试和审查的代码才能合并到 `main` 分支。
---

## 总结

在本节中，您使用 GitHub Actions 为容器化的 Vue.js 应用程序设置了一个完整的 CI/CD 管道。

以下是您完成的工作：

- 为您的项目创建了一个新的 GitHub 仓库。
- 生成了一个安全的 Docker Hub 访问令牌，并将其作为密钥添加到 GitHub。
- 定义了一个 GitHub Actions 工作流，该工作流：
   - 在 Docker 容器中构建您的应用程序。
   - 在一致的容器化环境中运行测试。
   - 如果测试通过，则将生产就绪的镜像推送到 Docker Hub。
- 通过 GitHub Actions 触发并验证了工作流执行。
- 确认您的镜像已成功发布到 Docker Hub。

通过此设置，您的 Vue.js 应用程序现在已准备好进行跨环境的自动化测试和部署 — 从而提高信心、一致性和团队生产力。

---

## 相关资源

深入了解容器化应用程序的自动化和最佳实践：

- [GitHub Actions 简介](/guides/gha.md) – 了解 GitHub Actions 如何自动化您的工作流  
- [Docker Build GitHub Actions](/manuals/build/ci/github-actions/_index.md) – 使用 GitHub Actions 设置容器构建  
- [GitHub Actions 的工作流语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) – 编写 GitHub 工作流的完整参考  
- [Compose 文件参考](/compose/compose-file/) – `compose.yaml` 的完整配置参考  
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 优化镜像的性能和安全性  

---

## 下一步

接下来，学习如何在部署之前在 Kubernetes 上本地测试和调试您的 Vue.js 工作负载。这有助于确保您的应用程序在类似生产的环境中按预期运行，从而减少部署期间的意外情况。