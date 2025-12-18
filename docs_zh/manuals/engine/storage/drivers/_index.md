---
description: 了解支持存储驱动的技术。
keywords: 容器, 存储, 驱动, btrfs, overlayfs, vfs, zfs, containerd
title: 存储驱动
weight: 40
aliases:
  - /storage/storagedriver/imagesandcontainers/
  - /storage/storagedriver/
  - /engine/userguide/storagedriver/imagesandcontainers/
---

> [!NOTE]
> Docker Engine 29.0 及更高版本默认为新安装使用
> [containerd 镜像存储](../containerd.md)。containerd 镜像存储使用快照器（snapshotters）而不是本页描述的经典存储驱动。如果您运行的是 Docker Engine 29.0 或更高版本的新安装，或者已迁移到 containerd 镜像存储，本页提供有关镜像层工作原理的背景信息，但实现细节有所不同。有关 containerd 镜像存储的信息，请参阅 [containerd 镜像存储](../containerd.md)。

要有效使用存储驱动，了解 Docker 如何构建和存储镜像，以及容器如何使用这些镜像非常重要。您可以利用这些信息，明智地选择持久化应用程序数据的最佳方式，并避免沿途的性能问题。

## 存储驱动与 Docker 卷

Docker 使用存储驱动存储镜像层，并在容器的可写层中存储数据。容器的可写层在容器删除后不会持久化，但适用于存储运行时生成的临时数据。存储驱动针对空间效率进行了优化，但（取决于存储驱动）写入速度低于原生文件系统性能，尤其是对于使用写时复制（copy-on-write）文件系统的存储驱动。写密集型应用程序（如数据库存储）会受到性能开销的影响，特别是当只读层中存在预有数据时。

对于写密集型数据、必须在容器生命周期之外持久化以及需要在容器间共享的数据，请使用 Docker 卷。请参阅
[卷部分](../volumes.md) 了解如何使用卷持久化数据并提高性能。

## 镜像和层

Docker 镜像由一系列层构建而成。每一层代表镜像 Dockerfile 中的一条指令。除了最后一层，每一层都是只读的。考虑以下 Dockerfile：

```dockerfile
# syntax=docker/dockerfile:1

FROM ubuntu:22.04
LABEL org.opencontainers.image.authors="org@example.com"
COPY . /app
RUN make /app
RUN rm -r $HOME/.cache
CMD python /app/app.py
```

此 Dockerfile 包含四条命令。修改文件系统的命令会创建新层。`FROM` 语句首先从 `ubuntu:22.04`
镜像创建一层。`LABEL` 命令仅修改镜像的元数据，不产生新层。`COPY` 命令添加 Docker 客户端当前目录中的一些文件。第一个 `RUN` 命令使用 `make` 命令构建应用程序，并将结果写入新层。第二个 `RUN` 命令删除缓存目录，并将结果写入新层。最后，`CMD` 指令指定在容器内运行的命令，仅修改镜像元数据，不产生镜像层。

每一层只是与前一层的差异集合。注意，添加和删除文件都会产生新层。在上面的例子中，`$HOME/.cache` 目录被删除，但仍会保留在前一层中，并计入镜像的总大小。请参阅
[编写 Dockerfile 的最佳实践](/manuals/build/building/best-practices.md) 和 [使用多阶段构建](/manuals/build/building/multi-stage.md)
部分，了解如何优化 Dockerfile 以获得高效的镜像。

层堆叠在一起。创建新容器时，会在底层之上添加新的可写层。此层通常称为“容器层”。对运行中容器的所有更改（如写入新文件、修改现有文件和删除文件）都写入这个薄的可写容器层。下图显示了基于 `ubuntu:15.04` 镜像的容器。

![基于 Ubuntu 镜像的容器层](images/container-layers.webp?w=450&h=300)

存储驱动处理这些层如何相互作用的详细信息。不同的存储驱动可用，在不同情况下各有优缺点。

## 容器和层

容器与镜像的主要区别在于顶层的可写层。所有对容器的写入（添加新数据或修改现有数据）都存储在此可写层中。删除容器时，可写层也会被删除。底层镜像保持不变。

因为每个容器都有自己的可写容器层，且所有更改都存储在此容器层中，所以多个容器可以共享访问同一底层镜像，同时拥有自己的数据状态。下图显示了多个容器共享同一 Ubuntu 15.04 镜像。

![容器共享同一镜像](images/sharing-layers.webp?w=600&h=300)

Docker 使用存储驱动管理镜像层内容和可写容器层。每个存储驱动以不同方式处理实现，但所有驱动都使用可堆叠的镜像层和写时复制（CoW）策略。

> [!NOTE]
>
> 如果需要多个容器对完全相同的数据具有共享访问权限，请使用 Docker 卷。请参阅 [卷部分](../volumes.md) 了解卷的详细信息。

## 容器在磁盘上的大小

