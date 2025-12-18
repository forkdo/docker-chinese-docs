---
title: Docker Engine API
description: 了解如何在你选择的语言中使用 Docker Engine API 和 SDK。
keywords: 开发, API, Docker Engine API, API 版本, SDK 版本
aliases:
  - /reference/api/docker_remote_api/
  - /reference/api/docker_remote_api_v1.0/
  - /reference/api/docker_remote_api_v1.1/
  - /reference/api/docker_remote_api_v1.2/
  - /reference/api/docker_remote_api_v1.3/
  - /reference/api/docker_remote_api_v1.4/
  - /reference/api/docker_remote_api_v1.5/
  - /reference/api/docker_remote_api_v1.6/
  - /reference/api/docker_remote_api_v1.7/
  - /reference/api/docker_remote_api_v1.8/
  - /reference/api/docker_remote_api_v1.9/
  - /reference/api/docker_remote_api_v1.10/
  - /reference/api/docker_remote_api_v1.11/
  - /reference/api/docker_remote_api_v1.12/
  - /reference/api/docker_remote_api_v1.13/
  - /reference/api/docker_remote_api_v1.14/
  - /reference/api/docker_remote_api_v1.15/
  - /reference/api/docker_remote_api_v1.16/
  - /reference/api/docker_remote_api_v1.17/
  - /engine/reference/api/
  - /engine/reference/api/docker_remote_api/
  - /engine/api/
---

Docker 提供了一个用于与 Docker 守护进程交互的 API（称为 Docker Engine API），以及 Go 和 Python 的 SDK。SDK 允许你高效地构建和扩展 Docker 应用和解决方案。如果你不使用 Go 或 Python，你也可以直接使用 Docker Engine API。

有关 Docker Engine SDK 的信息，请参阅 [使用 Docker Engine SDK 开发](sdk/_index.md)。

Docker Engine API 是一个 RESTful API，可通过 `wget` 或 `curl` 等 HTTP 客户端访问，或通过大多数现代编程语言中包含的 HTTP 库访问。

## 查看 API 参考

