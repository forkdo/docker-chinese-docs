---
title: 多容器应用
weight: 70
linkTitle: "第 6 部分：多容器应用"
keywords: get started, setup, orientation, quickstart, intro, concepts, containers,
  docker desktop
description: 在你的应用中使用多个容器
aliases:
 - /get-started/07_multi_container/
 - /guides/workshop/07_multi_container/
---

到目前为止，你一直在使用单容器应用。但现在，你将在应用栈中添加 MySQL。以下问题经常出现——“MySQL 应该在哪里运行？是安装在同一个容器中，还是单独运行？”通常，每个容器应该只做一件事，并且把它做好。以下是一些将容器分开运行的原因：

- 你很可能需要将 API 和前端与数据库分开扩展。
- 分开的容器让你可以独立地版本化和更新版本。
- 虽然你可能在本地使用容器来运行数据库，但在生产环境中你可能更倾向于使用托管服务。你并不希望将数据库引擎与你的应用一起打包。
- 运行多个进程需要一个进程管理器（容器只启动一个进程），这会增加容器启动/关闭的复杂性。

原因还有很多。因此，如下面的示意图所示，最好将你的应用运行在多个容器中。

![Todo 应用连接到 MySQL 容器](images/multi-container.webp?w=350h=250)


## 容器网络

请记住，容器默认情况下是相互隔离的，彼此之间不知道对方的存在。那么，如何让一个容器与另一个容器通信呢？答案就是网络。如果你将两个容器放在同一个网络中，它们就可以相互通信。

## 启动 MySQL

有两种方法可以将容器放到网络中：
 - 在启动容器时指定网络。
 - 将已运行的容器连接到网络。

在接下来的步骤中，你将首先创建网络，然后在启动时将 MySQL 容器附加到该网络。

1. 创建网络。

   ```console
   $ docker network create todo-app
   ```

