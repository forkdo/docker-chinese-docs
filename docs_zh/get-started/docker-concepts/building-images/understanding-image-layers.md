---
title: 理解镜像层
keywords: 概念, 构建, 镜像, 容器, Docker Desktop
description: 本概念页面将向你介绍容器镜像的层。
summary: |
  你是否好奇过镜像的工作原理？本指南将帮助你理解镜像层——容器镜像的基本构建块。你将全面了解层是如何创建、堆叠和使用的，以确保容器的高效和优化。
weight: 1
aliases: 
 - /guides/docker-concepts/building-images/understanding-image-layers/
---

{{< youtube-embed wJwqtAkmtQA >}}

## 解释

正如你在[什么是镜像？](../the-basics/what-is-an-image/)中学到的，容器镜像是由层组成的。每个层一旦创建，就是不可变的。但这到底意味着什么？这些层又是如何被用来创建容器可以使用的文件系统的？

### 镜像层

镜像中的每一层都包含一组文件系统更改——添加、删除或修改。让我们来看一个理论上的镜像：

1. 第一层添加基本命令和包管理器，比如 apt。
2. 第二层安装 Python 运行时和用于依赖管理的 pip。
3. 第三层复制应用程序特定的 requirements.txt 文件。
4. 第四层安装该应用程序的特定依赖项。
5. 第五层复制应用程序的实际源代码。

这个例子可能看起来像这样：

![展示镜像层概念的流程图截图](images/container_image_layers.webp?border=true)

这样做是有益的，因为它允许层在镜像之间重用。例如，想象一下你想创建另一个 Python 应用程序。由于分层，你可以利用相同的 Python 基础层。这将使构建更快，并减少分发镜像所需的存储和带宽。镜像分层可能看起来像下面这样：

![展示镜像分层好处的流程图截图](images/container_image_layer_reuse.webp?border=true)

分层让你可以通过重用他人的基础层来扩展镜像，只添加你的应用程序所需的数据。

### 堆叠层

分层是通过内容可寻址存储和联合文件系统实现的。虽然这会变得技术性很强，但其工作原理如下：

1. 每个层下载后，它会被提取到主机文件系统上的自己的目录中。
2. 当你从镜像运行容器时，会创建一个联合文件系统，其中层被堆叠在一起，创建一个新的统一视图。
3. 当容器启动时，其根目录被设置为这个统一目录的位置，使用 `chroot`。

创建联合文件系统时，除了镜像层外，还会为运行的容器创建一个特定的目录。这允许容器在保持原始镜像层不变的情况下进行文件系统更改。这使你能够从同一个底层镜像运行多个容器。

## 动手尝试

