---
title: 构建并推送你的第一个镜像
keywords: concepts, container, docker desktop
description: 本概念页将教你如何构建并推送你的第一个镜像
summary: '学习如何构建你的第一个 Docker 镜像，这是将你的应用容器化的关键一步。我们将指导你完成创建镜像仓库、构建镜像并将其推送到 Docker Hub 的过程。这样你就可以轻松地在团队内部分享你的镜像。

  '
weight: 3
aliases:
- /guides/getting-started/build-and-push-first-image/
---

{{< youtube-embed 7ge1s5nAa34 >}}

## 说明

现在你已经更新了[待办事项列表应用](develop-with-containers.md)，接下来就可以为这个应用创建一个容器镜像，并将其分享到 Docker Hub 上。为此，你需要完成以下步骤：

1. 使用你的 Docker 账户登录
2. 在 Docker Hub 上创建一个镜像仓库
3. 构建容器镜像
4. 将镜像推送到 Docker Hub

在开始动手实践之前，你需要了解以下几个核心概念。

### 容器镜像

如果你是容器镜像的新手，可以将其理解为包含运行应用所需的所有内容的标准化软件包，包括文件、配置和依赖项。这些软件包可以分发给其他人共享。

### Docker Hub

要分享你的 Docker 镜像，你需要一个存储它们的地方。这就是镜像仓库的作用。虽然有很多镜像仓库可供选择，但 Docker Hub 是镜像的默认首选仓库。Docker Hub 既为你提供了存储自己镜像的空间，也让你能够找到其他人发布的镜像，可以直接运行或用作自己镜像的基础。