2. 启动一个 MySQL 容器并将其附加到网络。你还将定义几个环境变量，数据库将使用这些变量来初始化数据库。要了解更多关于 MySQL 环境变量的信息，请参阅 [MySQL Docker Hub 页面](https://hub.docker.com/_/mysql/) 中的“环境变量”部分。

   {{< tabs >}}
   {{< tab name="Mac / Linux / Git Bash" >}}
   
   ```console
   $ docker run -d \
       --network todo-app --network-alias mysql \
       -v todo-mysql-data:/var/lib/mysql \
       -e MYSQL_ROOT_PASSWORD=secret \
       -e MYSQL_DATABASE=todos \
       mysql:8.0
   ```

   {{< /tab >}}
   {{< tab name="PowerShell" >}}

   ```powershell
   $ docker run -d `
       --network todo-app --network-alias mysql `
       -v todo-mysql-data:/var/lib/mysql `
       -e MYSQL_ROOT_PASSWORD=secret `
       -e MYSQL_DATABASE=todos `
       mysql:8.0
   ```
   
   {{< /tab >}}
   {{< tab name="Command Prompt" >}}

   ```console
   $ docker run -d ^
       --network todo-app --network-alias mysql ^
       -v todo-mysql-data:/var/lib/mysql ^
       -e MYSQL_ROOT_PASSWORD=secret ^
       -e MYSQL_DATABASE=todos ^
       mysql:8.0
   ```
   
   {{< /tab >}}
   {{< /tabs >}}
   
   在前面的命令中，你可以看到 `--network-alias` 标志。在稍后的部分，你将学到更多关于这个标志的内容。

   > [!TIP]
   >
   > 你会注意到上面的命令中有一个名为 `todo-mysql-data` 的卷挂载在 `/var/lib/mysql` 上，这是 MySQL 存储数据的位置。但是，你从未运行过 `docker volume create` 命令。Docker 识别到你想要使用命名卷，并自动为你创建一个。

3. 为了确认数据库已启动并运行，连接到数据库并验证连接。

   ```console
   $ docker exec -it <mysql-container-id> mysql -u root -p
   ```

   当密码提示出现时，输入 `secret`。在 MySQL shell 中，列出数据库并确认看到 `todos` 数据库。

   ```console
   mysql> SHOW DATABASES;
   ```

   你应该看到如下输出：

   ```plaintext
   +--------------------+
   | Database           |
   +--------------------+
   | information_schema |
   | mysql              |
   | performance_schema |
   | sys                |
   | todos              |
   +--------------------+
   5 rows in set (0.00 sec)
   ```

4. 退出 MySQL shell，返回到你的机器 shell。

   ```console
   mysql> exit
   ```

   现在你有了一个 `todos` 数据库，并且它已经准备好了。

## 连接到 MySQL

现在你知道 MySQL 已经启动并运行，你可以使用它了。但是，如何使用它呢？如果你在同一个网络上运行另一个容器，如何找到该容器？记住，每个容器都有自己的 IP 地址。

为了解答上述问题并更好地理解容器网络，你将使用 [nicolaka/netshoot](https://github.com/nicolaka/netshoot) 容器，它包含了许多有用的工具，可用于排查或调试网络问题。

1. 使用 nicolaka/netshoot 镜像启动一个新容器。确保将其连接到同一网络。

   ```console
   $ docker run -it --network todo-app nicolaka/netshoot
   ```

2. 在容器内，你将使用 `dig` 命令，这是一个有用的 DNS 工具。你将查找主机名 `mysql` 的 IP 地址。

   ```console
   $ dig mysql
   ```

   你应该得到如下输出：

   ```text
   ; <<>> DiG 9.18.8 <<>> mysql
   ;; global options: +cmd
   ;; Got answer:
   ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 32162
   ;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

   ;; QUESTION SECTION:
   ;mysql.				IN	A

   ;; ANSWER SECTION:
   mysql.			600	IN	A	172.23.0.2

   ;; Query time: 0 msec
   ;; SERVER: 127.0.0.11#53(127.0.0.11)
   ;; WHEN: Tue Oct 01 23:47:24 UTC 2019
   ;; MSG SIZE  rcvd: 44
   ```

   在“ANSWER SECTION”中，你会看到一个 `mysql` 的 `A` 记录，它解析为 `172.23.0.2`（你的 IP 地址可能与此不同）。虽然 `mysql` 通常不是一个有效的主机名，但 Docker 能够将其解析为具有该网络别名的容器的 IP 地址。记住，你之前使用了 `--network-alias`。

   这意味着你的应用只需简单地连接到名为 `mysql` 的主机，就能与数据库通信。

## 使用 MySQL 运行你的应用

Todo 应用支持设置几个环境变量来指定 MySQL 连接设置。它们是：

- `MYSQL_HOST` - 运行的 MySQL 服务器的主机名
- `MYSQL_USER` - 用于连接的用户名
- `MYSQL_PASSWORD` - 用于连接的密码
- `MYSQL_DB` - 连接后要使用的数据库

> [!NOTE]
>
> 虽然在开发中使用环境变量设置连接配置是被广泛接受的，但在生产环境中运行应用时，强烈不建议这样做。Docker 前安全负责人 Diogo Monica [写了一篇很棒的博客文章](https://blog.diogomonica.com/2017/03/27/why-you-shouldnt-use-env-variables-for-secret-data/)，解释了原因。
>
> 更安全的机制是使用容器编排框架提供的密钥支持。在大多数情况下，这些密钥作为文件挂载到运行的容器中。你会看到许多应用（包括 MySQL 镜像和 Todo 应用）也支持带有 `_FILE` 后缀的环境变量，以指向包含变量的文件。
>
> 例如，设置 `MYSQL_PASSWORD_FILE` 环境变量将导致应用使用引用文件的内容作为连接密码。Docker 本身不会对这些环境变量做任何特殊处理。你的应用需要知道去查找该变量并获取文件内容。

现在你可以启动你的开发就绪容器了。

1. 指定前面的每个环境变量，并将容器连接到你的应用网络。确保你在 `getting-started-app` 目录中运行此命令。

   {{< tabs >}}
   {{< tab name="Mac / Linux" >}}

   ```console
   $ docker run -dp 127.0.0.1:3000:3000 \
     -w /app -v "$(pwd):/app" \
     --network todo-app \
     -e MYSQL_HOST=mysql \
     -e MYSQL_USER=root \
     -e MYSQL_PASSWORD=secret \
     -e MYSQL_DB=todos \
     node:lts-alpine \
     sh -c "yarn install && yarn run dev"
   ```
   
   {{< /tab >}}
   {{< tab name="PowerShell" >}}
   在 Windows 中，在 PowerShell 中运行此命令。

   ```powershell
   $ docker run -dp 127.0.0.1:3000:3000 `
     -w /app -v "$(pwd):/app" `
     --network todo-app `
     -e MYSQL_HOST=mysql `
     -e MYSQL_USER=root `
     -e MYSQL_PASSWORD=secret `
     -e MYSQL_DB=todos `
     node:lts-alpine `
     sh -c "yarn install && yarn run dev"
   ```

   {{< /tab >}}
   {{< tab name="Command Prompt" >}}
   在 Windows 中，在命令提示符中运行此命令。

   ```console
   $ docker run -dp 127.0.0.1:3000:3000 ^
     -w /app -v "%cd%:/app" ^
     --network todo-app ^
     -e MYSQL_HOST=mysql ^
     -e MYSQL_USER=root ^
     -e MYSQL_PASSWORD=secret ^
     -e MYSQL_DB=todos ^
     node:lts-alpine ^
     sh -c "yarn install && yarn run dev"
   ```

   {{< /tab >}}
   {{< tab name="Git Bash" >}}

   ```console
   $ docker run -dp 127.0.0.1:3000:3000 \
     -w //app -v "/$(pwd):/app" \
     --network todo-app \
     -e MYSQL_HOST=mysql \
     -e MYSQL_USER=root \
     -e MYSQL_PASSWORD=secret \
     -e MYSQL_DB=todos \
     node:lts-alpine \
     sh -c "yarn install && yarn run dev"
   ```
   
   {{< /tab >}}
   {{< /tabs >}}

2. 如果查看容器的日志（`docker logs -f <container-id>`），你应该看到类似以下的消息，表明它正在使用 mysql 数据库。

   ```console
   $ nodemon src/index.js
   [nodemon] 2.0.20
   [nodemon] to restart at any time, enter `rs`
   [nodemon] watching dir(s): *.*
   [nodemon] starting `node src/index.js`
   Connected to mysql db at host mysql
   Listening on port 3000
   ```

3. 在浏览器中打开应用，向你的待办列表中添加几项。

4. 连接到 mysql 数据库，证明这些项目已写入数据库。记住，密码是 `secret`。

   ```console
   $ docker exec -it <mysql-container-id> mysql -p todos
   ```

   在 mysql shell 中，运行以下命令：

   ```console
   mysql> select * from todo_items;
   +--------------------------------------+--------------------+-----------+
   | id                                   | name               | completed |
   +--------------------------------------+--------------------+-----------+
   | c906ff08-60e6-44e6-8f49-ed56a0853e85 | Do amazing things! |         0 |
   | 2912a79e-8486-4bc3-a4c5-460793a575ab | Be awesome!        |         0 |
   +--------------------------------------+--------------------+-----------+
   ```

   你的表会看起来不同，因为它包含你的项目。但你应该看到它们被存储在那里。

## 总结

至此，你有了一个应用，它现在将数据存储在单独容器中运行的外部数据库中。你学到了一点关于容器网络和使用 DNS 的服务发现的知识。

相关信息：
 - [docker CLI 参考](/reference/cli/docker/)
 - [网络概述](/manuals/engine/network/_index.md)

## 下一步

你很可能开始觉得需要记住的东西有点多，启动这个应用需要做很多事情。你需要创建网络、启动容器、指定所有环境变量、暴露端口等等。这确实很复杂，也使得将这些内容传递给其他人变得困难。

在下一节中，你将学习 Docker Compose。使用 Docker Compose，你可以更轻松地共享你的应用栈，并让其他人只需一个简单的命令就能启动它们。

{{< button text="使用 Docker Compose" url="08_using_compose.md" >}}
