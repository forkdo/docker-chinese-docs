---
title: 共享应用程序
weight: 40
linkTitle: 'Part 3: Share the application'
keywords: get started, setup, orientation, quickstart, intro, concepts, containers, docker desktop, docker hub, sharing
description: 分享你为示例应用程序构建的镜像，以便你可以在其他地方运行它，其他开发者也可以使用它
aliases:
- /get-started/part3/
- /get-started/04_sharing_app/
- /guides/workshop/04_sharing_app/
---

现在你已经构建了一个镜像，你可以共享它。要共享 Docker 镜像，你必须使用 Docker 注册表。默认注册表是 Docker Hub，你使用的所有镜像都来自这里。

> **Docker ID**
>
> Docker ID 让你可以访问 Docker Hub，这是世界上最大的容器镜像库和社区。如果没有 Docker ID，可以免费注册一个 [Docker ID](https://hub.docker.com/signup)。

## 创建仓库

要推送镜像，你首先需要在 Docker Hub 上创建一个仓库。

1. [注册](https://www.docker.com/pricing?utm_source=docker&utm_medium=webreferral&utm_campaign=docs_driven_upgrade) 或登录 [Docker Hub](https://hub.docker.com)。

2. 选择 **Create Repository** 按钮。

3. 仓库名称使用 `getting-started`。确保 **Visibility** 为 **Public**。

4. 选择 **Create**。

在下图中，你可以看到 Docker Hub 上的示例 Docker 命令。此命令将推送到此仓库。

![Docker command with push example](images/push-command.webp)


## 推送镜像

让我们尝试将镜像推送到 Docker Hub。

1. 在命令行中，运行以下命令：

   ```console
   docker push docker/getting-started
   ```

   你会看到类似这样的错误：

   ```console
   $ docker push docker/getting-started
   The push refers to repository [docker.io/docker/getting-started]
   An image does not exist locally with the tag: docker/getting-started
   ```

   这个失败是预期的，因为镜像还没有正确标记。Docker 正在查找名为 `docker/getting started` 的镜像名称，但你的本地镜像仍然命名为 `getting-started`。

   你可以通过运行以下命令来确认这一点：

   ```console
   docker image ls
   ```

2. 要解决这个问题，首先使用你的 Docker ID 登录 Docker Hub：`docker login YOUR-USER-NAME`。
3. 使用 `docker tag` 命令为 `getting-started` 镜像赋予新名称。将 `YOUR-USER-NAME` 替换为你的 Docker ID。

   ```console
   $ docker tag getting-started YOUR-USER-NAME/getting-started
   ```

4. 现在再次运行 `docker push` 命令。如果你从 Docker Hub 复制值，可以省略 `tagname` 部分，因为你没有为镜像名称添加标签。如果你不指定标签，Docker 使用一个名为 `latest` 的标签。

   ```console
   $ docker push YOUR-USER-NAME/getting-started
   ```

## 在新实例上运行镜像

现在你的镜像已经构建并推送到注册表中，尝试在从未见过此容器镜像的全新实例上运行你的应用程序。为此，你将使用 Play with Docker。

> [!NOTE]
>
> Play with Docker 使用 amd64 平台。如果你使用的是基于 ARM 的 Apple silicon Mac，你需要重新构建镜像以兼容 Play with Docker，并将新镜像推送到你的仓库。
>
> 要为 amd64 平台构建镜像，请使用 `--platform` 标志。
> ```console
> $ docker build --platform linux/amd64 -t YOUR-USER-NAME/getting-started .
> ```
>
> Docker buildx 也支持构建多平台镜像。要了解更多信息，请参阅 [Multi-platform images](/manuals/build/building/multi-platform.md)。


1. 在浏览器中打开 [Play with Docker](https://labs.play-with-docker.com/)。

2. 选择 **Login**，然后从下拉列表中选择 **docker**。

3. 使用你的 Docker Hub 账户登录，然后选择 **Start**。

4. 在左侧边栏中选择 **ADD NEW INSTANCE** 选项。如果你看不到它，让浏览器窗口更宽一点。几秒钟后，浏览器中会打开一个终端窗口。

    ![Play with Docker add new instance](images/pwd-add-new-instance.webp)

5. 在终端中，启动你刚刚推送的应用程序。

   ```console
   $ docker run -dp 0.0.0.0:3000:3000 YOUR-USER-NAME/getting-started
   ```

    你应该看到镜像被拉取下来并最终启动。

    > [!TIP]
    >
    > 你可能已经注意到，此命令将端口映射绑定到不同的 IP 地址。之前的 `docker run` 命令将端口发布到主机上的 `127.0.0.1:3000`。这次，你使用的是 `0.0.0.0`。
    >
    > 绑定到 `127.0.0.1` 仅将容器的端口暴露给回环接口。而绑定到 `0.0.0.0` 会将容器的端口暴露在主机的所有接口上，使其可被外部世界访问。
    >
    > 有关端口映射工作原理的更多信息，请参阅 [Networking](/manuals/engine/network/_index.md#published-ports)。

6. 当 3000 徽章出现时，选择它。

   如果没有出现 3000 徽章，你可以选择 **Open Port** 并指定 `3000`。

## 总结

在本节中，你学习了如何通过将镜像推送到注册表来共享你的镜像。然后你去了一个全新的实例，能够运行刚刚推送的镜像。这在 CI 管道中很常见，管道会创建镜像并将其推送到注册表，然后生产环境可以使用最新版本的镜像。

相关信息：

 - [docker CLI reference](/reference/cli/docker/)
 - [Multi-platform images](/manuals/build/building/multi-platform.md)
 - [Docker Hub overview](/manuals/docker-hub/_index.md)

## 下一步

在下一节中，你将学习如何在容器化应用程序中持久化数据。

{{< button text="Persist the DB" url="05_persisting_data.md" >}}