你可以[查看最新版本 API 的参考文档](/reference/api/engine/version/v{{% param latest_engine_api_version %}}.md)，或[选择特定版本](/reference/api/engine/#api-version-matrix)。

## 版本化 API 和 SDK

你应该使用的 Docker Engine API 版本取决于你的 Docker 守护进程和 Docker 客户端的版本。

给定版本的 Docker Engine SDK 支持特定版本的 Docker Engine API 以及所有早期版本。如果发生破坏性更改，会进行显著的文档说明。

> [!NOTE]
>
> Docker 守护进程和客户端并不总是需要相同的版本。但请记住以下几点：
>
> - 如果守护进程比客户端新，客户端将不知道守护进程中的新功能或已弃用的 API 端点。
>
> - 如果客户端比守护进程新，客户端可能会请求守护进程不知道的 API 端点。

当添加新功能时，会发布 API 的新版本。Docker API 是向后兼容的，因此除非你需要利用新功能，否则不需要更新使用 API 的代码。

要查看你的 Docker 守护进程和客户端支持的 API 最高版本，请使用 `docker version`：

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

你可以通过以下任一方式指定要使用的 API 版本：

- 使用 SDK 时，使用最新版本。至少使用包含你需要的功能的 API 版本。
- 直接使用 `curl` 时，在 URL 的第一部分指定版本。例如，如果端点是 `/containers/`，你可以使用 `/v{{% param "latest_engine_api_version" %}}/containers/`。
- 要强制 Docker CLI 或 Docker Engine SDK 使用比 `docker version` 报告的更早版本的 API，请将环境变量 `DOCKER_API_VERSION` 设置为正确的版本。这在 Linux、Windows 或 macOS 客户端上都有效。

  {{% apiVersionPrevious.inline %}}
  {{- $version := site.Params.latest_engine_api_version }}
  {{- $parts := strings.Split $version "." }}
  {{- $major := cast.ToInt (index $parts 0) }}
  {{- $minor := cast.ToInt (index $parts 1) }}
  ```console
  $ DOCKER_API_VERSION={{ $major }}.{{ math.Sub $minor 1 }}
  ```
  {{% /apiVersionPrevious.inline %}}

  环境变量设置后，将使用该版本的 API，即使 Docker 守护进程支持更新的版本也是如此。此环境变量会禁用 API 版本协商，因此只有在必须使用特定版本的 API 或用于调试目的时才应使用它。

- Docker Go SDK 允许你启用 API 版本协商，自动选择客户端和使用的 Docker Engine 都支持的 API 版本。
- 对于 SDK，你也可以将 API 版本作为参数在 `client` 对象中编程指定。请参阅 [Go 构造函数](https://pkg.go.dev/github.com/docker/docker/client#NewClientWithOpts) 或 [Python SDK 文档中的 `client`](https://docker-py.readthedocs.io/en/stable/client.html)。

### API 版本矩阵

| Docker 版本 | 最高 API 版本                              | 变更日志                                                           |
| :---------- | :----------------------------------------- | :----------------------------------------------------------------- |
| 29.0        | [1.52](/reference/api/engine/version/v1.52/) | [变更](/reference/api/engine/version-history/#v152-api-changes) |
| 28.3        | [1.51](/reference/api/engine/version/v1.51/) | [变更](/reference/api/engine/version-history/#v151-api-changes) |
| 28.2        | [1.50](/reference/api/engine/version/v1.50/) | [变更](/reference/api/engine/version-history/#v150-api-changes) |
| 28.1        | [1.49](/reference/api/engine/version/v1.49/) | [变更](/reference/api/engine/version-history/#v149-api-changes) |
| 28.0        | [1.48](/reference/api/engine/version/v1.48/) | [变更](/reference/api/engine/version-history/#v148-api-changes) |
| 27.5        | [1.47](/reference/api/engine/version/v1.47/) | [变更](/reference/api/engine/version-history/#v147-api-changes) |
| 27.4        | [1.47](/reference/api/engine/version/v1.47/) | [变更](/reference/api/engine/version-history/#v147-api-changes) |
| 27.3        | [1.47](/reference/api/engine/version/v1.47/) | [变更](/reference/api/engine/version-history/#v147-api-changes) |
| 27.2        | [1.47](/reference/api/engine/version/v1.47/) | [变更](/reference/api/engine/version-history/#v147-api-changes) |
| 27.1        | [1.46](/reference/api/engine/version/v1.46/) | [变更](/reference/api/engine/version-history/#v146-api-changes) |
| 27.0        | [1.46](/reference/api/engine/version/v1.46/) | [变更](/reference/api/engine/version-history/#v146-api-changes) |
| 26.1        | [1.45](/reference/api/engine/version/v1.45/) | [变更](/reference/api/engine/version-history/#v145-api-changes) |
| 26.0        | [1.45](/reference/api/engine/version/v1.45/) | [变更](/reference/api/engine/version-history/#v145-api-changes) |
| 25.0        | [1.44](/reference/api/engine/version/v1.44/) | [变更](/reference/api/engine/version-history/#v144-api-changes) |
| 24.0        | 1.43                                       | [变更](/reference/api/engine/version-history/#v143-api-changes) |
| 23.0        | 1.42                                       | [变更](/reference/api/engine/version-history/#v142-api-changes) |
| 20.10       | 1.41                                       | [变更](/reference/api/engine/version-history/#v141-api-changes) |
| 19.03       | 1.40                                       | [变更](/reference/api/engine/version-history/#v140-api-changes) |
| 18.09       | 1.39                                       | [变更](/reference/api/engine/version-history/#v139-api-changes) |
| 18.06       | 1.38                                       | [变更](/reference/api/engine/version-history/#v138-api-changes) |
| 18.05       | 1.37                                       | [变更](/reference/api/engine/version-history/#v137-api-changes) |
| 18.04       | 1.37                                       | [变更](/reference/api/engine/version-history/#v137-api-changes) |
| 18.03       | 1.37                                       | [变更](/reference/api/engine/version-history/#v137-api-changes) |
| 18.02       | 1.36                                       | [变更](/reference/api/engine/version-history/#v136-api-changes) |
| 17.12       | 1.35                                       | [变更](/reference/api/engine/version-history/#v135-api-changes) |
| 17.11       | 1.34                                       | [变更](/reference/api/engine/version-history/#v134-api-changes) |
| 17.10       | 1.33                                       | [变更](/reference/api/engine/version-history/#v133-api-changes) |
| 17.09       | 1.32                                       | [变更](/reference/api/engine/version-history/#v132-api-changes) |
| 17.07       | 1.31                                       | [变更](/reference/api/engine/version-history/#v131-api-changes) |
| 17.06       | 1.30                                       | [变更](/reference/api/engine/version-history/#v130-api-changes) |
| 17.05       | 1.29                                       | [变更](/reference/api/engine/version-history/#v129-api-changes) |
| 17.04       | 1.28                                       | [变更](/reference/api/engine/version-history/#v128-api-changes) |
| 17.03.1     | 1.27                                       | [变更](/reference/api/engine/version-history/#v127-api-changes) |
| 17.03       | 1.26                                       | [变更](/reference/api/engine/version-history/#v126-api-changes) |
| 1.13.1      | 1.26                                       | [变更](/reference/api/engine/version-history/#v126-api-changes) |
| 1.13        | 1.25                                       | [变更](/reference/api/engine/version-history/#v125-api-changes) |
| 1.12        | 1.24                                       | [变更](/reference/api/engine/version-history/#v124-api-changes) |

### 已弃用的 API 版本

v1.44 之前的 API 版本已弃用。你可以在 GitHub 上的代码仓库中找到已弃用 API 版本文档的存档：

- [API 版本 1.24–1.43 的文档](https://github.com/moby/moby/tree/28.x/docs/api)。
- [API 版本 1.18–1.23 的文档](https://github.com/moby/moby/tree/v25.0.0/docs/api)。
- [API 版本 1.17 及更早版本的文档](https://github.com/moby/moby/tree/v1.9.1/docs/reference/api)。