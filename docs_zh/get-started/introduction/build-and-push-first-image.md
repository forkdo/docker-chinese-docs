---
title: 构建并推送你的第一个镜像
keywords: concepts, container, docker desktop
description: 本概念页将教你如何构建并推送你的第一个镜像
summary: |
  学习如何构建你的第一个 Docker 镜像，这是将应用容器化的关键一步。我们将指导你完成创建镜像仓库、构建镜像并将其推送到 Docker Hub 的过程。这样你就可以轻松地在团队内共享你的镜像。
weight: 3
aliases: 
 - /guides/getting-started/build-and-push-first-image/
---

{{< youtube-embed 7ge1s5nAa34 >}}

## 说明

现在你已经更新了[待办事项列表应用](develop-with-containers.md)，接下来就可以为该应用创建容器镜像，并将其共享到 Docker Hub 上。为此，你需要完成以下步骤：

1. 使用你的 Docker 账户登录
2. 在 Docker Hub 上创建一个镜像仓库
3. 构建容器镜像
4. 将镜像推送到 Docker Hub

在开始动手操作之前，请先了解以下几个核心概念。

### 容器镜像

如果你是容器镜像的新手，可以将其理解为包含运行应用所需全部内容的标准化软件包，包括应用文件、配置和依赖项。这些软件包随后可以分发给他人共享。

### Docker Hub

要共享你的 Docker 镜像，你需要一个存储它们的地方。这就是镜像仓库的作用。虽然现在有很多镜像仓库可供选择，但 Docker Hub 是镜像的默认首选仓库。Docker Hub 既为你提供了存储自己镜像的空间，也让你能够找到他人的镜像来运行或作为自己镜像的基础。

在选择基础镜像时，Docker Hub 提供两类受信任的、由 Docker 维护的镜像：

