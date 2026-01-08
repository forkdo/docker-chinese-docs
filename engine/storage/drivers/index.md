# 存储驱动程序

> [!NOTE]
> Docker Engine 29.0 及更高版本在全新安装时默认使用
> [containerd 镜像存储](../containerd.md)。
> containerd 镜像存储使用快照程序（snapshotters），而不是本页描述的经典存储驱动程序。
> 如果您运行的是 Docker Engine 29.0 或更高版本的全新安装，或者您已迁移到 containerd 镜像存储，
> 本页提供了关于镜像层工作原理的背景知识，但具体实现细节可能有所不同。
> 有关 containerd 镜像存储的信息，请参阅 [containerd 镜像存储](../containerd.md)。

要有效使用存储驱动程序，了解 Docker 如何构建和存储镜像，以及容器如何使用这些镜像是很重要的。
您可以利用这些信息，为持久化应用程序数据做出明智的选择，并避免在此过程中出现性能问题。

## 存储驱动程序与 Docker 卷

Docker 使用存储驱动程序来存储镜像层，并存储容器可写层中的数据。
容器的可写层在容器删除后不会持久存在，但适用于存储运行时生成的临时数据。
存储驱动程序针对空间效率进行了优化，但是（取决于存储驱动程序）写入速度低于原生文件系统性能，
特别是对于使用写时复制（copy-on-write）文件系统的存储驱动程序。
写入密集型应用程序（如数据库存储）会受到性能开销的影响，特别是当只读层中存在预先存在的数据时。

对于写入密集型数据、必须在容器生命周期之外持久存在的数据以及必须在容器之间共享的数据，请使用 Docker 卷。
请参阅 [卷部分](../volumes.md) 以了解如何使用卷来持久化数据和提高性能。

## 镜像和层

Docker 镜像由一系列层构建而成。每一层代表镜像 Dockerfile 中的一条指令。
除了最后一层之外，每一层都是只读的。考虑以下 Dockerfile：

```dockerfile
# syntax=docker/dockerfile:1

FROM ubuntu:22.04
LABEL org.opencontainers.image.authors="org@example.com"
COPY . /app
RUN make /app
RUN rm -r $HOME/.cache
CMD python /app/app.py
```

此 Dockerfile 包含四个命令。修改文件系统的命令会创建一个新层。
`FROM` 语句首先从 `ubuntu:22.04` 镜像创建一个层。
`LABEL` 命令仅修改镜像的元数据，不会产生新层。
`COPY` 命令从 Docker 客户端当前目录添加一些文件。
第一个 `RUN` 命令使用 `make` 命令构建您的应用程序，并将结果写入一个新层。
第二个 `RUN` 命令删除一个缓存目录，并将结果写入一个新层。
最后，`CMD` 指令指定在容器内运行的命令，这只修改镜像的元数据，不会产生镜像层。

每一层都只是与前一层相比的一组差异。请注意，_添加_和_删除_文件都会导致新层的产生。
在上面的例子中，`$HOME/.cache` 目录被删除，但它仍然存在于前一层中，并会增加镜像的总大小。
请参阅 [编写 Dockerfile 的最佳实践](/manuals/build/building/best-practices.md)
和 [使用多阶段构建](/manuals/build/building/multi-stage.md)
部分，以了解如何优化您的 Dockerfile 以获得高效的镜像。

这些层彼此堆叠。当您创建一个新容器时，您会在底层之上添加一个新的可写层。
这个层通常被称为“容器层”。对正在运行的容器所做的所有更改，例如写入新文件、修改现有文件和删除文件，
都会写入到这个薄的可写容器层中。下图显示了一个基于 `ubuntu:15.04` 镜像的容器。

![基于 Ubuntu 镜像的容器的层](images/container-layers.webp?w=450&h=300)

存储驱动程序处理这些层之间如何交互的细节。可以使用不同的存储驱动程序，它们在不同的情况下有优点和缺点。

## 容器和层

容器和镜像之间的主要区别在于顶部的可写层。
所有写入容器的、添加新数据或修改现有数据的操作都存储在这个可写层中。
当容器被删除时，可写层也会被删除。底层镜像保持不变。

因为每个容器都有自己的可写容器层，并且所有更改都存储在这个容器层中，
所以多个容器可以共享访问同一个底层镜像，同时拥有自己的数据状态。
下图显示了多个容器共享同一个 Ubuntu 15.04 镜像。

