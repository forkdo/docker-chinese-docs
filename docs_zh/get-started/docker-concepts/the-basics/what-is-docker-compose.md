---
title: 什么是 Docker Compose？
weight: 40
keywords: 概念, 构建, 镜像, 容器, docker desktop
description: 什么是 Docker Compose？
aliases:
 - /guides/walkthroughs/multi-container-apps/
 - /guides/docker-concepts/the-basics/what-is-docker-compose/
---

{{< youtube-embed xhcUIK4fGtY >}}

## 说明

如果你一直在跟进前面的指南，那么你一直在使用单容器应用程序。但现在你想要做一些更复杂的事情——运行数据库、消息队列、缓存，或者其他各种服务。你会把所有东西都安装在一个容器里吗？还是运行多个容器？如果你运行多个容器，那它们之间如何连接？

容器的一个最佳实践是：每个容器应该只做一件事，并且把它做好。虽然这个规则有例外，但要避免让一个容器做多件事的倾向。

你可以使用多个 `docker run` 命令来启动多个容器。但很快你就会意识到，你需要管理网络、所有连接容器到网络所需的标志，以及更多内容。而且完成之后，清理工作也会更复杂一些。

使用 Docker Compose，你可以将所有容器及其配置定义在一个 YAML 文件中。如果你将此文件包含在代码仓库中，那么任何克隆你仓库的人都可以通过一个命令快速启动并运行。

重要的是要理解，Compose 是一个声明式工具——你只需定义，然后执行。你并不总是需要从头开始重建所有内容。如果你做了更改，再次运行 `docker compose up`，Compose 会智能地协调你文件中的更改并应用它们。

> **Dockerfile 与 Compose 文件**
>
> Dockerfile 提供构建容器镜像的指令，而 Compose 文件定义你运行中的容器。通常，Compose 文件会引用一个 Dockerfile 来为特定服务构建镜像。

## 动手尝试

在这个实践中，你将学习如何使用 Docker Compose 运行一个多容器应用程序。你将使用一个用 Node.js 构建的待办事项列表应用，并使用 MySQL 作为数据库服务器。

### 启动应用程序

按照以下说明在你的系统上运行待办事项列表应用。

1. [下载并安装](https://www.docker.com/products/docker-desktop/) Docker Desktop。
2. 打开终端，[克隆这个示例应用](https://github.com/dockersamples/todo-list-app)。

    ```console
    git clone https://github.com/dockersamples/todo-list-app 
    ```

3. 导航到 `todo-list-app` 目录：

    ```console
    cd todo-list-app
    ```

    在此目录中，你会找到一个名为 `compose.yaml` 的文件。这个 YAML 文件就是所有魔法发生的地方！它定义了构成你应用程序的所有服务及其配置。每个服务都指定了其镜像、端口、卷、网络，以及其功能所需的任何其他设置。花点时间探索这个 YAML 文件，熟悉其结构。

4. 使用 [`docker compose up`](/reference/cli/docker/compose/up/) 命令启动应用程序：

    ```console
    docker compose up -d --build
    ```

    当你运行此命令时，你应该会看到类似以下的输出：

    ```console
    [+] Running 5/5
    ✔ app 3 layers [⣿⣿⣿]      0B/0B            Pulled          7.1s
      ✔ e6f4e57cc59e Download complete                          0.9s
      ✔ df998480d81d Download complete                          1.0s
      ✔ 31e174fedd23 Download complete                          2.5s
      ✔ 43c47a581c29 Download complete                          2.0s
    [+] Running 4/4
      ⠸ Network todo-list-app_default           Created         0.3s
      ⠸ Volume "todo-list-app_todo-mysql-data"  Created         0.3s
      ✔ Container todo-list-app-app-1           Started         0.3s
      ✔ Container todo-list-app-mysql-1         Started         0.3s
    ```

    这里发生了许多事情！有几点值得注意：

    - 两个容器镜像从 Docker Hub 下载——node 和 MySQL
    - 为你的应用程序创建了一个网络
    - 创建了一个卷以在容器重启之间持久化数据库文件
    - 启动了两个容器及其所有必要配置

    如果这让你感到不知所措，别担心！你会适应的！

5. 现在一切已启动并运行，你可以在浏览器中打开 [http://localhost:3000](http://localhost:3000) 查看网站。注意，应用程序可能需要 10-15 秒才能完全启动。如果页面没有立即加载，请稍等片刻并刷新。随意添加待办事项、标记完成并删除它们。

    ![A screenshot of a webpage showing the todo-list application running on port 3000](images/todo-list-app.webp?border=true&w=950&h=400)

6. 如果你查看 Docker Desktop GUI，你可以看到容器并深入了解其配置。

    ![A screenshot of Docker Desktop dashboard showing the list of containers running todo-list app](images/todo-list-containers.webp?border=true&w=950&h=400)


### 拆除应用

由于此应用程序是使用 Docker Compose 启动的，因此在完成后很容易将其全部拆除。

1. 在 CLI 中，使用 [`docker compose down`](/reference/cli/docker/compose/down/) 命令删除所有内容：

    ```console
    docker compose down
    ```

    你会看到类似以下的输出：

    ```console
    [+] Running 3/3
    ✔ Container todo-list-app-mysql-1  Removed        2.9s
    ✔ Container todo-list-app-app-1    Removed        0.1s
    ✔ Network todo-list-app_default    Removed        0.1s
    ```

    > **卷持久化**
    >
    > 默认情况下，当你拆除 Compose 栈时，卷 _不会_ 自动删除。其想法是，如果你再次启动栈，你可能需要这些数据。
    >
    > 如果你确实想删除卷，可以在运行 `docker compose down` 命令时添加 `--volumes` 标志：
    >
    > ```console
    > docker compose down --volumes
    > [+] Running 1/0
    > ✔ Volume todo-list-app_todo-mysql-data  Removed
    > ```

2. 或者，你可以使用 Docker Desktop GUI 通过选择应用程序栈并点击 **删除** 按钮来删除容器。

    ![A screenshot of the Docker Desktop GUI showing the containers view with an arrow pointing to the "Delete" button](images/todo-list-delete.webp?w=930&h=400)

    > **使用 GUI 管理 Compose 栈**
    >
    > 请注意，如果你在 GUI 中删除 Compose 应用的容器，它只会删除容器。如果你想删除，你必须手动删除网络和卷。

在这个演练中，你学习了如何使用 Docker Compose 启动和停止一个多容器应用程序。


## 额外资源

本页面是对 Compose 的简要介绍。在以下资源中，你可以更深入地了解 Compose 以及如何编写 Compose 文件。


* [Docker Compose 概述](/compose/)
* [Docker Compose CLI 概述](/compose/reference/)
* [Compose 如何工作](/compose/intro/compose-application-model/)