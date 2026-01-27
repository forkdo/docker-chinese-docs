# 使用 GitHub Actions 自动化构建


## 先决条件

完成本指南从[容器化 Python 应用程序](containerize.md)开始的所有先前章节。你必须拥有一个 [GitHub](https://github.com/signup) 账户和一个已验证的 [Docker](https://hub.docker.com/signup) 账户才能完成本节内容。

如果你尚未为你的项目创建 [GitHub 仓库](https://github.com/new)，现在是时候创建了。创建仓库后，不要忘记[添加远程仓库](https://docs.github.com/en/get-started/getting-started-with-git/managing-remote-repositories)，并确保你可以提交代码并[将代码推送到 GitHub](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository#about-git-push)。

1. 在你的项目 GitHub 仓库中，打开 **Settings**，然后转到 **Secrets and variables** > **Actions**。

2. 在 **Variables** 选项卡下，创建一个名为 `DOCKER_USERNAME` 的新 **Repository variable**，并将你的 Docker ID 作为其值。

3. 为 Docker Hub 创建一个新的[个人访问令牌 (PAT)](/manuals/security/access-tokens.md#create-an-access-token)。你可以将此令牌命名为 `docker-tutorial`。确保访问权限包括读取和写入权限。

4. 将 PAT 作为 **Repository secret** 添加到你的 GitHub 仓库中，名称为 `DOCKERHUB_TOKEN`。

## 概述

GitHub Actions 是 GitHub 内置的 CI/CD（持续集成和持续部署）自动化工具。它允许你在特定事件发生时（例如推送代码、创建拉取请求等）定义用于构建、测试和部署代码的自定义工作流。工作流是基于 YAML 的自动化脚本，定义了触发时要执行的一系列步骤。工作流存储在仓库的 `.github/workflows/` 目录中。

在本节中，你将学习如何设置和使用 GitHub Actions 来构建 Docker 镜像并将其推送到 Docker Hub。你将完成以下步骤：

1. 定义 GitHub Actions 工作流。
2. 运行工作流。

## 1. 定义 GitHub Actions 工作流

你可以通过在仓库的 `.github/workflows/` 目录中创建 YAML 文件来创建 GitHub Actions 工作流。为此，请使用你喜欢的文本编辑器或 GitHub Web 界面。以下步骤展示了如何使用 GitHub Web 界面创建工作流文件。

如果你更喜欢使用 GitHub Web 界面，请按照以下步骤操作：

1. 转到 GitHub 上的你的仓库，然后选择 **Actions** 选项卡。

2. 选择 **set up a workflow yourself**。

   这会将你带到一个页面，用于在仓库中创建新的 GitHub Actions 工作流文件。默认情况下，文件创建在 `.github/workflows/main.yml` 下，让我们将其名称更改为 `build.yml`。

如果你更喜欢使用文本编辑器，请在仓库的 `.github/workflows/` 目录中创建一个名为 `build.yml` 的新文件。

将以下内容添加到文件中：

```yaml
name: Build and push Docker image

on:
  push:
    branches:
      - main

jobs:
  lint-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run pre-commit hooks
        run: pre-commit run --all-files

      - name: Run pyright
        run: pyright

  build_and_push:
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
          push: true
          tags: ${{ vars.DOCKER_USERNAME }}/${{ github.event.repository.name }}:latest
```

每个 GitHub Actions 工作流包括一个或多个作业。每个作业由多个步骤组成。每个步骤可以运行一组命令或使用已有的[现有操作](https://github.com/marketplace?type=actions)。上述操作包含三个步骤：

1. [**Login to Docker Hub**](https://github.com/docker/login-action)：使用你之前创建的 Docker ID 和个人访问令牌 (PAT) 登录到 Docker Hub 的操作。

2. [**Set up Docker Buildx**](https://github.com/docker/setup-buildx-action)：设置 Docker [Buildx](https://github.com/docker/buildx) 的操作，这是一个扩展 Docker CLI 功能的 CLI 插件。

3. [**Build and push**](https://github.com/docker/build-push-action)：构建 Docker 镜像并将其推送到 Docker Hub 的操作。`tags` 参数指定镜像名称和标签。本例中使用 `latest` 标签。

## 2. 运行工作流

提交更改并将其推送到 `main` 分支。此工作流会在你每次向 `main` 分支推送更改时运行。你可以在 [GitHub 文档](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows) 中找到有关工作流触发器的更多信息。

转到 GitHub 仓库的 **Actions** 选项卡。它会显示工作流。选择工作流可以查看其所有步骤的细分。

当工作流完成后，转到 [Docker Hub 上的你的仓库](https://hub.docker.com/repositories)。如果你在该列表中看到新仓库，则表示 GitHub Actions 工作流已成功将镜像推送到 Docker Hub。

## 总结

在本节中，你学习了如何为你的 Python 应用程序设置 GitHub Actions 工作流，其中包括：

- 运行 pre-commit 钩子进行代码检查和格式化
- 使用 Pyright 进行静态类型检查
- 构建和推送 Docker 镜像

相关信息：

- [GitHub Actions 简介](/guides/gha.md)
- [Docker Build GitHub Actions](/manuals/build/ci/github-actions/_index.md)
- [GitHub Actions 工作流语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## 后续步骤

在下一节中，你将学习如何使用 Kubernetes 进行本地开发。
