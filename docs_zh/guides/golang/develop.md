---
title: 使用容器进行 Go 开发
linkTitle: 开发你的应用
weight: 20
keywords: 入门, go, golang, 本地, 开发
description: 了解如何在本地开发你的应用。
aliases:
  - /get-started/golang/develop/
  - /language/golang/develop/
  - /guides/language/golang/develop/
---

## 前置要求

完成 [将镜像作为容器运行](run-containers.md) 模块的步骤，学习如何管理容器的生命周期。

## 介绍

在本模块中，你将了解如何在容器中运行数据库引擎，并将其连接到示例应用的扩展版本。你将看到一些用于保持数据持久化以及连接容器之间通信的选项。最后，你将学习如何使用 Docker Compose 来有效管理这种多容器本地开发环境。

## 本地数据库与容器

你要使用的数据库引擎叫做 [CockroachDB](https://www.cockroachlabs.com/product/)。它是一个现代的、云原生的、分布式 SQL 数据库。

你不需要从源代码编译 CockroachDB，也不需要使用操作系统的原生包管理器来安装，而是使用 [CockroachDB 的 Docker 镜像](https://hub.docker.com/r/cockroachdb/cockroach) 并在容器中运行它。

CockroachDB 在很大程度上与 PostgreSQL 兼容，共享许多约定，特别是环境变量的默认名称。因此，如果你熟悉 Postgres，不要对看到一些熟悉的环境变量名感到惊讶。适用于 Postgres 的 Go 模块，如 [pgx](https://pkg.go.dev/github.com/jackc/pgx)、[pq](https://pkg.go.dev/github.com/lib/pq)、[GORM](https://gorm.io/index.html) 和 [upper/db](https://upper.io/v4/) 也适用于 CockroachDB。

有关 Go 与 CockroachDB 关系的更多信息，请参考 [CockroachDB 文档](https://www.cockroachlabs.com/docs/v20.2/build-a-go-app-with-cockroachdb.html)，尽管这对继续本指南来说不是必需的。

### 存储

数据库的目的是拥有持久的数据存储。[卷](/manuals/engine/storage/volumes.md) 是持久化 Docker 容器生成和使用的数据的首选机制。因此，在启动 CockroachDB 之前，先为它创建卷。

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

示例应用和数据库引擎将通过网络相互通信。有不同类型的网络配置是可能的，你将使用一种称为用户定义桥接网络的配置。它将为你提供 DNS 查找服务，以便你可以通过主机名引用数据库引擎容器。

以下命令创建一个名为 `mynet` 的新桥接网络：

```console
$ docker network create -d bridge mynet
51344edd6430b5acd121822cacc99f8bc39be63dd125a3b3cd517b6485ab7709
```

与托管卷一样，有一个命令可以列出 Docker 实例中设置的所有网络：

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

在为网络或托管卷选择名称时，最好选择一个能表明其预期用途的名称。本指南旨在简洁，因此使用了简短、通用的名称。

### 启动数据库引擎

现在，家务活已经完成，你可以在容器中运行 CockroachDB 并将其附加到刚刚创建的卷和网络上。当你运行以下命令时，Docker 将从 Docker Hub 拉取镜像并在本地为你运行：

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

# ... 输出省略 ...
```

注意巧妙使用标签 `latest-v25.4` 来确保你拉取的是 25.4 的最新补丁版本。可用标签的多样性取决于镜像维护者。在这里，你的意图是拥有 CockroachDB 的最新修补版本，同时随着时间的推移不会偏离已知的工作版本太远。要查看 CockroachDB 镜像的可用标签，你可以访问 [Docker Hub 上的 CockroachDB 页面](https://hub.docker.com/r/cockroachdb/cockroach/tags)。

### 配置数据库引擎

现在数据库引擎已经启动，还需要做一些配置才能让你的应用开始使用它。幸运的是，这并不多。你必须：

1. 创建一个空数据库。
2. 在数据库引擎中注册一个新用户账户。
3. 授予该新用户对数据库的访问权限。

你可以使用 CockroachDB 内置的 SQL shell 来完成这些操作。要在运行数据库引擎的同一容器中启动 SQL shell，输入：

```console
$ docker exec -it roach ./cockroach sql --insecure
```

1. 在 SQL shell 中，创建示例应用将要使用的数据库：

   ```sql
   CREATE DATABASE mydb;
   ```

2. 在数据库引擎中注册一个新 SQL 用户账户。使用用户名 `totoro`。

   ```sql
   CREATE USER totoro;
   ```

3. 给新用户必要的权限：

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
- 你可以克隆 [docker/docker-gs-ping-dev](https://github.com/docker/docker-gs-ping-dev) 仓库。推荐使用后一种方法。

要检出示例应用，运行：

```console
$ git clone https://github.com/docker/docker-gs-ping-dev.git
# ... 输出省略 ...
```

应用的 `main.go` 现在包含了数据库初始化代码，以及实现新业务需求的代码：

- 对 `/send` 的 HTTP `POST` 请求包含 `{ "value" : string }` JSON 必须将值保存到数据库中。

你还有另一个业务需求的更新。需求是：

- 应用在响应 `/` 的请求时返回包含心形符号（"`<3`"）的文本消息。

现在它将变成：

- 应用响应包含存储在数据库中的消息数量的字符串，用括号括起来。

  示例输出：`Hello, Docker! (7)`

以下是 `main.go` 的完整源代码列表。

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

仓库还包含 `Dockerfile`，它与前面模块中介绍的多阶段 `Dockerfile` 几乎完全相同。它使用官方的 Docker Go 镜像来构建应用，然后通过将编译后的二进制文件放入更精简的 distroless 镜像中来构建最终镜像。

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
> 由于你以不安全模式运行 CockroachDB 集群，密码值可以是任何内容。
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

关于这个命令有几个要点需要注意。

- 这次你将容器端口 `8080` 映射到主机端口 `80`。因此，对于 `GET` 请求，你可以简单地使用 `curl localhost`：

  ```console
  $ curl localhost
  Hello, Docker! (0)
  ```

  或者，如果你愿意，使用完整的 URL 也可以：

  ```console
  $ curl http://localhost/
  Hello, Docker! (0)
  ```

- 存储的消息总数目前是 `0`。这很好，因为你还没有向应用发布任何消息。
- 你通过其主机名 `db` 引用数据库容器。这就是为什么你在启动数据库容器时使用了 `--hostname db`。
- 实际密码并不重要，但必须设置为某个值以避免混淆示例应用。
- 你刚刚运行的容器名为 `rest-server`。这些名称对于管理容器生命周期很有用：

  ```console
  # 暂时不要这样做，这只是个示例：
  $ docker container rm --force rest-server
  ```

### 测试应用

在前面的部分中，你已经测试了用 `GET` 查询你的应用，它返回了存储消息计数器的零值。现在，向它发布一些消息：

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

同样，你得到了消息的值：

```json
{ "value": "Hello, Oliver!" }
```

运行 curl 查看消息计数器的值：

```console
$ curl localhost
Hello, Docker! (2)
```

在这个例子中，你发送了两条消息，数据库保存了它们。或者它真的保存了吗？停止并移除所有容器，但不要移除卷，然后再次尝试。

首先，停止容器：

```console
$ docker container stop rest-server roach
rest-server
roach
```

然后，移除它们：

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

太好了！数据库记录数的计数是正确的，尽管你不仅停止了容器，还在启动新实例之前移除了它们。区别在于你重用的 CockroachDB 托管卷。新的 CockroachDB 容器从磁盘读取了数据库文件，就像它在容器外运行时通常会做的那样。

### 收尾工作

请记住，你正在以不安全模式运行 CockroachDB。现在你已经构建并测试了你的应用，是时候在继续之前将其关闭。你可以使用 `list` 命令列出正在运行的容器：

```console
$ docker container list
```

现在你知道了容器 ID，可以使用 `docker container stop` 和 `docker container rm`，如前面模块中演示的那样。

在继续之前停止 CockroachDB 和 `docker-gs-ping-roach` 容器。

## 使用 Docker Compose 提高效率

在这一点上，你可能想知道是否有一种方法可以避免处理 `docker` 命令的长参数列表。本系列中使用的玩具示例需要五个环境变量来定义与数据库的连接。真实的应用可能需要更多。然后还有一个依赖关系的问题。理想情况下，你希望确保在运行应用之前先启动数据库。而启动数据库实例可能需要另一个带有许多选项的 Docker 命令。但对于本地开发目的，有一种更好的方法来协调这些部署。

在本节中，你将创建一个 Docker Compose 文件，使用单个命令启动你的 `docker-gs-ping-roach` 应用和 CockroachDB 数据库引擎。

### 配置 Docker Compose

在你的应用目录中，创建一个名为 `compose.yaml` 的新文本文件，内容如下。

```yaml
version: "3.8"

services:
  docker-gs-ping-roach:
    depends_on:
      - roach
    build:
      context: .
    container_name: rest-server
    hostname: rest-server
    networks:
      - mynet
    ports:
      - 80:8080
    environment:
      - PGUSER=${PGUSER:-totoro}
      - PGPASSWORD=${PGPASSWORD:?database password not set}
      - PGHOST=${PGHOST:-db}
      - PGPORT=${PGPORT:-26257}
      - PGDATABASE=${PGDATABASE:-mydb}
    deploy:
      restart_policy:
        condition: on-failure
  roach:
    image: cockroachdb/cockroach:latest-v25.4
    container_name: roach
    hostname: db
    networks:
      - mynet
    ports:
      - 26257:26257
      - 8080:8080
    volumes:
      - roach:/cockroach/cockroach-data
    command: start-single-node --insecure

volumes:
  roach:

networks:
  mynet:
    driver: bridge
```

这个 Docker Compose 配置非常方便，因为你不必键入所有传递给 `docker run` 命令的参数。你可以声明性地在 Docker Compose 文件中完成这些操作。[Docker Compose 文档页面](/manuals/compose/_index.md) 非常详尽，包括 Docker Compose 文件格式的完整参考。

### `.env` 文件

Docker Compose 将自动从 `.env` 文件中读取环境变量（如果可用）。由于你的 Compose 文件要求 `PGPASSWORD` 已设置，将以下内容添加到 `.env` 文件中：

```bash
PGPASSWORD=whatever
```

确切的值对这个例子来说并不重要，因为你以不安全模式运行 CockroachDB。确保你设置某个值以避免出现错误。

### 合并 Compose 文件

文件名 `compose.yaml` 是 `docker compose` 命令识别的默认文件名（如果未提供 `-f` 标志）。这意味着如果你的环境有此类要求，可以有多个 Docker Compose 文件。此外，Docker Compose 文件是... 可组合的（双关语），因此可以在命令行上指定多个文件以将配置的不同部分合并在一起。以下列表只是一些示例场景，其中此类功能将非常有用：

- 对于本地开发使用源代码的绑定挂载，但在运行 CI 测试时不使用；
- 在为某些 API 应用使用预构建的前端镜像与为源代码创建绑定挂载之间切换；
- 为集成测试添加额外的服务；
- 还有很多...

你不会在这里涵盖任何这些高级用例。

### Docker Compose 中的变量替换

Docker Compose 的一个真正酷的功能是 [变量替换](/reference/compose-file/interpolation.md)。你可以在 Compose 文件的 `environment` 部分看到一些示例。例如：

- `PGUSER=${PGUSER:-totoro}` 意味着在容器内，环境变量 `PGUSER` 将被设置为与在运行 Docker Compose 的主机上相同的值。如果主机上没有此名称的环境变量，容器内的变量将获得默认值 `totoro`。
- `PGPASSWORD=${PGPASSWORD:?database password not set}` 意味着如果环境变量 `PGPASSWORD` 在主机上未设置，Docker Compose 将显示错误。这是可以的，因为你不想为密码硬编码默认值。你在 `.env` 文件中设置密码值，该文件位于你的本地机器上。最好将 `.env` 添加到 `.gitignore` 中，以防止密钥被检入版本控制。

其他处理未定义或空值的方法也存在，如 Docker 文档的 [变量替换](/reference/compose-file/interpolation.md) 部分所述。

### 验证 Docker Compose 配置

在应用对 Compose 配置文件的更改之前，有机会使用以下命令验证配置文件的内容：

```console
$ docker compose config
```

当运行此命令时，Docker Compose 会读取文件 `compose.yaml`，将其解析为内存中的数据结构，尽可能验证，并将其内部表示重建的配置文件打印回来。如果由于错误而无法做到这一点，Docker 会显示错误消息。

### 使用 Docker Compose 构建和运行应用

启动你的应用并确认它正在运行。

```console
$ docker compose up --build
```

你传递了 `--build` 标志，因此 Docker 将编译你的镜像然后启动它。

> [!NOTE]
>
> Docker Compose 是一个有用的工具，但它也有自己的怪癖。例如，除非提供 `--build` 标志，否则更新源代码不会触发重建。一个非常常见的陷阱是编辑源代码，然后忘记在运行 `docker compose up` 时使用 `--build` 标志。

由于你的设置现在由 Docker Compose 运行，它为其分配了一个项目名称，因此你的 CockroachDB 实例将获得一个新卷。这意味着你的应用将无法连接到数据库，因为数据库不存在于这个新卷中。终端显示数据库的身份验证错误：

```text
# ... 省略输出 ...
rest-server             | 2021/05/10 00:54:25 failed to initialise the store: pq: password authentication failed for user totoro
roach                   | *
roach                   | * INFO: Replication was disabled for this cluster.
roach                   | * When/if adding nodes in the future, update zone configurations to increase the replication factor.
roach                   | *
roach                   | CockroachDB node starting at 2021-05-10 00:54:26.398177 +0000 UTC (took 3.0s)
roach                   | build:               CCL v20.1.15 @ 2021/04/26 16:11:58 (go1.13.9)
roach                   | webui:               http://db:8080
roach                   | sql:                 postgresql://root@db:26257?sslmode=disable
roach                   | RPC client flags:    /cockroach/cockroach <client cmd> --host=db:26257 --insecure
roach                   | logs:                /cockroach/cockroach-data/logs
roach                   | temp dir:            /cockroach/cockroach-data/cockroach-temp349434348
roach                   | external I/O path:   /cockroach/cockroach-data/extern
roach                   | store[0]:            path=/cockroach/cockroach-data
roach                   | storage engine:      rocksdb
roach                   | status:              initialized new cluster
roach                   | clusterID:           b7b1cb93-558f-4058-b77e-8a4ddb329a88
roach                   | nodeID:              1
rest-server exited with code 0
rest-server             | 2021/05/10 00:54:25 failed to initialise the store: pq: password authentication failed for user totoro
rest-server             | 2021/05/10 00:54:26 failed to initialise the store: pq: password authentication failed for user totoro
rest-server             | 2021/05/10 00:54:29 failed to initialise the store: pq: password authentication failed for user totoro
rest-server             | 2021/05/10 00:54:25 failed to initialise the store: pq: password authentication failed for user totoro
rest-server             | 2021/05/10 00:54:26 failed to initialise the store: pq: password authentication failed for user totoro
rest-server             | 2021/05/10 00:54:29 failed to initialise the store: pq: password authentication failed for user totoro
rest-server exited with code 1
# ... 省略输出 ...
```

由于你使用 `restart_policy` 设置部署的方式，失败的容器每 20 秒自动重启一次。因此，要解决这个问题，你需要登录到数据库引擎并创建用户，如 [配置数据库引擎](#configure-the-database-engine) 中所述。

这并不是什么大问题。你只需要连接到 CockroachDB 实例并运行三个 SQL 命令来创建数据库和用户，如前面 [配置数据库引擎](#configure-the-database-engine) 中所述。一旦你这样做了（并且示例应用容器自动重启），`rest-service` 停止失败和重启，控制台变得安静。

有可能连接到之前使用的卷，但就本示例而言，这样做更麻烦，而且不值得，这也提供了一个机会来展示如何通过 Compose 文件功能 `restart_policy` 在你的部署中引入弹性。

### 测试应用

现在，测试你的 API 端点。在新终端中，运行以下命令：

```console
$ curl http://localhost/
```

你应该收到以下响应：

```json
Hello, Docker! (0)
```

### 关闭

要停止 Docker Compose 启动的容器，在运行 `docker compose up` 的终端中按 `ctrl+c`。容器停止后，运行 `docker compose down` 以移除它们。

### 分离模式

你可以使用 `-d` 标志以分离模式运行 `docker compose` 命令启动的容器，就像使用 `docker` 命令一样。

要以分离模式启动 Compose 文件定义的堆栈，运行：

```console
$ docker compose up --build -d
```

然后，你可以使用 `docker compose stop` 停止容器，并使用 `docker compose down` 移除它们。

## 进一步探索

你可以运行 `docker compose` 来查看还有哪些可用命令。

## 总结

本章有意省略了一些边缘但有趣的点。对于更有冒险精神的读者，本节提供了一些进一步研究的指针。

### 持久存储

托管卷不是为容器提供持久存储的唯一方法。强烈建议熟悉 Docker 中可用的存储选项及其用例，这些在 [在 Docker 中管理数据](/manuals/engine/storage/_index.md) 中有涵盖。

### CockroachDB 集群

你运行了单个 CockroachDB 实例，这对本示例来说已经足够了。但是，可以运行 CockroachDB 集群，它由多个 CockroachDB 实例组成，每个实例在自己的容器中运行。由于 CockroachDB 引擎在设计上是分布式的，运行具有多个节点的集群所需的更改出奇地少。

这种分布式设置提供了有趣的可能性，例如应用混沌工程技巧来模拟集群部分失败，并评估你的应用应对这些故障的能力。

如果你有兴趣试验 CockroachDB 集群，请查看：

- [在 Docker 中启动 CockroachDB 集群](https://www.cockroachlabs.com/docs/v20.2/start-a-local-cluster-in-docker-mac.html) 文章；以及
- Docker Compose 关键字 [`deploy`](/reference/compose-file/legacy-versions.md) 和 [`replicas`](/reference/compose-file/legacy-versions.md) 的文档。

### 其他数据库

由于你没有运行 CockroachDB 实例集群，你可能想知道是否可以使用非分布式数据库引擎。答案是“是的”，如果你要选择更传统的 SQL 数据库，比如 [PostgreSQL](https://www.postgresql.org/)，本章描述的过程会非常相似。

## 下一步

在本模块中，你设置了一个容器化开发环境，应用和数据库引擎在不同的容器中运行。你还编写了一个 Docker Compose 文件，将两个容器连接在一起，并提供了轻松启动和拆除开发环境的方法。

在下一模块中，你将了解在 Docker 中运行功能测试的一种可能方法。