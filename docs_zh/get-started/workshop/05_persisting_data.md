---
title: 持久化数据库
weight: 50
linkTitle: 第 4 部分：持久化数据库
keywords: 入门, 设置, 导向, 快速入门, 简介, 概念, 容器, docker desktop
description: 在应用程序中实现数据库持久化
aliases:
- /get-started/05_persisting_data/
- /guides/workshop/05_persisting_data/
---

如果你没有注意到，每次启动容器时，你的待办事项列表都是空的。为什么会这样？在本部分中，你将深入了解容器的工作原理。

## 容器的文件系统

当容器运行时，它使用镜像中的各个层作为其文件系统。
每个容器还会获得自己的“暂存空间”来创建/更新/删除文件。任何更改都不会在另一个容器中看到，即使它们使用的是同一个镜像。

### 实践演示

为了亲眼看到这一点，你将启动两个容器。在一个容器中，你将创建一个文件。在另一个容器中，你将检查该文件是否存在。

1. 启动一个 Alpine 容器并在其中创建一个新文件。

    ```console
    $ docker run --rm alpine touch greeting.txt
    ```

    > [!TIP]
    > 你在镜像名称（本例中为 `alpine`）之后指定的任何命令都会在容器内执行。在本例中，命令 `touch greeting.txt` 会在容器的文件系统上放置一个名为 `greeting.txt` 的文件。

2. 运行一个新的 Alpine 容器，并使用 `stat` 命令检查文件是否存在。
   
   ```console
   $ docker run --rm alpine stat greeting.txt
   ```

   你应该会看到类似以下的输出，表明该文件在新容器中不存在。

   ```console
   stat: can't stat 'greeting.txt': No such file or directory
   ```

第一个容器创建的 `greeting.txt` 文件在第二个容器中不存在。这是因为每个容器的可写“顶层”是隔离的。即使两个容器共享组成基础镜像的相同底层，可写层对于每个容器也是唯一的。

## 容器卷

通过之前的实验，你看到每个容器在每次启动时都从镜像定义开始。虽然容器可以创建、更新和删除文件，但当你移除容器时，这些更改会丢失，而且 Docker 会将所有更改隔离到该容器中。使用卷，你可以改变这一切。

[卷](/manuals/engine/storage/volumes.md) 提供了将容器的特定文件系统路径连接回主机的能力。如果你在容器中挂载一个目录，该目录中的更改也会在主机上看到。如果你在容器重启时挂载相同的目录，你会看到相同的文件。

主要有两种类型的卷。你最终会使用这两种，但你将从卷挂载开始。

## 持久化待办事项数据

默认情况下，待办事项应用将其数据存储在容器文件系统中 `/etc/todos/todo.db` 的 SQLite 数据库中。如果你不熟悉 SQLite，不用担心！它只是一个关系型数据库，将所有数据存储在单个文件中。虽然这对于大规模应用程序来说不是最佳选择，但对于小型演示来说很有效。稍后你将学习如何将其切换到不同的数据库引擎。

由于数据库是一个单文件，如果你能在主机上持久化该文件并使其对下一个容器可用，它就应该能够从上一个容器停止的地方继续。通过创建一个卷并将其附加（通常称为“挂载”）到你存储数据的目录，你可以持久化数据。当你的容器写入 `todo.db` 文件时，它会将数据持久化到主机上的卷中。

如前所述，你将使用卷挂载。可以将卷挂载视为一个不透明的数据桶。Docker 完全管理卷，包括磁盘上的存储位置。你只需要记住卷的名称。

### 创建卷并启动容器

你可以使用 CLI 或 Docker Desktop 的图形界面来创建卷并启动容器。

{{< tabs >}}
{{< tab name="CLI" >}}

1. 使用 `docker volume create` 命令创建卷。

   ```console
   $ docker volume create todo-db
   ```

2. 再次使用 `docker rm -f <id>` 停止并移除待办事项应用容器，因为它仍在运行且未使用持久卷。

3. 启动待办事项应用容器，但添加 `--mount` 选项以指定卷挂载。给卷一个名称，并将其挂载到容器中的 `/etc/todos`，这会捕获在该路径下创建的所有文件。

   ```console
   $ docker run -dp 127.0.0.1:3000:3000 --mount type=volume,src=todo-db,target=/etc/todos getting-started
   ```

   > [!NOTE]
   >
   > 如果你使用 Git Bash，必须为此命令使用不同的语法。
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
3. 指定 `todo-db` 作为卷名称，然后选择 **Create**。

停止并移除应用容器：

1. 在 Docker Desktop 中选择 **Containers**。
2. 在容器的 **Actions** 列中选择 **Delete**。

启动挂载了卷的待办事项应用容器：

1. 选择 Docker Desktop 顶部的搜索框。
2. 在搜索窗口中，选择 **Images** 选项卡。
3. 在搜索框中，指定镜像名称 `getting-started`。

   > [!TIP]
   >
   > 使用搜索过滤器过滤镜像，仅显示 **Local images**。

4. 选择你的镜像，然后选择 **Run**。
5. 选择 **Optional settings**。
6. 在 **Host port** 中，指定端口，例如 `3000`。
7. 在 **Host path** 中，指定卷的名称 `todo-db`。
8. 在 **Container path** 中，指定 `/etc/todos`。
9. 选择 **Run**。

{{< /tab >}}
{{< /tabs >}}

### 验证数据是否持久化

1. 容器启动后，打开应用并向你的待办事项列表添加几个项目。

    ![添加到待办事项列表的项目](images/items-added.webp)
    

2. 停止并移除待办事项应用的容器。使用 Docker Desktop 或 `docker ps` 获取 ID，然后使用 `docker rm -f <id>` 移除它。

3. 使用之前的步骤启动一个新容器。

4. 打开应用。你应该会看到你的项目仍在列表中。

5. 检查完列表后，继续移除容器。

你现在已学会如何持久化数据。

## 深入了解卷

很多人经常问“当我使用卷时，Docker 将我的数据存储在哪里？”如果你想了解，可以使用 `docker volume inspect` 命令。

```console
$ docker volume inspect todo-db
```
你应该会看到类似以下的输出：
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

`Mountpoint` 是磁盘上数据的实际位置。请注意，在大多数机器上，你需要 root 权限才能从主机访问此目录。

## 总结

在本节中，你学习了如何持久化容器数据。

相关信息：

 - [docker CLI 参考](/reference/cli/docker/)
 - [卷](/manuals/engine/storage/volumes.md)

## 下一步

接下来，你将学习如何使用绑定挂载更高效地开发你的应用。

{{< button text="使用绑定挂载" url="06_bind_mounts.md" >}}