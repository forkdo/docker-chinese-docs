---
title: 多容器应用程序
weight: 5
keywords: 概念, 构建, 镜像, 容器, docker desktop
description: 本概念页面将教你多容器应用程序的重要性，以及它与单容器应用程序的区别
aliases: 
 - /guides/docker-concepts/running-containers/multi-container-applications/
---

{{< youtube-embed 1jUwR6F9hvM >}}

## 说明

启动单容器应用程序很容易。例如，执行特定数据处理任务的 Python 脚本可以在包含所有依赖项的容器中运行。类似地，提供静态网站和小型 API 端点的 Node.js 应用程序可以使用所有必要的库和依赖项进行容器化。然而，随着应用程序规模的增长，将它们作为独立容器进行管理变得越来越困难。

想象一下，数据处理 Python 脚本需要连接到数据库。突然间，你不仅要管理脚本，还要在同一容器中管理数据库服务器。如果脚本需要用户登录，你还需要身份验证机制，这进一步增加了容器的体积。

容器的一个最佳实践是每个容器应该只做一件事，并且把它做好。虽然这条规则有例外，但要避免让一个容器做多件事的倾向。

现在你可能会问：“我需要分别运行这些容器吗？如果我分别运行它们，如何将它们连接在一起？”

虽然 `docker run` 是启动容器的便捷工具，但随着应用栈的增长，使用它来管理变得困难。原因如下：

- 想象一下，为开发、测试和生产环境运行多个 `docker run` 命令（前端、后端和数据库），每个都有不同的配置。这容易出错且耗时。
- 应用程序通常相互依赖。随着栈的扩展，手动按特定顺序启动容器并管理网络连接变得困难。
- 每个应用程序都需要自己的 `docker run` 命令，这使得扩展单个服务变得困难。扩展整个应用程序意味着可能浪费资源在不需要提升的组件上。
- 为每个应用程序持久化数据需要单独的卷挂载或每个 `docker run` 命令内的配置。这导致了分散的数据管理方法。
- 通过单独的 `docker run` 命令为每个应用程序设置环境变量是繁琐且容易出错的。

这就是 Docker Compose 挽救局面的地方。

Docker Compose 在一个名为 `compose.yml` 的 YAML 文件中定义你的整个多容器应用程序。此文件指定了所有容器的配置、依赖项、环境变量，甚至卷和网络。使用 Docker Compose：

- 你不需要运行多个 `docker run` 命令。你只需要在一个 YAML 文件中定义你的整个多容器应用程序。这集中了配置并简化了管理。
- 你可以按特定顺序运行容器并轻松管理网络连接。
- 你可以在多容器设置中简单地扩展单个服务。这允许根据实时需求进行高效分配。
- 你可以轻松实现持久卷。
- 在 Docker Compose 文件中设置一次环境变量很容易。

通过利用 Docker Compose 运行多容器设置，你可以构建以模块化、可扩展性和一致性为核心的高度复杂应用程序。

## 动手试试

在本实践指南中，你将首先看到如何使用 `docker run` 命令构建和运行基于 Node.js、Nginx 反向代理和 Redis 数据库的计数器 Web 应用程序。你还将看到如何使用 Docker Compose 简化整个部署过程。

### 设置

1. 获取示例应用程序。如果你有 Git，可以克隆示例应用程序的仓库。否则，你可以下载示例应用程序。选择以下选项之一。

   {{< tabs >}}
   {{< tab name="使用 git 克隆" >}}

   在终端中使用以下命令克隆示例应用程序仓库。

   ```console
   $ git clone https://github.com/dockersamples/nginx-node-redis
   ```
   
   导航到 `nginx-node-redis` 目录：

   ```console
   $ cd nginx-node-redis
   ```

   在此目录内，你会发现两个子目录 - `nginx` 和 `web`。
   

   {{< /tab >}}
   {{< tab name="下载" >}}

   下载源代码并解压。

   {{< button url="https://github.com/dockersamples/nginx-node-redis/archive/refs/heads/main.zip" text="下载源代码" >}}


   导航到 `nginx-node-redis-main` 目录：

   ```console
   $ cd nginx-node-redis-main
   ```

   在此目录内，你会发现两个子目录 - `nginx` 和 `web`。

   {{< /tab >}}
   {{< /tabs >}}


2. [下载并安装](/get-started/get-docker.md) Docker Desktop。

### 构建镜像


1. 导航到 `nginx` 目录，通过运行以下命令构建镜像：

    ```console
    $ docker build -t nginx .
    ```

2. 导航到 `web` 目录，运行以下命令构建第一个 Web 镜像：
    
    ```console
    $ docker build -t web .
    ```

### 运行容器

1. 在运行多容器应用程序之前，你需要创建一个网络供它们通信。你可以使用 `docker network create` 命令完成：

    ```console
    $ docker network create sample-app
    ```