![共享同一镜像的容器](images/sharing-layers.webp?w=600&h=300)

Docker 使用存储驱动程序来管理镜像层和可写容器层的内容。
每个存储驱动程序的实现方式不同，但所有驱动程序都使用可堆叠的镜像层和写时复制（CoW）策略。

> [!NOTE]
>
> 如果您需要多个容器共享访问完全相同的数据，请使用 Docker 卷。
> 请参阅 [卷部分](../volumes.md) 了解卷。

## 容器在磁盘上的大小

要查看正在运行的容器的近似大小，可以使用 `docker ps -s` 命令。
有两个不同的列与大小相关。

- `size`：用于每个容器可写层的数据量（在磁盘上）。
- `virtual size`：容器使用的只读镜像数据量加上容器的可写层 `size`。
  多个容器可能共享部分或全部只读镜像数据。从同一镜像启动的两个容器共享 100% 的只读数据，
  而具有不同镜像但共享某些层的两个容器则共享这些公共层。
  因此，您不能简单地将虚拟大小相加。这可能会高估总磁盘使用量，且可能高出不少。

磁盘上所有正在运行的容器使用的总磁盘空间是每个容器的 `size` 和 `virtual size` 值的某种组合。
如果从完全相同的镜像启动多个容器，则这些容器在磁盘上的总大小将是 容器 `size` 之和 加上 一个镜像大小（`virtual size` - `size`）。

这还不包括容器占用磁盘空间的以下其他方式：

- 由 [日志驱动程序](/manuals/engine/logging/_index.md) 存储的日志文件使用的磁盘空间。
  如果您的容器生成大量日志数据且未配置日志轮转，这可能相当可观。
- 容器使用的卷和绑定挂载。
- 容器配置文件使用的磁盘空间，这些文件通常很小。
- 写入磁盘的内存（如果启用了交换）。
- 检查点（checkpoints），如果您使用的是实验性的检查点/恢复功能。

## 写时复制（CoW）策略

写时复制是一种共享和复制文件以实现最大效率的策略。
如果文件或目录存在于镜像的较低层中，并且另一层（包括可写层）需要读取访问权限，
它只需使用现有文件。当另一层第一次需要修改该文件时（在构建镜像或运行容器时），
该文件会被复制到该层并进行修改。这最大限度地减少了 I/O 和后续每一层的大小。
这些优势将在下面更深入地解释。

### 共享促进更小的镜像

当您使用 `docker pull` 从仓库拉取镜像，或者从本地尚不存在的镜像创建容器时，
每个层都会被单独拉取，并存储在 Docker 的本地存储区域中，在 Linux 主机上通常是 `/var/lib/docker/`。
在此示例中，您可以看到正在拉取这些层：

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

这些层中的每一层都存储在 Docker 主机本地存储区域内的其自己的目录中。
要检查文件系统上的层，请列出 `/var/lib/docker/<storage-driver>` 的内容。
此示例使用 `overlay2` 存储驱动程序：

```console
$ ls /var/lib/docker/overlay2
16802227a96c24dcbeab5b37821e2b67a9f921749cd9a2e386d5a6d5bc6fc6d3
377d73dbb466e0bc7c9ee23166771b35ebdbe02ef17753d79fd3571d4ce659d7
3f02d96212b03e3383160d31d7c6aeca750d2d8a1879965b89fe8146594c453d
ec1ec45792908e90484f7e629330666e7eee599f08729c93890a7205a6ba35f5
l
```

目录名与层 ID 不对应。

现在想象一下，您有两个不同的 Dockerfile。您使用第一个来创建一个名为 `acme/my-base-image:1.0` 的镜像。

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

第二个镜像包含第一个镜像的所有层，加上由 `COPY` 和 `RUN` 指令创建的新层，以及一个读写容器层。
Docker 已经拥有第一个镜像的所有层，因此不需要再次拉取它们。两个镜像共享它们共有的任何层。

如果您从这两个 Dockerfile 构建镜像，可以使用 `docker image ls` 和 `docker image history` 命令来验证共享层的加密 ID 是否相同。

1. 创建一个新目录 `cow-test/` 并进入该目录。

2. 在 `cow-test/` 中，创建一个名为 `hello.sh` 的新文件，内容如下。

   ```bash
   #!/usr/bin/env bash
   echo "Hello world"
   ```

