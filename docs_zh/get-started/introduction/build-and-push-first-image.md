---
title: 构建并推送你的第一个镜像
keywords: 概念, 容器, Docker Desktop
description: 本概念页面将教你如何构建并推送你的第一个镜像
summary: |
  学习如何构建你的第一个 Docker 镜像，这是容器化应用程序的关键步骤。我们将指导你完成创建镜像仓库、构建镜像并将其推送到 Docker Hub 的过程。这使你能够轻松地在团队内共享镜像。
weight: 3
aliases: 
 - /guides/getting-started/build-and-push-first-image/
---

{{< youtube-embed 7ge1s5nAa34 >}}

## 说明

现在你已经更新了[待办事项应用](develop-with-containers.md)，接下来你需要为应用程序创建一个容器镜像，并将其共享到 Docker Hub。为此，你需要完成以下步骤：

1. 使用你的 Docker 账户登录
2. 在 Docker Hub 上创建一个镜像仓库
3. 构建容器镜像
4. 将镜像推送到 Docker Hub

在开始实际操作之前，以下是一些你需要了解的核心概念。

### 容器镜像

如果你对容器镜像还不熟悉，可以将它们看作是一个标准化的包，其中包含了运行应用程序所需的一切，包括文件、配置和依赖项。这些包随后可以被分发和共享给其他人。

### Docker Hub

为了共享你的 Docker 镜像，你需要一个地方来存储它们。这就是镜像仓库（registry）的作用。虽然有很多镜像仓库，但 Docker Hub 是镜像的默认和首选仓库。Docker Hub 既为你提供存储自己镜像的地方，也让你能够找到他人的镜像，可以直接运行或用作构建自己镜像的基础。

