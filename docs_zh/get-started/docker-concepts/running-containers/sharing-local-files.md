---
title: 使用容器共享本地文件
weight: 4
keywords: 概念, 镜像, 容器, Docker Desktop
description: 本概念页面将向您介绍 Docker 中可用的各种存储选项及其常见用法。
aliases: 
 - /guides/docker-concepts/running-containers/sharing-local-files/
---

{{< youtube-embed 2dAzsVg3Dek >}}


## 说明

每个容器都包含其运行所需的一切，不依赖于主机上预安装的任何依赖项。由于容器是隔离运行的，它们对主机和其他容器几乎没有影响。这种隔离带来了一个主要好处：容器最大限度地减少了与主机系统和其他容器的冲突。但这种隔离也意味着默认情况下容器无法直接访问主机上的数据。

考虑这样一种场景：您有一个 Web 应用容器，需要访问存储在主机系统文件中的配置设置。该文件可能包含敏感数据，如数据库凭据或 API 密钥。将此类敏感信息直接存储在容器镜像中会带来安全风险，尤其是在共享镜像时。为了解决这一挑战，Docker 提供了存储选项，在容器隔离与主机数据之间架起了桥梁。

Docker 提供两种主要的存储选项，用于在主机和容器之间持久化数据和共享文件：卷（volumes）和绑定挂载（bind mounts）。

### 卷与绑定挂载

如果您希望确保容器内生成或修改的数据在容器停止后依然保留，应选择卷。请参阅 [持久化容器数据](/get-started/docker-concepts/running-containers/persisting-container-data/) 了解卷及其用例的更多信息。

如果您有主机上的特定文件或目录需要直接与容器共享（如配置文件或开发代码），则应使用绑定挂载。它就像在主机和容器之间打开一个直接通道用于共享。绑定挂载非常适合开发环境，因为实时文件访问和主机与容器之间的共享至关重要。

### 主机与容器之间共享文件

`docker run` 命令中的 `-v`（或 `--volume`）和 `--mount` 标志都允许您在本地机器（主机）和 Docker 容器之间共享文件或目录。但它们在行为和用法上存在一些关键差异。

`-v` 标志更简单，对于基本的卷或绑定挂载操作更方便。如果使用 `-v` 或 `--volume` 时主机位置不存在，会自动创建一个目录。

想象一下，您是一名开发人员，正在开发一个项目。您的开发机器上有一个源目录，代码位于其中。当您编译或构建代码时，生成的构件（编译后的代码、可执行文件、镜像等）会保存在源目录内的一个单独子目录中。在以下示例中，此子目录为 `/HOST/PATH`。现在您希望这些构建构件在运行应用程序的 Docker 容器内可访问。此外，您希望容器在每次重新构建代码时自动访问最新的构建构件。

以下是使用 `docker run` 启动容器并使用绑定挂载映射到容器文件位置的方法：

```console
$ docker run -v /HOST/PATH:/CONTAINER/PATH -it nginx
```

`--mount` 标志提供更高级的功能和更精细的控制，适合复杂的挂载场景或生产部署。如果您使用 `--mount` 绑定挂载主机上尚不存在的文件或目录，`docker run` 命令不会自动为您创建，而是会生成错误。

```console
$ docker run --mount type=bind,source=/HOST/PATH,target=/CONTAINER/PATH,readonly nginx
```

> [!NOTE]
>
> Docker 建议使用 `--mount` 语法而非 `-v`。它提供更好的挂载过程控制，并避免目录缺失时的潜在问题。

### Docker 访问主机文件的文件权限

使用绑定挂载时，确保 Docker 具有访问主机目录所需的权限至关重要。要在创建容器期间授予读写访问权限，您可以使用 `-v` 或 `--mount` 标志的 `:ro` 标志（只读）或 `:rw`（读写）。
例如，以下命令授予读写访问权限：

```console
$ docker run -v HOST-DIRECTORY:/CONTAINER-DIRECTORY:rw nginx
```

只读绑定挂载允许容器访问主机上的挂载文件进行读取，但不能更改或删除文件。使用读写绑定挂载，容器可以修改或删除挂载的文件，这些更改或删除也会反映在主机系统上。只读绑定挂载确保主机上的文件不会被容器意外修改或删除。

