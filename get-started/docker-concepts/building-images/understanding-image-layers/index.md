# 了解镜像层




## 说明

正如您在[什么是镜像？](../the-basics/what-is-an-image/)中所学到的，容器镜像由多个层组成。而每一层一旦创建，就是不可变的。但这究竟意味着什么？这些层又是如何被用来创建容器可以使用的文件系统的呢？

### 镜像层

镜像中的每一层都包含一组文件系统变更——添加、删除或修改。让我们来看一个理论上的镜像示例：

1. 第一层添加基本命令和包管理器，例如 apt。
2. 第二层安装 Python 运行时和用于依赖管理的 pip。
3. 第三层复制应用程序特定的 requirements.txt 文件。
4. 第四层安装该应用程序特定的依赖项。
5. 第五层复制应用程序的实际源代码。

这个示例可能如下所示：

![显示镜像层概念的流程图截图](images/container_image_layers.webp?border=true)

这种方式非常有益，因为它允许在不同镜像之间重复使用层。例如，假设您想创建另一个 Python 应用程序。由于分层机制，您可以复用相同的 Python 基础层。这将使构建速度更快，并减少分发镜像所需的存储空间和带宽。镜像分层可能如下所示：

![显示镜像分层优势的流程图截图](images/container_image_layer_reuse.webp?border=true)

层使您能够通过复用他人的基础层来扩展他们的镜像，从而只添加您的应用程序所需的数据。

### 堆叠层

分层是通过内容寻址存储和联合文件系统实现的。虽然这涉及一些技术细节，但其工作原理如下：

1. 每一层下载后，会被提取到主机文件系统上的独立目录中。
2. 当您从镜像运行容器时，会创建一个联合文件系统，其中各层被堆叠在一起，形成一个新的统一视图。
3. 容器启动时，其根目录被设置为该统一目录的位置，使用 `chroot` 实现。

在创建联合文件系统时，除了镜像层之外，还会专门为正在运行的容器创建一个目录。这使得容器可以进行文件系统变更，同时保持原始镜像层不被修改。这也使得您可以从同一个底层镜像运行多个容器。

## 动手实践

在本实践指南中，您将使用 [`docker container commit`](https://docs.docker.com/reference/cli/docker/container/commit/) 命令手动创建新的镜像层。请注意，您很少会这样创建镜像，因为通常您会[使用 Dockerfile](./writing-a-dockerfile.md)。但这种方式更容易理解其工作原理。

### 创建基础镜像

在本步骤中，您将创建自己的基础镜像，然后在后续步骤中使用它。

1. [下载并安装](https://www.docker.com/products/docker-desktop/) Docker Desktop。

2. 在终端中运行以下命令以启动新容器：

    ```console
    $ docker run --name=base-container -ti ubuntu
    ```

    镜像下载完成且容器启动后，您应该会看到一个新的 shell 提示符。这表示您正在容器内部运行。它看起来类似于以下内容（容器 ID 会有所不同）：

    ```console
    root@d8c5ca119fcd:/#
    ```

3. 在容器内部，运行以下命令以安装 Node.js：

    ```console
    $ apt update && apt install -y nodejs
    ```

    当此命令运行时，它会在容器内部下载并安装 Node。在联合文件系统的上下文中，这些文件系统变更发生在该容器独有的目录中。

4. 通过运行以下命令验证 Node 是否已安装：

    ```console
    $ node -e 'console.log("Hello world!")'
    ```

    然后您应该在控制台中看到“Hello world!”的输出。

5. 现在您已经安装了 Node，可以准备将所做的更改保存为一个新的镜像层，从中可以启动新容器或构建新镜像。为此，您将使用 [`docker container commit`](https://docs.docker.com/reference/cli/docker/container/commit/) 命令。在新的终端中运行以下命令：

    ```console
    $ docker container commit -m "Add node" base-container node-base
    ```

6. 使用 `docker image history` 命令查看镜像的层：

    ```console
    $ docker image history node-base
    ```

    您将看到类似于以下内容的输出：

    ```console
    IMAGE          CREATED          CREATED BY                                      SIZE      COMMENT
    9e274734bb25   10 seconds ago   /bin/bash                                       157MB     Add node
    cd1dba651b30   7 days ago       /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B
    <missing>      7 days ago       /bin/sh -c #(nop) ADD file:6089c6bede9eca8ec…   110MB
    <missing>      7 days ago       /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B
    <missing>      7 days ago       /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B
    <missing>      7 days ago       /bin/sh -c #(nop)  ARG LAUNCHPAD_BUILD_ARCH     0B
    <missing>      7 days ago       /bin/sh -c #(nop)  ARG RELEASE                  0B
    ```

    注意第一行的“Add node”注释。这一层包含了您刚刚安装的 Node.js。

7. 为了证明您的镜像已安装 Node，您可以使用此新镜像启动一个新容器：

    ```console
    $ docker run node-base node -e "console.log('Hello again')"
    ```

    这样，您应该在终端中看到“Hello again”的输出，表明 Node 已安装并可正常工作。

8. 现在您已完成基础镜像的创建，可以删除该容器：

    ```console
    $ docker rm -f base-container
    ```

> **基础镜像定义**
>
> 基础镜像是构建其他镜像的基础。您可以使用任何镜像作为基础镜像。然而，有些镜像是专门创建为构建块的，为应用程序提供基础或起点。
>
> 在本示例中，您可能不会部署这个 `node-base` 镜像，因为它实际上还没有做任何事情。但它是您可以用于其他构建的基础。

### 构建应用镜像

现在您已经有了基础镜像，可以扩展该镜像以构建其他镜像。

1. 使用新创建的 node-base 镜像启动一个新容器：

    ```console
    $ docker run --name=app-container -ti node-base
    ```

2. 在此容器内部，运行以下命令以创建一个 Node 程序：

    ```console
    $ echo 'console.log("Hello from an app")' > app.js
    ```

    要运行此 Node 程序，您可以使用以下命令并在屏幕上看到打印的消息：

    ```console
    $ node app.js
    ```

3. 在另一个终端中，运行以下命令以将此容器的更改保存为一个新镜像：

    ```console
    $ docker container commit -c "CMD node app.js" -m "Add app" app-container sample-app
    ```

    此命令不仅创建了一个名为 `sample-app` 的新镜像，还为镜像添加了额外配置，以设置在启动容器时的默认命令。在本例中，您将其设置为自动运行 `node app.js`。

4. 在容器外部的终端中，运行以下命令以查看更新后的层：

    ```console
    $ docker image history sample-app
    ```

然后，您将看到类似以下的输出。请注意，最顶层的注释显示“Add app”，而下一层显示“Add node”：

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

5. 最后，使用全新的镜像启动一个新容器。由于您已指定了默认命令，因此可以使用以下命令：

    ```console
    $ docker run sample-app
    ```

    您应该会在终端中看到来自 Node 程序的问候语。

6. 现在您已经完成了容器的使用，可以使用以下命令将其删除：

    ```console
    $ docker rm -f app-container
    ```

## 其他资源

如果您想深入了解所学内容，请查看以下资源：

* [`docker image history`](/reference/cli/docker/image/history/)
* [`docker container commit`](/reference/cli/docker/container/commit/)

## 下一步

如前所述，大多数镜像构建不会使用 `docker container commit`。相反，您将使用 Dockerfile 来自动执行这些步骤。

[编写 Dockerfile](writing-a-dockerfile)