3. 将上面第一个 Dockerfile 的内容复制到一个名为 `Dockerfile.base` 的新文件中。

4. 将上面第二个 Dockerfile 的内容复制到一个名为 `Dockerfile` 的新文件中。

5. 在 `cow-test/` 目录中，构建第一个镜像。不要忘记在命令中包含最后的 `.`。这设置了 `PATH`，告诉 Docker 在哪里查找需要添加到镜像中的任何文件。

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

8. 查看每个镜像的历史记录。

   ```console
   $ docker image history acme/my-base-image:1.0

   IMAGE          CREATED         CREATED BY                                      SIZE      COMMENT
   da3cf8df55ee   5 minutes ago   RUN /bin/sh -c apk add --no-cache bash # bui…   2.15MB    buildkit.dockerfile.v0
   <missing>      7 weeks ago     /bin/sh -c #(nop)  CMD ["/bin/sh"]              0B
   <missing>      7 weeks ago     /bin/sh -c #(nop) ADD file:f278386b0cef68136…   5.6MB
   ```

   有些步骤没有大小（`0B`），它们是仅元数据的更改，不产生镜像层，也不占用任何大小（元数据本身除外）。
   上面的输出显示此镜像由 2 个镜像层组成。

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

   请注意，第一个镜像的所有步骤也包含在最终镜像中。最终镜像包含来自第一个镜像的两个层，以及在第二个镜像中添加的两个层。

   `docker history` 输出中的 `<missing>` 行表示这些步骤要么是在另一个系统上构建的，并且是作为从 Docker Hub 拉取的 `alpine` 镜像的一部分，
   要么是使用 BuildKit 作为构建器构建的。在 BuildKit 之前，“经典”构建器会为每个步骤生成一个新的“中间”镜像用于缓存目的，`IMAGE` 列将显示该镜像的 ID。

   BuildKit 使用自己的缓存机制，不再需要中间镜像进行缓存。请参阅 [BuildKit](/manuals/build/buildkit/_index.md) 以了解 BuildKit 中的其他增强功能。

