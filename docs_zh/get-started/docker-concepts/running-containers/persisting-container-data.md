---
title: 持久化容器数据
weight: 3
keywords: 概念, 构建, 镜像, 容器, Docker Desktop
description: 本概念页面将向你介绍 Docker 中数据持久化的重要性
aliases:
 - /guides/walkthroughs/persist-data/
 - /guides/docker-concepts/running-containers/persisting-container-data/
---

{{< youtube-embed 10_2BjqB_Ls >}}

## 说明

当容器启动时，它使用镜像提供的文件和配置。每个容器都能够创建、修改和删除文件，且这些操作不会影响其他容器。当容器被删除时，这些文件更改也会被删除。

虽然容器的这种短暂特性很好，但它在需要持久化数据时带来了挑战。例如，如果你重启一个数据库容器，你可能不希望从一个空数据库开始。那么，如何持久化文件呢？

### 容器卷

卷是一种存储机制，它提供了在单个容器生命周期之外持久化数据的能力。你可以将其理解为在容器内部和外部之间提供一个快捷方式或符号链接。

举个例子，假设你创建了一个名为 `log-data` 的卷。

```console
$ docker volume create log-data
```

当使用以下命令启动容器时，该卷将被挂载（或附加）到容器的 `/logs` 目录：

```console
$ docker run -d -p 80:80 -v log-data:/logs docker/welcome-to-docker
```

如果卷 `log-data` 不存在，Docker 会自动为你创建它。

当容器运行时，它写入 `/logs` 文件夹的所有文件都将保存在这个卷中，位于容器外部。如果你删除容器并使用同一卷启动新容器，文件仍然会存在。

> **使用卷共享文件**
>
> 你可以将同一卷附加到多个容器，以在容器之间共享文件。这在日志聚合、数据管道或其他事件驱动应用等场景中可能很有用。

### 管理卷

卷的生命周期超越容器本身，根据你使用的数据和应用类型，卷可能会变得相当大。以下命令将有助于管理卷：

- `docker volume ls` - 列出所有卷
- `docker volume rm <volume-name-or-id>` - 删除卷（仅在卷未附加到任何容器时生效）
- `docker volume prune` - 删除所有未使用（未附加）的卷



## 动手实践

在本指南中，你将练习创建和使用卷来持久化 Postgres 容器创建的数据。当数据库运行时，它将文件存储到 `/var/lib/postgresql` 目录。通过在此处附加卷，你将能够多次重启容器，同时保留数据。

### 使用卷

1. [下载并安装](/get-started/get-docker/) Docker Desktop。

2. 使用 [Postgres 镜像](https://hub.docker.com/_/postgres) 启动容器，命令如下：

    ```console
    $ docker run --name=db -e POSTGRES_PASSWORD=secret -d -v postgres_data:/var/lib/postgresql postgres:18
    ```

    这将使数据库在后台运行，使用密码配置它，并将卷附加到 PostgreSQL 持久化数据库文件的目录。

3. 使用以下命令连接到数据库：

    ```console
    $ docker exec -ti db psql -U postgres
    ```

4. 在 PostgreSQL 命令行中，运行以下命令创建一个数据库表并插入两条记录：

    ```text
    CREATE TABLE tasks (
        id SERIAL PRIMARY KEY,
        description VARCHAR(100)
    );
    INSERT INTO tasks (description) VALUES ('Finish work'), ('Have fun');
    ```

5. 通过在 PostgreSQL 命令行中运行以下命令验证数据是否在数据库中：

    ```text
    SELECT * FROM tasks;
    ```

    你应该得到如下输出：

    ```text
     id | description
    ----+-------------
      1 | Finish work
      2 | Have fun
    (2 rows)
    ```

6. 通过运行以下命令退出 PostgreSQL shell：

    ```console
    \q
    ```

7. 停止并删除数据库容器。请记住，即使容器已被删除，数据仍持久化在 `postgres_data` 卷中。

    ```console
    $ docker stop db
    $ docker rm db
    ```

8. 使用以下命令启动新容器，附加带有持久化数据的同一卷：

    ```console
    $ docker run --name=new-db -d -v postgres_data:/var/lib/postgresql postgres:18
    ```

    你可能注意到 `POSTGRES_PASSWORD` 环境变量已被省略。这是因为该变量仅在引导新数据库时使用。

9. 通过运行以下命令验证数据库仍然有记录：

    ```console
    $ docker exec -ti new-db psql -U postgres -c "SELECT * FROM tasks"
    ```

### 查看卷内容

Docker Desktop 仪表板提供了查看任何卷内容的能力，以及导出、导入和克隆卷的能力。

1. 打开 Docker Desktop 仪表板并导航到 **Volumes** 视图。在此视图中，你应该看到 **postgres_data** 卷。

2. 选择 **postgres_data** 卷的名称。

3. **Data** 选项卡显示卷的内容，并提供浏览文件的能力。双击文件可以查看其内容并进行修改。

4. 右键点击任何文件可以保存或删除它。


### 删除卷

在删除卷之前，它不能附加到任何容器。如果你还没有删除之前的容器，请使用以下命令删除（`-f` 会先停止容器，然后删除它）：

```console
$ docker rm -f new-db
```

有几种方法可以删除卷，包括：

- 在 Docker Desktop 仪表板中选择卷的 **Delete Volume** 选项。
- 使用 `docker volume rm` 命令：

    ```console
    $ docker volume rm postgres_data
    ```
- 使用 `docker volume prune` 命令删除所有未使用的卷：

    ```console
    $ docker volume prune
    ```


## 额外资源

以下资源将帮助你更深入地了解卷：

- [在 Docker 中管理数据](/engine/storage)
- [卷](/engine/storage/volumes)
- [卷挂载](/engine/containers/run/#volume-mounts)


## 下一步

现在你已经了解了持久化容器数据，是时候学习如何与容器共享本地文件了。

{{< button text="与容器共享本地文件" url="sharing-local-files" >}}


