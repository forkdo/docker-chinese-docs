---
description: 学习如何运行、连接和持久化本地容器化数据库中的数据。
keywords: database, mysql
title: 使用容器化数据库
summary: |
  学习如何高效地运行和管理容器化数据库。
tags: [databases]
aliases:
  - /guides/use-case/databases/
params:
  time: 20 minutes
---

使用本地容器化数据库提供了灵活性和便捷的设置方式，让你能够紧密地模拟生产环境，而无需传统数据库安装的开销。Docker 简化了这一过程，只需几个命令即可在隔离的容器中部署、管理和扩展数据库。

在本指南中，你将学习如何：

- 运行本地容器化数据库
- 访问容器化数据库的 shell
- 从主机连接到容器化数据库
- 从另一个容器连接到容器化数据库
- 在卷中持久化数据库数据
- 构建自定义数据库镜像
- 使用 Docker Compose 运行数据库

本指南使用 MySQL 镜像作为示例，但这些概念同样适用于其他数据库镜像。

## 前置条件

要跟随本指南操作，你必须安装 Docker。如需安装 Docker，请参阅 [获取 Docker](/get-started/get-docker.md)。

## 运行本地容器化数据库

大多数流行的数据库系统，包括 MySQL、PostgreSQL 和 MongoDB，都在 Docker Hub 上提供了 Docker 官方镜像。这些镜像是经过精心策划的镜像集合，遵循最佳实践，确保你能够访问最新的功能和安全更新。要开始使用，请访问 [Docker Hub](https://hub.docker.com) 并搜索你感兴趣的数据库。每个镜像的页面都提供了详细的运行容器、自定义设置和根据你的需求配置数据库的说明。有关本指南中使用的 MySQL 镜像的更多信息，请参阅 Docker Hub 上的 [MySQL 镜像](https://hub.docker.com/_/mysql) 页面。

要运行数据库容器，你可以使用 Docker Desktop GUI 或 CLI。

{{< tabs group="ui" >}}
{{< tab name="CLI" >}}

要使用 CLI 运行容器，在终端中运行以下命令：

```console
$ docker run --name my-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_DATABASE=mydb -d mysql:latest
```

在此命令中：

- `--name my-mysql` 为容器指定名称为 my-mysql，便于引用。
- `-e MYSQL_ROOT_PASSWORD=my-secret-pw` 设置 MySQL 的 root 密码为 my-secret-pw。请将 my-secret-pw 替换为你选择的安全密码。
- `-e MYSQL_DATABASE=mydb` 可选地创建一个名为 mydb 的数据库。你可以将 mydb 更改为所需的数据库名称。
- `-d` 在后台以分离模式运行容器。
- `mysql:latest` 指定使用最新版本的 MySQL 镜像。

要在终端中验证容器是否正在运行，运行 `docker ps` 命令。

{{< /tab >}}
{{< tab name="GUI" >}}

要使用 GUI 运行容器：

1. 在 Docker Desktop 仪表板中，选择窗口顶部的全局搜索。
2. 在搜索框中输入 `mysql`，如果未选中，请选择 `Images` 选项卡。
3. 将鼠标悬停在 `mysql` 镜像上，然后选择 `Run`。
   此时会显示 **Run a new container**（运行新容器）对话框。
4. 展开 **Optional settings**（可选设置）。
5. 在可选设置中，指定以下内容：

   - **Container name**（容器名称）：`my-mysql`
   - **Environment variables**（环境变量）：
     - `MYSQL_ROOT_PASSWORD`:`my-secret-pw`
     - `MYSQL_DATABASE`:`mydb`

   ![可选设置屏幕，已指定选项。](images/databases-1.webp)

6. 选择 `Run`。
7. 打开 Docker Desktop 仪表板中的 **Container**（容器）视图，验证容器是否正在运行。

{{< /tab >}}
{{< /tabs >}}

## 访问容器化数据库的 shell

当你在 Docker 容器中运行数据库时，你可能需要访问其 shell 来管理数据库、执行命令或执行管理任务。Docker 提供了一种使用 `docker exec` 命令直接执行此操作的简单方法。此外，如果你更喜欢图形界面，可以使用 Docker Desktop 的 GUI。

如果你还没有运行数据库容器，请参阅 [运行本地容器化数据库](#run-a-local-containerized-database)。

{{< tabs group="ui" >}}
{{< tab name="CLI" >}}

要使用 CLI 访问 MySQL 容器的终端，可以使用以下 `docker exec` 命令。

```console
$ docker exec -it my-mysql bash
```

在此命令中：

- `docker exec` 告诉 Docker 你想在正在运行的容器中执行命令。
- `-it` 确保你访问的终端是交互式的，因此你可以在其中键入命令。
- `my-mysql` 是你的 MySQL 容器的名称。如果你在运行容器时使用了不同的名称，请使用该名称。
- `bash` 是你想在容器中运行的命令。它会打开一个 bash shell，让你与容器的文件系统和已安装的应用程序进行交互。

执行此命令后，你将获得对 MySQL 容器内 bash shell 的访问权限，你可以直接管理 MySQL 服务器。你可以运行 `exit` 返回到你的终端。

{{< /tab >}}
{{< tab name="GUI" >}}

1. 打开 Docker Desktop 仪表板并选择 **Containers**（容器）视图。
2. 在容器的 **Actions**（操作）列中，选择 **Show container actions**（显示容器操作），然后选择 **Open in terminal**（在终端中打开）。

在此终端中，你可以访问 MySQL 容器内的 shell，从而直接管理你的 MySQL 服务器。

{{< /tab >}}
{{< /tabs >}}

一旦你访问了容器的终端，你就可以运行容器中可用的任何工具。以下示例展示了如何在容器中使用 `mysql` 列出数据库。

```console
# mysql -u root -p
Enter password: my-secret-pw

mysql> SHOW DATABASES;

+--------------------+
| Database           |
+--------------------+
| information_schema |
| mydb               |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)
```

## 从主机连接到容器化数据库

从主机机器连接到容器化数据库涉及将容器内的端口映射到主机机器上的端口。此过程确保容器内的数据库可通过主机机器的网络访问。对于 MySQL，默认端口是 3306。通过暴露此端口，你可以使用主机机器上的各种数据库管理工具或应用程序与 MySQL 数据库进行交互。

在开始之前，你必须删除之前为此指南运行的任何容器。要停止并删除容器，可以：

- 在终端中运行 `docker rm --force my-mysql` 删除名为 `my-mysql` 的容器。
- 或者，在 Docker Desktop 仪表板中，在 **Containers**（容器）视图中选择容器旁边的 **Delete**（删除）图标，然后选择 **Delete forever**（永久删除）。

接下来，你可以使用 Docker Desktop GUI 或 CLI 在映射端口的情况下运行容器。

{{< tabs group="ui" >}}
{{< tab name="CLI" >}}

在终端中运行以下命令。

```console
$ docker run -p 3307:3306 --name my-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_DATABASE=mydb -d mysql:latest
```

在此命令中，`-p 3307:3306` 将主机上的端口 3307 映射到容器中的端口 3306。

要验证端口已映射，运行以下命令。

```console
$ docker ps
```

你应该看到如下输出。

```console
CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS          PORTS                               NAMES
6eb776cfd73c   mysql:latest   "docker-entrypoint.s…"   17 minutes ago   Up 17 minutes   33060/tcp, 0.0.0.0:3307->3306/tcp   my-mysql
```

{{< /tab >}}
{{< tab name="GUI" >}}

要使用 GUI 运行容器：

1. 在 Docker Desktop 仪表板中，选择窗口顶部的全局搜索。
2. 在搜索框中输入 `mysql`，如果未选中，请选择 `Images` 选项卡。
3. 将鼠标悬停在 `mysql` 镜像上，然后选择 `Run`。
   此时会显示 **Run a new container**（运行新容器）对话框。
4. 展开 **Optional settings**（可选设置）。
5. 在可选设置中，指定以下内容：

   - **Container name**（容器名称）：`my-mysql`
   - **Host port**（主机端口）对于 **3306/tcp** 端口：`3307`
   - **Environment variables**（环境变量）：
     - `MYSQL_ROOT_PASSWORD`:`my-secret-pw`
     - `MYSQL_DATABASE`:`mydb`

   ![可选设置屏幕，已指定选项。](images/databases-2.webp)

6. 选择 `Run`。
7. 在 **Containers**（容器）视图中，验证端口是否在 **Port(s)**（端口）列中映射。对于 **my-mysql** 容器，你应该看到 **3307:3306**。

{{< /tab >}}
{{< /tabs >}}

此时，运行在主机上的任何应用程序都可以在 `localhost:3307` 访问容器中的 MySQL 服务。

## 从另一个容器连接到容器化数据库

从另一个容器连接到容器化数据库是在微服务架构和开发过程中常见的场景。Docker 的网络功能使得在不将数据库暴露给主机网络的情况下建立此连接变得简单。这通过将数据库容器和需要访问它的容器放置在同一个 Docker 网络上来实现。

在开始之前，你必须删除之前为此指南运行的任何容器。要停止并删除容器，可以：

- 在终端中运行 `docker rm --force my-mysql` 删除名为 `my-mysql` 的容器。
- 或者，在 Docker Desktop 仪表板中，在 **Containers**（容器）视图中选择容器旁边的 **Delete**（删除）图标，然后选择 **Delete forever**（永久删除）。

要创建网络并运行容器：

1. 运行以下命令创建名为 my-network 的 Docker 网络。

   ```console
   $ docker network create my-network
   ```

2. 运行你的数据库容器并使用 `--network` 选项指定网络。这将在 my-network 网络上运行容器。

   ```console
   $ docker run --name my-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_DATABASE=mydb --network my-network -d mysql:latest
   ```

3. 运行你的其他容器并使用 `--network` 选项指定网络。在此示例中，你将运行一个可以连接到数据库的 phpMyAdmin 容器。

   1. 运行一个 phpMyAdmin 容器。使用 `--network` 选项指定网络，使用 `-p` 选项让你可以从主机机器访问容器，使用 `-e` 选项指定此镜像所需的环境变量。

      ```console
      $ docker run --name my-phpmyadmin -d --network my-network -p 8080:80 -e PMA_HOST=my-mysql phpmyadmin
      ```

4. 验证容器是否可以通信。在此示例中，你将访问 phpMyAdmin 并验证它是否连接到数据库。

   1. 打开 [http://localhost:8080](http://localhost:8080) 访问你的 phpMyAdmin 容器。
   2. 使用 `root` 作为用户名，`my-secret-pw` 作为密码登录。你应该能够连接到 MySQL 服务器并看到你的数据库列出。

此时，任何在你的 `my-network` 容器网络上运行的应用程序都可以在 `my-mysql:3306` 访问容器中的 MySQL 服务。

## 在卷中持久化数据库数据

在 Docker 卷中持久化数据库数据对于确保你的数据在容器重启和删除时得以保留是必要的。Docker 卷让你将数据库文件存储在容器的可写层之外，使得升级容器、切换基础镜像和共享数据成为可能，而不会丢失数据。以下是如何使用 Docker CLI 或 Docker Desktop GUI 将卷附加到数据库容器的方法。

在开始之前，你必须删除之前为此指南运行的任何容器。要停止并删除容器，可以：

- 在终端中运行 `docker rm --force my-mysql` 删除名为 `my-mysql` 的容器。
- 或者，在 Docker Desktop 仪表板中，在 **Containers**（容器）视图中选择容器旁边的 **Delete**（删除）图标，然后选择 **Delete forever**（永久删除）。

接下来，你可以使用 Docker Desktop GUI 或 CLI 在附加卷的情况下运行容器。

{{< tabs group="ui" >}}
{{< tab name="CLI" >}}

要在运行数据库容器时附加卷，在 `docker run` 命令中包含 `-v` 选项，指定卷名和数据库在容器内存储数据的路径。如果卷不存在，Docker 会自动为你创建它。

要在运行数据库容器时附加卷，然后验证数据是否持久化：

1. 运行容器并附加卷。

   ```console
   $ docker run --name my-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_DATABASE=mydb -v my-db-volume:/var/lib/mysql -d mysql:latest
   ```

   此命令将名为 `my-db-volume` 的卷挂载到容器中的 `/var/lib/mysql` 目录。

2. 在数据库中创建一些数据。使用 `docker exec` 命令在容器内运行 `mysql` 并创建一个表。

   ```console
   $ docker exec my-mysql mysql -u root -pmy-secret-pw -e "CREATE TABLE IF NOT EXISTS mydb.mytable (column_name VARCHAR(255)); INSERT INTO mydb.mytable (column_name) VALUES ('value');"
   ```

   此命令使用容器中的 `mysql` 工具创建一个名为 `mytable` 的表，其中包含一个名为 `column_name` 的列，最后插入一个值为 `value` 的值。

3. 停止并删除容器。如果没有卷，当你删除容器时，你创建的表将会丢失。

   ```console
   $ docker rm --force my-mysql
   ```

4. 使用附加的卷启动一个新容器。这次，你不需要指定任何环境变量，因为配置已保存在卷中。

   ```console
   $ docker run --name my-mysql -v my-db-volume:/var/lib/mysql -d mysql:latest
   ```

5. 验证你创建的表是否仍然存在。再次使用 `docker exec` 命令在容器内运行 `mysql`。

   ```console
   $ docker exec my-mysql mysql -u root -pmy-secret-pw -e "SELECT * FROM mydb.mytable;"
   ```

   此命令使用容器中的 `mysql` 工具从 `mytable` 表中选择所有记录。

   你应该看到如下输出。

   ```console
   column_name
   value
   ```

{{< /tab >}}
{{< tab name="GUI" >}}

要在运行数据库容器时附加卷，然后验证数据是否持久化：

1. 运行一个附加卷的容器。

   1. 在 Docker Desktop 仪表板中，选择窗口顶部的全局搜索。
   2. 在搜索框中输入 `mysql`，如果未选中，请选择 **Images** 选项卡。
   3. 将鼠标悬停在 **mysql** 镜像上，然后选择 **Run**。
      此时会显示 **Run a new container**（运行新容器）对话框。
   4. 展开 **Optional settings**（可选设置）。
   5. 在可选设置中，指定以下内容：

      - **Container name**（容器名称）：`my-mysql`
      - **Environment variables**（环境变量）：
        - `MYSQL_ROOT_PASSWORD`:`my-secret-pw`
        - `MYSQL_DATABASE`:`mydb`
      - **Volumes**（卷）：
        - `my-db-volume`:`/var/lib/mysql`

      ![可选设置屏幕，已指定选项。](images/databases-3.webp)

      在这里，卷的名称是 `my-db-volume`，它在容器中挂载在 `/var/lib/mysql`。

   6. 选择 `Run`。

2. 在数据库中创建一些数据。

   1. 在 **Containers** 视图中，在容器旁边选择 **Show container actions**（显示容器操作）图标，然后选择 **Open in terminal**（在终端中打开）。
   2. 在容器的终端中运行以下命令添加一个表。

      ```console
      # mysql -u root -pmy-secret-pw -e "CREATE TABLE IF NOT EXISTS mydb.mytable (column_name VARCHAR(255)); INSERT INTO mydb.mytable (column_name) VALUES ('value');"
      ```

      此命令使用容器中的 `mysql` 工具创建一个名为 `mytable` 的表，其中包含一个名为 `column_name` 的列，最后插入一个值为 value 的值。

3. 在 **Containers** 视图中，选择容器旁边的 **Delete**（删除）图标，然后选择 **Delete forever**（永久删除）。如果没有卷，当你删除容器时，你创建的表将会丢失。
4. 运行一个附加卷的容器。

   1. 在 Docker Desktop 仪表板中，选择窗口顶部的全局搜索。
   2. 在搜索框中输入 `mysql`，如果未选中，请选择 **Images** 选项卡。
   3. 将鼠标悬停在 **mysql** 镜像上，然后选择 **Run**。
      此时会显示 **Run a new container**（运行新容器）对话框。
   4. 展开 **Optional settings**（可选设置）。
   5. 在可选设置中，指定以下内容：

      - **Container name**（容器名称）：`my-mysql`
      - **Environment variables**（环境变量）：
        - `MYSQL_ROOT_PASSWORD`:`my-secret-p