> **同步文件共享**
>
> 随着代码库的增长，传统的文件共享方法（如绑定挂载）可能变得效率低下或缓慢，尤其是在需要频繁访问文件的开发环境中。[同步文件共享](/manuals/desktop/features/synchronized-file-sharing.md) 通过利用同步文件系统缓存来提高绑定挂载性能。此优化确保主机和虚拟机（VM）之间的文件访问快速高效。

## 动手实践

在本实践指南中，您将练习如何创建和使用绑定挂载在主机和容器之间共享文件。

### 运行容器

1. [下载并安装](/get-started/get-docker/) Docker Desktop。

2. 使用 [httpd](https://hub.docker.com/_/httpd) 镜像启动容器，命令如下：

   ```console
   $ docker run -d -p 8080:80 --name my_site httpd:2.4
   ```

   这将在后台启动 `httpd` 服务，并将网页发布到主机的 `8080` 端口。

3. 打开浏览器访问 [http://localhost:8080](http://localhost:8080) 或使用 curl 命令验证是否正常工作。

    ```console
    $ curl localhost:8080
    ```


### 使用绑定挂载

使用绑定挂载，您可以将主机计算机上的配置文件映射到容器内的特定位置。在此示例中，您将看到如何通过使用绑定挂载来更改网页的外观：

1. 使用 Docker Desktop 仪表板删除现有容器：

   ![Docker Desktop 仪表板截图，显示如何删除 httpd 容器](images/delete-httpd-container.webp?border=true)


2. 在主机系统上创建一个名为 `public_html` 的新目录。

    ```console
    $ mkdir public_html
    ```

3. 导航到新创建的目录 `public_html`，并创建一个名为 `index.html` 的文件，内容如下。这是一个基本的 HTML 文档，创建一个简单的网页，以友好的鲸鱼欢迎您。

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title> My Website with a Whale & Docker!</title>
    </head>
    <body>
    <h1>Whalecome!!</h1>
    <p>Look! There's a friendly whale greeting you!</p>
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

4. 现在启动容器。`--mount` 和 `-v` 示例产生相同的结果。除非您在运行第一个后删除 `my_site` 容器，否则无法同时运行它们。

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
   > 在 Windows PowerShell 中使用 `-v` 或 `--mount` 标志时，您需要提供目录的绝对路径，而不是仅 `./`。这是因为 PowerShell 处理相对路径的方式与 bash（通常在 Mac 和 Linux 环境中使用）不同。    



   现在一切就绪，您应该能够通过 [http://localhost:8080](http://localhost:8080) 访问网站，并看到一个以友好的鲸鱼欢迎您的新网页。


### 在 Docker Desktop 仪表板中访问文件

1. 您可以通过选择容器的 **Files** 选项卡，然后选择 `/usr/local/apache2/htdocs/` 目录内的文件来查看容器内挂载的文件。然后，选择 **Open file editor**。


   ![Docker Desktop 仪表板截图，显示容器内挂载的文件](images/mounted-files.webp?border=true)

2. 删除主机上的文件并验证容器中的文件也被删除。您会发现文件在 Docker Desktop 仪表板的 **Files** 下不再存在。


   ![Docker Desktop 仪表板截图，显示容器内已删除的文件](images/deleted-files.webp?border=true)


3. 在主机系统上重新创建 HTML 文件，查看文件在 Docker Desktop 仪表板的 **Containers** 下 **Files** 选项卡中重新出现。此时，您也应该能够访问网站了。



### 停止容器

容器会持续运行，直到您停止它。

1. 转到 Docker Desktop 仪表板的 **Containers** 视图。

2. 找到您要停止的容器。

3. 在操作列中选择 **Stop** 操作。

## 额外资源

以下资源将帮助您进一步了解绑定挂载：

* [管理 Docker 中的数据](/storage/)
* [卷](/storage/volumes/)
* [绑定挂载](/storage/bind-mounts/)
* [运行容器](/reference/run/)
* [排查存储错误](/storage/troubleshooting_volume_errors/)
* [持久化容器数据](/get-started/docker-concepts/running-containers/persisting-container-data/)

## 下一步

现在您已经了解了与容器共享本地文件的知识，是时候学习多容器应用程序了。

{{< button text="多容器应用程序" url="Multi-container applications" >}}
