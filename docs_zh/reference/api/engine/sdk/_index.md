---
title: 使用 Docker Engine SDK 进行开发
linkTitle: SDK
weight: 10
description: 了解如何使用 Docker Engine SDK 以您选择的语言自动化 Docker 任务
keywords: developing, sdk, Docker Engine SDKs, install SDKs, SDK versions
aliases:
- /develop/sdk/
- /engine/api/sdks/
- /engine/api/sdk/
---

Docker 提供了一个用于与 Docker 守护进程交互的 API（称为 Docker Engine API），以及用于 Go 和 Python 的 SDK。这些 SDK 让您可以高效地构建和扩展 Docker 应用程序和解决方案。如果 Go 或 Python 不适合您，您可以直接使用 Docker Engine API。

Docker Engine API 是一个 RESTful API，可以通过 `wget` 或 `curl` 等 HTTP 客户端访问，或者通过大多数现代编程语言附带的 HTTP 库访问。

## 安装 SDK

使用以下命令安装 Go 或 Python SDK。两个 SDK 可以同时安装并共存。

### Go SDK

```console
$ go get github.com/moby/moby/client
```

该客户端需要较新版本的 Go。运行 `go version` 并确保您运行的是当前受支持的 Go 版本。

更多信息，请参阅 [Go 客户端参考](https://pkg.go.dev/github.com/moby/moby/client)。

### Python SDK

- 推荐：运行 `pip install docker`。

- 如果您无法使用 `pip`：
  1.  [直接下载软件包](https://pypi.python.org/pypi/docker/)。
  2.  解压并切换到解压后的目录。
  3.  运行 `python setup.py install`。

更多信息，请参阅 [Docker Engine Python SDK 参考](https://docker-py.readthedocs.io/)。

## 查看 API 参考

您可以[查看最新版本 API 的参考](/reference/api/engine/latest/)或[选择特定版本](/reference/api/engine/#api-version-matrix)。

## 版本化的 API 和 SDK

您应该使用的 Docker Engine API 版本取决于您的 Docker 守护进程和 Docker 客户端的版本。有关详细信息，请参阅 API 文档中的[版本化 API 和 SDK](/reference/api/engine/#versioned-api-and-sdk)部分。

## SDK 和 API 快速入门

使用以下指南选择要在代码中使用的 SDK 或 API 版本：

- 如果您要启动一个新项目，请使用[最新版本](/reference/api/engine/latest/)，但要使用 API 版本协商或指定您正在使用的版本。这有助于避免意外情况。
- 如果您需要新功能，请将代码更新为至少使用支持该功能的最低版本，并优先使用您可以使用的最新版本。
- 否则，请继续使用代码已经在使用的版本。

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

当使用 cURL 通过 Unix 套接字连接时，主机名并不重要。前面的示例使用 `localhost`，但任何主机名都可以工作。

> [!IMPORTANT]
>
> 前面的示例假设您使用的是 cURL 7.50.0 或更高版本。旧版本的 cURL 在使用套接字连接时使用了[非标准 URL 表示法](https://github.com/moby/moby/issues/17960)。
>
> 如果您使用的是旧版本的 cURL，请改用 `http:/<API version>/`，例如：`http:/v{{% param "latest_engine_api_version" %}}/containers/1c6594faf5/start`。

{{< /tab >}}
{{< /tabs >}}

更多示例，请参阅 [SDK 示例](examples.md)。

## 非官方库

有许多社区支持的其他语言库。它们未经 Docker 测试，因此如果您遇到任何问题，请向库维护者提交问题。

| 语言 | 库 |
| :------- | :-------------------------------------------------------------------------- |
| C | [libdocker](https://github.com/danielsuo/libdocker) |
| C# | [Docker.DotNet](https://github.com/ahmetalpbalkan/Docker.DotNet) |
| C++ | [lasote/docker_client](https://github.com/lasote/docker_client) |
| Clojure | [clj-docker-client](https://github.com/into-docker/clj-docker-client) |
| Clojure | [contajners](https://github.com/lispyclouds/contajners) |
| Dart | [bwu_docker](https://github.com/bwu-dart/bwu_docker) |
| Erlang | [erldocker](https://github.com/proger/erldocker) |
| Gradle | [gradle-docker-plugin](https://github.com/gesellix/gradle-docker-plugin) |
| Groovy | [docker-client](https://github.com/gesellix/docker-client) |
| Haskell | [docker-hs](https://github.com/denibertovic/docker-hs) |
| Java | [docker-client](https://github.com/spotify/docker-client) |
| Java | [docker-java](https://github.com/docker-java/docker-java) |
| Java | [docker-java-api](https://github.com/amihaiemil/docker-java-api) |
| Java | [jocker](https://github.com/ndeloof/jocker) |
| NodeJS | [dockerode](https://github.com/apocas/dockerode) |
| NodeJS | [harbor-master](https://github.com/arhea/harbor-master) |
| NodeJS | [the-moby-effect](https://github.com/leonitousconforti/the-moby-effect) |
| Perl | [Eixo::Docker](https://github.com/alambike/eixo-docker) |
| PHP | [Docker-PHP](https://github.com/docker-php/docker-php) |
| Ruby | [docker-api](https://github.com/swipely/docker-api) |
| Rust | [bollard](https://github.com/fussybeaver/bollard) |
| Rust | [docker-rust](https://github.com/abh1nav/docker-rust) |
| Rust | [shiplift](https://github.com/softprops/shiplift) |
| Scala | [tugboat](https://github.com/softprops/tugboat) |
| Scala | [reactive-docker](https://github.com/almoehi/reactive-docker) |
| Swift | [docker-client-swift](https://github.com/valeriomazzeo/docker-client-swift) |