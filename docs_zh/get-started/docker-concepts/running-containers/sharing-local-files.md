---
title: 与容器共享本地文件
weight: 4
keywords: concepts, images, container, docker desktop
description: &desc 本概念页面将向您介绍 Docker 中可用的各种存储选项及其常见用途。
aliases: 
 - /guides/docker-concepts/running-containers/sharing-local-files/
---

{{< youtube-embed 2dAzsVg3Dek >}}


## 说明

每个容器都包含其运行所需的一切，不依赖主机上预装的任何依赖项。由于容器是隔离运行的，它们对主机和其他容器的影响极小。这种隔离有一个主要好处：容器可以最大程度减少与主机系统及其他容器的冲突。然而，这种隔离也意味着容器默认无法直接访问主机上的数据。

设想一个场景：您有一个 Web 应用容器，需要访问存储在主机系统文件中的配置设置。该文件可能包含敏感数据，例如数据库凭据或 API 密钥。将这些敏感信息直接存储在容器镜像中会带来安全风险，尤其是在共享镜像时。为了解决这一挑战，Docker 提供了存储选项，以弥合容器隔离与主机数据之间的差距。

Docker 提供了两种主要的存储选项，用于持久化数据以及在主机和容器之间共享文件：volumes 和 bind mounts。

### Volume 与 bind mounts 对比

如果您希望确保容器内生成或修改的数据在容器停止运行后仍然保留，您应该选择 volume。请参阅[持久化容器数据](/get-started/docker-concepts/running-containers/persisting-container-data/)，了解有关 volume 及其用例的更多信息。

如果您有主机系统上的特定文件或目录希望直接与容器共享，例如配置文件或开发代码，那么您应该使用 bind mount。这就像在主机和容器之间打开一个直接共享的通道。bind mounts 非常适合开发环境，其中主机和容器之间的实时文件访问和共享至关重要。

### 在主机和容器之间共享文件

与 `docker run` 命令一起使用的 `-v`（或 `--volume`）和 `--mount` 标志都允许您在本地主机（主机）和 Docker 容器之间共享文件或目录。然而，它们的行为和用法存在一些关键差异。

`-v` 标志更简单，更适合基本的 volume 或 bind mount 操作。如果使用 `-v` 或 `--volume` 时主机位置不存在，将自动创建一个目录。

假设您是一名开发人员，正在开发一个项目。您在开发机器上有一个源代码目录，其中存放着您的代码。当您编译或构建代码时，生成的构件（编译后的代码、可执行文件、镜像等）将保存在源代码目录中的单独子目录中。在以下示例中，此子目录为 `/HOST/PATH`。现在，您希望这些构建构件能够在一个运行您应用的 Docker 容器中访问。此外，您还希望容器在每次重新构建代码时自动访问最新的构建构件。

以下是一种使用 `docker run` 启动容器并使用 bind mount 将其映射到容器文件位置的方法。

```console
$ docker run -v /HOST/PATH:/CONTAINER/PATH -it nginx
```

`--mount` 标志提供了更高级的功能和更精细的控制，使其适用于复杂的挂载场景或生产部署。如果您使用 `--mount` 来绑定挂载一个在 Docker 主机上尚不存在的文件或目录，`docker run` 命令不会自动为您创建它，而是生成一个错误。

```console
$ docker run --mount type=bind,source=/HOST/PATH,target=/CONTAINER/PATH,readonly nginx
```

> [!NOTE]
>
> Docker 建议使用 `--mount` 语法而不是 `-v`。它提供了对挂载过程的更好控制，并避免了目录缺失可能引发的问题。

### Docker 访问主机文件的文件权限

使用 bind mounts 时，确保 Docker 具有访问主机目录的必要权限至关重要。为了授予读写访问权限，您可以在创建容器时使用 `-v` 或 `--mount` 标志加上 `:ro`（只读）或 `:rw`（读写）。
例如，以下命令授予读写访问权限。

```console
$ docker run -v HOST-DIRECTORY:/CONTAINER-DIRECTORY:rw nginx
```

只读 bind mounts 允许容器访问主机上挂载的文件进行读取，但不能更改或删除这些文件。使用读写 bind mounts，容器可以修改或删除挂载的文件，这些更改或删除也会反映在主机系统上。只读 bind mounts 确保主机上的文件不会被容器意外修改或删除。

> **同步文件共享**
>
> 随着代码库的增大，传统的文件共享方法（如 bind mounts）可能变得低效或缓慢，尤其是在需要频繁访问文件的开发环境中。[同步文件共享](/manuals/desktop/features/synchronized-file-sharing.md)通过利用同步文件系统缓存来提高 bind mount 性能。这种优化确保主机和虚拟机（VM）之间的文件访问快速高效。

## 动手实践

