# 多容器应用程序




## 说明

启动单容器应用程序很容易。例如，执行特定数据处理任务的 Python 脚本可以在包含其所有依赖项的容器中运行。同样，提供静态网站和小型 API 端点的 Node.js 应用程序也可以有效地容器化，并包含其所有必要的库和依赖项。然而，随着应用程序规模的增长，将它们作为单独的容器进行管理会变得更加困难。

想象一下，数据处理 Python 脚本需要连接到数据库。突然之间，您现在不仅要管理脚本，还要在同一容器中管理数据库服务器。如果脚本需要用户登录，您将需要一个身份验证机制，这将进一步增加容器的大小。

容器的一个最佳实践是每个容器应该只做一件事，并且要做好。虽然这条规则也有例外，但要避免让一个容器做多个事情的倾向。

现在您可能会问：“我需要分别运行这些容器吗？如果我分别运行它们，如何将它们全部连接在一起？”

虽然 `docker run` 是启动容器的便捷工具，但随着应用程序堆栈的增长，使用它进行管理会变得困难。原因如下：

- 想象一下，在开发、测试和生产环境中，您需要运行多个带有不同配置的 `docker run` 命令（前端、后端和数据库）。这很容易出错且耗时。
- 应用程序通常相互依赖。随着堆栈的扩展，手动按特定顺序启动容器并管理网络连接会变得困难。
- 每个应用程序都需要其 `docker run` 命令，这使得扩展单个服务变得困难。扩展整个应用程序可能意味着在不需要提升的组件上浪费资源。
- 为每个应用程序保留数据需要在每个 `docker run` 命令中进行单独的数据卷挂载或配置。这会造成数据管理方法的分散。
- 通过单独的 `docker run` 命令为每个应用程序设置环境变量既繁琐又容易出错。

这就是 Docker Compose 的用武之地。

Docker Compose 在一个名为 `compose.yml` 的 YAML 文件中定义整个多容器应用程序。该文件指定所有容器的配置、它们的依赖项、环境变量，甚至是数据卷和网络。使用 Docker Compose：

- 您不需要运行多个 `docker run` 命令。您只需要在一个 YAML 文件中定义整个多容器应用程序。这可以集中配置并简化管理。
- 您可以按特定顺序运行容器并轻松管理网络连接。
- 您可以在多容器设置中轻松扩展或缩减单个服务。这允许根据实时需求进行高效分配。
- 您可以轻松实现持久化数据卷。
- 在 Docker Compose 文件中设置环境变量很容易。

通过利用 Docker Compose 运行多容器设置，您可以构建具有模块化、可扩展性和一致性的复杂应用程序。

## 动手实践

在本实践指南中，您将首先了解如何使用 `docker run` 命令构建和运行基于 Node.js 的计数器 Web 应用程序、Nginx 反向代理和 Redis 数据库。您还将了解如何使用 Docker Compose 简化整个部署过程。

### 设置