要查看运行中容器的大致大小，可以使用 `docker ps -s` 命令。两个不同的列与大小相关。

- `size`：每个容器的可写层使用的数据量（在磁盘上）。
- `virtual size`：容器使用的只读镜像数据量加上容器的可写层 `size`。
  多个容器可能共享部分或全部只读镜像数据。从同一镜像启动的两个容器共享 100% 的只读数据，而具有不同镜像但有共同层的两个容器共享这些共同层。因此，您不能简单地将虚拟大小相加。这会高估总磁盘使用量，可能是一个显著的量。

所有运行中容器在磁盘上使用的总磁盘空间是每个容器的 `size` 和 `virtual size` 值的某种组合。如果多个容器从完全相同的镜像启动，这些容器在磁盘上的总大小为 SUM（容器的 `size`）加上一个镜像大小（`virtual size` - `size`）。

这也未计算容器占用磁盘空间的以下额外方式：

- [日志驱动](/manuals/engine/logging/_index.md) 存储的日志文件使用的磁盘空间。如果您的容器生成大量日志数据且未配置日志轮转，这可能是一个显著的量。
- 容器使用的卷和绑定挂载。
- 容器配置文件使用的磁盘空间，通常很小。
- 写入磁盘的内存（如果启用了交换）。
- 检查点，如果您使用实验性的检查点/恢复功能。

## 写时复制（CoW）策略

写时复制是一种共享和复制文件以实现最大效率的策略。如果文件或目录存在于镜像的较低层中，而另一层（包括可写层）需要读取访问，它只是使用现有文件。当另一层首次需要修改文件时（在构建镜像或运行容器期间），文件被复制到该层并修改。这最大限度地减少了 I/O 和后续各层的大小。这些优势在下面更深入地解释。

### 共享促进更小的镜像

当您使用 `docker pull` 从仓库拉取镜像，或从本地尚不存在的镜像创建容器时，每层会单独拉取，并存储在 Docker 的本地存储区中，通常在 Linux 主机上为 `/var/lib/docker/`。您可以在以下示例中看到这些层被拉取：

```console
$ docker pull ubuntu:22.04
22.04: Pulling from library/ubuntu
f476d66f5408: Pull complete
8882c27f669e: Pull complete
d9af21273955: Pull complete
f5029279ec12: Pull complete
Digest: sha256:6120be6a2b7ce665d0cbddc3ce6eae60fe94637c6a66985312d1f02f63cc0bcd
Status: Downloaded newer image for ubuntu:22.04
docker.io/library/ubuntu:22.04
```

每层都存储在 Docker 主机本地存储区内的单独目录中。要检查文件系统上的层，请列出 `/var/lib/docker/<storage-driver>` 的内容。此示例使用 `overlay2` 
存储驱动：

```console
$ ls /var/lib/docker/overlay2
16802227a96c24dcbeab5b37821e2b67a9f921749cd9a2e386d5a6d5bc6fc6d3
377d73dbb466e0bc7c9ee23166771b35ebdbe02ef17753d79fd3571d4ce659d7
3f02d96212b03e3383160d31d7c6aeca750d2d8a1879965b89fe8146594c453d
ec1ec45792908e90484f7e629330666e7eee599f08729c93890a7205a6ba35f5
l
```

目录名与层 ID 不对应。