在[使用容器开发](develop-with-containers.md)中，你使用了以下来自 Docker Hub 的镜像，它们都是[Docker 官方镜像](/manuals/docker-hub/image-library/trusted-content.md#docker-official-images)：

- [node](https://hub.docker.com/_/node) - 提供 Node 环境，用作你开发的基础。该镜像也用作最终应用镜像的基础。
- [mysql](https://hub.docker.com/_/mysql) - 提供 MySQL 数据库来存储待办事项
- [phpmyadmin](https://hub.docker.com/_/phpmyadmin) - 提供 phpMyAdmin，一个基于 Web 的 MySQL 数据库管理界面
- [traefik](https://hub.docker.com/_/traefik) - 提供 Traefik，一个现代的 HTTP 反向代理和负载均衡器，根据路由规则将请求路由到相应的容器

浏览完整的 [Docker 官方镜像](https://hub.docker.com/search?badges=official)、[Docker 认证发布者](https://hub.docker.com/search?badges=verified_publisher) 和 [Docker 赞助开源软件](https://hub.docker.com/search?badges=open_source) 镜像目录，了解更多可运行和构建的内容。

## 动手尝试

在本实践指南中，你将学习如何登录 Docker Hub 并将镜像推送到 Docker Hub 仓库。

## 使用你的 Docker 账户登录

要将镜像推送到 Docker Hub，你需要使用 Docker 账户登录。

1. 打开 Docker Dashboard。

2. 选择右上角的 **Sign in**（登录）。

3. 如果需要，创建一个账户并完成登录流程。

完成后，你应该看到 **Sign in** 按钮变成个人资料图片。

## 创建一个镜像仓库

现在你有了账户，可以创建一个镜像仓库。就像 Git 仓库存储源代码一样，镜像仓库存储容器镜像。

1. 访问 [Docker Hub](https://hub.docker.com)。

2. 选择 **Create repository**（创建仓库）。

3. 在 **Create repository** 页面，输入以下信息：

    - **Repository name**（仓库名称） - `getting-started-todo-app`
    - **Short description**（简短描述） - 可选，随意填写
    - **Visibility**（可见性） - 选择 **Public**（公开）以允许其他人拉取你自定义的待办应用

4. 选择 **Create**（创建）以创建仓库。

## 构建并推送镜像

现在你有了仓库，可以构建并推送你的镜像了。重要提示：你正在构建的镜像扩展了 Node 镜像，这意味着你不需要安装或配置 Node、yarn 等。你可以专注于你应用程序的独特之处。

> **什么是镜像/Dockerfile？**
>
> 简单来说，将容器镜像看作一个独立的包，其中包含运行进程所需的一切。在本例中，它将包含 Node 环境、后端代码和编译后的 React 代码。
>
> 任何使用该镜像运行容器的机器，都可以在无需预装任何其他软件的情况下运行应用程序。
>
> `Dockerfile` 是一个基于文本的脚本，提供如何构建镜像的指令集。对于本次快速入门，仓库中已经包含了 Dockerfile。

{{< tabs group="cli-or-vs-code" persist=true >}}
{{< tab name="CLI" >}}

1. 首先，克隆或将项目作为 ZIP 文件[下载到本地机器](https://github.com/docker/getting-started-todo-app/archive/refs/heads/main.zip)。

   ```console
   $ git clone https://github.com/docker/getting-started-todo-app
   ```

   克隆完成后，进入新创建的目录：

   ```console
   $ cd getting-started-todo-app
   ```

2. 运行以下命令构建项目，将 `DOCKER_USERNAME` 替换为你的用户名。

    ```console
    $ docker build -t <DOCKER_USERNAME>/getting-started-todo-app .
    ```

    例如，如果你的 Docker 用户名是 `mobydock`，你需要运行：

    ```console
    $ docker build -t mobydock/getting-started-todo-app .
    ```

3. 要验证镜像是否在本地存在，可以使用 `docker image ls` 命令：

    ```console
    $ docker image ls
    ```

    你会看到类似以下的输出：

    ```console
    REPOSITORY                          TAG       IMAGE ID       CREATED          SIZE
    mobydock/getting-started-todo-app   latest    1543656c9290   2 minutes ago    1.12GB
    ...
    ```

4. 要推送镜像，使用 `docker push` 命令。确保将 `DOCKER_USERNAME` 替换为你的用户名：

    ```console
    $ docker push <DOCKER_USERNAME>/getting-started-todo-app
    ```

    根据你的上传速度，推送可能需要一些时间。

{{< /tab >}}
{{< tab name="VS Code" >}}

1. 打开 Visual Studio Code。确保你已从[扩展市场](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)安装了 **Docker 扩展 for VS Code**。

   ![VS Code 扩展市场截图](images/install-docker-extension.webp)

2. 在 **File** 菜单中，选择 **Open Folder**。选择 **Clone Git Repository** 并粘贴此 URL：[https://github.com/docker/getting-started-todo-app](https://github.com/docker/getting-started-todo-app)

    ![VS Code 显示如何克隆仓库的截图](images/clone-the-repo.webp?border=true)

3. 右键点击 `Dockerfile` 并选择 **Build Image...**（构建镜像）菜单项。

    ![VS Code 显示右键菜单和"Build Image"菜单项的截图](images/build-vscode-menu-item.webp?border=true)

4. 在出现的对话框中，输入名称 `DOCKER_USERNAME/getting-started-todo-app`，将 `DOCKER_USERNAME` 替换为你的 Docker 用户名。

5. 按 **Enter** 后，你会看到一个终端出现，构建将在其中进行。完成后，可以关闭终端。

6. 通过选择左侧导航菜单中的 Docker 标志打开 VS Code 的 Docker 扩展。

7. 找到你创建的镜像。它的名称将是 `docker.io/DOCKER_USERNAME/getting-started-todo-app`。

8. 展开镜像以查看标签（或不同版本）。你应该看到一个名为 `latest` 的标签，这是镜像的默认标签。

9. 右键点击 **latest** 项并选择 **Push...**（推送）选项。

    ![Docker 扩展和推送镜像的右键菜单截图](images/build-vscode-push-image.webp)

10. 按 **Enter** 确认，然后观察你的镜像被推送到 Docker Hub。根据你的上传速度，推送镜像可能需要一些时间。

    上传完成后，可以关闭终端。

{{< /tab >}}
{{< /tabs >}}

## 回顾

在继续之前，花点时间反思一下刚才发生的事情。在短短几分钟内，你就能构建一个包含你应用程序的容器镜像，并将其推送到 Docker Hub。

接下来，请记住以下几点：

- Docker Hub 是查找可信内容的首选仓库。Docker 提供了一系列可信内容，包括 Docker 官方镜像、Docker 认证发布者和 Docker 赞助开源软件，可直接使用或作为你自己的镜像基础。

- Docker Hub 提供了一个分发你自己的应用程序的市场。任何人都可以创建账户并分发镜像。虽然你正在公开分发你创建的镜像，但私有仓库可以确保你的镜像仅对授权用户可见。

> **使用其他仓库**
>
> 虽然 Docker Hub 是默认仓库，但仓库是标准化的，并通过[开放容器倡议](https://opencontainers.org/)实现互操作。这允许公司和组织运行自己的私有仓库。通常，可信内容会从 Docker Hub 镜像（或复制）到这些私有仓库中。

## 下一步

现在你已经构建了一个镜像，是时候讨论为什么你作为开发者应该学习更多关于 Docker 的知识，以及它将如何帮助你完成日常任务。

{{< button text="下一步" url="whats-next" >}}