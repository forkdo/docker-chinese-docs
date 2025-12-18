---
title: 使用容器进行 Go 开发
linkTitle: 开发你的应用
weight: 20
keywords: get started, go, golang, local, development
description: 了解如何在本地开发你的应用程序。
aliases:
  - /get-started/golang/develop/
  - /language/golang/develop/
  - /guides/language/golang/develop/
---

## 前置条件

完成 [将镜像作为容器运行](run-containers.md) 模块中的步骤，学习如何管理容器的生命周期。

## 介绍

在本模块中，你将了解如何在容器中运行数据库引擎，并将其连接到示例应用的扩展版本。你将看到一些用于保持持久数据和连接容器以相互通信的选项。最后，你将学习如何使用 Docker Compose 有效管理此类多容器本地开发环境。

## 本地数据库和容器

你将使用的数据库引擎叫做 [CockroachDB](https://www.cockroachlabs.com/product/)。它是一个现代的、云原生的、分布式 SQL 数据库。

与其从源代码编译 CockroachDB 或使用操作系统的原生包管理器安装 CockroachDB，不如使用 [CockroachDB 的 Docker 镜像](https://hub.docker.com/r/cockroachdb/cockroach) 并在容器中运行它。

CockroachDB 在很大程度上与 PostgreSQL 兼容，与后者共享许多约定，尤其是环境变量的默认名称。因此，如果你熟悉 Postgres，不要对看到一些熟悉的环境变量名感到惊讶。适用于 Postgres 的 Go 模块，如 [pgx](https://pkg.go.dev/github.com/jackc/pgx)、[pq](https://pkg.go.dev/github.com/lib/pq)、[GORM](https://gorm.io/index.html) 和 [upper/db](https://upper.io/v4/) 也适用于 CockroachDB。

有关 Go 和 CockroachDB 关系的更多信息，请参考 [CockroachDB 文档](https://www.cockroachlabs.com/docs/v20.2/build-a-go-app-with-cockroachdb.html)，尽管这对继续本指南来说不是必需的。

### 存储

数据库的要点是拥有持久的数据存储。[卷](/manuals/engine/storage/volumes.md) 是持久化 Docker 容器生成和使用数据的首选机制。因此，在启动 CockroachDB 之前，先为其创建卷。

要创建一个托管卷，运行：

```console
$ docker volume create roach
roach
```

你可以使用以下命令查看 Docker 实例中所有托管卷的列表：

```console
$ docker volume list
DRIVER    VOLUME NAME
local     roach
```

### 网络

示例应用和数据库引擎将通过网络相互通信。有不同类型的网络配置是可能的，你将使用所谓的用户定义桥接网络。它将为你提供 DNS 查找服务，以便你可以通过主机名引用数据库引擎容器。

以下命令创建一个名为 `mynet` 的新桥接网络：

```console
$ docker network create -d bridge mynet
51344edd6430b5acd121822cacc99f8bc39be63dd125a3b3cd517b6485ab7709
```

与托管卷的情况一样，有一个命令可以列出 Docker 实例中设置的所有网络：

```console
$ docker network list
NETWORK ID     NAME          DRIVER    SCOPE
0ac2b1819fa4   bridge        bridge    local
51344edd6430   mynet         bridge    local
daed20bbecce   host          host      local
6aee44f40a39   none          null      local
```

你的桥接网络 `mynet` 已成功创建。其他三个网络，名为 `bridge`、`host` 和 `none`，是默认网络，由 Docker 本身创建。虽然这与本指南无关，但你可以在 [网络概述](/manuals/engine/network/_index.md) 部分了解有关 Docker 网络的更多信息。

### 为卷和网络选择好名字

俗话说，计算机科学中只有两件难事：缓存失效和命名。以及差一错误。

在为网络或托管卷选择名称时，最好选择一个能表明预期用途的名称。本指南旨在简洁，所以使用了简短、通用的名称。

### 启动数据库引擎

现在家务活都做完了，你可以在容器中运行 CockroachDB 并将其附加到刚刚创建的卷和网络上。当你运行以下命令时，Docker 将从 Docker Hub 拉取镜像并在本地为你运行：

```console
$ docker run -d \
  --name roach \
  --hostname db \
  --network mynet \
  -p 26257:26257 \
  -p 8080:8080 \
  -v roach:/cockroach/cockroach-data \
  cockroachdb/cockroach:latest-v25.4 start-single-node \
  --insecure

# ... output omitted ...
```

注意巧妙地使用标签 `latest-v25.4` 来确保你拉取的是最新的 25.4 补丁版本。可用标签的多样性取决于镜像维护者。在这里，你的意图是拥有最新修补版本的 CockroachDB，同时随着时间的推移不会偏离已知的工作版本太远。要查看 CockroachDB 镜像的可用标签，你可以访问 [Docker Hub 上的 CockroachDB 页面](https://hub.docker.com/r/cockroachdb/cockroach/tags)。

### 配置数据库引擎

现在数据库引擎已经启动，还需要做一些配置才能让你的应用开始使用它。幸运的是，这并不多。你必须：

1. 创建一个空数据库。
2. 在数据库引擎中注册一个新用户账户。
3. 授予该新用户对数据库的访问权限。

你可以使用 CockroachDB 内置的 SQL shell 来完成这些操作。要在运行数据库引擎的同一容器中启动 SQL shell，请输入：

```console
$ docker exec -it roach ./cockroach sql --insecure
```

1. 在 SQL shell 中，创建示例应用将使用的数据库：

   ```sql
   CREATE DATABASE mydb;
   ```

2. 使用用户名 `totoro` 在数据库引擎中注册一个新 SQL 用户账户。

   ```sql
   CREATE USER totoro;
   ```

3. 授予新用户必要的权限：

   ```sql
   GRANT ALL ON DATABASE mydb TO totoro;
   ```

4. 输入 `quit` 退出 shell。

以下是与 SQL shell 交互的示例。

```console
$ sudo docker exec -it roach ./cockroach sql --insecure
#
# Welcome to the CockroachDB SQL shell.
# All statements must be terminated by a semicolon.
# To exit, type: \q.
#
# Server version: CockroachDB CCL v20.1.15 (x86_64-unknown-linux-gnu, built 2021/04/26 16:11:58, go1.13.9) (same version as client)
# Cluster ID: 7f43a490-ccd6-4c2a-9534-21f393ca80ce
#
# Enter \? for a brief introduction.
#
root@:26257/defaultdb> CREATE DATABASE mydb;
CREATE DATABASE

Time: 22.985478ms

root@:26257/defaultdb> CREATE USER totoro;
CREATE ROLE

Time: 13.921659ms

root@:26257/defaultdb> GRANT ALL ON DATABASE mydb TO totoro;
GRANT

Time: 14.217559ms

root@:26257/defaultdb> quit
oliver@hki:~$
```

### 认识示例应用

现在你已经启动并配置了数据库引擎，可以将注意力转向应用了。

本模块的示例应用是你在前面模块中使用的 `docker-gs-ping` 应用的扩展版本。你有两个选择：

- 你可以更新本地的 `docker-gs-ping` 副本以匹配本章介绍的新扩展版本；或者
- 你可以克隆 [docker/docker-gs-ping-dev](https://github.com/docker/docker-gs-ping-dev) 仓库。推荐后一种方法。

要检出示例应用，请运行：

```console
$ git clone https://github.com/docker/docker-gs-ping-dev.git
# ... output omitted ...
```

应用的 `main.go` 现在包含了数据库初始化代码，以及实现新业务需求的代码：

- 发送到 `/send` 的 HTTP `POST` 请求，包含 `{ "value" : string }` JSON，必须将值保存到数据库中。

你还有另一个业务需求的更新。需求是：

- 应用在响应 `/` 请求时返回包含心形符号（"`<3`"）的文本消息。

现在它将是：

- 应用响应包含存储在数据库中的消息计数的字符串，用括号括起来。

  示例输出：`Hello, Docker! (7)`

`main.go` 的完整源代码如下。

```go
package main

import (
	"context"
	"database/sql"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/cenkalti/backoff/v4"
	"github.com/cockroachdb/cockroach-go/v2/crdb"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func main() {

	e := echo.New()

	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	db, err := initStore()
	if err != nil {
		log.Fatalf("failed to initialize the store: %s", err)
	}
	defer db.Close()

	e.GET("/", func(c echo.Context) error {
		return rootHandler(db, c)
	})

	e.GET("/ping", func(c echo.Context) error {
		return c.JSON(http.StatusOK, struct{ Status string }{Status: "OK"})
	})

	e.POST("/send", func(c echo.Context) error {
		return sendHandler(db, c)
	})

	httpPort := os.Getenv("HTTP_PORT")
	if httpPort == "" {
		httpPort = "8080"
	}

	e.Logger.Fatal(e.Start(":" + httpPort))
}

type Message struct {
	Value string `json:"value"`
}

func initStore() (*sql.DB, error) {

	pgConnString := fmt.Sprintf("host=%s port=%s dbname=%s user=%s password=%s sslmode=disable",
		os.Getenv("PGHOST"),
		os.Getenv("PGPORT"),
		os.Getenv("PGDATABASE"),
		os.Getenv("PGUSER"),
		os.Getenv("PGPASSWORD"),
	)

	var (
		db  *sql.DB
		err error
	)
	openDB := func() error {
		db, err = sql.Open("postgres", pgConnString)
		return err
	}

	err = backoff.Retry(openDB, backoff.NewExponentialBackOff())
	if err != nil {
		return nil, err
	}

	if _, err := db.Exec(
		"CREATE TABLE IF NOT EXISTS message (value TEXT PRIMARY KEY)"); err != nil {
		return nil, err
	}

	return db, nil
}

func rootHandler(db *sql.DB, c echo.Context) error {
	r, err := countRecords(db)
	if err != nil {
		return c.HTML(http.StatusInternalServerError, err.Error())
	}
	return c.HTML(http.StatusOK, fmt.Sprintf("Hello, Docker! (%d)\n", r))
}

func sendHandler(db *sql.DB, c echo.Context) error {

	m := &Message{}

	if err := c.Bind(m); err != nil {
		return c.JSON(http.StatusInternalServerError, err)
	}

	err := crdb.ExecuteTx(context.Background(), db, nil,
		func(tx *sql.Tx) error {
			_, err := tx.Exec(
				"INSERT INTO message (value) VALUES ($1) ON CONFLICT (value) DO UPDATE SET value = excluded.value",
				m.Value,
			)
			if err != nil {
				return c.JSON(http.StatusInternalServerError, err)
			}
			return nil
		})

	if err != nil {
		return c.JSON(http.StatusInternalServerError, err)
	}

	return c.JSON(http.StatusOK, m)
}

func countRecords(db *sql.DB) (int, error) {

	rows, err := db.Query("SELECT COUNT(*) FROM message")
	if err != nil {
		return 0, err
	}
	defer rows.Close()

	count := 0
	for rows.Next() {
		if err := rows.Scan(&count); err != nil {
			return 0, err
		}
		rows.Close()
	}

	return count, nil
}
```

仓库还包含了 `Dockerfile`，它与前面模块中介绍的多阶段 `Dockerfile` 几乎完全相同。它使用官方的 Docker Go 镜像构建应用，然后通过将编译后的二进制文件放入更精简的 distroless 镜像中来构建最终镜像。

无论你是更新了旧示例应用还是检出了新示例应用，都必须构建这个新 Docker 镜像以反映应用源代码的更改。

### 构建应用

你可以使用熟悉的 `build` 命令构建镜像：

```console
$ docker build --tag docker-gs-ping-roach .
```

### 运行应用

现在，运行你的容器。这次你需要设置一些环境变量，以便你的应用知道如何访问数据库。目前，你将在 `docker run` 命令中直接这样做。稍后你将看到使用 Docker Compose 的更方便方法。

> [!NOTE]
>
> 由于你以不安全模式运行 CockroachDB 集群，密码值可以是任何值。
>
> 在生产环境中，不要以不安全模式运行。

```console
$ docker run -it --rm -d \
  --network mynet \
  --name rest-server \
  -p 80:8080 \
  -e PGUSER=totoro \
  -e PGPASSWORD=myfriend \
  -e PGHOST=db \
  -e PGPORT=26257 \
  -e PGDATABASE=mydb \
  docker-gs-ping-roach
```

关于这个命令有几个要点。

- 这次你将容器端口 `8080` 映射到主机端口 `80`。因此，对于 `GET` 请求，你可以简单地使用 `curl localhost`：

  ```console
  $ curl localhost
  Hello, Docker! (0)
  ```

  或者，如果你喜欢，使用正确的 URL 也可以：

  ```console
  $ curl http://localhost/
  Hello, Docker! (0)
  ```

- 目前存储的消息总数是 `0`。这很好，因为你还没有向应用发布任何消息。
- 你通过主机名 `db` 引用数据库容器。这就是为什么你在启动数据库容器时使用了 `--hostname db`。

- 实际密码并不重要，但必须设置为某个值以避免混淆示例应用。
- 你刚刚运行的容器名为 `rest-server`。这些名称对于管理容器生命周期很有用：

  ```console
  # 还不要这样做，这只是个示例：
  $ docker container rm --force rest-server
  ```

### 测试应用

在上一节中，你已经测试了用 `GET` 查询你的应用，它返回了存储消息计数器的零值。现在，向它发布一些消息：

```console
$ curl --request POST \
  --url http://localhost/send \
  --header 'content-type: application/json' \
  --data '{"value": "Hello, Docker!"}'
```

应用响应消息的内容，这意味着它已保存在数据库中：

```json
{ "value": "Hello, Docker!" }
```

再发送一条消息：

```console
$ curl --request POST \
  --url http://localhost/send \
  --header 'content-type: application/json' \
  --data '{"value": "Hello, Oliver!"}'
```

同样，你得到了消息值的响应：

```json
{ "value": "Hello, Oliver!" }
```

运行 curl 并查看消息计数器怎么说：

```console
$ curl localhost
Hello, Docker! (2)
```

在这个示例中，你发送了两条消息，数据库保存了它们。或者它真的保存了吗？停止并删除所有容器，但不要删除卷，然后再次尝试。

首先，停止容器：

```console
$ docker container stop rest-server roach
rest-server
roach
```

然后，删除它们：

```console
$ docker container rm rest-server roach
rest-server
roach
```

验证它们已消失：

```console
$ docker container list --all
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

然后再次启动它们，先启动数据库：

```console
$ docker run -d \
  --name roach \
  --hostname db \
  --network mynet \
  -p 26257:26257 \
  -p 8080:8080 \
  -v roach:/cockroach/cockroach-data \
  cockroachdb/cockroach:latest-v25.4 start-single-node \
  --insecure
```

然后启动服务：

```console
$ docker run -it --rm -d \
  --network mynet \
  --name rest-server \
  -p 80:8080 \
  -e PGUSER=totoro \
  -e PGPASSWORD=myfriend \
  -e PGHOST=db \
  -e PGPORT=26257 \
  -e PGDATABASE=mydb \
  docker-gs-ping-roach
```

最后，查询你的服务：

```console
$ curl localhost
Hello, Docker! (2)
```

太好了！数据库记录数的计数是正确的，尽管你不仅停止了容器，还在启动新实例之前删除了它们。区别在于你重用的 CockroachDB 托管卷。新的 CockroachDB 容器从磁盘读取了数据库文件，就像它在容器外运行时通常会做的那样。

### 收尾工作

记住，你正在以不安全模式运行 CockroachDB。现在你已经构建并测试了你的应用，是时候在继续之前收尾一切了。你可以使用 `list` 命令列出正在运行的容器：

```console
$ docker container list
```

现在你知道了容器 ID，可以使用 `docker container stop` 和 `docker container rm`，如前面模块中演示的那样。

在继续之前停止 CockroachDB 和 `docker-gs-ping-ro