- [Docker 官方镜像 (DOI)](/manuals/docker-hub/image-library/trusted-content.md#docker-official-images) —— 针对流行软件的精选镜像，遵循最佳实践并定期更新。
- [Docker 加固镜像 (DHI)](/manuals/dhi/_index.md) —— 最小化、安全、生产就绪的镜像，几乎不含 CVE 漏洞，旨在减少攻击面并简化合规性。DHI 镜像是基于 Apache 2.0 许可的免费开源软件。

在[使用容器开发](develop-with-containers.md)中，你使用了以下来自 Docker Hub 的镜像，它们都是 [Docker 官方镜像](/manuals/docker-hub/image-library/trusted-content.md#docker-official-images)：

- [node](https://hub.docker.com/_/node) —— 提供 Node 环境，是你开发工作的基础。该镜像也用作最终应用镜像的基础。
- [mysql](https://hub.docker.com/_/mysql) —— 提供 MySQL 数据库，用于存储待办事项列表项
- [phpmyadmin](https://hub.docker.com/_/phpmyadmin) —— 提供 phpMyAdmin，一个基于 Web 的 MySQL 数据库管理界面
- [traefik](https://hub.docker.com/_/traefik) —— 提供 Traefik，一个现代化的 HTTP 反向代理和负载均衡器，可根据路由规则将请求路由到相应的容器

探索 Docker Hub 上完整的可信内容目录：
- [Docker 官方镜像](https://hub.docker.com/search?badges=official) —— 针对流行软件的精选镜像
- [Docker 加固镜像](https://hub.docker.com/hardened-images/catalog) —— 安全加固的最小化生产镜像（也可在 [dhi.io](https://dhi.io) 获取）
- [Docker 认证发布者](https://hub.docker.com/search?badges=verified_publisher) —— 来自认证软件供应商的镜像
- [Docker 赞助开源项目](https://hub.docker.com/search?badges=open_source) —— 来自赞助的开源项目的镜像

## 动手实践

在本动手指南中，你将学习如何登录 Docker Hub 并将镜像推送到 Docker Hub 仓库。

## 使用你的 Docker 账户登录

要将镜像推送到 Docker Hub，你需要使用 Docker 账户登录。

1. 打开 Docker 仪表板。

2. 点击右上角的**登录**按钮。

3. 如果需要，请先创建一个账户，然后完成登录流程。

完成后，你应该会看到**登录**按钮变为你的头像。

## 创建镜像仓库

现在你已经拥有账户，可以创建一个镜像仓库。就像 Git 仓库保存源代码一样，镜像仓库用于存储容器镜像。

1. 访问 [Docker Hub](https://hub.docker.com)。

2. 点击**创建仓库**。

3. 在**创建仓库**页面，输入以下信息：

    - **仓库名称** —— `getting-started-todo-app`
    - **简短描述** —— 如果需要，可以输入描述
    - **可见性** —— 选择**公开**，以便其他人可以拉取你定制的待办事项应用

4. 点击**创建**以创建仓库。

## 构建并推送镜像

现在你已经拥有仓库，就可以构建并推送你的镜像了。需要注意的是，你正在构建的镜像是基于 Node 镜像扩展的，这意味着你无需安装或配置 Node、yarn 等工具。你可以专注于让你的应用变得独特。

> **什么是镜像/Dockerfile？**
>
> 暂时不必深入细节，可以将容器镜像理解为包含运行某个进程所需全部内容的单一软件包。在本例中，它将包含 Node 环境、后端代码以及编译后的 React 代码。
>
> 任何运行使用该镜像的容器的机器，都能够运行该应用，就像它原本构建的那样，而无需在机器上预装任何其他内容。
>
> `Dockerfile` 是一个基于文本的脚本，提供了构建镜像的指令集。在本快速入门中，仓库已经包含了 Dockerfile。

{{< tabs group="cli-or-vs-code" persist=true >}}
{{< tab name="CLI" >}}

1. 首先，将项目克隆或[以 ZIP 文件形式下载](https://github.com/docker/getting-started-todo-app/archive/refs/heads/main.zip)到本地机器。

   ```console
   $ git clone https://github.com/docker/getting-started-todo-app
   ```

   克隆项目后，进入克隆创建的新目录：

   ```console
   $ cd getting-started-todo-app
   ```

2. 通过运行以下命令构建项目，将 `DOCKER_USERNAME` 替换为你的用户名。

    ```console
    $ docker build -t <DOCKER_USERNAME>/getting-started-todo-app .
    ```

    例如，如果你的 Docker 用户名是 `mobydock`，则运行以下命令：

    ```console
    $ docker build -t mobydock/getting-started-todo-app .
    ```

3. 要验证镜像是否已在本地存在，可以使用 `docker image ls` 命令：

    ```console
    $ docker image ls
    ```

    你将看到类似以下的输出：

    ```console
    REPOSITORY                          TAG       IMAGE ID       CREATED          SIZE
    mobydock/getting-started-todo-app   latest    1543656c9290   2 minutes ago    1.12GB
    ...
    ```

4. 要推送镜像，请使用 `docker push` 命令。确保将 `DOCKER_USERNAME` 替换为你的用户名：

    ```console
    $ docker push <DOCKER_USERNAME>/getting-started-todo-app
    ```

    根据你的上传速度，推送过程可能需要一些时间。

{{< /tab >}}
{{< tab name="VS Code" >}}

1. 打开 Visual Studio Code。确保已从[扩展市场](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)安装了 **Docker extension for VS Code**。

   ![VS Code 扩展市场截图](images/install-docker-extension.webp)

2. 在**文件**菜单中，选择**打开文件夹**。选择**克隆 Git 仓库**，并粘贴此 URL：[https://github.com/docker/getting-started-todo-app](https://github.com/docker/getting-started-todo-app)

    ![VS Code 显示如何克隆仓库的截图](images/clone-the-repo.webp?border=true)

3. 右键点击 `Dockerfile`，选择**构建镜像...**菜单项。

    ![VS Code 显示右键菜单和“构建镜像”菜单项的截图](images/build-vscode-menu-item.webp?border=true)

4. 在弹出的对话框中，输入名称 `DOCKER_USERNAME/getting-started-todo-app`，将 `DOCKER_USERNAME` 替换为你的 Docker 用户名。

5. 按下 **Enter** 后，将出现一个终端窗口，构建过程将在其中进行。构建完成后，您可以关闭该终端。

6. 通过点击左侧导航菜单中的 Docker 图标，打开 VS Code 的 Docker 扩展。

7. 找到您创建的镜像。它的名称应为 `docker.io/DOCKER_USERNAME/getting-started-todo-app`。

8. 展开该镜像以查看其标签（或不同版本）。您应该会看到一个名为 `latest` 的标签，这是镜像的默认标签。

9. 右键点击 **latest** 项，然后选择 **Push...** 选项。

    ![Docker 扩展及右键菜单中推送镜像的截图](images/build-vscode-push-image.webp)

10. 按下 **Enter** 确认，然后观察您的镜像被推送至 Docker Hub。根据您的上传速度，推送镜像可能需要一些时间。

    上传完成后，您可以关闭终端。

{{< /tab >}}
{{< /tabs >}}


## 回顾

在继续之前，请花点时间回顾一下刚才的操作。在短短几分钟内，您就成功构建了一个打包应用程序的容器镜像，并将其推送到了 Docker Hub。

接下来，请记住以下几点：

- Docker Hub 是查找可信内容的权威镜像仓库。Docker 提供了一系列可信内容，包括 Docker 官方镜像、Docker 认证发布者和 Docker 赞助的开源软件，您可以直接使用这些内容，或将其作为自己镜像的基础。

- Docker Hub 提供了一个分发您自己应用程序的市场。任何人都可以创建账户并分发镜像。虽然您创建的是公开分发的镜像，但私有仓库可以确保您的镜像仅对授权用户可见。

> **其他镜像仓库的使用**
>
> 虽然 Docker Hub 是默认的镜像仓库，但通过 [Open Container Initiative](https://opencontainers.org/) 实现了镜像仓库的标准化和互操作性。这使得公司和组织能够运行自己的私有镜像仓库。通常情况下，可信内容会从 Docker Hub 镜像（或复制）到这些私有仓库中。
>



## 下一步

现在您已经成功构建了一个镜像，接下来我们将讨论为什么作为开发者，您应该进一步了解 Docker，以及它将如何帮助您完成日常任务。

{{< button text="下一步" url="whats-next" >}}