1. 获取示例应用程序。如果您有 Git，可以克隆示例应用程序的仓库。否则，您可以下载示例应用程序。选择以下选项之一。

   **使用 git 克隆**



   在终端中使用以下命令克隆示例应用程序仓库。

   ```console
   $ git clone https://github.com/dockersamples/nginx-node-redis
   ```
   
   导航到 `nginx-node-redis` 目录：

   ```console
   $ cd nginx-node-redis
   ```

   在此目录中，您将找到两个子目录 - `nginx` 和 `web`。
   

   **下载**



   下载源代码并解压。

   [下载源代码](https://github.com/dockersamples/nginx-node-redis/archive/refs/heads/main.zip)



   导航到 `nginx-node-redis-main` 目录：

   ```console
   $ cd nginx-node-redis-main
   ```

   在此目录中，您将找到两个子目录 - `nginx` 和 `web`。

   


2. [下载并安装](/get-started/get-docker.md) Docker Desktop。

### 构建镜像

1. 导航到 `nginx` 目录，运行以下命令构建镜像：

    ```console
    $ docker build -t nginx .
    ```

2. 导航到 `web` 目录，运行以下命令构建第一个 Web 镜像：
    
    ```console
    $ docker build -t web .
    ```

### 运行容器

1. 在运行多容器应用程序之前，您需要为它们创建一个网络以便通信。您可以使用 `docker network create` 命令：

    ```console
    $ docker network create sample-app
    ```

2. 运行以下命令启动 Redis 容器，将其连接到先前创建的网络并创建网络别名（对 DNS 查找很有用）：

    ```console
    $ docker run -d  --name redis --network sample-app --network-alias redis redis
    ```

3. 运行以下命令启动第一个 Web 容器：

    ```console
    $ docker run -d --name web1 -h web1 --network sample-app --network-alias web1 web
    ```

4. 运行以下命令启动第二个 Web 容器：

    ```console
    $ docker run -d --name web2 -h web2 --network sample-app --network-alias web2 web
    ```
    
5. 运行以下命令启动 Nginx 容器：

    ```console
    $ docker run -d --name nginx --network sample-app  -p 80:80 nginx
    ```

     > [!NOTE]
     >
     > Nginx 通常用作 Web 应用程序的反向代理，将流量路由到后端服务器。在本例中，它路由到 Node.js 后端容器（web1 或 web2）。


6. 运行以下命令验证容器是否已启动：

    ```console
    $ docker ps
    ```

    您将看到类似以下的输出： 

    ```text
    CONTAINER ID   IMAGE     COMMAND                  CREATED              STATUS              PORTS                NAMES
    2cf7c484c144   nginx     "/docker-entrypoint.…"   9 seconds ago        Up 8 seconds        0.0.0.0:80->80/tcp   nginx
    7a070c9ffeaa   web       "docker-entrypoint.s…"   19 seconds ago       Up 18 seconds                            web2
    6dc6d4e60aaf   web       "docker-entrypoint.s…"   34 seconds ago       Up 33 seconds                            web1
    008e0ecf4f36   redis     "docker-entrypoint.s…"   About a minute ago   Up About a minute   6379/tcp             redis
    ```

7. 如果您查看 Docker Desktop 仪表板，可以看到容器并深入了解其配置。

   ![显示多容器应用程序的 Docker Desktop 仪表板屏幕截图](images/multi-container-apps.webp?w=5000&border=true)

8. 一切正常运行后，您可以在浏览器中打开 [http://localhost](http://localhost) 查看网站。刷新页面几次，查看处理请求的主机和请求总数：

    ```console
    web2: Number of visits is: 9
    web1: Number of visits is: 10
    web2: Number of visits is: 11
    web1: Number of visits is: 12
    ```

> [!NOTE]
>
> 您可能已经注意到，Nginx 作为反向代理，可能会以轮询的方式在两个后端容器之间分配传入的请求。这意味着每个请求可能会轮流被定向到不同的容器（web1 和 web2）。输出显示 web1 和 web2 容器的计数器值连续递增，而 Redis 中存储的实际计数器值仅在响应发送回客户端后才会更新。

9. 您可以使用 Docker Desktop Dashboard 删除容器：选择容器，然后点击 **Delete** 按钮。

   ![Docker Desktop Dashboard 截图，展示如何删除多容器应用程序](images/delete-multi-container-apps.webp?border=true)

## 使用 Docker Compose 简化部署

Docker Compose 为管理多容器部署提供了一种结构化和简化的方法。如前所述，使用 Docker Compose 时，您无需运行多个 `docker run` 命令。您只需在一个名为 `compose.yml` 的 YAML 文件中定义整个多容器应用程序。让我们看看它是如何工作的。

导航到项目目录的根目录。在此目录中，您会找到一个名为 `compose.yml` 的文件。这个 YAML 文件就是实现所有功能的地方。它定义了构成应用程序的所有服务及其配置。每个服务都指定其镜像、端口、卷、网络以及任何其他必要的设置。

1. 使用 `docker compose up` 命令启动应用程序：

    ```console
    $ docker compose up -d --build
    ```

    运行此命令时，您应该会看到类似以下的输出：

    ```console
     ✔ Network nginx-node-redis_default   Created                                                                                                   0.0s
     ✔ Container nginx-node-redis-web2-1  Created                                                                                                   0.1s
     ✔ Container nginx-node-redis-web1-1  Created                                                                                                   0.1s
     ✔ Container nginx-node-redis-redis-1 Created                                                                                                   0.1s
     ✔ Container nginx-node-redis-nginx-1 Created
    ```

2. 如果您查看 Docker Desktop Dashboard，可以看到容器并深入了解其配置。

    ![Docker Desktop Dashboard 截图，展示使用 Docker Compose 部署的应用程序堆栈的容器](images/list-containers.webp?border=true)

3. 或者，您可以使用 Docker Desktop Dashboard 删除容器：选择应用程序堆栈，然后点击 **Delete** 按钮。

   ![Docker Desktop Dashboard 截图，展示如何删除使用 Docker Compose 部署的容器](images/delete-containers.webp?border=true)

在本指南中，您学习了与使用 `docker run`（容易出错且难以管理）相比，使用 Docker Compose 启动和停止多容器应用程序是多么简单。

## 其他资源

* [`docker container run` CLI 参考](reference/cli/docker/container/run/)
* [什么是 Docker Compose](/get-started/docker-concepts/the-basics/what-is-docker-compose/)