在本实践指南中，你将使用 [`docker container commit`](https://docs.docker.com/reference/cli/docker/container/commit/) 命令手动创建新的镜像层。请注意，你很少会这样创建镜像，因为你通常会[使用 Dockerfile](./writing-a-dockerfile.md)。但这让你更容易理解它是如何工作的。

### 创建基础镜像

在这第一步中，你将创建自己的基础镜像，然后在后续步骤中使用它。

1. [下载并安装](https://www.docker.com/products/docker-desktop/) Docker Desktop。


2. 在终端中，运行以下命令启动一个新容器：

    ```console
    $ docker run --name=base-container -ti ubuntu
    ```

    一旦镜像下载完成并且容器启动，你应该会看到一个新的 shell 提示符。这正在你的容器内运行。它看起来应该像下面这样（容器 ID 会有所不同）：

    ```console
    root@d8c5ca119fcd:/#
    ```

3. 在容器内，运行以下命令安装 Node.js：

    ```console
    $ apt update && apt install -y nodejs
    ```

    当这个命令运行时，它会下载并安装容器内的 Node。在联合文件系统的上下文中，这些文件系统更改发生在该容器独有的目录内。

4. 通过运行以下命令验证 Node 是否已安装：

    ```console
    $ node -e 'console.log("Hello world!")'
    ```

    然后你应该会在控制台中看到 "Hello world!" 出现。

5. 现在你已经安装了 Node，你已准备好将你所做的更改保存为新的镜像层，从该层你可以启动新容器或构建新镜像。为此，你将使用 [`docker container commit`](https://docs.docker.com/reference/cli/docker/container/commit/) 命令。在新终端中运行以下命令：

    ```console
    $ docker container commit -m "Add node" base-container node-base
    ```

6. 使用 `docker image history` 命令查看你的镜像层：

    ```console
    $ docker image history node-base
    ```

    你会看到类似以下的输出：

    ```console
    IMAGE          CREATED          CREATED BY                                      SIZE      COMMENT
    d5c1fca2cdc4   10 seconds ago   /bin/bash                                       126MB     Add node
    2b7cc08dcdbb   5 weeks ago      /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B
    <missing>      5 weeks ago      /bin/sh -c #(nop) ADD file:07cdbabf782942af0…   69.2MB
    <missing>      5 weeks ago      /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B
    <missing>      5 weeks ago      /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B
    <missing>      5 weeks ago      /bin/sh -c #(nop)  ARG LAUNCHPAD_BUILD_ARCH     0B
    <missing>      5 weeks ago      /bin/sh -c #(nop)  ARG RELEASE                  0B
    ```

    注意第一行的 "Add node" 注释。这一层包含你刚刚安装的 Node.js。

7. 为了证明你的镜像已安装 Node，你可以使用这个新镜像启动一个新容器：

    ```console
    $ docker run node-base node -e "console.log('Hello again')"
    ```

    这样，你应该会在终端中得到 "Hello again" 输出，显示 Node 已安装并正在工作。

8. 现在你已经完成了基础镜像的创建，你可以删除该容器：

    ```console
    $ docker rm -f base-container
    ```

> **基础镜像定义**
>
> 基础镜像是构建其他镜像的基础。你可以使用任何镜像作为基础镜像。然而，有些镜像是有意创建为构建块的，为应用程序提供基础或起点。
>
> 在这个例子中，你可能不会部署这个 `node-base` 镜像，因为它目前还没有做任何事情。但它是你可以用于其他构建的基础。

### 构建应用镜像

现在你有了一个基础镜像，你可以扩展该镜像来构建其他镜像。

1. 使用新创建的 node-base 镜像启动一个新容器：

    ```console
    $ docker run --name=app-container -ti node-base
    ```

2. 在这个容器内，运行以下命令创建一个 Node 程序：

    ```console
    $ echo 'console.log("Hello from an app")' > app.js
    ```

    要运行这个 Node 程序，你可以使用以下命令并在屏幕上看到消息：

    ```console
    $ node app.js
    ```

3. 在另一个终端中，运行以下命令将此容器的更改保存为新镜像：

    ```console
    $ docker container commit -c "CMD node app.js" -m "Add app" app-container sample-app
    ```

    此命令不仅创建了一个名为 `sample-app` 的新镜像，还添加了额外的配置来设置启动容器时的默认命令。在这种情况下，你设置它自动运行 `node app.js`。

4. 在容器外的终端中，运行以下命令查看更新的层：

    ```console
    $ docker image history sample-app
    ```

    然后你会看到类似以下的输出。注意顶层注释有 "Add app"，下一层有 "Add node"：

    ```console
    IMAGE          CREATED              CREATED BY                                      SIZE      COMMENT
    c1502e2ec875   About a minute ago   /bin/bash                                       33B       Add app
    5310da79c50a   4 minutes ago        /bin/bash                                       126MB     Add node
    2b7cc08dcdbb   5 weeks ago          /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B
    <missing>      5 weeks ago          /bin/sh -c #(nop) ADD file:07cdbabf782942af0…   69.2MB
    <missing>      5 weeks ago          /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B
    <missing>      5 weeks ago          /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B
    <missing>      5 weeks ago          /bin/sh -c #(nop)  ARG LAUNCHPAD_BUILD_ARCH     0B
    <missing>      5 weeks ago          /bin/sh -c #(nop)  ARG RELEASE                  0B
    ```

5. 最后，使用全新的镜像启动一个新容器。由于你指定了默认命令，你可以使用以下命令：

    ```console
    $ docker run sample-app
    ```

    你应该会在终端中看到你的问候语从你的 Node 程序中出现。

6. 现在你已经完成了容器的工作，你可以使用以下命令删除它们：

    ```console
    $ docker rm -f app-container
    ```

## 额外资源

如果你想更深入地了解你学到的内容，请查看以下资源：

* [`docker image history`](/reference/cli/docker/image/history/)
* [`docker container commit`](/reference/cli/docker/container/commit/)


## 下一步

如前面暗示的，大多数镜像构建不使用 `docker container commit`。相反，你会使用 Dockerfile，它会自动为你执行这些步骤。

{{< button text="编写 Dockerfile" url="writing-a-dockerfile" >}}