2. 通过运行以下命令启动 Redis 容器，这将使其连接到之前创建的网络并创建一个网络别名（对 DNS 查找很有用）：

    ```console
    $ docker run -d  --name redis --network sample-app --network-alias redis redis
    ```

3. 通过运行以下命令启动第一个 Web 容器：

    ```console
    $ docker run -d --name web1 -h web1 --network sample-app --network-alias web1 web
    ```

4. 通过运行以下命令启动第二个 Web 容器：

    ```console
    $ docker run -d --name web2 -h web2 --network sample-app --network-alias web2 web
    ```
    
5. 通过运行以下命令启动 Nginx 容器：

    ```console
    $ docker run -d --name nginx --network sample-app  -p 80:80 nginx
    ```

     > [!NOTE]
     >
     > Nginx 通常用作 Web 应用程序的反向代理，将流量路由到后端服务器。在这种情况下，它路由到 Node.js 后端容器（web1 或 web2）。

6. 通过运行以下命令验证容器已启动：

    ```console
    $ docker ps
    ```

    你会看到类似以下的输出：

    ```text
    CONTAINER ID   IMAGE     COMMAND                  CREATED              STATUS              PORTS                NAMES
    2cf7c484c144   nginx     "/docker-entrypoint.…"   9 seconds ago        Up 8 seconds        0.0.0.0:80->80/tcp   nginx
    7a070c9ffeaa   web       "docker-entrypoint.s…"   19 seconds ago       Up 18 seconds                            web2
    6dc6d4e60aaf   web       "docker-entrypoint.s…"   34 seconds ago       Up 33 seconds                            web1
    008e0ecf4f36   redis     "docker-entrypoint.s…"   About a minute ago   Up About a minute   6379/tcp             redis
    ```

7. 如果查看 Docker Desktop 仪表板，你可以看到容器并深入了解其配置。

   ![Docker Desktop 仪表板显示多容器应用程序的截图](images/multi-container-apps.webp?w=5000&border=true)

8. 一切启动并运行后，你可以在浏览器中打开 [http://localhost](http://localhost) 查看网站。多次刷新页面以查看处理请求的主机和总请求数：

    ```console
    web2: Number of visits is: 9
    web1: Number of visits is: 10
    web2: Number of visits is: 11
    web1: Number of visits is: 12
    ```

    > [!NOTE]
    >
    > 你可能已经注意到，Nginx 作为反向代理，可能在两个后端容器之间以轮询方式分发传入请求。这意味着每个请求可能按轮换方式定向到不同的容器（web1 和 web2）。输出显示 web1 和 web2 容器的连续递增，实际存储在 Redis 中的计数器值仅在响应发送回客户端后更新。

9. 你可以使用 Docker Desktop 仪表板通过选择容器并选择 **删除** 按钮来删除容器。

   ![Docker Desktop 仪表板显示如何删除多容器应用程序的截图](images/delete-multi-container-apps.webp?border=true)
 
## 使用 Docker Compose 简化部署


Docker Compose 为管理多容器部署提供了结构化和简化的方法。如前所述，使用 Docker Compose，你不需要运行多个 `docker run` 命令。你只需要在一个名为 `compose.yml` 的 YAML 文件中定义你的整个多容器应用程序。让我们看看它是如何工作的。

导航到项目目录的根目录。在此目录内，你会发现一个名为 `compose.yml` 的文件。这个 YAML 文件是所有魔法发生的地方。它定义了构成你的应用程序的所有服务及其配置。每个服务指定其镜像、端口、卷、网络以及其功能所需的任何其他设置。

1. 使用 `docker compose up` 命令启动应用程序：

    ```console
    $ docker compose up -d --build
    ```

    当你运行此命令时，你应该看到类似以下的输出：

    ```console
    Running 5/5
    ✔ Network nginx-nodejs-redis_default    Created                                                0.0s
    ✔ Container nginx-nodejs-redis-web1-1   Started                                                0.1s
    ✔ Container nginx-nodejs-redis-redis-1  Started                                                0.1s
    ✔ Container nginx-nodejs-redis-web2-1   Started                                                0.1s
    ✔ Container nginx-nodejs-redis-nginx-1  Started
    ```

2. 如果查看 Docker Desktop 仪表板，你可以看到容器并深入了解其配置。

    ![Docker Desktop 仪表板显示使用 Docker Compose 部署的应用程序栈容器的截图](images/list-containers.webp?border=true)

3. 或者，你可以使用 Docker Desktop 仪表板通过选择应用程序栈并选择 **删除** 按钮来删除容器。

   ![Docker Desktop 仪表板显示如何删除使用 Docker Compose 部署的容器的截图](images/delete-containers.webp?border=true)

在本指南中，你了解到使用 Docker Compose 启动和停止多容器应用程序相比 `docker run` 是多么容易，后者容易出错且难以管理。

## 额外资源

* [`docker container run` CLI 参考](reference/cli/docker/container/run/)
* [什么是 Docker Compose](/get-started/docker-concepts/the-basics/what-is-docker-compose/)