现在想象您有两个不同的 Dockerfile。您使用第一个创建一个名为 `acme/my-base-image:1.0` 的镜像。

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN apk add --no-cache bash
```

第二个基于 `acme/my-base-image:1.0`，但有一些额外的层：

```dockerfile
# syntax=docker/dockerfile:1
FROM acme/my-base-image:1.0
COPY . /app
RUN chmod +x /app/hello.sh
CMD /app/hello.sh
```

第二个镜像包含第一个镜像的所有层，以及 `COPY` 和 `RUN` 指令创建的新层，还有一个可读写容器层。Docker 已经有了第一个镜像的所有层，所以不需要再次拉取。两个镜像共享它们共有的任何层。

如果您从两个 Dockerfile 构建镜像，可以使用 `docker image ls` 和 `docker image history` 命令验证共享层的加密 ID 相同。

1. 创建一个新目录 `cow-test/` 并进入该目录。

2. 在 `cow-test/` 内，创建一个名为 `hello.sh` 的新文件，内容如下。

   ```bash
   #!/usr/bin/env bash
   echo "Hello world"
   ```

3. 将上面第一个 Dockerfile 的内容复制到名为 `Dockerfile.base` 的新文件中。

4. 将上面第二个 Dockerfile 的内容复制到名为 `Dockerfile` 的新文件中。

5. 在 `cow-test/` 目录内，构建第一个镜像。不要忘记命令末尾的 `.`。这设置了 `PATH`，告诉 Docker 在哪里查找需要添加到镜像中的文件。

   ```console
   $ docker build -t acme/my-base-image:1.0 -f Dockerfile.base .
   [+] Building 6.0s (11/11) FINISHED
   => [internal] load build definition from Dockerfile.base                                      0.4s
   => => transferring dockerfile: 116B                                                           0.0s
   => [internal] load .dockerignore                                                              0.3s
   => => transferring context: 2B                                                                0.0s
   => resolve image config for docker.io/docker/dockerfile:1                                     1.5s
   => [auth] docker/dockerfile:pull token for registry-1.docker.io                               0.0s
   => CACHED docker-image://docker.io/docker/dockerfile:1@sha256:9e2c9eca7367393aecc68795c671... 0.0s
   => [internal] load .dockerignore                                                              0.0s
   => [internal] load build definition from Dockerfile.base                                      0.0s
   => [internal] load metadata for docker.io/library/alpine:latest                               0.0s
   => CACHED [1/2] FROM docker.io/library/alpine                                                 0.0s
   => [2/2] RUN apk add --no-cache bash                                                          3.1s
   => exporting to image                                                                         0.2s
   => => exporting layers                                                                        0.2s
   => => writing image sha256:da3cf8df55ee9777ddcd5afc40fffc3ead816bda99430bad2257de4459625eaa   0.0s
   => => naming to docker.io/acme/my-base-image:1.0                                              0.0s
   ```

6. 构建第二个镜像。

   ```console
   $ docker build -t acme/my-final-image:1.0 -f Dockerfile .

   [+] Building 3.6s (12/12) FINISHED
   => [internal] load build definition from Dockerfile                                            0.1s
   => => transferring dockerfile: 156B                                                            0.0s
   => [internal] load .dockerignore                                                               0.1s
   => => transferring context: 2B                                                                 0.0s
   => resolve image config for docker.io/docker/dockerfile:1                                      0.5s
   => CACHED docker-image://docker.io/docker/dockerfile:1@sha256:9e2c9eca7367393aecc68795c671...  0.0s
   => [internal] load .dockerignore                                                               0.0s
   => [internal] load build definition from Dockerfile                                            0.0s
   => [internal] load metadata for docker.io/acme/my-base-image:1.0                               0.0s
   => [internal] load build context                                                               0.2s
   => => transferring context: 340B                                                               0.0s
   => [1/3] FROM docker.io/acme/my-base-image:1.0                                                 0.2s
   => [2/3] COPY . /app                                                                           0.1s
   => [3/3] RUN chmod +x /app/hello.sh                                                            0.4s
   => exporting to image                                                                          0.1s
   => => exporting layers                                                                         0.1s
   => => writing image sha256:8bd85c42fa7ff6b33902ada7dcefaaae112bf5673873a089d73583b0074313dd    0.0s
   => => naming to docker.io/acme/my-final-image:1.0                                              0.0s
   ```

7. 查看镜像的大小。

   ```console
   $ docker image ls

   REPOSITORY             TAG     IMAGE ID         CREATED               SIZE
   acme/my-final-image    1.0     8bd85c42fa7f     About a minute ago    7.75MB
   acme/my-base-image     1.0     da3cf8df55ee     2 minutes ago         7.75MB
   ```

8. 查看每个镜像的历史。

   ```console
   $ docker image history acme/my-base-image:1.0

   IMAGE          CREATED         CREATED BY                                      SIZE      COMMENT
   da3cf8df55ee   5 minutes ago   RUN /bin/sh -c apk add --no-cache bash # bui…   2.15MB    buildkit.dockerfile.v0
   <missing>      7 weeks ago     /bin/sh -c #(nop)  CMD ["/bin/sh"]              0B
   <missing>      7 weeks ago     /bin/sh -c #(nop) ADD file:f278386b0cef68136…   5.6MB
   ```

   某些步骤没有大小（`0B`），只是元数据更改，不产生镜像层，除了元数据本身外不占用任何大小。上面的输出显示此镜像由 2 个镜像层组成。

   ```console
   $ docker image history  acme/my-final-image:1.0

   IMAGE          CREATED         CREATED BY                                      SIZE      COMMENT
   8bd85c42fa7f   3 minutes ago   CMD ["/bin/sh" "-c" "/app/hello.sh"]            0B        buildkit.dockerfile.v0
   <missing>      3 minutes ago   RUN /bin/sh -c chmod +x /app/hello.sh # buil…   39B       buildkit.dockerfile.v0
   <missing>      3 minutes ago   COPY . /app # buildkit                          222B      buildkit.dockerfile.v0
   <missing>      4 minutes ago   RUN /bin/sh -c apk add --no-cache bash # bui…   2.15MB    buildkit.dockerfile.v0
   <missing>      7 weeks ago     /bin/sh -c #(nop)  CMD ["/bin/sh"]              0B
   <missing>      7 weeks ago     /bin/sh -c #(nop) ADD file:f278386b0cef68136…   5.6MB
   ```

   注意第一个镜像的所有步骤也包含在最终镜像中。最终