# 检查你的构建配置




构建检查（Build checks）是 Dockerfile 1.8 中引入的一项功能。它可以让你
在执行构建之前验证构建配置并运行一系列检查。可以将其视为针对你的 Dockerfile
和构建选项的一种高级 lint 形式，或者说是一种构建的预检（dry-run）模式。

你可以在 [构建检查参考](/reference/build-checks/) 中找到可用的检查列表以及各自的描述。

## 构建检查的工作原理

通常，当你运行构建时，Docker 会按照你的 Dockerfile 和构建选项中所指定的那样
执行构建步骤。而使用构建检查后，Docker 不会执行构建步骤，而是检查你提供的
Dockerfile 和选项，并报告它发现的任何问题。

构建检查适用于以下场景：

- 在运行构建之前验证你的 Dockerfile 和构建选项。
- 确保你的 Dockerfile 和构建选项与最新的最佳实践保持一致。
- 识别你的 Dockerfile 和构建选项中潜在的问题或反模式。

> [!TIP]
>
> 若要在 Visual Studio Code 中改进 Dockerfile 的 lint、代码导航和漏洞扫描，
> 请参阅 [Docker DX](https://marketplace.visualstudio.com/items?itemName=docker.docker) 扩展。

## 构建时运行检查

以下版本支持构建检查：

- Buildx 0.15.0 及更高版本
- [docker/build-push-action](https://github.com/docker/build-push-action) 6.6.0 及更高版本
- [docker/bake-action](https://github.com/docker/bake-action) 5.6.0 及更高版本

默认情况下，调用构建时就会运行检查，并在构建输出中显示任何违规项。例如，下面的命令
既构建镜像又运行检查：

```console
$ docker build .
[+] Building 3.5s (11/11) FINISHED
...

1 warning found (use --debug to expand):
  - Lint Rule 'JSONArgsRecommended': JSON arguments recommended for CMD to prevent unintended behavior related to OS signals (line 7)

```

在此示例中，构建成功运行，但报告了一个
[JSONArgsRecommended](/reference/build-checks/json-args-recommended/) 警告，
因为 `CMD` 指令应使用 JSON 数组语法。

在 GitHub Actions 中，检查会显示在拉取请求的 diff 视图中。

```yaml
name: Build and push Docker images
on:
  push:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Build and push
        uses: docker/build-push-action@v7
```

![GitHub Actions 构建检查注解](./images/gha-check-annotations.png)

### 更详细的输出

常规 `docker build` 的检查警告会显示一条简洁的消息，其中包含规则名称、消息，
以及问题在 Dockerfile 中所在的行号。如果你想查看有关检查的更详细信息，可以使用
`--debug` 标志。例如：

```console
$ docker --debug build .
[+] Building 3.5s (11/11) FINISHED
...

 1 warning found:
 - JSONArgsRecommended: JSON arguments recommended for CMD to prevent unintended behavior related to OS signals (line 4)
JSON arguments recommended for ENTRYPOINT/CMD to prevent unintended behavior related to OS signals
More info: https://docs.docker.com/go/dockerfile/rule/json-args-recommended/
Dockerfile:4
--------------------
   2 |
   3 |     FROM alpine
   4 | >>> CMD echo "Hello, world!"
   5 |
--------------------

```

使用 `--debug` 标志时，输出中会包含指向该检查文档的链接，以及问题所在 Dockerfile 片段。

## 在不构建的情况下检查构建

要在不实际构建的情况下运行构建检查，你可以像往常一样使用 `docker build` 命令，
只是额外加上 `--check` 标志。示例如下：

```console
$ docker build --check .
```

该命令不会执行构建步骤，而只会运行检查并报告它发现的任何问题。如果存在任何问题，
它们将在输出中报告。例如：

```text {title="使用 --check 的输出"}
[+] Building 1.5s (5/5) FINISHED
=> [internal] connecting to local controller
=> [internal] load build definition from Dockerfile
=> => transferring dockerfile: 253B
=> [internal] load metadata for docker.io/library/node:22
=> [auth] library/node:pull token for registry-1.docker.io
=> [internal] load .dockerignore
=> => transferring context: 50B
JSONArgsRecommended - https://docs.docker.com/go/dockerfile/rule/json-args-recommended/
JSON arguments recommended for ENTRYPOINT/CMD to prevent unintended behavior related to OS signals
Dockerfile:7
--------------------
5 |
6 |     COPY index.js .
7 | >>> CMD node index.js
8 |
--------------------
```

带有 `--check` 的此输出显示了该检查的 [verbose message](#more-verbose-output)。

与常规构建不同，当使用 `--check` 标志时报告了任何违规项，命令会以非零状态码退出。

## 在检查违规时使构建失败

默认情况下，构建的检查违规会被报告为警告，退出码为 0。你可以配置 Docker，
当报告违规时使构建失败，方法是在 Dockerfile 中使用 `check=error=true` 指令。
这会导致在运行构建检查之后、实际构建执行之前，构建报错退出。

```dockerfile {title=Dockerfile,linenos=true,hl_lines=2}
# syntax=docker/dockerfile:1
# check=error=true

FROM alpine
CMD echo "Hello, world!"
```

如果没有 `# check=error=true` 指令，此构建将以退出码 0 完成。然而，使用该指令后，
构建检查违规会导致非零退出码：

```console
$ docker build .
[+] Building 1.5s (5/5) FINISHED
...

 1 warning found (use --debug to expand):
 - JSONArgsRecommended: JSON arguments recommended for CMD to prevent unintended behavior related to OS signals (line 5)
Dockerfile:1
--------------------
   1 | >>> # syntax=docker/dockerfile:1
   2 |     # check=error=true
   3 |
--------------------
ERROR: lint violation found for rules: JSONArgsRecommended
$ echo $?
1
```

你也可以通过在 CLI 上传递 `BUILDKIT_DOCKERFILE_CHECK` 构建参数来设置该错误指令：

```console
$ docker build --check --build-arg "BUILDKIT_DOCKERFILE_CHECK=error=true" .
```

## 跳过检查

默认情况下，构建镜像时会运行所有检查。如果要跳过特定检查，可以在 Dockerfile 中
使用 `check=skip` 指令。`skip` 参数接受一个 CSV 格式的待跳过检查 ID 字符串。
例如：

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=skip=JSONArgsRecommended,StageNameCasing

FROM alpine AS BASE_STAGE
CMD echo "Hello, world!"
```

构建此 Dockerfile 不会产生任何检查违规。

你也可以通过在构建参数中传递 `BUILDKIT_DOCKERFILE_CHECK` 并附带一个 CSV 格式的
待跳过检查 ID 字符串来跳过检查。例如：

```console
$ docker build --check --build-arg "BUILDKIT_DOCKERFILE_CHECK=skip=JSONArgsRecommended,StageNameCasing" .
```

要跳过所有检查，使用 `skip=all` 参数：

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=skip=all
```

## 组合 error 与 skip 参数用于检查指令

若要同时跳过特定检查并在检查违规时报错，可将 `skip` 和 `error` 两个参数用分号（`;`）
分隔后传递给 Dockerfile 中的 `check` 指令，或传递给构建参数。例如：

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=skip=JSONArgsRecommended,StageNameCasing;error=true
```

```console {title="构建参数"}
$ docker build --check --build-arg "BUILDKIT_DOCKERFILE_CHECK=skip=JSONArgsRecommended,StageNameCasing;error=true" .
```

## 实验性检查

在检查被提升为稳定版之前，它们可能作为实验性检查提供。实验性检查默认是禁用的。
要查看可用的实验性检查列表，请参阅 [构建检查参考](/reference/build-checks/)。

要启用所有实验性检查，请将 `BUILDKIT_DOCKERFILE_CHECK` 构建参数设置为 `experimental=all`：

```console
$ docker build --check --build-arg "BUILDKIT_DOCKERFILE_CHECK=experimental=all" .
```

你也可以使用 `check` 指令在 Dockerfile 中启用实验性检查：

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=experimental=all
```

要选择性地启用实验性检查，可以传入一个 CSV 格式的待启用检查 ID 字符串，既可传给
Dockerfile 中的 `check` 指令，也可作为构建参数。例如：

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=experimental=JSONArgsRecommended,StageNameCasing
```

请注意，`experimental` 指令优先于 `skip` 指令，这意味着无论你设置的 `skip` 指令
如何，实验性检查都会运行。例如，如果你设置了 `skip=all` 并启用了实验性检查，
实验性检查仍会运行：

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=skip=all;experimental=all
```

## 延伸阅读

有关使用构建检查的更多信息，请参阅：

- [构建检查参考](/reference/build-checks/)
- [使用 GitHub Actions 验证构建配置](/manuals/build/ci/github-actions/checks.md)

