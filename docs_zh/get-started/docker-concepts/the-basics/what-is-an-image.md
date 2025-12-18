---
title: 什么是镜像？
weight: 20
keywords: 概念、构建、镜像、容器、Docker Desktop
description: 什么是镜像
aliases:
  - /guides/docker-concepts/the-basics/what-is-an-image/
  - /get-started/run-docker-hub-images/
---

{{< youtube-embed NyvT9REqLe4 >}}

## 说明

既然[容器](./what-is-a-container.md)是一个隔离的进程，那么它的文件和配置是从哪里来的呢？你又如何共享这些环境呢？

这就引出了容器镜像的概念。容器镜像是一种标准化的包，包含了运行容器所需的所有文件、二进制文件、库和配置。

对于一个[PostgreSQL](https://hub.docker.com/_/postgres)镜像，该镜像会打包数据库的二进制文件、配置文件和其他依赖项。对于一个 Python Web 应用，它会包含 Python 运行时、你的应用代码及其所有依赖项。

镜像有两个重要的原则：

1. 镜像是不可变的。一旦镜像被创建，就无法修改。你只能创建新镜像，或在现有镜像之上添加更改。

2. 容器镜像是由多层组成的。每一层代表一组文件系统变更，用于添加、删除或修改文件。

这两个原则让你可以扩展或在现有镜像基础上添加内容。例如，如果你正在构建一个 Python 应用，你可以从[Python 镜像](https://hub.docker.com/_/python)开始，然后添加额外的层来安装应用依赖并添加你的代码。这样你就可以专注于应用本身，而无需关心 Python 的细节。

### 查找镜像

[Docker Hub](https://hub.docker.com) 是默认的全球镜像市场，用于存储和分发镜像。它拥有超过 10 万由开发者创建的镜像，你可以直接在本地运行。你可以在 Docker Desktop 中搜索 Docker Hub 镜像并直接运行它们。

Docker Hub 提供了多种 Docker 官方支持和认可的镜像，称为 Docker 可信内容。这些镜像提供完全托管的服务，或作为你自定义镜像的良好起点。包括：

- [Docker 官方镜像](https://hub.docker.com/search?badges=official) - 一组经过精心挑选的 Docker 仓库，作为大多数用户的起点，是 Docker Hub 上最安全的镜像之一
- [Docker 认证发布者](https://hub.docker.com/search?badges=verified_publisher) - 由商业发布者提供的高质量镜像，经 Docker 认证
- [Docker 赞助的开源镜像](https://hub.docker.com/search?badges=open_source) - 由 Docker 开源计划赞助的开源项目发布和维护的镜像

例如，[Redis](https://hub.docker.com/_/redis) 和 [Memcached](https://hub.docker.com/_/memcached) 是几个流行的即用型 Docker 官方镜像。你可以下载这些镜像，几秒钟内就能启动这些服务。还有一些基础镜像，比如 [Node.js](https://hub.docker.com/_/node) Docker 镜像，你可以将其作为起点，添加自己的文件和配置。

## 动手尝试

{{< tabs group=concept-usage persist=true >}}
{{< tab name="使用 GUI" >}}

在本实验中，你将学习如何使用 Docker Desktop GUI 搜索和拉取容器镜像。

### 搜索并下载镜像

1. 打开 Docker Desktop 仪表板，从左侧导航菜单中选择 **Images** 视图。

   ![Docker Desktop 仪表板截图，显示左侧边栏中的镜像视图](images/click-image.webp?border=true&w=1050&h=400)

2. 选择 **Search images to run** 按钮。如果看不到该按钮，请选择屏幕顶部的 _全局搜索栏_。

   ![Docker Desktop 仪表板截图，显示搜索标签](images/search-image.webp?border)

3. 在 **Search** 字段中输入 "welcome-to-docker"。搜索完成后，选择 `docker/welcome-to-docker` 镜像。

   ![Docker Desktop 仪表板截图，显示 docker/welcome-to-docker 镜像的搜索结果](images/select-image.webp?border=true&w=1050&h=400)

4. 选择 **Pull** 下载镜像。

### 了解镜像

下载镜像后，你可以通过 GUI 或 CLI 了解镜像的详细信息。

1. 在 Docker Desktop 仪表板中，选择 **Images** 视图。

2. 选择 **docker/welcome-to-docker** 镜像，打开镜像详细信息。

   ![Docker Desktop 仪表板截图，显示镜像视图，箭头指向 docker/welcome-to-docker 镜像](images/pulled-image.webp?border=true&w=1050&h=400)

3. 镜像详细信息页面会显示镜像的层、安装的包和库，以及发现的任何漏洞信息。

   ![docker/welcome-to-docker 镜像的详细信息视图截图](images/image-layers.webp?border=true&w=1050&h=400)

{{< /tab >}}

{{< tab name="使用 CLI" >}}

按照说明使用 CLI 搜索和拉取 Docker 镜像，并查看其层结构。

### 搜索并下载镜像

1. 打开终端，使用 [`docker search`](/reference/cli/docker/search.md) 命令搜索镜像：

   ```console
   docker search docker/welcome-to-docker
   ```

   你会看到类似以下的输出：

   ```console
   NAME                       DESCRIPTION                                     STARS     OFFICIAL
   docker/welcome-to-docker   Docker image for new users getting started w…   20
   ```

   此输出显示了 Docker Hub 上可用的相关镜像信息。

2. 使用 [`docker pull`](/reference/cli/docker/image/pull.md) 命令拉取镜像：

   ```console
   docker pull docker/welcome-to-docker
   ```

   你会看到类似以下的输出：

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

   每一行代表镜像的不同层。记住，每一层都是一组文件系统变更，提供镜像的功能。

### 了解镜像

1. 使用 [`docker image ls`](/reference/cli/docker/image/ls.md) 命令列出已下载的镜像：

   ```console
   docker image ls
   ```

   你会看到类似以下的输出：

   ```console
   REPOSITORY                 TAG       IMAGE ID       CREATED        SIZE
   docker/welcome-to-docker   latest    eedaff45e3c7   4 months ago   29.7MB
   ```

   该命令显示当前系统上可用的 Docker 镜像列表。`docker/welcome-to-docker` 镜像的总大小约为 29.7MB。

   > **镜像大小**
   >
   > 此处显示的镜像大小反映的是镜像的未压缩大小，而不是层的下载大小。

2. 使用 [`docker image history`](/reference/cli/docker/image/history.md) 命令列出镜像的层：

   ```console
   docker image history docker/welcome-to-docker
   ```

   你会看到类似以下的输出：

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

   此输出显示了所有层、它们的大小以及创建层所用的命令。

   > **查看完整命令**
   >
   > 如果在命令中添加 `--no-trunc` 标志，你将看到完整的命令。注意，由于输出是表格格式，较长的命令会导致输出难以导航。

{{< /tab >}}
{{< /tabs >}}

在本演练中，你搜索并拉取了一个 Docker 镜像。除了拉取 Docker 镜像外，你还了解了 Docker 镜像的层结构。

## 额外资源

以下资源将帮助你进一步学习如何探索、查找和构建镜像：

- [Docker 可信内容](/manuals/docker-hub/image-library/trusted-content.md)
- [探索 Docker Desktop 中的镜像视图](/manuals/desktop/use-desktop/images.md)
- [Docker Build 概述](/manuals/build/concepts/overview.md)
- [Docker Hub](https://hub.docker.com)

## 下一步

现在你已经了解了镜像的基础知识，接下来学习如何通过注册表分发镜像。

{{< button text="什么是注册表？" url="what-is-a-registry" >}}