在本实践指南中，您将练习如何创建和使用 bind mount 来在主机和容器之间共享文件。

### 运行容器

1. [下载并安装](/get-started/get-docker/) Docker Desktop。

2. 使用以下命令启动一个使用 [httpd](https://hub.docker.com/_/httpd) 镜像的容器：

   ```console
   $ docker run -d -p 8080:80 --name my_site httpd:2.4
   ```

   这将在后台启动 `httpd` 服务，并将网页发布到主机的 `8080` 端口。

3. 打开浏览器并访问 [http://localhost:8080](http://localhost:8080)，或使用 curl 命令验证其是否正常工作。

    ```console
    $ curl localhost:8080
    ```


### 使用 bind mount

使用 bind mount，您可以将主机上的配置文件映射到容器内的特定位置。在本示例中，您将看到如何使用 bind mount 通过更改网页的外观和感觉：

1. 使用 Docker Desktop 仪表板删除现有容器：

   ![Docker Desktop 仪表板截图，显示如何删除 httpd 容器](images/delete-httpd-container.webp?border=true)


2. 在主机系统上创建一个名为 `public_html` 的新目录。

    ```console
    $ mkdir public_html
    ```

3. 进入新创建的 `public_html` 目录，并创建一个名为 `index.html` 的文件，内容如下。这是一个基本的 HTML 文档，创建一个简单的网页，用友好的鲸鱼欢迎您。

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title> 我的网站与鲸鱼 & Docker!</title>
    </head>
    <body>
    <h1>鲸鱼欢迎您!!</h1>
    <p>看！有一条友好的鲸鱼在向您打招呼！</p>
    <pre id="docker-art">
       ##         .
      ## ## ##        ==
     ## ## ## ## ##    ===
     /"""""""""""""""""\___/ ===
   {                       /  ===-
   \______ O           __/
    \    \         __/
     \____\_______/

    Hello from Docker!
    </pre>
    </body>
    </html>
    ```

4. 是时候运行容器了。`--mount` 和 `-v` 示例会产生相同的结果。除非您在运行第一个容器后删除 `my_site` 容器，否则不能同时运行两者。

   {{< tabs >}}
   {{< tab name="`-v`" >}}

   ```console
   $ docker run -d --name my_site -p 8080:80 -v .:/usr/local/apache2/htdocs/ httpd:2.4
   ```

   {{< /tab >}}
   {{< tab name="`--mount`" >}}

   ```console
   $ docker run -d --name my_site -p 8080:80 --mount type=bind,source=./,target=/usr/local/apache2/htdocs/ httpd:2.4
   ```

   {{< /tab >}}
   {{< /tabs >}}


   > [!TIP]  
   > 在 Windows PowerShell 中使用 `-v` 或 `--mount` 标志时，您需要提供目录的绝对路径，而不仅仅是 `./`。这是因为 PowerShell 处理相对路径的方式与 bash（通常在 Mac 和 Linux 环境中使用）不同。    


   现在一切都在运行，您应该能够通过 [http://localhost:8080](http://localhost:8080) 访问该网站，并看到一个用友好的鲸鱼欢迎您的全新网页。


### 在 Docker Desktop 仪表板中访问文件

1. 您可以通过选择容器的 **Files** 选项卡，然后选择 `/usr/local/apache2/htdocs/` 目录中的文件，来查看容器内的挂载文件。然后，选择 **Open file editor**。


   ![Docker Desktop 仪表板截图，显示容器内的挂载文件](images/mounted-files.webp?border=true)

2. 删除主机上的文件，并验证文件是否也在容器中被删除。您会发现文件不再存在于 Docker Desktop 仪表板的 **Files** 下。


   ![Docker Desktop 仪表板截图，显示容器内已删除的文件](images/deleted-files.webp?border=true)


3. 在主机系统上重新创建 HTML 文件，并查看该文件是否重新出现在 Docker Desktop 仪表板的 **Containers** 下的 **Files** 选项卡中。此时，您也能够访问该网站。


### 停止您的容器

容器将继续运行，直到您停止它。

1. 转到 Docker Desktop 仪表板中的 **Containers** 视图。

2. 找到您希望停止的容器。

3. 在操作列中选择 **Stop** 操作。

## 其他资源

以下资源将帮助您了解更多关于 bind mounts 的信息：

* [管理 Docker 中的数据](/storage/)
* [Volumes](/storage/volumes/)
* [Bind mounts](/storage/bind-mounts/)
* [运行容器](/reference/run/)
* [排查存储错误](/storage/troubleshooting_volume_errors/)
* [持久化容器数据](/get-started/docker-concepts/running-containers/persisting-container-data/)

## 下一步

现在您已经学会了如何与容器共享本地文件，是时候学习多容器应用了。

{{< button text="多容器应用" url="Multi-container applications" >}}