9. 查看每个镜像的层

   使用 `docker image inspect` 命令查看每个镜像中层的加密 ID：

   ```console
   $ docker image inspect --format "{{json .RootFS.Layers}}" acme/my-base-image:1.0
   [
     "sha256:72e830a4dff5f0d5225cdc0a320e85ab1ce06ea5673acfe8d83a7645cbd0e9cf",
     "sha256:07b4a9068b6af337e8b8f1f1dae3dd14185b2c0003a9a1f0a6fd2587495b204a"
   ]
   ```
   
   ```console
   $ docker image inspect --format "{{json .RootFS.Layers}}" acme/my-final-image:1.0
   [
     "sha256:72e830a4dff5f0d5225cdc0a320e85ab1ce06ea5673acfe8d83a7645cbd0e9cf",
     "sha256:07b4a9068b6af337e8b8f1f1dae3dd14185b2c0003a9a1f0a6fd2587495b204a",
     "sha256:cc644054967e516db4689b5282ee98e4bc4b11ea2255c9630309f559ab96562e",
     "sha256:e84fb818852626e89a09f5143dbc31fe7f0e0a6a24cd8d2eb68062b904337af4"
   ]
   ```

   请注意，前两层在两个镜像中是相同的。第二个镜像添加了两个额外的层。
   共享的镜像层在 `/var/lib/docker/` 中只存储一次，并且在将镜像推送到镜像仓库和从镜像仓库拉取时也会共享。
   因此，共享镜像层可以减少网络带宽和存储。

   > [!TIP]
   >
   > 使用 `--format` 选项格式化 Docker 命令的输出。
   > 
   > 上面的示例使用带有 `--format` 选项的 `docker image inspect` 命令来查看层 ID，格式化为 JSON 数组。
   > Docker 命令上的 `--format` 选项是一个强大的功能，它允许您从输出中提取和格式化特定信息，
   > 而无需 `awk` 或 `sed` 等额外工具。要了解有关使用 `--format` 标志格式化 docker 命令输出的更多信息，
   > 请参阅 [格式化命令和日志输出部分](/manuals/engine/cli/formatting.md)。
   > 我们还使用 [`jq` 实用程序](https://stedolan.github.io/jq/) 美化了 JSON 输出以提高可读性。

### 复制使容器高效

当您启动一个容器时，一个薄的可写容器层会被添加到其他层之上。
容器对文件系统所做的任何更改都存储在这里。容器未更改的任何文件都不会被复制到此可写层。
这意味着可写层尽可能小。

当容器中的现有文件被修改时，存储驱动程序会执行写时复制操作。
所涉及的具体步骤取决于特定的存储驱动程序。对于 `overlay2` 驱动程序，写时复制操作遵循以下大致顺序：

*  在镜像层中搜索要更新的文件。该过程从最新层开始，逐层向下直到基础层。
   找到结果后，它们会添加到缓存中以加速未来的操作。
*  对找到的第一个文件副本执行 `copy_up` 操作，将文件复制到容器的可写层。
*  对此文件副本进行任何修改，容器无法看到存在于较低层中的只读文件副本。

Btrfs、ZFS 和其他驱动程序处理写时复制的方式不同。您可以在其详细描述中阅读有关这些驱动程序方法的更多信息。

写入大量数据的容器比不写入数据的容器消耗更多空间。这是因为大多数写入操作会在容器薄的可写顶层中消耗新空间。
请注意，更改文件的元数据，例如更改文件的权限或所有权，也可能导致 `copy_up` 操作，从而将文件复制到可写层。

> [!TIP]
>
> 对于写入密集型应用程序，请使用卷。
>
> 不要将数据存储在容器中用于写入密集型应用程序。此类应用程序，例如写入密集型数据库，已知是有问题的，
> 特别是当只读层中存在预先存在的数据时。
> 
> 相反，使用 Docker 卷，它独立于正在运行的容器，并且设计为对 I/O 高效。
> 此外，卷可以在容器之间共享，并且不会增加容器可写层的大小。
> 请参阅 [使用卷](../volumes.md) 部分以了解卷。

`copy_up` 操作会产生明显的性能开销。此开销因使用的存储驱动程序而异。
大文件、大量层和深层目录树会使影响更加明显。
通过以下事实可以缓解这种情况：每个 `copy_up` 操作仅在首次修改给定文件时发生。

为了验证写时复制的工作方式，以下过程启动了 5 个基于我们之前构建的 `acme/my-final-image:1.0` 镜像的容器，
并检查它们占用了多少空间。

1. 在 Docker 主机的终端上，运行以下 `docker run` 命令。末尾的字符串是每个容器的 ID。

   ```console
   $ docker run -dit --name my_container_1 acme/my-final-image:1.0 bash \
     && docker run -dit --name my_container_2 acme/my-final-image:1.0 bash \
     && docker run -dit --name my_container_3 acme/my-final-image:1.0 bash \
     && docker run -dit --name my_container_4 acme/my-final-image:1.0 bash \
     && docker run -dit --name my_container_5 acme/my-final-image:1.0 bash

   40ebdd7634162eb42bdb1ba76a395095527e9c0aa40348e6c325bd0aa289423c
   a5ff32e2b551168b9498870faf16c9cd0af820edf8a5c157f7b80da59d01a107
   3ed3c1a10430e09f253704116965b01ca920202d52f3bf381fbb833b8ae356bc
   939b3bf9e7ece24bcffec57d974c939da2bdcc6a5077b5459c897c1e2fa37a39
   cddae31c314fbab3f7eabeb9b26733838187abc9a2ed53f97bd5b04cd7984a5a
   ```

2. 运行带有 `--size` 选项的 `docker ps` 命令，以验证 5 个容器正在运行，并查看每个容器的大小。

   
   ```console
   $ docker ps --size --format "table {{.ID}}\t{{.Image}}\t{{.Names}}\t{{.Size}}"

   CONTAINER ID   IMAGE                     NAMES            SIZE
   cddae31c314f   acme/my-final-image:1.0   my_container_5   0B (virtual 7.75MB)
   939b3bf9e7ec   acme/my-final-image:1.0   my_container_4   0B (virtual 7.75MB)
   3ed3c1a10430   acme/my-final-image:1.0   my_container_3   0B (virtual 7.75MB)
   a5ff32e2b551   acme/my-final-image:1.0   my_container_2   0B (virtual 7.75MB)
   40ebdd763416   acme/my-final-image:1.0   my_container_1   0B (virtual 7.75MB)
   ```
   
   上面的输出显示所有容器共享镜像的只读层（7.75MB），但没有数据写入容器的文件系统，因此容器没有使用额外的存储空间。

   




<div
  id="高级容器使用的元数据和日志存储"
  x-data="{ open: false }"
  class="my-6 rounded-sm border border-gray-200 bg-white py-2 dark:border-gray-700 dark:bg-gray-900"
>
  <button
    class="not-prose flex w-full justify-between px-4 py-2"
    x-on:click="open = ! open"
  >
    <div class=" flex items-center gap-2">
      高级：容器使用的元数据和日志存储
    </div>
    <span :class="{ 'hidden' : !open }" class="icon-svg"
      ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M316-400q-6.75 0-10.87-4.64-4.13-4.63-4.13-10.81 0-1.55 5-10.55l158-157q3-3 7.06-5 4.07-2 8.94-2 4.88 0 8.94 2t7.06 5l158 157q2 2 3.5 4.76 1.5 2.77 1.5 5.92 0 6.32-4.12 10.82-4.13 4.5-10.88 4.5H316Z"/></svg></span
    >
    <span :class="{ 'hidden' : open }" class="icon-svg"
      ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M464-376 306-533q-2-2-3.5-4.76-1.5-2.77-1.5-5.92 0-6.32 4.13-10.82 4.12-4.5 10.87-4.5h328q6.75 0 10.88 4.64 4.12 4.63 4.12 10.81 0 1.55-5 10.55L496-376q-3 3-7.06 5t-8.94 2q-4.87 0-8.94-2-4.06-2-7.06-5Z"/></svg></span
    >
  </button>
  <div x-show="open" x-collapse class="px-4">
    

  

  <blockquote
    
    class="admonition admonition-note admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 16V12M12 8H12.01M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

      </span>
      <span class="admonition-title">
        Note
      </span>
    </div>
    <div class="admonition-content">
      <p>此步骤需要 Linux 机器，在 Docker Desktop 上不起作用，因为它需要访问 Docker 守护进程的文件存储。</p>
    </div>
  </blockquote>

<p>虽然 <code>docker ps</code> 的输出提供了有关容器可写层消耗的磁盘空间的信息，但它不包括有关为每个容器存储的元数据和日志文件的信息。</p>
<p>通过探索 Docker 守护进程的存储位置（默认为 <code>/var/lib/docker/</code>）可以获得更多详细信息。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBzdWRvIGR1IC1zaCAvdmFyL2xpYi9kb2NrZXIvY29udGFpbmVycy8qCgozNksgIC92YXIvbGliL2RvY2tlci9jb250YWluZXJzLzNlZDNjMWExMDQzMGUwOWYyNTM3MDQxMTY5NjViMDFjYTkyMDIwMmQ1MmYzYmYzODFmYmI4MzNiOGFlMzU2YmMKMzZLICAvdmFyL2xpYi9kb2NrZXIvY29udGFpbmVycy80MGViZGQ3NjM0MTYyZWI0MmJkYjFiYTc2YTM5NTA5NTUyN2U5YzBhYTQwMzQ4ZTZjMzI1YmQwYWEyODk0MjNjCjM2SyAgL3Zhci9saWIvZG9ja2VyL2NvbnRhaW5lcnMvOTM5YjNiZjllN2VjZTI0YmNmZmVjNTdkOTc0YzkzOWRhMmJkY2M2YTUwNzdiNTQ1OWM4OTdjMWUyZmEzN2EzOQozNksgIC92YXIvbGliL2RvY2tlci9jb250YWluZXJzL2E1ZmYzMmUyYjU1MTE2OGI5NDk4ODcwZmFmMTZjOWNkMGFmODIwZWRmOGE1YzE1N2Y3YjgwZGE1OWQwMWExMDcKMzZLICAvdmFyL2xpYi9kb2NrZXIvY29udGFpbmVycy9jZGRhZTMxYzMxNGZiYWIzZjdlYWJlYjliMjY3MzM4MzgxODdhYmM5YTJlZDUzZjk3YmQ1YjA0Y2Q3OTg0YTVh', copying: false }"
        class="
          top-1
         absolute right-2 z-10 text-gray-300 dark:text-gray-500"
        title="copy"
        @click="window.navigator.clipboard.writeText(atob(code).replaceAll(/^[\$>]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);"
      >
        <span
          :class="{ 'group-hover:block' : !copying }"
          class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M300-200q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h440q24 0 42 18t18 42v560q0 24-18 42t-42 18H300ZM180-80q-24 0-42-18t-18-42v-590q0-13 8.5-21.5T150-760q13 0 21.5 8.5T180-730v590h470q13 0 21.5 8.5T680-110q0 13-8.5 21.5T650-80H180Z"/></svg></span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m421-389-98-98q-9-9-22-9t-23 10q-9 9-9 22t9 22l122 123q9 9 21 9t21-9l239-239q10-10 10-23t-10-23q-10-9-23.5-8.5T635-603L421-389Zm59 309q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Z"/></svg></span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> sudo du -sh /var/lib/docker/containers/*
</span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="go">36K  /var/lib/docker/containers/3ed3c1a10430e09f253704116965b01ca920202d52f3bf381fbb833b8ae356bc
</span></span></span><span class="line"><span class="cl"><span class="go">36K  /var/lib/docker/containers/40ebdd7634162eb42bdb1ba76a395095527e9c0aa40348e6c325bd0aa289423c
</span></span></span><span class="line"><span class="cl"><span class="go">36K  /var/lib/docker/containers/939b3bf9e7ece24bcffec57d974c939da2bdcc6a5077b5459c897c1e2fa37a39
</span></span></span><span class="line"><span class="cl"><span class="go">36K  /var/lib/docker/containers/a5ff32e2b551168b9498870faf16c9cd0af820edf8a5c157f7b80da59d01a107
</span></span></span><span class="line"><span class="cl"><span class="go">36K  /var/lib/docker/containers/cddae31c314fbab3f7eabeb9b26733838187abc9a2ed53f97bd5b04cd7984a5a
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>这些容器中的每一个在文件系统上仅占用 36k 的空间。</p>

  </div>
</div>



3. 每个容器的存储

   为了演示这一点，运行以下命令，将单词 'hello' 写入容器 `my_container_1`、`my_container_2` 和 `my_container_3` 的可写层上的文件中：

   ```console
   $ for i in {1..3}; do docker exec my_container_$i sh -c 'printf hello > /out.txt'; done
   ```
   
   之后再次运行 `docker ps` 命令，显示这些容器现在每个消耗 5 个字节。此数据是每个容器独有的，不共享。
   容器的只读层不受影响，并且仍然由所有容器共享。

   
   ```console
   $ docker ps --size --format "table {{.ID}}\t{{.Image}}\t{{.Names}}\t{{.Size}}"

   CONTAINER ID   IMAGE                     NAMES            SIZE
   cddae31c314f   acme/my-final-image:1.0   my_container_5   0B (virtual 7.75MB)
   939b3bf9e7ec   acme/my-final-image:1.0   my_container_4   0B (virtual 7.75MB)
   3ed3c1a10430   acme/my-final-image:1.0   my_container_3   5B (virtual 7.75MB)
   a5ff32e2b551   acme/my-final-image:1.0   my_container_2   5B (virtual 7.75MB)
   40ebdd763416   acme/my-final-image:1.0   my_container_1   5B (virtual 7.75MB)
   ```

前面的例子说明了写时复制文件系统如何帮助使容器高效。写时复制不仅节省空间，还减少了容器启动时间。
当您创建一个容器（或从同一镜像创建多个容器）时，Docker 只需要创建薄的可写容器层。

如果 Docker 每次创建新容器时都必须复制整个底层镜像堆栈，容器创建时间和使用的磁盘空间将显著增加。
这将类似于虚拟机的工作方式，每个虚拟机有一个或多个虚拟磁盘。[`vfs` 存储](vfs-driver.md)
不提供 CoW 文件系统或其他优化。使用此存储驱动程序时，会为每个容器创建镜像数据的完整副本。

## 相关信息

* [卷](../volumes.md)
* [选择存储驱动程序](select-storage-driver.md)

- [选择存储驱动程序](/engine/storage/drivers/select-storage-driver/)

- [AUFS 存储驱动程序](/engine/storage/drivers/aufs-driver/)

- [BTRFS 存储驱动](/engine/storage/drivers/btrfs-driver/)

- [Device Mapper 存储驱动程序（已弃用）](/engine/storage/drivers/device-mapper-driver/)

- [OverlayFS 存储驱动程序](/engine/storage/drivers/overlayfs-driver/)

- [VFS 存储驱动](/engine/storage/drivers/vfs-driver/)

- [windowsfilter 存储驱动程序](/engine/storage/drivers/windowsfilter-driver/)

- [ZFS 存储驱动程序](/engine/storage/drivers/zfs-driver/)

