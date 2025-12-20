# Docker Engine API

Docker 提供了一个用于与 Docker 守护进程交互的 API（称为 Docker Engine API），以及用于 Go 和 Python 的 SDK。这些 SDK 让您可以高效地构建和扩展 Docker 应用和解决方案。如果 Go 或 Python 不适合您，您可以直接使用 Docker Engine API。

有关 Docker Engine SDK 的信息，请参阅 [使用 Docker Engine SDK 进行开发](sdk/_index.md)。

Docker Engine API 是一个 RESTful API，可以通过 HTTP 客户端（如 `wget` 或 `curl`）或大多数现代编程语言附带的 HTTP 库进行访问。

## 查看 API 参考

您可以[查看最新版本的 API 参考](/reference/api/engine/version/v1.52.md)或[选择特定版本](/reference/api/engine/#api-version-matrix)。

## 版本化的 API 和 SDK

您应该使用的 Docker Engine API 版本取决于您的 Docker 守护进程和 Docker 客户端的版本。

特定版本的 Docker Engine SDK 支持特定版本的 Docker Engine API，以及所有早期版本。如果发生破坏性变更，会显著记录这些变更。

> [!NOTE]
>
> Docker 守护进程和客户端不一定总是需要相同的版本。但是，请记住以下几点：
>
> - 如果守护进程比客户端新，客户端将不知道守护进程中的新功能或已弃用的 API 端点。
> - 如果客户端比守护进程新，客户端可以请求守护进程不知道的 API 端点。

当添加新功能时，会发布新版本的 API。Docker API 是向后兼容的，因此除非您需要利用新功能，否则不需要更新使用 API 的代码。

要查看您的 Docker 守护进程和客户端支持的最高 API 版本，请使用 `docker version`：

```console
$ docker version
Client: Docker Engine - Community
 Version:           29.1.3
 API version:       1.52
 Go version:        go1.25.5
 Git commit:        f52814d
 Built:             Fri Dec 12 14:50:13 2025
 OS/Arch:           linux/arm64
 Context:           default

Server: Docker Engine - Community
 Engine:
  Version:          29.1.3
  API version:      1.52 (minimum version 1.44)
  Go version:       go1.25.5
  Git commit:       fbf3ed2
  Built:            Fri Dec 12 14:50:13 2025
  OS/Arch:          linux/arm64
  ...
```

您可以通过以下任何一种方式指定要使用的 API 版本：

- 使用 SDK 时，请使用最新版本。至少，使用包含您所需功能的 API 版本。
- 直接使用 `curl` 时，将版本指定为 URL 的第一部分。例如，如果端点是 `/containers/`，您可以使用 `/v1.52/containers/`。
- 要强制 Docker CLI 或 Docker Engine SDK 使用比 `docker version` 报告的版本更旧的 API 版本，请将环境变量 `DOCKER_API_VERSION` 设置为正确的版本。这在 Linux、Windows 或 macOS 客户端上有效。

  
  ```console
  $ DOCKER_API_VERSION=1.51
  ```
  

  虽然设置了环境变量，但会使用该版本的 API，即使 Docker 守护进程支持更新的版本也是如此。此环境变量会禁用 API 版本协商，因此您应该仅在必须使用特定版本的 API 或出于调试目的时才使用它。

- Docker Go SDK 允许您启用 API 版本协商，自动选择由客户端和正在使用的 Docker Engine 都支持的 API 版本。
- 对于 SDK，您还可以以编程方式将 API 版本指定为 `client` 对象的参数。请参阅 [Go 构造函数](https://pkg.go.dev/github.com/docker/docker/client#NewClientWithOpts)或 [Python SDK 的 `client` 文档](https://docker-py.readthedocs.io/en/stable/client.html)。

### API 版本矩阵

| Docker 版本 | 最大 API 版本                                | 变更日志                                                               |
| :---------- | :------------------------------------------- | :--------------------------------------------------------------------- |
| 29.0        | [1.52](/reference/api/engine/version/v1.52/) | [变更](/reference/api/engine/version-history/#v152-api-changes)        |
| 28.3        | [1.51](/reference/api/engine/version/v1.51/) | [变更](/reference/api/engine/version-history/#v151-api-changes)        |
| 28.2        | [1.50](/reference/api/engine/version/v1.50/) | [变更](/reference/api/engine/version-history/#v150-api-changes)        |
| 28.1        | [1.49](/reference/api/engine/version/v1.49/) | [变更](/reference/api/engine/version-history/#v149-api-changes)        |
| 28.0        | [1.48](/reference/api/engine/version/v1.48/) | [变更](/reference/api/engine/version-history/#v148-api-changes)        |
| 27.5        | [1.47](/reference/api/engine/version/v1.47/) | [变更](/reference/api/engine/version-history/#v147-api-changes)        |
| 27.4        | [1.47](/reference/api/engine/version/v1.47/) | [变更](/reference/api/engine/version-history/#v147-api-changes)        |
| 27.3        | [1.47](/reference/api/engine/version/v1.47/) | [变更](/reference/api/engine/version-history/#v147-api-changes)        |
| 27.2        | [1.47](/reference/api/engine/version/v1.47/) | [变更](/reference/api/engine/version-history/#v147-api-changes)        |
| 27.1        | [1.46](/reference/api/engine/version/v1.46/) | [变更](/reference/api/engine/version-history/#v146-api-changes)        |
| 27.0        | [1.46](/reference/api/engine/version/v1.46/) | [变更](/reference/api/engine/version-history/#v146-api-changes)        |
| 26.1        | [1.45](/reference/api/engine/version/v1.45/) | [变更](/reference/api/engine/version-history/#v145-api-changes)        |
| 26.0        | [1.45](/reference/api/engine/version/v1.45/) | [变更](/reference/api/engine/version-history/#v145-api-changes)        |
| 25.0        | [1.44](/reference/api/engine/version/v1.44/) | [变更](/reference/api/engine/version-history/#v144-api-changes)        |
| 24.0        | 1.43                                         | [变更](/reference/api/engine/version-history/#v143-api-changes)        |
| 23.0        | 1.42                                         | [变更](/reference/api/engine/version-history/#v142-api-changes)        |
| 20.10       | 1.41                                         | [变更](/reference/api/engine/version-history/#v141-api-changes)        |
| 19.03       | 1.40                                         | [变更](/reference/api/engine/version-history/#v140-api-changes)        |
| 18.09       | 1.39                                         | [变更](/reference/api/engine/version-history/#v139-api-changes)        |
| 18.06       | 1.38                                         | [变更](/reference/api/engine/version-history/#v138-api-changes)        |
| 18.05       | 1.37                                         | [变更](/reference/api/engine/version-history/#v137-api-changes)        |
| 18.04       | 1.37                                         | [变更](/reference/api/engine/version-history/#v137-api-changes)        |
| 18.03       | 1.37                                         | [变更](/reference/api/engine/version-history/#v137-api-changes)        |
| 18.02       | 1.36                                         | [变更](/reference/api/engine/version-history/#v136-api-changes)        |
| 17.12       | 1.35                                         | [变更](/reference/api/engine/version-history/#v135-api-changes)        |
| 17.11       | 1.34                                         | [变更](/reference/api/engine/version-history/#v134-api-changes)        |
| 17.10       | 1.33                                         | [变更](/reference/api/engine/version-history/#v133-api-changes)        |
| 17.09       | 1.32                                         | [变更](/reference/api/engine/version-history/#v132-api-changes)        |
| 17.07       | 1.31                                         | [变更](/reference/api/engine/version-history/#v131-api-changes)        |
| 17.06       | 1.30                                         | [变更](/reference/api/engine/version-history/#v130-api-changes)        |
| 17.05       | 1.29                                         | [变更](/reference/api/engine/version-history/#v129-api-changes)        |
| 17.04       | 1.28                                         | [变更](/reference/api/engine/version-history/#v128-api-changes)        |
| 17.03.1     | 1.27                                         | [变更](/reference/api/engine/version-history/#v127-api-changes)        |
| 17.03       | 1.26                                         | [变更](/reference/api/engine/version-history/#v126-api-changes)        |
| 1.13.1      | 1.26                                         | [变更](/reference/api/engine/version-history/#v126-api-changes)        |
| 1.13        | 1.25                                         | [变更](/reference/api/engine/version-history/#v125-api-changes)        |
| 1.12        | 1.24                                         | [变更](/reference/api/engine/version-history/#v124-api-changes)        |

### 已弃用的 API 版本

v1.44 之前的 API 版本已弃用。您可以在 GitHub 上的代码仓库中找到已弃用 API 版本的归档文档：

- [API 版本 1.24–1.43 的文档](https://github.com/moby/moby/tree/28.x/docs/api)。
- [API 版本 1.18–1.23 的文档](https://github.com/moby/moby/tree/v25.0.0/docs/api)。
- [API 版本 1.17 及更早版本的文档](https://github.com/moby/moby/tree/v1.9.1/docs/reference/api)。

- [使用 Docker Engine SDK 进行开发](https://docs.docker.com/reference/api/engine/sdk/)

- [](https://docs.docker.com/reference/api/engine/latest/)

- [Engine API version history](https://docs.docker.com/reference/api/engine/version-history/)