在[使用容器进行开发](develop-with-containers.md)中，你使用了以下来自 Docker Hub 的镜像，它们都是 [Docker 官方镜像](/manuals/docker-hub/image-library/trusted-content.md#docker-official-images)：

- [node](https://hub.docker.com/_/node) - 提供 Node 环境，用作你开发工作的基础。这个镜像也被用作最终应用镜像的基础。
- [mysql](https://hub.docker.com/_/mysql) - 提供 MySQL 数据库，用于存储待办事项列表项
- [phpmyadmin](https://hub.docker.com/_/phpmyadmin) - 提供 phpMyAdmin，一个基于 Web 的 MySQL 数据库管理界面
- [traefik](https://hub.docker.com/_/traefik) - 提供 Traefik，一个现代的 HTTP 反向代理和负载均衡器，根据路由规则将请求路由到适当的容器

浏览 [Docker 官方镜像](https://hub.docker.com/search?badges=official)、[Docker 认证发布者](https://hub.docker.com/search?badges=verified_publisher) 和 [Docker 赞助的开源软件](https://hub.docker.com/search?badges=open_source) 的完整目录，了解更多可以运行和构建的内容。

## 动手实践

在本动手指南中，你将学习如何登录 Docker Hub 并将镜像推送到 Docker Hub 仓库。

## 使用你的 Docker 账户登录

要将镜像推送到 Docker Hub，你需要使用 Docker 账户登录。

1. 打开 Docker 仪表板。

2. 点击右上角的 **登录**。

3. 如果需要，请创建一个账户，然后完成登录流程。

完成后，你应该看到 **登录** 按钮变成了你的头像。

## 创建镜像仓库

现在你已经有了账户，可以创建一个镜像仓库。就像 Git 仓库保存源代码一样，镜像仓库存储容器镜像。

1. 访问 [Docker Hub](https://hub.docker.com)。

2. 点击 **创建仓库**。

3. 在 **创建仓库** 页面，输入以下信息：

    - **仓库名称** - `getting-started-todo-app`
    - **简短描述** - 如果需要，可以输入描述
    - **可见性** - 选择 **公开**，以便其他人可以拉取你定制的待办事项应用

4. 点击 **创建** 来创建仓库。

## 构建并推送镜像

现在你已经有了仓库，就可以构建并推送你的镜像了。需要注意的是，你正在构建的镜像是基于 Node 镜像的，这意味着你不需要安装或配置 Node、yarn 等。你只需专注于让你的应用变得独特。

> **什么是镜像/Dockerfile？**
>
> 暂时不用深入了解，可以将容器镜像理解为包含运行某个进程所需的所有内容的单一软件包。在本例中，它将包含 Node 环境、后端代码和编译后的 React 代码。
>
> 任何运行使用该镜像的容器的机器，都能够运行这个应用，就像它是被构建的一样，而无需在机器上预先安装任何其他东西。
>
> `Dockerfile` 是一个基于文本的脚本，提供了构建镜像的指令集。在这个快速入门中，仓库已经包含了 Dockerfile。

{{< tabs group="cli-or-vs-code" persist=true >}}
{{< tab name="CLI" >}}

1. 要开始，可以将项目克隆或[以 ZIP 文件的形式下载](https://github.com/docker/getting-started-todo-app/archive/refs/heads/main.zip)到本地机器。

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

    例如，如果你的 Docker 用户名是 `mobydock`，你可以运行以下命令：

    ```console
    $ docker build -t mobydock/getting-started-todo-app .
    ```

3. 要验证镜像是否已在本地存在，可以使用 `docker image ls` 命令：

    ```console
    $ docker image ls
    ```

    你会看到类似以下的输出：

    ```console
    REPOSITORY                          TAG       IMAGE ID       CREATED          SIZE
    mobydock/getting-started-todo-app   latest    1543656c9290   2 minutes ago    1.12GB
    ...
    ```

4. 要推送镜像，请使用 `docker push` 命令。确保将 `DOCKER_USERNAME` 替换为你的用户名：

    ```console
    $ docker push <DOCKER_USERNAME>/getting-started-todo-app
    ```

    根据你的上传速度，这可能需要一点时间。

{{< /tab >}}
{{< tab name="VS Code" >}}

1. 打开 Visual Studio Code。确保你已经从[扩展市场](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)安装了 **VS Code 的 Docker 扩展**。

   ![VS Code 扩展市场的截图](images/install-docker-extension.webp)

2. 在 **文件** 菜单中，选择 **打开文件夹**。选择 **克隆 Git 仓库** 并粘贴这个 URL：[https://github.com/docker/getting-started-todo-app](https://github.com/docker/getting-started-todo-app)

    ![显示如何克隆仓库的 VS Code 截图](images/clone-the-repo.webp?border=true)

3. 右键点击 `Dockerfile`，选择 **构建镜像...** 菜单项。

    ![显示右键菜单和“构建镜像”菜单项的 VS Code 截图](images/build-vscode-menu-item.webp?border=true)

4. 在出现的对话框中，输入名称 `DOCKER_USERNAME/getting-started-todo-app`，将 `DOCKER_USERNAME` 替换为你的 Docker 用户名。

5. 按下 **Enter** 后，你会看到一个终端出现，构建过程将在其中进行。完成后，可以关闭终端。

6. 通过点击左侧导航菜单中的 Docker 图标，打开 VS Code 的 Docker 扩展。

7. 找到你创建的镜像。它的名称将是 `docker.io/DOCKER_USERNAME/getting-started-todo-app`。

8. 展开镜像以查看镜像的标签（或不同版本）。你应该会看到一个名为 `latest` 的标签，这是镜像的默认标签。

9. 右键点击 **latest** 项，选择 **推送...** 选项。

    ![显示 Docker 扩展和右键菜单以推送镜像的截图](images/build-vscode-push-image.webp)

10. 按下 **Enter** 确认，然后观察你的镜像被推送到 Docker Hub。根据你的上传速度，这可能需要一点时间。

    上传完成后，可以关闭终端。

{{< /tab >}}
{{< /tabs >}}

## 总结

在继续之前，花点时间回顾一下这里发生的事情。在短短几分钟内，你就成功构建了一个打包你应用的容器镜像，并将其推送到了 Docker Hub。

今后，请记住以下几点：

- Docker Hub 是查找可信内容的最佳仓库。Docker 提供了一系列可信内容，包括 Docker 官方镜像、Docker 认证发布者和 Docker 赞助的开源软件，你可以直接使用或用作自己镜像的基础。

- Docker Hub 提供了一个分发你自己应用的市场。任何人都可以创建账户并分发镜像。虽然你公开分发了你创建的镜像，但私有仓库可以确保你的镜像只能被授权用户访问。

> **其他仓库的使用**
>
> 虽然 Docker Hub 是默认仓库，但仓库是通过 [开放容器倡议](https://opencontainers.org/) 实现标准化和互操作的。这使得公司和组织可以运行自己的私有仓库。通常，可信内容会从 Docker Hub 镜像（或复制）到这些私有仓库中。

## 下一步

现在你已经构建了一个镜像，是时候讨论为什么作为开发者你应该更多地了解 Docker，以及它将如何帮助你的日常任务。

{{< button text="下一步" url="whats-next" >}}