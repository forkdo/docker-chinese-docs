---
title: 理解镜像层
keywords: concepts, build, images, container, docker desktop
description: 本概念页将向您介绍容器镜像的层。
summary: '您是否曾想过镜像是如何工作的？本指南将帮助您理解镜像层——容器镜像的

  基本构建块。您将全面了解层是如何被创建、堆叠和利用，以确保容器的高效和优化。

  '
weight: 1
aliases:
- /guides/docker-concepts/building-images/understanding-image-layers/
---

{{< youtube-embed wJwqtAkmtQA >}}

## 说明

正如您在 [什么是镜像？](../the-basics/what-is-an-image/) 中所学到的，容器镜像由层组成。并且这些层一旦创建，就是不可变的。但这究竟意味着什么？这些层又是如何被用来创建容器可用的文件系统的呢？

### 镜像层

镜像中的每一层都包含一组文件系统变更——添加、删除或修改。让我们来看一个理论上的镜像：

1.  第一层添加了基本命令和一个包管理器，例如 `apt`。
2.  第二层安装了 Python 运行时和用于依赖管理的 `pip`。
3.  第三层复制了应用程序特定的 `requirements.txt` 文件。
4.  第四层安装了该应用程序的特定依赖项。
5.  第五层复制了应用程序的实际源代码。

这个例子可能看起来像这样：

![展示镜像层概念的流程图截图](images/container_image_layers.webp?border=true)

这样做的好处是它允许层在镜像之间被重用。例如，假设您想创建另一个 Python 应用程序。由于分层机制，您可以利用相同的 Python 基础镜像。这将使构建更快，并减少分发镜像所需的存储量和带宽量。镜像分层可能类似于下图：

![展示镜像分层好处的流程图截图](images/container_image_layer_reuse.webp?border=true)

层让您可以通过重用他人的基础镜像来扩展镜像，从而只需添加您的应用程序所需的数据。

### 层的堆叠

分层是通过内容可寻址存储和联合文件系统实现的。虽然这会涉及一些技术细节，但其工作原理如下：

1.  每一层下载后，会被解压到主机文件系统上其各自的目录中。
2.  当您从一个镜像运行容器时，会创建一个联合文件系统，其中各层相互堆叠，形成一个全新的统一视图。
3.  当容器启动时，其根目录会使用 `chroot` 设置为这个统一目录的位置。

创建联合文件系统时，除了镜像层之外，还会为正在运行的容器专门创建一个目录。这允许容器进行文件系统更改，同时使原始镜像层保持不变。这使您能够从同一个底层镜像运行多个容器。

## 动手试试

在本实践指南中，您将使用 [`docker container commit`](https://docs.docker.com/reference/cli/docker/container/commit/) 命令手动创建新的镜像层。请注意，您很少会以这种方式创建镜像，因为通常您会 [使用 Dockerfile](./writing-a-dockerfile.md)。但这有助于您更容易地理解其工作原理。

### 创建基础镜像

在第一步中，您将创建自己的基础镜像，以便在后续步骤中使用。

1.  [下载并安装](https://www.docker.com/products/docker-desktop/) Docker Desktop。

2.  在终端中，运行以下命令来启动一个新容器：

    ```console
    $ docker run --name=base-container -ti ubuntu
    ```

    镜像下载完成且容器启动后，您应该会看到一个全新的 shell 提示符。这是在您的容器内部运行的。它看起来类似于以下内容（容器 ID 会不同）：

    ```console
    root@d8c5ca119fcd:/#
    ```

3.  在容器内部，运行以下命令来安装 Node.js：

    ```console
    $ apt update && apt install -y nodejs
    ```

    当此命令运行时，它会在容器内下载并安装 Node。在联合文件系统的上下文中，这些文件系统变更发生在该容器独有的目录内。

4.  通过运行以下命令来验证 Node 是否已安装：

    ```console
    $ node -e 'console.log("Hello world!")'
    ```

    然后您应该在控制台中看到 “Hello world!” 出现。

5.  现在您已经安装了 Node，可以准备将所做的更改保存为一个新的镜像层，并可以基于该层启动新容器或构建新镜像。为此，您将使用 [`docker container commit`](https://docs.docker.com/reference/cli/docker/container/commit/) 命令。在新的终端中运行以下命令：

    ```console
    $ docker container commit -m "Add node" base-container node-base
    ```

6.  使用 `docker image history` 命令查看您镜像的层：

    ```console
    $ docker image history node-base
    ```

    您将看到类似于以下的输出：

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

    请注意顶行的 “Add node” 注释。这一层包含了您刚刚安装的 Node.js。

7.  为了证明您的镜像已安装 Node，您可以使用这个新镜像启动一个新容器：

    ```console
    $ docker run node-base node -e "console.log('Hello again')"
    ```

    这样，您应该在终端中得到 “Hello again” 的输出，表明 Node 已安装并正常工作。

8.  既然您已完成基础镜像的创建，就可以删除该容器了：

    ```console
    $ docker rm -f base-container
    ```

> **基础镜像定义**
>
> 基础镜像是构建其他镜像的基础。可以使用任何镜像作为基础镜像。但是，有些镜像是专门作为构建块创建的，为应用程序提供基础或起点。
>
> 在本例中，您可能不会部署这个 `node-base` 镜像，因为它实际上还没有做任何事情。但它是您可用于其他构建的基础。

### 构建应用镜像

现在您有了一个基础镜像，可以扩展该镜像来构建更多镜像。

1.  使用新创建的 node-base 镜像启动一个新容器：

    ```console
    $ docker run --name=app-container -ti node-base
    ```

2.  在此容器内部，运行以下命令来创建一个 Node 程序：

    ```console
    $ echo 'console.log("Hello from an app")' > app.js
    ```

    要运行此 Node 程序，您可以使用以下命令并看到消息打印在屏幕上：

    ```console
    $ node app.js
    ```

3.  在另一个终端中，运行以下命令将此容器的更改保存为新镜像：

    ```console
    $ docker container commit -c "CMD node app.js" -m "Add app" app-container sample-app
    ```

    此命令不仅创建了一个名为 `sample-app` 的新镜像，还向镜像添加了额外的配置，以设置启动容器时的默认命令。在本例中，您将其设置为自动运行 `node app.js`。

4.  在容器外部的终端中，运行以下命令查看更新后的层：

    ```console
    $ docker image history sample-app
    ```

    然后您会看到类似于以下的输出。请注意，顶层注释是 “Add app”，下一层是 “Add node”：

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

5.  最后，使用全新的镜像启动一个新容器。由于您指定了默认命令，因此可以使用以下命令：

    ```console
    $ docker run sample-app
    ```

    您应该在终端中看到您的问候语出现，它来自您的 Node 程序。

6.  既然您已完成了容器的操作，就可以使用以下命令将它们删除：

    ```console
    $ docker rm -f app-container
    ```

## 其他资源

如果您想深入了解所学内容，请查看以下资源：

* [`docker image history`](/reference/cli/docker/image/history/)
* [`docker container commit`](/reference/cli/docker/container/commit/)


## 后续步骤

正如前面所暗示的，大多数镜像构建并不使用 `docker container commit`。相反，您将使用 Dockerfile，它会为您自动执行这些步骤。

{{< button text="编写 Dockerfile" url="writing-a-dockerfile" >}}