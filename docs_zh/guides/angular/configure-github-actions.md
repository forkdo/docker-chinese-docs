---
title: 使用 GitHub Actions 自动化构建
linkTitle: 使用 GitHub Actions 自动化构建
weight: 60
keywords: CI/CD, GitHub( Actions), Angular
description: 了解如何为 Angular 应用程序配置基于 GitHub Actions 的 CI/CD。

---

## 先决条件

请完成本指南之前的所有章节，从 [容器化 Angular 应用程序](containerize.md) 开始。

此外，您必须拥有：
- 一个 [GitHub](https://github.com/signup) 账号。
- 一个 [Docker Hub](https://hub.docker.com/signup) 账号。

---

## 概述

在本节中，您将使用 [GitHub Actions](https://docs.github.com/en/actions) 设置一个 CI/CD 流程，用于自动执行以下操作：

- 在 Docker 容器中构建您的 Angular 应用程序。
- 在一致的环境中运行测试。
- 将生产就绪的镜像推送到 [Docker Hub](https://hub.docker.com)。

---

## 将您的 GitHub 仓库连接到 Docker Hub

为了使 GitHub Actions 能够构建和推送 Docker 镜像，您需要将 Docker Hub 凭证安全地存储在新的 GitHub 仓库中。

### 第 1 步：生成 Docker Hub 凭证并设置 GitHub Secrets

1.  从 [Docker Hub](https://hub.docker.com) 创建个人访问令牌 (PAT)
    1.  进入您的 **Docker Hub 账号 → 账户设置 → 安全性 (Security)**。
    2.  生成一个新的访问令牌，权限设置为 **读/写 (Read/Write)**。
    3.  将其命名为类似 `docker-angular-sample` 的名称。
    4.  复制并保存该令牌 — 您将在第 4 步用到它。

2.  在 [Docker Hub](https://hub.docker.com/repositories/) 创建一个仓库
    1.  进入您的 **Docker Hub 账号 → 创建仓库 (Create a repository)**。
    2.  对于仓库名称，请使用具有描述性的名称 — 例如：`angular-sample`。
    3.  创建后，复制并保存仓库名称 — 您将在第 4 步用到它。

3.  为您的 Angular 项目创建一个新的 [GitHub 仓库](https://github.com/new)

4.  将 Docker Hub 凭证添加为 GitHub 仓库机密 (Secrets)

    在您新创建的 GitHub 仓库中：
    
    1.  导航至：
    **Settings (设置) → Secrets and variables (机密和变量) → Actions → New repository secret (新建仓库机密)**。

    2.  添加以下机密：

    | 名称 (Name)              | 值 (Value)                          |
    |-------------------|--------------------------------|
    | `DOCKER_USERNAME` | 您的 Docker Hub 用户名       |
    | `DOCKERHUB_TOKEN` | 您的 Docker Hub 访问令牌（在第 1 步创建）   |
    | `DOCKERHUB_PROJECT_NAME` | 您的 Docker 项目名称（在第第 2 步创建）   |

    这些机密允许 GitHub Actions 在自动化工作流期间安全地向 Docker Hub 进行身份验证。

5.  将本地项目连接到 GitHub

    通过在项目根目录下运行以下命令，将您的本地项目 `docker-angular-sample` 链接到您刚刚创建的 GitHub 仓库：

    ```console
       $ git remote set-url origin https://github.com/{your-username}/{your-repository-name}.git
    ```

    >[!IMPORTANT]
    >请将 `{your-username}` 和 `{your-repository}` 替换为您实际的 GitHub 用户名和仓库名称。

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

6.  将源代码推送到 GitHub

    按照以下步骤提交并将本地项目推送到您的 GitHub 仓库：

    1.  将所有文件暂存以供提交。

        ```console
        $ git add -A
        ```
        此命令暂存所有更改 — 包括新文件、已修改文件和已删除文件 — 为提交做准备。

    2.  使用描述性消息提交暂存的更改。

        ```console
        $ git commit -m "Initial commit"
        ```
        此命令创建一个提交，以描述性消息快照暂存的更改。

    3.  将代码推送到 `main` 分支。

        ```console
        $ git push -u origin main
        ```
        此命令将您的本地提交推送到远程 GitHub 仓库的 `main` 分支，并设置上游分支。

完成后，您的代码将在 GitHub 上可用，并且您配置的任何 GitHub Actions 工作流都将自动运行。

> [!NOTE]  
> 了解更多关于本步骤中使用的 Git 命令的信息：
> - [Git add](https://git-scm.com/docs/git-add) – 暂存更改（新建、修改、删除）以供提交  
> - [Git commit](https://git-scm.com/docs/git-commit) – 保存暂存更改的快照  
> - [Git push](https://git-scm.com/docs/git-push) – 将本地提交上传到您的 GitHub 仓库  
> - [Git remote](https://git-scm.com/docs/git-remote) – 查看和管理远程仓库 URL

---

### 第 2 步：设置工作流

现在您将创建一个 GitHub Actions 工作流，用于构建您的 Docker 镜像、运行测试并将镜像推送到 Docker Hub。

1.  转到 GitHub 上的仓库，并在顶部菜单中选择 **Actions (操作)** 选项卡。

2.  当提示时，选择 **Set up a workflow yourself (自己设置工作流)**。

    这将打开一个内联编辑器以创建新的工作流文件。默认情况下，它将保存到：
    `.github/workflows/main.yml`

    
3.  将以下工作流配置添加到新文件中：

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
      # 1. 签出源代码
      - name: Checkout source code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      # 2. 设置 Docker Buildx
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      # 3. 缓存 Docker 层
      - name: Cache Docker layers
        uses: actions/cache@v4
        with:
          path: /tmp/.buildx-cache
          key: ${{ runner.os }}-buildx-${{ github.sha }}
          restore-keys: |
            ${{ runner.os }}-buildx-

      # 4. 缓存 npm 依赖项
      - name: Cache npm dependencies
        uses: actions/cache@v4
        with:
          path: ~/.npm
          key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-npm-

      # 5. 提取元数据
      - name: Extract metadata
        id: meta
        run: |
          echo "REPO_NAME=${GITHUB_REPOSITORY##*/}" >> "$GITHUB_OUTPUT"
          echo "SHORT_SHA=${GITHUB_SHA::7}" >> "$GITHUB_OUTPUT"

      # 6. 构建开发版 Docker 镜像
      - name: Build Docker image for tests
        uses: docker/build-push-action@v6
        with:
          context: .
          file: Dockerfile.dev
          tags: ${{ steps.meta.outputs.REPO_NAME }}-dev:latest
          load: true
          cache-from: type=local,src=/tmp/.buildx-cache
          cache-to: type=local,dest=/tmp/.buildx-cache,mode=max

      # 7. 使用 Jasmine 运行 Angular 测试
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

      # 8. 登录 Docker Hub
      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      # 9. 构建并推送生产镜像
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

此工作流为您的 Angular 应用程序执行以下任务：
- 在针对 `main` 分支的每次 `push` 或 `pull request` 时触发。
- 使用 `Dockerfile.dev` 构建一个针对测试优化的开发版 Docker 镜像。
- 在干净的容器化环境中使用 Vitest 执行单元测试，以确保一致性。
- 如果任何测试失败，立即停止工作流 — 强制执行代码质量。
- 缓存 Docker 构建层和 npm 依赖项，以加快 CI 运行速度。
- 使用 GitHub 仓库机密安全地向 Docker Hub 进行身份验证。
- 使用 `Dockerfile` 中的 `prod` 阶段构建生产就绪的镜像。
- 使用 `latest` 和短 SHA 标记最终镜像并将其推送到 Docker Hub，以便于跟踪。

> [!NOTE]
>  有关 `docker/build-push-action` 的更多信息，请参阅 [GitHub Action README](https://github.com/docker/build-push-action/blob/master/README.md)。

---

### 第 3 步：运行工作流

添加工作流文件后，是时候触发并观察 CI/CD 流程的运行了。

1.  提交并推送您的工作流文件

    - 在 GitHub 编辑器中选择 "Commit changes…" (提交更改…)。

    - 此推送将自动触发 GitHub Actions 流程。

2.  监控工作流执行

    - 转到 GitHub 仓库中的 Actions (操作) 选项卡。
    - 点击进入工作流运行，以跟踪每个步骤：**build (构建)**、**test (测试)** 以及（如果成功）**push (推送)**。

3.  在 Docker Hub 上验证 Docker 镜像

    - 工作流成功运行后，访问您的 [Docker Hub 仓库](https://hub.docker.com/repositories)。
    - 您应该会在您的仓库下看到一个新镜像，包含：
       - 仓库名称：`${your-repository-name}`
       - 标签包括：
          - `latest` – 代表最近一次成功的构建；非常适合快速测试或部署。
          - `<short-sha>` – 基于提交哈希的唯一标识符，对版本跟踪、回滚和可追溯性很有用。

> [!TIP] 保护您的主分支
> 要维护代码质量并防止意外直接推送，请启用分支保护规则：
>  - 导航至您的 **GitHub 仓库 → Settings (设置) → Branches (分支)**。
>  - 在分支保护规则下，点击 **Add rule (添加规则)**。
>  - 指定 `main` 作为分支名称。
>  - 启用以下选项：
>     - *Require a pull request before merging (合并前需要拉取请求)*。
>     - *Require status checks to pass before merging (合并前需要状态检查通过)*。
>
>  这确保只有经过测试和审查的代码才能合并到 `main` 分支。
---

## 总结

在本节中，您使用 GitHub Actions 为容器化的 Angular 应用程序设置了一个完整的 CI/CD 流程。

以下是您完成的工作：

- 为您的项目创建了一个新的 GitHub 仓库。
- 生成了一个安全的 Docker Hub 访问令牌，并将其作为机密添加到 GitHub。
- 定义了一个 GitHub Actions 工作流，该工作流：
   - 在 Docker 容器中构建您的应用程序。
   - 在一致的容器化环境中运行测试。
   - 如果测试通过，则将生产就绪的镜像推送到 Docker Hub。
- 通过 GitHub Actions 触发并验证了工作流执行。
- 确认您的镜像已成功发布到 Docker Hub。

通过此设置，您的 Angular 应用程序现在已准备好进行跨环境的自动化测试和部署 — 从而提高信心、一致性和团队生产力。

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

接下来，学习如何在部署之前在 Kubernetes 上本地测试和调试您的 Angular 工作负载。这有助于确保您的应用程序在类生产环境中按预期运行，从而减少部署过程中的意外情况。