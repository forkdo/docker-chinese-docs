---
title: 什么是镜像？
weight: 20
keywords: 概念, 构建, 镜像, 容器, docker desktop
description: 什么是镜像
aliases:
  - /guides/docker-concepts/the-basics/what-is-an-image/
  - /get-started/run-docker-hub-images/
---

{{< youtube-embed NyvT9REqLe4 >}}

## 解释

鉴于[容器](./what-is-a-container.md)是一个隔离的进程，那么它的文件和配置从何而来？又该如何共享这些环境？

这就是容器镜像发挥作用的地方。容器镜像是一个标准化的软件包，其中包含运行容器所需的所有文件、二进制文件、库和配置。

对于一个 [PostgreSQL](https://hub.docker.com/_/postgres) 镜像，该镜像会打包数据库二进制文件、配置文件和其他依赖项。对于一个 Python Web 应用，它会包含 Python 运行时、你的应用代码及其所有依赖项。

镜像有两个重要的原则：

1.  **镜像是不可变的**。镜像一旦创建，就无法修改。你只能创建一个新镜像，或者在现有镜像之上添加更改。
2.  **容器镜像由多个层组成**。每层代表一组文件系统的更改，包括添加、删除或修改文件。

这两个原则让你能够扩展现有的镜像或在其基础上添加内容。例如，如果你正在构建一个 Python 应用，可以从 [Python 镜像](https://hub.docker.com/_/python)开始，然后添加额外的层来安装应用的依赖项并添加你的代码。这样你就可以专注于应用本身，而不是 Python。

### 查找镜像

[Docker Hub](https://hub.docker.com) 是用于存储和分发镜像的默认全球市场。它拥有超过 100,000 个由开发者创建的镜像，你可以在本地运行。你可以直接从 Docker Desktop 搜索 Docker Hub 镜像并运行它们。

Docker Hub 提供了各种 Docker 支持和认可的镜像，称为 Docker Trusted Content（Docker 受信任内容）。这些镜像提供了完全托管的服务，或者作为你自己镜像的绝佳起点。这些包括：

- [Docker 官方镜像](https://hub.docker.com/search?badges=official) - 一组精心策划的 Docker 仓库，是大多数用户的起点，也是 Docker Hub 上最安全的镜像之一。
- [Docker 验证发布者](https://hub.docker.com/search?badges=verified_publisher) - 由 Docker 验证的商业发布者提供的高质量镜像。
- [Docker 赞助的开源项目](https://hub.docker.com/search?badges=open_source) - 由通过 Docker 开源计划获得赞助的开源项目发布和维护的镜像。

例如，[Redis](https://hub.docker.com/_/redis) 和 [Memcached](https://hub.docker.com/_/memcached) 是几个流行的、开箱即用的 Docker 官方镜像。你可以下载这些镜像，并在几秒钟内启动和运行这些服务。还有一些基础镜像，例如 [Node.js](https://hub.docker.com/_/node) Docker 镜像，你可以将其作为起点，并添加你自己的文件和配置。

## 动手尝试

{{< tabs group=concept-usage persist=true >}}
{{< tab name="使用 GUI" >}}

在这个动手实践中，你将学习如何使用 Docker Desktop GUI 搜索和拉取容器镜像。

### 搜索并下载镜像

1.  打开 Docker Desktop 仪表板，在左侧导航菜单中选择 **Images（镜像）**视图。

   ![Docker Desktop 仪表板的截图，显示左侧边栏中的镜像视图](images/click-image.webp?border=true&w=1050&h=400)

2.  选择 **Search images to run（搜索要运行的镜像）**按钮。如果看不到该按钮，请选择屏幕顶部的*全局搜索栏*。

   ![Docker Desktop 仪表板的截图，显示搜索标签](images/search-image.webp?border)

3.  在 **Search（搜索）**字段中，输入 "welcome-to-docker"。搜索完成后，选择 `docker/welcome-to-docker` 镜像。

   ![Docker Desktop 仪表板的截图，显示 docker/welcome-to-docker 镜像的搜索结果](images/select-image.webp?border=true&w=1050&h=400)

4.  选择 **Pull（拉取）**以下载镜像。

### 了解镜像

下载镜像后，你可以通过 GUI 或 CLI 了解镜像的许多详细信息。

1.  在 Docker Desktop 仪表板中，选择 **Images（镜像）**视图。
2.  选择 **docker/welcome-to-docker** 镜像以打开镜像的详细信息。

   ![Docker Desktop 仪表板的截图，显示镜像视图，箭头指向 docker/welcome-to-docker 镜像](images/pulled-image.webp?border=true&w=1050&h=400)

3.  镜像详情页面会显示有关镜像层、镜像中安装的软件包和库以及任何已发现漏洞的信息。

   ![docker/welcome-to-docker 镜像的镜像详情视图截图](images/image-layers.webp?border=true&w=1050&h=400)

{{< /tab >}}

{{< tab name="使用 CLI" >}}

按照以下说明使用 CLI 搜索和拉取 Docker 镜像，并查看其层。

### 搜索并下载镜像

1.  打开终端，使用 [`docker search`](/reference/cli/docker/search.md) 命令搜索镜像：

   ```console
   docker search docker/welcome-to-docker
   ```

   你将看到类似以下的输出：

   ```console
   NAME                       DESCRIPTION                                     STARS     OFFICIAL
   docker/welcome-to-docker   Docker image for new users getting started w…   20
   ```

   此输出显示了 Docker Hub 上可用的相关镜像信息。

2.  使用 [`docker pull`](/reference/cli/docker/image/pull.md) 命令拉取镜像。

   ```console
   docker pull docker/welcome-to-docker
   ```

   你将看到类似以下的输出：

   ```console
   Using default tag: latest
   latest: Pulling from docker/welcome-to-docker
   579b34f0a95b: Download complete
   d11a451e6399: Download complete
   1c2214f9937c: Download complete
   b42a2f288f4d: Download complete
   54b19e12c655: Download complete
   1fb28e078240: Download complete
   94be7e780731: Download complete
   89578ce72c35: Download complete
   Digest: sha256:eedaff45e3c78538087bdd9dc7afafac7e110061bbdd836af4104b10f10ab693
   Status: Downloaded newer image for docker/welcome-to-docker:latest
   docker.io/docker/welcome-to-docker:latest
   ```

   每一行都代表镜像的一个已下载层。请记住，每层都是一组文件系统更改，并提供镜像的功能。

### 了解镜像

1.  使用 [`docker image ls`](/reference/cli/docker/image/ls.md) 命令列出你下载的镜像：

   ```console
   docker image ls
   ```

   你将看到类似以下的输出：

   ```console
   REPOSITORY                 TAG       IMAGE ID       CREATED        SIZE
   docker/welcome-to-docker   latest    eedaff45e3c7   4 months ago   29.7MB
   ```

   该命令显示当前系统上可用的 Docker 镜像列表。`docker/welcome-to-docker` 的总大小约为 29.7MB。

   > **镜像大小**
   >
   > 这里显示的镜像大小反映了镜像的未压缩大小，而不是层的下载大小。

2.  使用 [`docker image history`](/reference/cli/docker/image/history.md) 命令列出镜像的层：

   ```console
   docker image history docker/welcome-to-docker
   ```

   你将看到类似以下的输出：

   ```console
   IMAGE          CREATED        CREATED BY                                      SIZE      COMMENT
   648f93a1ba7d   4 months ago   COPY /app/build /usr/share/nginx/html # buil…   1.6MB     buildkit.dockerfile.v0
   <missing>      5 months ago   /bin/sh -c #(nop)  CMD ["nginx" "-g" "daemon…   0B
   <missing>      5 months ago   /bin/sh -c #(nop)  STOPSIGNAL SIGQUIT           0B
   <missing>      5 months ago   /bin/sh -c #(nop)  EXPOSE 80                    0B
   <missing>      5 months ago   /bin/sh -c #(nop)  ENTRYPOINT ["/docker-entr…   0B
   <missing>      5 months ago   /bin/sh -c #(nop) COPY file:9e3b2b63db9f8fc7…   4.62kB
   <missing>      5 months ago   /bin/sh -c #(nop) COPY file:57846632accc8975…   3.02kB
   <missing>      5 months ago   /bin/sh -c #(nop) COPY file:3b1b9915b7dd898a…   298B
   <missing>      5 months ago   /bin/sh -c #(nop) COPY file:caec368f5a54f70a…   2.12kB
   <missing>      5 months ago   /bin/sh -c #(nop) COPY file:01e75c6dd0ce317d…   1.62kB
   <missing>      5 months ago   /bin/sh -c set -x     && addgroup -g 101 -S …   9.7MB
   <missing>      5 months ago   /bin/sh -c #(nop)  ENV PKG_RELEASE=1            0B
   <missing>      5 months ago   /bin/sh -c #(nop)  ENV NGINX_VERSION=1.25.3     0B
   <missing>      5 months ago   /bin/sh -c #(nop)  LABEL maintainer=NGINX Do…   0B
   <missing>      5 months ago   /bin/sh -c #(nop)  CMD ["/bin/sh"]              0B
   <missing>      5 months ago   /bin/sh -c #(nop) ADD file:ff3112828967e8004…   7.66MB
   ```

   此输出显示了所有层、它们的大小以及用于创建该层的命令。

   > **查看完整命令**
   >
   > 如果你在命令中添加 `--no-trunc` 标志，你将看到完整的命令。请注意，由于输出是类似表格的格式，较长的命令会使输出非常难以浏览。

{{< /tab >}}
{{< /tabs >}}

在这个演练中，你搜索并拉取了一个 Docker 镜像。除了拉取 Docker 镜像，你还了解了 Docker 镜像的层。

## 其他资源

以下资源将帮助你进一步了解如何探索、查找和构建镜像：

- [Docker 受信任内容](/manuals/docker-hub/image-library/trusted-content.md)
- [探索 Docker Desktop 中的镜像视图](/manuals/desktop/use-desktop/images.md)
- [Docker Build 概述](/manuals/build/concepts/overview.md)
- [Docker Hub](https://hub.docker.com)

## 下一步

现在你已经了解了镜像的基础知识，是时候学习如何通过注册中心来分发镜像了。

{{< button text="什么是注册中心？" url="what-is-a-registry" >}}