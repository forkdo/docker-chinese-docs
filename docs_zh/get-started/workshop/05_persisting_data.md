---
title: 持久化数据库
weight: 50
linkTitle: "第四部分：持久化数据库"
keywords: 快速开始, 设置, 方向, 快速入门, 介绍, 概念, 容器,
  docker desktop
description: 在应用程序中持久化数据库
aliases:
 - /get-started/05_persisting_data/
 - /guides/workshop/05_persisting_data/
---

如果您没注意到，每次启动容器时，待办列表都是空的。为什么会出现这种情况？在本部分中，您将深入了解容器的工作原理。

## 容器的文件系统

当容器运行时，它使用镜像的各个层作为其文件系统。每个容器还会获得自己的“临时存储空间”来创建/更新/删除文件。任何更改都不会在另一个容器中看到，即使它们使用相同的镜像。

### 实践演示

为了实际演示这一点，您将启动两个容器。在一个容器中，您将创建一个文件。在另一个容器中，您将检查该文件是否存在。

1. 启动一个 Alpine 容器，并在其中创建一个新文件。

    ```console
    $ docker run --rm alpine touch greeting.txt
    ```

    > [!TIP]
    > 您在镜像名称（本例中为 `alpine`）后指定的任何命令都会在容器内执行。在本例中，命令 `touch
    > greeting.txt` 会在容器的文件系统上放置一个名为 `greeting.txt` 的文件。

2. 运行一个新的 Alpine 容器，并使用 `stat` 命令检查文件是否存在。
   
   ```console
   $ docker run --rm alpine stat greeting.txt
   ```

   您应该看到类似以下的输出，表明该文件在新容器中不存在。

   ```console
   stat: can't stat 'greeting.txt': No such file or directory
   ```

第一个容器创建的 `greeting.txt` 文件在第二个容器中不存在。这是因为每个容器的可写“顶层”是隔离的。即使两个容器共享构成基础镜像的相同底层，但可写层对每个容器来说是唯一的。

## 容器卷

通过前面的实验，您看到每个容器每次启动时都从镜像定义开始。虽然容器可以创建、更新和删除文件，但这些更改在删除容器时会丢失，Docker 将所有更改隔离到该容器中。使用卷，您可以改变所有这些。

[卷](/manuals/engine/storage/volumes.md) 提供了将容器特定文件系统路径连接回主机机器的能力。如果您挂载容器中的目录，该目录中的更改也会在主机机器上看到。如果您在容器重启时挂载同一目录，您会看到相同的文件。

有两种主要类型的卷。最终您会使用两者，但您将从卷挂载开始。

## 持久化待办数据

默认情况下，待办应用将其数据存储在容器文件系统中的 `/etc/todos/todo.db` 处的 SQLite 数据库中。如果您不熟悉 SQLite，不用担心！它只是一个将所有数据存储在单个文件中的关系型数据库。虽然这对于大规模应用来说不是最佳选择，但对小规模演示来说是有效的。稍后您将学习如何切换到不同的数据库引擎。

由于数据库是单个文件，如果您可以在主机上持久化该文件并使其对下一个容器可用，它应该能够从上一个容器停止的地方继续。通过创建一个卷并将其附加（通常称为“挂载”）到存储数据的目录，您可以持久化数据。当您的容器写入 `todo.db` 文件时，它会将数据持久化到主机上的卷中。

如前所述，您将使用卷挂载。将卷挂载视为一个不透明的数据桶。Docker 完全管理卷，包括磁盘上的存储位置。您只需要记住卷的名称。

### 创建卷并启动容器

您可以使用 CLI 或 Docker Desktop 的图形界面创建卷并启动容器。

{{< tabs >}}
{{< tab name="CLI" >}}

1. 使用 `docker volume create` 命令创建一个卷。

   ```console
   $ docker volume create todo-db
   ```

2. 再次使用 `docker rm -f <id>` 停止并删除待办应用容器，因为它仍在运行而未使用持久卷。

3. 启动待办应用容器，但添加 `--mount` 选项来指定卷挂载。给卷命名，并将其挂载到容器中的 `/etc/todos`，这会捕获在该路径创建的所有文件。

   ```console
   $ docker run -dp 127.0.0.1:3000:3000 --mount type=volume,src=todo-db,target=/etc/todos getting-started
   ```

   > [!NOTE]
   >
   > 如果您使用 Git Bash，必须为此命令使用不同的语法。
   >
   > ```console
   > $ docker run -dp 127.0.0.1:3000:3000 --mount type=volume,src=todo-db,target=//etc/todos getting-started
   > ```
   >
   > 有关 Git Bash 语法差异的更多详细信息，请参阅
   > [使用 Git Bash](/desktop/troubleshoot-and-support/troubleshoot/topics/#docker-commands-failing-in-git-bash)。


{{< /tab >}}
{{< tab name="Docker Desktop" >}}

创建卷：

1. 在 Docker Desktop 中选择 **Volumes**。
2. 在 **Volumes** 中，选择 **Create**。
3. 指定 `todo-db` 作为卷名，然后选择 **Create**。

停止并删除应用容器：

1. 在 Docker Desktop 中选择 **Containers**。
2. 在 **Actions** 列中选择容器的 **Delete**。

使用挂载的卷启动待办应用容器：

1. 选择 Docker Desktop 顶部的搜索框。
2. 在搜索窗口中，选择 **Images** 选项卡。
3. 在搜索框中，指定镜像名称 `getting-started`。

   > [!TIP]
   >
   > 使用搜索过滤器过滤镜像，仅显示 **Local images**。

4. 选择您的镜像，然后选择 **Run**。
5. 选择 **Optional settings**。
6. 在 **Host port** 中，指定端口，例如 `3000`。
7. 在 **Host path** 中，指定卷名 `todo-db`。
8. 在 **Container path** 中，指定 `/etc/todos`。
9. 选择 **Run**。

{{< /tab >}}
{{< /tabs >}}

### 验证数据持久化

1. 容器启动后，打开应用并向待办列表添加几项。

    ![添加到待办列表的项目](images/items-added.webp)
    

2. 停止并删除待办应用的容器。使用 Docker Desktop 或 `docker ps` 获取 ID，然后使用 `docker rm -f <id>` 删除它。

3. 使用前面的步骤启动一个新容器。

4. 打开应用。您应该看到您的项目仍然在列表中。

5. 检查完列表后，继续删除容器。

现在您已经学会了如何持久化容器数据。

## 深入了解卷

很多人经常问“当我使用卷时，Docker 在磁盘上的哪里存储我的数据？”如果您想知道，可以使用 `docker volume inspect` 命令。

```console
$ docker volume inspect todo-db
```
您应该看到类似以下的输出：
```console
[
    {
        "CreatedAt": "2019-09-26T02:18:36Z",
        "Driver": "local",
        "Labels": {},
        "Mountpoint": "/var/lib/docker/volumes/todo-db/_data",
        "Name": "todo-db",
        "Options": {},
        "Scope": "local"
    }
]
```

`Mountpoint` 是磁盘上数据的实际位置。注意，在大多数机器上，您需要具有 root 权限才能从主机访问此目录。

## 总结

在本部分中，您学习了如何持久化容器数据。

相关信息：

 - [docker CLI 参考](/reference/cli/docker/)
 - [卷](/manuals/engine/storage/volumes.md)

## 下一步

接下来，您将学习如何使用绑定挂载更高效地开发应用。

{{< button text="使用绑定挂载" url="06_bind_mounts.md" >}}
