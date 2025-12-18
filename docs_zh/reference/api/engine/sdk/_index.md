---
title: 使用 Docker Engine SDK 开发
linkTitle: SDK
weight: 10
description: 了解如何使用 Docker Engine SDK 在你选择的语言中自动化 Docker 任务
keywords: 开发, SDK, Docker Engine SDK, 安装 SDK, SDK 版本
aliases:
  - /develop/sdk/
  - /engine/api/sdks/
  - /engine/api/sdk/
---

Docker 提供了一个用于与 Docker 守护进程交互的 API（称为 Docker Engine API），以及 Go 和 Python 的 SDK。这些 SDK 允许你高效地构建和扩展 Docker 应用及解决方案。如果你不使用 Go 或 Python，也可以直接使用 Docker Engine API。

Docker Engine API 是一个 RESTful API，可通过 `wget` 或 `curl` 等 HTTP 客户端访问，或通过大多数现代编程语言内置的 HTTP 库访问。

## 安装 SDK

使用以下命令安装 Go 或 Python SDK。两个 SDK 可以同时安装并共存。

### Go SDK

```console
$ go get github.com/moby/moby/client
```

客户端需要较新版本的 Go。运行 `go version` 并确保你使用的是当前受支持的 Go 版本。

更多信息请参见 [Go 客户端参考](https://pkg.go.dev/github.com/moby/moby/client)。

### Python SDK

- 推荐方式：运行 `pip install docker`。

- 如果无法使用 `pip`：
  1.  [直接下载包](https://pypi.python.org/pypi/docker/)。
  2.  解压并切换到解压目录。
  3.  运行 `python setup.py install`。

更多信息请参见 [Docker Engine Python SDK 参考](https://docker-py.readthedocs.io/)。

## 查看 API 参考

你可以
[查看最新版本 API 的参考文档](/reference/api/engine/latest/)，
或 [选择特定版本](/reference/api/engine/#api-version-matrix)。

## 版本化 API 和 SDK

你应该使用的 Docker Engine API 版本取决于你的 Docker 守护进程和 Docker 客户端版本。详细信息请参见 API 文档中的 [版本化 API 和 SDK](/reference/api/engine/#versioned-api-and-sdk) 部分。

## SDK 和 API 快速入门

使用以下指南在代码中选择要使用的 SDK 或 API 版本：

- 如果你正在启动一个新项目，请使用 [最新版本](/reference/api/engine/latest/)，但使用 API 版本协商或指定你正在使用的版本。这有助于避免意外情况。
- 如果需要新功能，请更新代码以使用至少支持该功能的最低版本，并优先使用你能使用的最新版本。
- 否则，继续使用代码已有的版本。

例如，`docker run` 命令可以直接使用 Docker API 实现，也可以使用 Python 或 Go SDK 实现。

{{< tabs >}}
{{< tab name="Go" >}}

```go
package main

import (
	"context"
	"io"
	"os"

	"github.com/moby/moby/api/pkg/stdcopy"
	"github.com/moby/moby/api/types/container"
	"github.com/moby/moby/client"
)

func main() {
	ctx := context.Background()
	apiClient, err := client.New(client.FromEnv)
	if err != nil {
		panic(err)
	}
	defer apiClient.Close()

	reader, err := apiClient.ImagePull(ctx, "docker.io/library/alpine", client.ImagePullOptions{})
	if err != nil {
		panic(err)
	}
	io.Copy(os.Stdout, reader)

	resp, err := apiClient.ContainerCreate(ctx, client.ContainerCreateOptions{
		Image: "alpine",
		Config: &container.Config{
			Cmd: []string{"echo", "hello world"},
		},
	})
	if err != nil {
		panic(err)
	}

	if _, err := apiClient.ContainerStart(ctx, resp.ID, client.ContainerStartOptions{}); err != nil {
		panic(err)
	}

	wait := apiClient.ContainerWait(ctx, resp.ID, client.ContainerWaitOptions{})
	select {
	case err := <-wait.Error:
		if err != nil {
			panic(err)
		}
	case <-wait.Result:
	}

	out, err := apiClient.ContainerLogs(ctx, resp.ID, client.ContainerLogsOptions{ShowStdout: true})
	if err != nil {
		panic(err)
	}

	stdcopy.StdCopy(os.Stdout, os.Stderr, out)
}
```

{{< /tab >}}
{{< tab name="Python" >}}

```python
import docker
client = docker.from_env()
print(client.containers.run("alpine", ["echo", "hello", "world"]))
```

{{< /tab >}}
{{< tab name="HTTP" >}}

```console
$ curl --unix-socket /var/run/docker.sock -H "Content-Type: application/json" \
  -d '{"Image": "alpine", "Cmd": ["echo", "hello world"]}' \
  -X POST http://localhost/v{{% param "latest_engine_api_version" %}}/containers/create
{"Id":"1c6594faf5","Warnings":null}

$ curl --unix-socket /var/run/docker.sock -X POST http://localhost/v{{% param "latest_engine_api_version" %}}/containers/1c6594faf5/start

$ curl --unix-socket /var/run/docker.sock -X POST http://localhost/v{{% param "latest_engine_api_version" %}}/containers/1c6594faf5/wait
{"StatusCode":0}

$ curl --unix-socket /var/run/docker.sock "http://localhost/v{{% param "latest_engine_api_version" %}}/containers/1c6594faf5/logs?stdout=1"
hello world
```

使用 cURL 通过 Unix 套接字连接时，主机名不重要。前面的示例使用 `localhost`，但任何主机名都可以工作。

> [!IMPORTANT]
>
> 前面的示例假设你使用的是 cURL 7.50.0 或更高版本。较旧版本的 cURL 在使用套接字连接时使用了[非标准的 URL 表示法](https://github.com/moby/moby/issues/17960)。
>
> 如果你使用的是较旧版本的 cURL，请改用 `http:/<API version>/`，例如：`http:/v{{% param "latest_engine_api_version" %}}/containers/1c6594faf5/start`。

{{< /tab >}}
{{< /tabs >}}

更多示例请查看 [SDK 示例](examples.md)。

## 非官方库

有许多社区维护的其他语言库。它们未经 Docker 测试，因此如果遇到任何问题，请向库维护者提交问题。

| 语言 | 库                                                                     |
| :------- | :-------------------------------------------------------------------------- |
| C        | [libdocker](https://github.com/danielsuo/libdocker)                         |
| C#       | [Docker.DotNet](https://github.com/ahmetalpbalkan/Docker.DotNet)            |
| C++      | [lasote/docker_client](https://github.com/lasote/docker_client)             |
| Clojure  | [clj-docker-client](https://github.com/into-docker/clj-docker-client)       |
| Clojure  | [contajners](https://github.com/lispyclouds/contajners)                     |
| Dart     | [bwu_docker](https://github.com/bwu-dart/bwu_docker)                        |
| Erlang   | [erldocker](https://github.com/proger/erldocker)                            |
| Gradle   | [gradle-docker-plugin](https://github.com/gesellix/gradle-docker-plugin)    |
| Groovy   | [docker-client](https://github.com/gesellix/docker-client)                  |
| Haskell  | [docker-hs](https://github.com/denibertovic/docker-hs)                      |
| Java     | [docker-client](https://github.com/spotify/docker-client)                   |
| Java     | [docker-java](https://github.com/docker-java/docker-java)                   |
| Java     | [docker-java-api](https://github.com/amihaiemil/docker-java-api)            |
| Java     | [jocker](https://github.com/ndeloof/jocker)                                 |
| NodeJS   | [dockerode](https://github.com/apocas/dockerode)                            |
| NodeJS   | [harbor-master](https://github.com/arhea/harbor-master)                     |
| NodeJS   | [the-moby-effect](https://github.com/leonitousconforti/the-moby-effect)     |
| Perl     | [Eixo::Docker](https://github.com/alambike/eixo-docker)                     |
| PHP      | [Docker-PHP](https://github.com/docker-php/docker-php)                      |
| Ruby     | [docker-api](https://github.com/swipely/docker-api)                         |
| Rust     | [bollard](https://github.com/fussybeaver/bollard)                           |
| Rust     | [docker-rust](https://github.com/abh1nav/docker-rust)                       |
| Rust     | [shiplift](https://github.com/softprops/shiplift)                           |
| Scala    | [tugboat](https://github.com/softprops/tugboat)                             |
| Scala    | [reactive-docker](https://github.com/almoehi/reactive-docker)               |
| Swift    | [docker-client-swift](https://github.com/valeriomazzeo/docker-client-swift) |
