---
description: 了解如何开始使用 Docker Hub
keywords: Docker Hub, 推送镜像, 拉取镜像, 仓库
title: Docker Hub 快速入门
linkTitle: 快速入门
weight: 10
---

Docker Hub 提供了庞大的预构建镜像和资源库，可加速开发工作流并减少设置时间。你可以基于 Docker Hub 中的预构建镜像进行开发，然后使用仓库与团队或数百万其他开发者共享和分发你自己的镜像。

本指南将向你展示如何查找和运行预构建镜像。然后，它将引导你创建自定义镜像并通过 Docker Hub 共享它。

## 前置条件

- [下载并安装 Docker](../../get-started/get-docker.md)
- [创建 Docker 账户](https://app.docker.com/signup)

## 步骤 1：在 Docker Hub 库中查找镜像

你可以在 Docker Hub 本身、Docker Desktop 仪表板或通过 CLI 中搜索内容。

在 Docker Hub 中搜索或浏览内容：

{{< tabs >}}
{{< tab name="Docker Hub" >}}

1. 导航到 [Docker Hub 探索页面](https://hub.docker.com/explore)。

   在 **探索** 页面，你可以按目录或类别浏览，或使用搜索快速找到内容。

2. 在 **类别** 下，选择 **Web 服务器**。

   结果显示后，你可以使用页面左侧的过滤器进一步筛选结果。

3. 在过滤器中，选择 **Docker 官方镜像**。

   按可信内容过滤可确保你只看到由 Docker 和验证发布合作伙伴策划的高质量、安全的镜像。

4. 在结果中，选择 **nginx** 镜像。

   选择镜像将打开镜像的页面，你可以在其中了解如何使用该镜像。在页面上，你还会找到 `docker pull` 命令来拉取镜像。

{{< /tab >}}
{{< tab name="Docker Desktop" >}}

1. 打开 Docker Desktop 仪表板。
2. 选择 **Docker Hub** 视图。

   在 **Docker Hub** 视图中，你可以按目录或类别浏览，或使用搜索快速找到内容。

3. 保持搜索框为空，然后选择 **搜索**。

   搜索结果会显示在搜索框旁边，现在有额外的过滤器。

4. 选择搜索过滤器图标，然后选择 **Docker 官方镜像** 和 **Web 服务器**。
5. 在结果中，选择 **nginx** 镜像。

{{< /tab >}}
{{< tab name="CLI" >}}

1. 打开终端窗口。

   > [!TIP]
   >
   > Docker Desktop 仪表板包含一个内置终端。在仪表板底部，选择 **>_ 终端** 打开它。

2. 在终端中，运行以下命令。

   ```console
   $ docker search --filter is-official=true nginx
   ```

   与 Docker Hub 和 Docker Desktop 界面不同，你无法使用 `docker search` 命令按类别浏览。有关该命令的更多详细信息，请参阅 [docker search](/reference/cli/docker/search/)。

{{< /tab >}}
{{< /tabs >}}

现在你已经找到了一个镜像，是时候将它拉取并在你的设备上运行了。

## 步骤 2：从 Docker Hub 拉取并运行镜像

你可以使用 CLI 或 Docker Desktop 仪表板从 Docker Hub 运行镜像。

{{< tabs >}}
{{< tab name="Docker Desktop" >}}

1. 在 Docker Desktop 仪表板中，选择 **Docker Hub** 视图中的 **nginx** 镜像。详细信息请参阅 [步骤 1：在 Docker Hub 库中查找镜像](#步骤-1在-docker-hub-库中查找镜像)。

2. 在 **nginx** 屏幕上，选择 **运行**。

   如果镜像在你的设备上不存在，它会自动从 Docker Hub 拉取。根据你的连接情况，拉取镜像可能需要几秒或几分钟。镜像拉取后，Docker Desktop 中会弹出一个窗口，你可以指定运行选项。

3. 在 **主机端口** 选项中，指定 `8080`。
4. 选择 **运行**。

   容器启动后会显示容器日志。

5. 选择 **8080:80** 链接打开服务器，或在浏览器中访问 [http://localhost:8080](http://localhost:8080)。

6. 在 Docker Desktop 仪表板中，选择 **停止** 按钮停止容器。

{{< /tab >}}
{{< tab name="CLI" >}}

1. 打开终端窗口。

   > [!TIP]
   >
   > Docker Desktop 仪表板包含一个内置终端。在仪表板底部，选择 **>_ 终端** 打开它。

2. 在终端中，运行以下命令拉取并运行 Nginx 镜像。

   ```console
   $ docker run -p 8080:80 --rm nginx
   ```

   `docker run` 命令会自动拉取并运行镜像，无需先运行 `docker pull`。要了解有关该命令及其选项的更多信息，请参阅 [`docker run` CLI 参考](../../reference/cli/docker/container/run.md)。运行该命令后，你应该看到类似以下的输出。

   ```console {collapse=true}
   Unable to find image 'nginx:latest' locally
   latest: Pulling from library/nginx
   a480a496ba95: Pull complete
   f3ace1b8ce45: Pull complete
   11d6fdd0e8a7: Pull complete
   f1091da6fd5c: Pull complete
   40eea07b53d8: Pull complete
   6476794e50f4: Pull complete
   70850b3ec6b2: Pull complete
   Digest: sha256:28402db69fec7c17e179ea87882667f1e054391138f77ffaf0c3eb388efc3ffb
   Status: Downloaded newer image for nginx:latest
   /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
   /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
   /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
   10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
   10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
   /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
   /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
   /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
   /docker-entrypoint.sh: Configuration complete; ready for start up
   2024/11/07 21:43:41 [notice] 1#1: using the "epoll" event method
   2024/11/07 21:43:41 [notice] 1#1: nginx/1.27.2
   2024/11/07 21:43:41 [notice] 1#1: built by gcc 12.2.0 (Debian 12.2.0-14)
   2024/11/07 21:43:41 [notice] 1#1: OS: Linux 6.10.11-linuxkit
   2024/11/07 21:43:41 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
   2024/11/07 21:43:41 [notice] 1#1: start worker processes
   2024/11/07 21:43:41 [notice] 1#1: start worker process 29
   ...
   ```

3. 访问 [http://localhost:8080](http://localhost:8080) 查看默认的 Nginx 页面，验证容器正在运行。

4. 在终端中，按 <kdb>Ctrl+C</kbd> 停止容器。

{{< /tab >}}
{{< /tabs >}}

现在你已经运行了一个 Web 服务器，无需任何设置或配置。Docker Hub 提供对预构建、即用型容器镜像的即时访问，让你可以快速拉取和运行应用程序，而无需手动安装或配置软件。借助 Docker Hub 庞大的镜像库，你可以轻松地试验和部署应用程序，提高生产力，并轻松尝试新工具、设置开发环境或在现有软件基础上构建。

你也可以扩展 Docker Hub 中的镜像，让你能够快速构建和自定义自己的镜像以满足特定需求。

## 步骤 3：构建并推送镜像到 Docker Hub

1. 创建一个 [Dockerfile](/reference/dockerfile.md) 来指定你的应用程序：

   ```dockerfile
   FROM nginx
   RUN echo "<h1>Hello world from Docker!</h1>" > /usr/share/nginx/html/index.html
   ```

   这个 Dockerfile 扩展了 Docker Hub 中的 Nginx 镜像，创建一个简单的网站。只需几行代码，你就可以轻松设置、自定义和共享一个静态网站。

2. 运行以下命令构建你的镜像。将 `<YOUR-USERNAME>` 替换为你的 Docker ID。

   ```console
   $ docker build -t <YOUR-USERNAME>/nginx-custom .
   ```

   此命令构建你的镜像并标记它，以便 Docker 知道将其推送到 Docker Hub 中的哪个仓库。要了解有关该命令及其选项的更多信息，请参阅 [`docker build` CLI 参考](../../reference/cli/docker/buildx/build.md)。运行该命令后，你应该看到类似以下的输出。

   ```console {collapse=true}
   [+] Building 0.6s (6/6) FINISHED                      docker:desktop-linux
    => [internal] load build definition from Dockerfile                  0.0s
    => => transferring dockerfile: 128B                                  0.0s
    => [internal] load metadata for docker.io/library/nginx:latest       0.0s
    => [internal] load .dockerignore                                     0.0s
    => => transferring context: 2B                                       0.0s
    => [1/2] FROM docker.io/library/nginx:latest                         0.1s
    => [2/2] RUN echo "<h1>Hello world from Docker!</h1>" > /usr/share/  0.2s
    => exporting to image                                                0.1s
    => => exporting layers                                               0.0s
    => => writing image sha256:f85ab68f4987847713e87a95c39009a5c9f4ad78  0.0s
    => => naming to docker.io/mobyismyname/nginx-custom                  0.0s
   ```

3. 运行以下命令测试你的镜像。将 `<YOUR-USERNAME>` 替换为你的 Docker ID。

   ```console
   $ docker run -p 8080:80 --rm <YOUR-USERNAME>/nginx-custom
   ```

4. 访问 [http://localhost:8080](http://localhost:8080) 查看页面。你应该看到 `Hello world from Docker!`。

5. 在终端中，按 CTRL+C 停止容器。

6. 登录 Docker Desktop。在将镜像推送到 Docker Hub 之前，你必须先登录。

7. 运行以下命令将你的镜像推送到 Docker Hub。将 `<YOUR-USERNAME>` 替换为你的 Docker ID。

   ```console
   $ docker push <YOUR-USERNAME>/nginx-custom
   ```

    > [!NOTE]
    >
    > 你必须通过 Docker Desktop 或命令行登录 Docker Hub，并且还必须正确命名你的镜像，如上述步骤所示。

   该命令将镜像推送到 Docker Hub，并在仓库不存在时自动创建仓库。要了解有关该命令的更多信息，请参阅 [`docker push` CLI 参考](../../reference/cli/docker/image/push.md)。运行该命令后，你应该看到类似以下的输出。

   ```console {collapse=true}
   Using default tag: latest
   The push refers to repository [docker.io/mobyismyname/nginx-custom]
   d0e011850342: Pushed
   e4e9e9ad93c2: Mounted from library/nginx
   6ac729401225: Mounted from library/nginx
   8ce189049cb5: Mounted from library/nginx
   296af1bd2844: Mounted from library/nginx
   63d7ce983cd5: Mounted from library/nginx
   b33db0c3c3a8: Mounted from library/nginx
   98b5f35ea9d3: Mounted from library/nginx
   latest: digest: sha256:7f5223ae866e725a7f86b856c30edd3b86f60d76694df81d90b08918d8de1e3f size: 1985
   ```

  现在你已经创建了一个仓库并推送了你的镜像，是时候查看你的仓库并探索其选项了。

## 步骤 4：在 Docker Hub 上查看你的仓库并探索选项

你可以在 Docker Hub 或 Docker Desktop 界面中查看你的 Docker Hub 仓库。

{{< tabs >}}
{{< tab name="Docker Hub" >}}

1. 访问 [Docker Hub](https://hub.docker.com) 并登录。

   登录后，你应该在 **仓库** 页面。如果没有，请转到 [**仓库**](https://hub.docker.com/repositories/) 页面。

2. 找到 **nginx-custom** 仓库并选择该行。

   选择仓库后，你应该看到更多关于你的仓库的详细信息和选项。

{{< /tab >}}
{{< tab name="Docker Desktop" >}}

1. 登录 Docker Desktop。
2. 选择 **镜像** 视图。
3. 选择 **Hub 仓库** 选项卡。

   你的 Docker Hub 仓库列表会出现。

4. 找到 **nginx-custom** 仓库，将鼠标悬停在行上，然后选择 **在 Hub 中查看**。

   Docker Hub 会打开，你可以查看镜像的更多详细信息。

{{< /tab >}}
{{< /tabs >}}

现在你已经验证了你的仓库存在于 Docker Hub 上，并且你发现了更多选项。查看下一步以了解这些选项的更多信息。

## 下一步

添加 [仓库信息](./repos/manage/information.md) 以帮助用户查找和使用你的镜像。