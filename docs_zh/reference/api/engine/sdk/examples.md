---
title: 使用 Docker Engine SDK 和 Docker API 的示例
linkTitle: 示例
description: 使用 Go 和 Python SDK 以及使用 curl 的 HTTP API 执行特定 Docker 操作的示例。
keywords: developing, api, sdk, developers, rest, curl, python, go
aliases:
  - /engine/api/getting-started/
  - /engine/api/client-libraries/
  - /engine/reference/api/remote_api_client_libraries/
  - /reference/api/remote_api_client_libraries/
  - /develop/sdk/examples/
  - /engine/api/sdk/examples/
---

在您
[安装 Docker](/get-started/get-docker.md) 之后，您可以
[安装 Go 或 Python SDK](index.md#install-the-sdks) 并尝试使用 Docker Engine API。

以下每个示例都展示了如何使用 Go 和 Python SDK 以及使用 `curl` 的 HTTP API 执行特定的 Docker 操作。

## 运行容器

第一个示例展示了如何使用 Docker API 运行容器。在命令行中，您会使用 `docker run` 命令，但从您自己的应用程序中执行同样简单。

这相当于在命令提示符下输入 `docker run alpine echo hello world`：

{{< tabs group="lang" >}}
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

	defer reader.Close()
	// cli.ImagePull 是异步的。
	// 需要完全读取 reader 才能完成拉取操作。
	// 如果不需要 stdout，可以考虑使用 io.Discard 替代 os.Stdout。
	io.Copy(os.Stdout, reader)

	resp, err := apiClient.ContainerCreate(ctx, client.ContainerCreateOptions{
		Config: &container.Config{
			Cmd: []string{"echo", "hello world"},
			Tty: false,
		},
		Image: "alpine",
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

使用 cURL 通过 Unix 套接字连接时，主机名并不重要。前面的示例使用了 `localhost`，但任何主机名都可以。

> [!IMPORTANT]
>
> 前面的示例假设您使用的是 cURL 7.50.0 或更高版本。旧版本的 cURL 在使用套接字连接时使用了[非标准 URL 表示法](https://github.com/moby/moby/issues/17960)。
>
> 如果您使用的是旧版本的 cURL，请使用 `http:/<API version>/`，例如：`http:/v{{% param "latest_engine_api_version" %}}/containers/1c6594faf5/start`。

{{< /tab >}}
{{< /tabs >}}

## 在后台运行容器

您也可以在后台运行容器，相当于输入 `docker run -d bfirsh/reticulate-splines`：

{{< tabs group="lang" >}}
{{< tab name="Go" >}}

```go
package main

import (
	"context"
	"fmt"
	"io"
	"os"

	"github.com/moby/moby/client"
)

func main() {
	ctx := context.Background()
	apiClient, err := client.New(client.FromEnv)
	if err != nil {
		panic(err)
	}
	defer apiClient.Close()

	imageName := "bfirsh/reticulate-splines"

	out, err := apiClient.ImagePull(ctx, imageName, client.ImagePullOptions{})
	if err != nil {
		panic(err)
	}
	defer out.Close()
	io.Copy(os.Stdout, out)

	resp, err := apiClient.ContainerCreate(ctx, client.ContainerCreateOptions{
		Image: imageName,
	})
	if err != nil {
		panic(err)
	}

	if _, err := apiClient.ContainerStart(ctx, resp.ID, client.ContainerStartOptions{}); err != nil {
		panic(err)
	}

	fmt.Println(resp.ID)
}
```

{{< /tab >}}
{{< tab name="Python" >}}

```python
import docker
client = docker.from_env()
container = client.containers.run("bfirsh/reticulate-splines", detach=True)
print(container.id)
```

{{< /tab >}}
{{< tab name="HTTP" >}}

```console
$ curl --unix-socket /var/run/docker.sock -H "Content-Type: application/json" \
  -d '{"Image": "bfirsh/reticulate-splines"}' \
  -X POST http://localhost/v{{% param "latest_engine_api_version" %}}/containers/create
{"Id":"1c6594faf5","Warnings":null}

$ curl --unix-socket /var/run/docker.sock -X POST http://localhost/v{{% param "latest_engine_api_version" %}}/containers/1c6594faf5/start
```

{{< /tab >}}
{{< /tabs >}}

## 列出和管理容器

您可以使用 API 列出正在运行的容器，就像使用 `docker ps` 一样：

{{< tabs group="lang" >}}
{{< tab name="Go" >}}

```go
package main

import (
	"context"
	"fmt"

	"github.com/moby/moby/client"
)

func main() {
	ctx := context.Background()
	apiClient, err := client.New(client.FromEnv)
	if err != nil {
		panic(err)
	}
	defer apiClient.Close()

	containers, err := apiClient.ContainerList(ctx, client.ContainerListOptions{})
	if err != nil {
		panic(err)
	}

	for _, container := range containers.Items {
		fmt.Println(container.ID)
	}
}
```

{{< /tab >}}
{{< tab name="Python" >}}

```python
import docker
client = docker.from_env()
for container in client.containers.list():
  print(container.id)
```

{{< /tab >}}
{{< tab name="HTTP" >}}

```console
$ curl --unix-socket /var/run/docker.sock http://localhost/v{{% param "latest_engine_api_version" %}}/containers/json
[{
  "Id":"ae63e8b89a26f01f6b4b2c9a7817c31a1b6196acf560f66586fbc8809ffcd772",
  "Names":["/tender_wing"],
  "Image":"bfirsh/reticulate-splines",
  ...
}]
```

{{< /tab >}}
{{< /tabs >}}

## 停止所有正在运行的容器

现在您知道了哪些容器存在，可以对它们执行操作。此示例停止所有正在运行的容器。

> [!NOTE]
>
> 请勿在生产服务器上运行此操作。此外，如果您使用的是 swarm 服务，容器会停止，但 Docker 会创建新的容器以保持服务在其配置状态下运行。

{{< tabs group="lang" >}}
{{< tab name="Go" >}}

```go
package main

import (
	"context"
	"fmt"

	"github.com/moby/moby/client"
)

func main() {
	ctx := context.Background()
	apiClient, err := client.New(client.FromEnv)
	if err != nil {
		panic(err)
	}
	defer apiClient.Close()

	containers, err := apiClient.ContainerList(ctx, client.ContainerListOptions{})
	if err != nil {
		panic(err)
	}

	for _, container := range containers.Items {
		fmt.Print("正在停止容器 ", container.ID[:10], "... ")
		noWaitTimeout := 0 // 不等待容器正常退出
		if _, err := apiClient.ContainerStop(ctx, container.ID, client.ContainerStopOptions{Timeout: &noWaitTimeout}); err != nil {
			panic(err)
		}
		fmt.Println("成功")
	}
}
```

{{< /tab >}}
{{< tab name="Python" >}}

```python
import docker
client = docker.from_env()
for container in client.containers.list():
  container.stop()
```

{{< /tab >}}
{{< tab name="HTTP" >}}

```console
$ curl --unix-socket /var/run/docker.sock http://localhost/v{{% param "latest_engine_api_version" %}}/containers/json
[{
  "Id":"ae63e8b89a26f01f6b4b2c9a7817c31a1b6196acf560f66586fbc8809ffcd772",
  "Names":["/tender_wing"],
  "Image":"bfirsh/reticulate-splines",
  ...
}]

$ curl --unix-socket /var/run/docker.sock \
  -X POST http://localhost/v{{% param "latest_engine_api_version" %}}/containers/ae63e8b89a26/stop
```

{{< /tab >}}
{{< /tabs >}}

## 打印特定容器的日志

您也可以对单个容器执行操作。此示例打印给定 ID 的容器的日志。在运行代码之前，您需要修改代码以更改硬编码的容器 ID，以打印对应容器的日志。

{{< tabs group="lang" >}}
{{< tab name="Go" >}}

```go
package main

import (
	"context"
	"io"
	"os"

	"github.com/moby/moby/client"
)

func main() {
	ctx := context.Background()
	apiClient, err := client.New(client.FromEnv)
	if err != nil {
		panic(err)
	}
	defer apiClient.Close()

	options := client.ContainerLogsOptions{ShowStdout: true}
	// 将此 ID 替换为实际存在的容器
	out, err := apiClient.ContainerLogs(ctx, "f1064a8a4c82", options)
	if err != nil {
		panic(err)
	}

	io.Copy(os.Stdout, out)
}
```

{{< /tab >}}
{{< tab name="Python" >}}

```python
import docker
client = docker.from_env()
container = client.containers.get('f1064a8a4c82')
print(container.logs())
```

{{< /tab >}}
{{< tab name="HTTP" >}}

```console
$ curl --unix-socket /var/run/docker.sock "http://localhost/v{{% param "latest_engine_api_version" %}}/containers/ca5f55cdb/logs?stdout=1"
Reticulating spline 1...
Reticulating spline 2...
Reticulating spline 3...
Reticulating spline 4...
Reticulating spline 5...
```

{{< /tab >}}
{{< /tabs >}}

## 列出所有镜像

列出引擎上的镜像，类似于 `docker image ls`：

{{< tabs group="lang" >}}
{{< tab name="Go" >}}

```go
package main

import (
	"context"
	"fmt"

	"github.com/moby/moby/client"
)

func main() {
	ctx := context.Background()
	apiClient, err := client.New(client.FromEnv)
	if err != nil {
		panic(err)
	}
	defer apiClient.Close()

	images, err := apiClient.ImageList(ctx, client.ImageListOptions{})
	if err != nil {
		panic(err)
	}

	for _, image := range images.Items {
		fmt.Println(image.ID)
	}
}
```

{{< /tab >}}
{{< tab name="Python" >}}

```python
import docker
client = docker.from_env()
for image in client.images.list():
  print(image.id)
```

{{< /tab >}}
{{< tab name="HTTP" >}}

```console
$ curl --unix-socket /var/run/docker.sock http://localhost/v{{% param "latest_engine_api_version" %}}/images/json
[{
  "Id":"sha256:31d9a31e1dd803470c5a151b8919ef1988ac3efd44281ac59d43ad623f275dcd",
  "ParentId":"sha256:ee4603260daafe1a8c2f3b78fd760922918ab2441cbb2853ed5c439e59c52f96",
  ...
}]
```

{{< /tab >}}
{{< /tabs >}}

## 拉取镜像

拉取镜像，类似于 `docker pull`：

{{< tabs group="lang" >}}
{{< tab name="Go" >}}

```go
package main

import (
	"context"
	"io"
	"os"

	"github.com/moby/moby/client"
)

func main() {
	ctx := context.Background()
	apiClient, err := client.New(client.FromEnv)
	if err != nil {
		panic(err)
	}
	defer apiClient.Close()

	out, err := apiClient.ImagePull(ctx, "alpine", client.ImagePullOptions{})
	if err != nil {
		panic(err)
	}

	defer out.Close()

	io.Copy(os.Stdout, out)
}
```

{{< /tab >}}
{{< tab name="Python" >}}

```python
import docker
client = docker.from_env()
image = client.images.pull("alpine")
print(image.id)
```

{{< /tab >}}
{{< tab name="HTTP" >}}

```console
$ curl --unix-socket /var/run/docker.sock \
  -X POST "http://localhost/v{{% param "latest_engine_api_version" %}}/images/create?fromImage=alpine"
{"status":"Pulling from library/alpine","id":"3.1"}
{"status":"Pulling fs layer","progressDetail":{},"id":"8f13703509f7"}
{"status":"Downloading","progressDetail":{"current":32768,"total":2244027},"progress":"[\u003e                                                  ] 32.77 kB/2.244 MB","id":"8f13703509f7"}
...
```

{{< /tab >}}
{{< /tabs >}}

## 使用身份验证拉取镜像

使用身份验证拉取镜像，类似于 `docker pull`：

> [!NOTE]
>
> 凭据以明文形式发送。Docker 的官方注册表使用 HTTPS。私有注册表也应配置为使用 HTTPS。

{{< tabs group="lang" >}}
{{< tab name="Go" >}}

```go
package main

import (
	"context"
	"encoding/base64"
	"encoding/json"
	"io"
	"os"

	"github.com/moby/moby/api/types/registry"
	"github.com/moby/moby/client"
)

func main() {
	ctx := context.Background()
	apiClient, err := client.New(client.FromEnv)
	if err != nil {
		panic(err)
	}
	defer apiClient.Close()

	authConfig := registry.AuthConfig{
		Username: "username",
		Password: "password",
	}
	encodedJSON, err := json.Marshal(authConfig)
	if err != nil {
		panic(err)
	}
	authStr := base64.URLEncoding.EncodeToString(encodedJSON)

	out, err := apiClient.ImagePull(ctx, "alpine", client.ImagePullOptions{RegistryAuth: authStr})
	if err != nil {
		panic(err)
	}

	defer out.Close()
	io.Copy(os.Stdout, out)
}
```

{{< /tab >}}
{{< tab name="Python" >}}

Python SDK 从 [凭据存储](/reference/cli/docker/login/#credential-stores) 文件中检索身份验证信息，并与 [凭据助手](https://github.com/docker/docker-credential-helpers) 集成。可以覆盖这些凭据，但这超出了本示例指南的范围。使用 `docker login` 后，Python SDK 会自动使用这些凭据。

```python
import docker
client = docker.from_env()
image = client.images.pull("alpine")
print(image.id)
```

{{< /tab >}}
{{< tab name="HTTP" >}}

此示例将凭据保留在 shell 的历史记录中，因此请将其视为一种简单的实现方式。凭据以 Base-64 编码的 JSON 结构传递。

```console
$ JSON=$(echo '{"username": "string", "password": "string", "serveraddress": "string"}' | base64)

$ curl --unix-socket /var/run/docker.sock \
  -H "Content-Type: application/tar"
  -X POST "http://localhost/v{{% param "latest_engine_api_version" %}}/images/create?fromImage=alpine"
  -H "X-Registry-Auth"
  -d "$JSON"
{"status":"Pulling from library/alpine","id":"3.1"}
{"status":"Pulling fs layer","progressDetail":{},"id":"8f13703509f7"}
{"status":"Downloading","progressDetail":{"current":32768,"total":2244027},"progress":"[\u003e                                                  ] 32.77 kB/2.244 MB","id":"8f13703509f7"}
...
```

{{< /tab >}}
{{< /tabs >}}

## 提交容器

提交容器以从其内容创建镜像：

{{< tabs group="lang" >}}
{{< tab name="Go" >}}

```go
package main

import (
	"context"
	"fmt"

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

	createResp, err := apiClient.ContainerCreate(ctx, client.ContainerCreateOptions{
		Config: &container.Config{
			Cmd: []string{"touch", "/helloworld"},
		},
		Image: "alpine",
	})
	if err != nil {
		panic(err)
	}

	if _, err := apiClient.ContainerStart(ctx, createResp.ID, client.ContainerStartOptions{}); err != nil {
		panic(err)
	}

	wait := apiClient.ContainerWait(ctx, createResp.ID, client.ContainerWaitOptions{})
	select {
	case err := <-wait.Error:
		if err != nil {
			panic(err)
		}
	case <-wait.Result:
	}

	commitResp, err := apiClient.ContainerCommit(ctx, createResp.ID, client.ContainerCommitOptions{Reference: "helloworld"})
	if err != nil {
		panic(err)
	}

	fmt.Println(commitResp.ID)
}
```

{{< /tab >}}
{{< tab name="Python" >}}

```python
import docker
client = docker.from_env()
container = client.containers.run("alpine", ["touch", "/helloworld"], detach=True)
container.wait()
image = container.commit("helloworld")
print(image.id)
```

{{< /tab >}}
{{< tab name="HTTP" >}}

```console
$ docker run -d alpine touch /helloworld
0888269a9d584f0fa8fc96b3c0d8d57969ceea3a64acf47cd34eebb4744dbc52
$ curl --unix-socket /var/run/docker.sock\
  -X POST "http://localhost/v{{% param "latest_engine_api_version" %}}/commit?container=0888269a9d&repo=helloworld"
{"Id":"sha256:6c86a5cd4b87f2771648ce619e319f3e508394b5bfc2cdbd2d60f59d52acda6c"}
```

{{< /tab >}}
{{< /tabs >}}