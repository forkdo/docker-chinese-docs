---
description: 了解如何开始使用 Docker Hub
keywords: Docker Hub, push image, pull image, repositories
title: Docker Hub 快速入门
linkTitle: 快速入门
weight: 10
---

Docker Hub 提供了大量预构建的镜像和资源，可加快开发工作流程并减少设置时间。您可以基于 Docker Hub 中的预构建镜像进行构建，然后使用仓库与团队或数百万其他开发者共享和分发您自己的镜像。

本指南将向您展示如何查找并运行预构建镜像。然后，指导您创建自定义镜像并通过 Docker Hub 共享。

## 先决条件

- [下载并安装 Docker](../../get-started/get-docker.md)
- 已验证的 [Docker](https://app.docker.com/signup) 账户

## 第 1 步：在 Docker Hub 库中查找镜像

您可以直接在 Docker Hub 中搜索内容，在 Docker Desktop 仪表板中搜索，或使用 CLI 搜索。

要在 Docker Hub 上搜索或浏览内容：

{{< tabs >}}
{{< tab name="Docker Hub" >}}

1. 导航至 [Docker Hub 探索页面](https://hub.docker.com/explore)。

   在 **探索** 页面上，您可以按目录或类别浏览，或使用搜索功能快速查找内容。

2. 在 **类别** 下，选择 **Web 服务器**。

   显示结果后，您可以使用页面左侧的筛选器进一步筛选结果。

3. 在筛选器中，选择 **Docker 官方镜像**。

   按可信内容筛选可确保您只看到由 Docker 精选和已验证发布合作伙伴提供的高质量、安全镜像。

4. 在结果中，选择 **nginx** 镜像。

   选择镜像将打开镜像页面，您可以在其中了解有关如何使用该镜像的更多信息。在页面上，您还会找到用于拉取镜像的 `docker pull` 命令。

{{< /tab >}}
{{< tab name="Docker Desktop" >}}

1. 打开 Docker Desktop 仪表板。
2. 选择 **Docker Hub** 视图。

   在 **Docker Hub** 视图中，您可以按目录或类别浏览，或使用搜索功能快速查找内容。

3. 保持搜索框为空，然后选择 **搜索**。

   搜索结果将显示出来，现在搜索框旁边还有额外的筛选器。

4. 选择搜索筛选器图标，然后选择 **Docker 官方镜像** 和 **Web 服务器**。
5. 在结果中，选择 **nginx** 镜像。

{{< /tab >}}
{{< tab name="CLI" >}}

1. 打开终端窗口。

   > [!TIP]
   >
   > Docker Desktop 仪表板包含一个内置终端。在仪表板底部，选择 **>_ 终端** 将其打开。

2. 在终端中，运行以下命令。

   ```console
   $ docker search --filter is-official=true nginx
   ```

   与 Docker Hub 和 Docker Desktop 界面不同，您无法使用 `docker search` 命令按类别浏览。有关该命令的更多详细信息，请参阅 [docker search](/reference/cli/docker/search/)。

{{< /tab >}}
{{< /tabs >}}

现在您已找到镜像，是时候将其拉取并运行到您的设备上了。

## 第 2 步：从 Docker Hub 拉取并运行镜像

您可以使用 CLI 或 Docker Desktop 仪表板从 Docker Hub 运行镜像。

{{< tabs >}}
{{< tab name="Docker Desktop" >}}

1. 在 Docker Desktop 仪表板中，选择 **Docker Hub** 视图中的 **nginx** 镜像。有关更多详细信息，请参阅 [第 1 步：在 Docker Hub 库中查找镜像](#step-1-find-an-image-in-docker-hubs-library)。

2. 在 **nginx** 屏幕上，选择 **运行**。

   如果镜像在您的设备上不存在，它会自动从 Docker Hub 拉取。根据您的连接速度，拉取镜像可能需要几秒钟或几分钟。镜像拉取完成后，Docker Desktop 中会出现一个窗口，您可以指定运行选项。

3. 在 **主机端口** 选项中，指定 `8080`。
4. 选择 **运行**。

   容器启动后，容器日志将出现。

5. 选择 **8080:80** 链接以打开服务器，或在 Web 浏览器中访问 [http://localhost:8080](http://localhost:8080)。

6. 在 Docker Desktop 仪表板中，选择 **停止** 按钮以停止容器。

{{< /tab >}}
{{< tab name="CLI" >}}

1. 打开终端窗口。

   > [!TIP]
   >
   > Docker Desktop 仪表板包含一个内置终端。在仪表板底部，选择 **>_ 终端** 将其打开。

2. 在终端中，运行以下命令以拉取并运行 Nginx 镜像。

   ```console
   $ docker run -p 8080:80 --rm nginx
   ```

   `docker run` 命令会自动拉取并运行镜像，无需先运行 `docker pull`。要了解有关该命令及其选项的更多信息，请参阅 [`docker run` CLI 参考](../../reference/cli/docker/container/run.md)。运行命令后，您应该会看到类似以下的输出。

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

3. 访问 [http://localhost:8080](http://localhost:8080) 查看默认 Nginx 页面并验证容器是否正在运行。

4. 在终端中，按 <kbd>Ctrl+C</kbd> 停止容器。

{{< /tab >}}
{{< /tabs >}}

您现在无需任何设置或配置就运行了一个 Web 服务器。Docker Hub 提供对预构建、即用型容器镜像的即时访问，让您无需手动安装或配置软件即可快速拉取和运行应用程序。借助 Docker Hub 庞大的镜像库，您可以轻松实验和部署应用程序，提高生产力，并轻松试用新工具、设置开发环境或基于现有软件进行构建。

您还可以扩展 Docker Hub 中的镜像，让您快速构建和自定义自己的镜像以满足特定需求。

## 第 3 步：构建镜像并推送到 Docker Hub

1. 创建一个 [Dockerfile](/reference/dockerfile.md) 来指定您的应用程序：

   ```dockerfile
   FROM nginx
   RUN echo "<h1>Hello world from Docker!</h1>" > /usr/share/nginx/html/index.html
   ```

   此 Dockerfile 扩展了 Docker Hub 中的 Nginx 镜像以创建一个简单的网站。只需几行代码，您就可以使用 Docker 轻松设置、自定义和共享静态网站。

2. 运行以下命令来构建您的镜像。将 `<YOUR-USERNAME>` 替换为您的 Docker ID。

   ```console
   $ docker build -t <YOUR-USERNAME>/nginx-custom .
   ```

此命令会构建您的镜像并为其打标签，以便 Docker 知道将其推送到 Docker Hub 中的哪个仓库。要了解有关该命令及其选项的更多信息，请参阅 [`docker build` CLI 参考](../../reference/cli/docker/buildx/build.md)。运行该命令后，您应该会看到类似以下的输出。

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

3. 运行以下命令来测试您的镜像。将 `<YOUR-USERNAME>` 替换为您的 Docker ID。

   ```console
   $ docker run -p 8080:80 --rm <YOUR-USERNAME>/nginx-custom
   ```

4. 访问 [http://localhost:8080](http://localhost:8080) 查看页面。您应该会看到 `Hello world from Docker!`。

5. 在终端中按 CTRL+C 停止容器。

6. 登录 Docker Desktop。在将镜像推送到 Docker Hub 之前，您必须登录。

7. 运行以下命令将您的镜像推送到 Docker Hub。将 `<YOUR-USERNAME>` 替换为您的 Docker ID。

   ```console
   $ docker push <YOUR-USERNAME>/nginx-custom
   ```

    > [!NOTE]
    >
    > 您必须通过 Docker Desktop 或命令行登录 Docker Hub，并且还必须按照上述步骤正确命名您的镜像。

   该命令会将镜像推送到 Docker Hub，如果仓库不存在，则会自动创建。要了解有关该命令的更多信息，请参阅 [`docker push` CLI 参考](../../reference/cli/docker/image/push.md)。运行该命令后，您应该会看到类似以下的输出。

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

  现在您已经创建了一个仓库并推送了您的镜像，是时候查看您的仓库并探索其选项了。

## 步骤 4：在 Docker Hub 上查看您的仓库并探索选项

您可以在 Docker Hub 或 Docker Desktop 界面中查看您的 Docker Hub 仓库。

{{< tabs >}}
{{< tab name="Docker Hub" >}}

1. 访问 [Docker Hub](https://hub.docker.com) 并登录。

   登录后，您应该会进入 **Repositories** 页面。如果没有，请转到 [**Repositories**](https://hub.docker.com/repositories/) 页面。

2. 找到 **nginx-custom** 仓库并选择该行。

   选择仓库后，您应该会看到有关该仓库的更多详细信息和选项。

{{< /tab >}}
{{< tab name="Docker Desktop" >}}

1. 登录 Docker Desktop。
2. 选择 **Images** 视图。
3. 选择 **Hub repositories** 选项卡。

   您的 Docker Hub 仓库列表将会显示。

4. 找到 **nginx-custom** 仓库，将鼠标悬停在该行上，然后选择 **View in Hub**。

   Docker Hub 将打开，您可以查看有关该镜像的更多详细信息。

{{< /tab >}}
{{< /tabs >}}

现在您已经验证了您的仓库存在于 Docker Hub 上，并且您已经发现了更多选项。查看下一步以了解有关这些选项的更多信息。

## 下一步

添加[仓库信息](./repos/manage/information.md)以帮助用户找到并使用您的镜像。