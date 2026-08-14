---
title: Docker Engine API
description: 了解如何在您选择的编程语言中使用 Docker Engine API 和 SDK。
keywords: developing, api, Docker Engine API, API versions, SDK versions
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
  - /engine/reference/api/
  - /engine/reference/api/docker_remote_api/
  - /engine/api/
---

Docker 提供了一个用于与 Docker 守护进程（称为 Docker Engine API）交互的 API，以及 Go 和 Python 的 SDK。这些 SDK 可让您高效地构建和扩展 Docker 应用程序和解决方案。如果您不使用 Go 或 Python，也可以直接使用 Docker Engine API。

有关 Docker Engine SDK 的信息，请参阅[使用 Docker Engine SDK 进行开发](sdk/_index.md)。

Docker Engine API 是一个 RESTful API，可通过 `wget` 或 `curl` 等 HTTP 客户端，或大多数现代编程语言内置的 HTTP 库进行访问。

## 查看 API 参考文档

您可以[查看最新版本的 API 参考文档](/reference/api/engine/version/v{{% param latest_engine_api_version %}}.md)，或[选择特定版本](/reference/api/engine/#api-version-matrix)。

## 版本化 API 和 SDK

您应使用的 Docker Engine API 版本取决于 Docker 守护进程和 Docker 客户端的版本。

特定版本的 Docker Engine SDK 支持特定版本的 Docker Engine API 以及所有早期版本。如果发生破坏性变更，这些变更会被显著记录。

> [!NOTE]
>
> Docker 守护进程和客户端不必始终保持相同版本。但请注意以下几点：
>
> - 如果守护进程版本比客户端新，客户端将无法了解守护进程中的新功能或已弃用的 API 端点。
>
> - 如果客户端版本比守护进程新，客户端可能会请求守护进程未知的 API 端点。

当添加新功能时，会发布新版本的 API。Docker API 向后兼容，因此除非您需要使用新功能，否则无需更新使用 API 的代码。

要查看 Docker 守护进程和客户端支持的最高和最低 API 版本，请使用 `docker version` 命令：

```console
$ docker version
Client: Docker Engine - Community
 Version:           {{% param "docker_ce_version" %}}
 API version:       {{% param "latest_engine_api_version" %}}
 ...

Server: Docker Engine - Community
 Engine:
  Version:          {{% param "docker_ce_version" %}}
  API version:      {{% param "latest_engine_api_version" %}} (minimum version 1.40)
  ...
```

您可以通过以下任意方式指定要使用的 API 版本：

- 使用 SDK 时，请使用最新版本。至少应使用包含您所需功能对应 API 版本的版本。
- 直接使用 `curl` 时，请在 URL 的第一部分指定版本。例如，如果端点是 `/containers/`，可以使用 `/v{{% param "latest_engine_api_version" %}}/containers/`。
- 要强制 Docker CLI 或 Docker Engine SDK 使用比 `docker version` 报告的更旧的 API 版本，请将环境变量 `DOCKER_API_VERSION` 设置为正确的版本。此方法适用于 Linux、Windows 和 macOS 客户端。

  {{% apiVersionPrevious.inline %}}
  {{- $version := site.Params.latest_engine_api_version }}
  {{- $parts := strings.Split $version "." }}
  {{- $major := cast.ToInt (index $parts 0) }}
  {{- $minor := cast.ToInt (index $parts 1) }}
  ```console
  $ DOCKER_API_VERSION={{ $major }}.{{ math.Sub $minor 1 }}
  ```
  {{% /apiVersionPrevious.inline %}}

  在设置此环境变量期间，即使 Docker 守护进程支持更新的版本，也会使用该版本的 API。此环境变量会禁用 API 版本协商，因此仅在必须使用特定 API 版本或用于调试目的时才应使用。

- Docker Go SDK 允许您启用 API 版本协商，自动选择客户端和正在使用的 Docker Engine 均支持的 API 版本。
- 对于 SDK，您还可以在程序中通过将 API 版本作为 `client` 对象的参数来指定。请参阅 [Go 构造函数](https://pkg.go.dev/github.com/docker/docker/client#NewClientWithOpts) 或 [Python SDK 的 `client` 文档](https://docker-py.readthedocs.io/en/stable/client.html)。

### 最低 API 版本

Docker Engine API 服务端和客户端支持 API 版本协商。如果
客户端连接到较旧版本的 Docker Engine，它会协商
客户端和守护进程均支持的最高 API 版本，
并在必要时降级到较旧的 API 版本。

当降级到较旧的 API 版本时，在后续 API
版本中引入的功能会被禁用，并且 API 请求和响应会根据
协商的 API 版本进行调整。

API 版本协商允许尚未升级到
最新 API 版本规范的工具与较新的 Docker Engine
进行通信（反之亦然），但兼容性是“尽力而为”的；尽管 Docker 努力做到
完全兼容，但某些功能可能不可用。

### API 版本矩阵

| Docker 版本 | 最大 API 版本                          | 最小 API 版本                          | 变更日志                                                         |
| :--------------- | :--------------------------------------------- | :--------------------------------------------- | :------------------------------------------------------------------- |
| 29.7           | [1.55](/reference/api/engine/version/v1.55/) | [1.40](/reference/api/engine/version/v1.40/) | [变更内容](/reference/api/engine/version-history/#v155-api-changes) |
| 29.6           | [1.55](/reference/api/engine/version/v1.55/) | [1.40](/reference/api/engine/version/v1.40/) | [变更内容](/reference/api/engine/version-history/#v155-api-changes) |
| 29.5           | [1.54](/reference/api/engine/version/v1.54/) | [1.40](/reference/api/engine/version/v1.40/) | [变更内容](/reference/api/engine/version-history/#v154-api-changes) |
| 29.4           | [1.54](/reference/api/engine/version/v1.54/) | [1.40](/reference/api/engine/version/v1.40/) | [变更内容](/reference/api/engine/version-history/#v154-api-changes) |
| 29.3           | [1.54](/reference/api/engine/version/v1.54/) | [1.40](/reference/api/engine/version/v1.40/) | [变更内容](/reference/api/engine/version-history/#v154-api-changes) |
| 29.2           | [1.53](/reference/api/engine/version/v1.53/) | [1.44](/reference/api/engine/version/v1.44/) | [变更内容](/reference/api/engine/version-history/#v153-api-changes) |
| 29.1           | [1.52](/reference/api/engine/version/v1.52/) | [1.44](/reference/api/engine/version/v1.44/) | [变更内容](/reference/api/engine/version-history/#v152-api-changes) |
| 29.0           | [1.52](/reference/api/engine/version/v1.52/) | [1.44](/reference/api/engine/version/v1.44/) | [变更内容](/reference/api/engine/version-history/#v152-api-changes) |
| 28.5           | [1.51](/reference/api/engine/version/v1.51/) | 1.24                                         | [变更内容](/reference/api/engine/version-history/#v151-api-changes) |
| 28.4           | [1.51](/reference/api/engine/version/v1.51/) | 1.24                                         | [变更内容](/reference/api/engine/version-history/#v151-api-changes) |
| 28.3           | [1.51](/reference/api/engine/version/v1.51/) | 1.24                                         | [变更内容](/reference/api/engine/version-history/#v151-api-changes) |
| 28.2           | [1.50](/reference/api/engine/version/v1.50/) | 1.24                                         | [变更内容](/reference/api/engine/version-history/#v150-api-changes) |
| 28.1           | [1.49](/reference/api/engine/version/v1.49/) | 1.24                                         | [变更内容](/reference/api/engine/version-history/#v149-api-changes) |
| 28.0           | [1.48](/reference/api/engine/version/v1.48/) | 1.24                                         | [变更内容](/reference/api/engine/version-history/#v148-api-changes) |
| 27.5           | [1.47](/reference/api/engine/version/v1.47/) | 1.24                                         | [变更内容](/reference/api/engine/version-history/#v147-api-changes) |
| 27.4           | [1.47](/reference/api/engine/version/v1.47/) | 1.24                                         | [变更内容](/reference/api/engine/version-history/#v147-api-changes) |
| 27.3           | [1.47](/reference/api/engine/version/v1.47/) | 1.24                                         | [变更内容](/reference/api/engine/version-history/#v147-api-changes) |
| 27.2           | [1.47](/reference/api/engine/version/v1.47/) | 1.24                                         | [变更内容](/reference/api/engine/version-history/#v147-api-changes) |
| 27.1           | [1.46](/reference/api/engine/version/v1.46/) | 1.24                                         | [变更内容](/reference/api/engine/version-history/#v146-api-changes) |
| 27.0           | [1.46](/reference/api/engine/version/v1.46/) | 1.24                                         | [变更内容](/reference/api/engine/version-history/#v146-api-changes) |
| 26.1           | [1.45](/reference/api/engine/version/v1.45/) | 1.24                                         | [变更内容](/reference/api/engine/version-history/#v145-api-changes) |
| 26.0           | [1.45](/reference/api/engine/version/v1.45/) | 1.24                                         | [变更内容](/reference/api/engine/version-history/#v145-api-changes) |
| 25.0           | [1.44](/reference/api/engine/version/v1.44/) | 1.24                                         | [变更内容](/reference/api/engine/version-history/#v144-api-changes) |
| 24.0           | [1.43](/reference/api/engine/version/v1.43/) | 1.12                                         | [变更内容](/reference/api/engine/version-history/#v143-api-changes) |
| 23.0           | [1.42](/reference/api/engine/version/v1.42/) | 1.12                                         | [变更内容](/reference/api/engine/version-history/#v142-api-changes) |
| 20.10          | [1.41](/reference/api/engine/version/v1.41/) | 1.12                                         | [变更内容](/reference/api/engine/version-history/#v141-api-changes) |
| 19.03          | [1.40](/reference/api/engine/version/v1.40/) | 1.12                                         | [变更内容](/reference/api/engine/version-history/#v140-api-changes) |

### 已弃用的 API 版本

v1.40 之前的 API 版本已被弃用，且不再受当前
Docker Engine 和 CLI 版本支持。您可以在 [GitHub 代码仓库中](https://github.com/moby/moby/tree/docker-v{{% param "docker_ce_version" %}}/api/docs) 找到已弃用 API 版本的归档文档：

| Docker 版本 | 最大 API 版本 | 最小 API 版本 | 变更日志                                                         |
| :--------------- | :-------------------- | :-------------------- | :------------------------------------------------------------------- |
| 18.09          | 1.39                | 1.12                | [变更内容](/reference/api/engine/version-history/#v139-api-changes) |
| 18.06          | 1.38                | 1.12                | [变更内容](/reference/api/engine/version-history/#v138-api-changes) |
| 18.05          | 1.37                | 1.12                | [变更内容](/reference/api/engine/version-history/#v137-api-changes) |
| 18.04          | 1.37                | 1.12                | [变更内容](/reference/api/engine/version-history/#v137-api-changes) |
| 18.03          | 1.37                | 1.12                | [变更内容](/reference/api/engine/version-history/#v137-api-changes) |
| 18.02          | 1.36                | 1.12                | [变更内容](/reference/api/engine/version-history/#v136-api-changes) |
| 17.12          | 1.35                | 1.12                | [变更内容](/reference/api/engine/version-history/#v135-api-changes) |
| 17.11          | 1.34                | 1.12                | [变更内容](/reference/api/engine/version-history/#v134-api-changes) |
| 17.10          | 1.33                | 1.12                | [变更内容](/reference/api/engine/version-history/#v133-api-changes) |
| 17.09          | 1.32                | 1.12                | [变更内容](/reference/api/engine/version-history/#v132-api-changes) |
| 17.07          | 1.31                | 1.12                | [变更内容](/reference/api/engine/version-history/#v131-api-changes) |
| 17.06          | 1.30                | 1.12                | [变更内容](/reference/api/engine/version-history/#v130-api-changes) |
| 17.05          | 1.29                | 1.12                | [变更内容](/reference/api/engine/version-history/#v129-api-changes) |
| 17.04          | 1.28                | 1.12                | [变更内容](/reference/api/engine/version-history/#v128-api-changes) |
| 17.03.1        | 1.27                | 1.12                | [变更内容](/reference/api/engine/version-history/#v127-api-changes) |
| 17.03          | 1.26                | 1.12                | [变更内容](/reference/api/engine/version-history/#v126-api-changes) |
| 1.13.1         | 1.26                | 1.12                | [变更内容](/reference/api/engine/version-history/#v126-api-changes) |
| 1.13           | 1.25                | 1.12                | [变更内容](/reference/api/engine/version-history/#v125-api-changes) |
| 1.12           | 1.24                | 1.12                | [变更内容](/reference/api/engine/version-history/#v124-api-changes) |
| 1.11           | 1.23                | 1.12                | [变更内容](/reference/api/engine/version-history/#v123-api-changes) |
| 1.10           | 1.22                | 1.12                | [变更内容](/reference/api/engine/version-history/#v122-api-changes) |
| 1.9            | 1.21                | 1.12                | [变更内容](/reference/api/engine/version-history/#v121-api-changes) |
| 1.8            | 1.20                | 1.12                | [变更内容](/reference/api/engine/version-history/#v120-api-changes) |
| 1.7            | 1.19                | 1.0                 | [变更内容](/reference/api/engine/version-history/#v119-api-changes) |
| 1.6            | 1.18                | 1.0                 | [变更内容](/reference/api/engine/version-history/#v118-api-changes) |
| 1.5            | 1.17                | 1.0                 | [变更内容](/reference/api/engine/version-history/#v117-api-changes) |
| 1.4            | 1.16                | 1.0                 | [变更内容](/reference/api/engine/version-history/#v116-api-changes) |
| 1.3            | 1.15                | 1.0                 | [变更内容](/reference/api/engine/version-history/#v115-api-changes) |
| 1.2            | 1.14                | 1.0                 | [变更内容](/reference/api/engine/version-history/#v114-api-changes) |
| 1.1            | 1.13                | 1.0                 | [变更内容](/reference/api/engine/version-history/#v113-api-changes) |
| 1.0            | 1.12                | 1.0                 | [变更内容](/reference/api/engine/version-history/#v112-api-changes) |
| 0.12           | 1.12                | 1.0                 | [变更内容](/reference/api/engine/version-history/#v112-api-changes) |
| 0.11           | 1.11                | 1.0                 | [变更内容](/reference/api/engine/version-history/#v111-api-changes) |
| 0.10           | 1.10                | 1.0                 | [变更内容](/reference/api/engine/version-history/#v110-api-changes) |
| 0.9            | 1.10                | 1.0                 | [变更内容](/reference/api/engine/version-history/#v110-api-changes) |
| 0.8            | 1.9                 | 1.0                 | [变更内容](/reference/api/engine/version-history/#v19-api-changes)  |
| 0.7.1          | 1.8                 | 1.0                 | [变更内容](/reference/api/engine/version-history/#v18-api-changes)  |
| 0.7            | 1.7                 | 1.0                 | [变更内容](/reference/api/engine/version-history/#v17-api-changes)  |
| 0.6.4          | 1.6                 | 1.0                 | [变更内容](/reference/api/engine/version-history/#v16-api-changes)  |
| 0.6.2          | 1.5                 | 1.0                 | [变更内容](/reference/api/engine/version-history/#v15-api-changes)  |
| 0.6            | 1.4                 | 1.0                 | [变更内容](/reference/api/engine/version-history/#v14-api-changes)  |
| 0.5            | 1.3                 | 1.0                 | [变更内容](/reference/api/engine/version-history/#v13-api-changes)  |
| 0.4.1          | 1.2                 | 1.0                 | [变更内容](/reference/api/engine/version-history/#v12-api-changes)  |
| 0.3.4          | 1.1                 | 1.0                 | [变更内容](/reference/api/engine/version-history/#v11-api-changes)  |
| 0.3.3          | 1.0                 | 1.0                 | [变更内容](/reference/api/engine/version-history/#v10-api-changes)  |
| 0.3.2          | -                   | -                   |                                                                    |
| 0.2            | -                   | -                   |                                                                    |
| 0.1            | -                   | -                   |                                                                    |
