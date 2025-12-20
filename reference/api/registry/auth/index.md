# Registry 认证

本文档概述了 Registry 的认证方案：

![v2 registry auth](./images/v2-registry-auth.png)

1. 尝试开始与 Registry 进行推送/拉取操作。
2. 如果 Registry 需要授权，它将返回一个 `401 Unauthorized` HTTP 响应，其中包含如何进行认证的信息。
3. Registry 客户端向授权服务请求一个 Bearer token。
4. 授权服务返回一个不透明的 Bearer token，代表客户端的授权访问。
5. 客户端使用嵌入在请求的 Authorization 头中的 Bearer token 重试原始请求。
6. Registry 通过验证 Bearer token 及其内部嵌入的声明集（claim set）来授权客户端，并像往常一样开始推送/拉取会话。

## 要求

- Registry 客户端能够理解并响应资源服务器返回的 token 认证质询。
- 授权服务器能够管理对托管在任何给定服务（如 Docker Registry 中的仓库）上的资源的访问控制。
- Docker Registry 能够信任授权服务器来签署客户端可用于授权的 token，并且能够验证这些 token 是单次使用还是在足够短的时间内使用。

## 授权服务器端点描述

所述的服务器旨在作为独立的访问控制管理器，服务于托管在其他服务上的资源，这些服务希望使用单独的访问控制管理器进行身份验证和管理授权。

官方 Docker Registry 使用此类服务来验证客户端并验证其对 Docker 镜像仓库的授权。

自 Docker 1.6 起，Docker Engine 中的 Registry 客户端已更新以处理此类授权工作流。

## 如何进行认证

Registry V1 客户端首先联系索引（index）以启动推送或拉取。在 Registry V2 工作流下，客户端应首先联系 Registry。如果 Registry 服务器需要认证，它将返回一个 `401 Unauthorized` 响应，并带有 `WWW-Authenticate` 头，详细说明如何向此 Registry 进行认证。

例如，假设我（用户名 `jlhawn`）正尝试将镜像推送到仓库 `samalba/my-app`。为了使 Registry 授权此操作，我需要对 `samalba/my-app` 仓库拥有 `push` 访问权限。Registry 将首先返回此响应：

```text
HTTP/1.1 401 Unauthorized
Content-Type: application/json; charset=utf-8
Docker-Distribution-Api-Version: registry/2.0
Www-Authenticate: Bearer realm="https://auth.docker.io/token",service="registry.docker.io",scope="repository:samalba/my-app:pull,push"
Date: Thu, 10 Sep 2015 19:32:31 GMT
Content-Length: 235
Strict-Transport-Security: max-age=31536000

{"errors":[{"code":"UNAUTHORIZED","message":"access to the requested resource is not authorized","detail":[{"Type":"repository","Name":"samalba/my-app","Action":"pull"},{"Type":"repository","Name":"samalba/my-app","Action":"push"}]}]}
```

注意指示认证质询的 HTTP 响应头：

```text
Www-Authenticate: Bearer realm="https://auth.docker.io/token",service="registry.docker.io",scope="repository:samalba/my-app:pull,push"
```

此格式记录在 [RFC 6750 第 3 节：OAuth 2.0 授权框架：Bearer Token 用法](https://tools.ietf.org/html/rfc6750#section-3) 中。

此质询表示 Registry 需要由指定的 token 服务器颁发的 token，并且客户端尝试的请求需要在其声明集中包含足够的访问条目。要响应此质询，客户端需要使用 `WWW-Authenticate` 头中的 `service` 和 `scope` 值向 URL `https://auth.docker.io/token` 发起 `GET` 请求。

## 请求 Token

定义使用 token 端点获取 bearer token 和 refresh token。

### 查询参数

#### `service`

托管资源的服务名称。

#### `offline_token`

是否随 bearer token 一起返回 refresh token。Refresh token 能够为同一主体（subject）获取具有不同作用域（scope）的额外 bearer token。Refresh token 没有到期时间，应被视为对客户端完全不透明。

#### `client_id`

标识客户端的字符串。此 `client_id` 不需要在授权服务器注册，但应设置为有意义的值，以便允许审计由未注册客户端创建的密钥。接受的语法定义在 [RFC6749 附录 A.1](https://tools.ietf.org/html/rfc6749#appendix-A.1)。

#### `scope`

相关资源，格式化为先前显示的 `WWW-Authenticate` 头中 `scope` 参数的空格分隔条目之一。如果 `WWW-Authenticate` 头中有多个 `scope` 条目，则应多次指定此查询参数。前面的示例将指定为：`scope=repository:samalba/my-app:push`。Scope 字段可以为空，以请求 refresh token 而不向返回的 bearer token 提供任何资源权限。

### Token 响应字段

#### `token`

一个不透明的 `Bearer` token，客户端应在后续请求的 `Authorization` 头中提供。

#### `access_token`

为了与 OAuth 2.0 兼容，名为 `access_token` 的 `token` 也被接受。必须至少指定其中一个字段，但也可以同时出现（为了与旧客户端兼容）。当两者都指定时，它们应该是等效的；如果它们不同，客户端的选择是未定义的。

#### `expires_in`

（可选）自 token 颁发以来它将保持有效的持续时间（以秒为单位）。如果省略，默认为 60 秒。为了与旧客户端兼容，返回的 token 剩余有效期不应少于 60 秒。

#### `issued_at`

（可选）给定 token 颁发时的 [RFC3339](https://www.ietf.org/rfc/rfc3339.txt) 序列化的 UTC 标准时间。如果省略 `issued_at`，到期时间从 token 交换完成时开始计算。

#### `refresh_token`

（可选）可用于为同一主体获取具有不同作用域的额外访问 token 的 token。此 token 应由客户端安全保存，并且仅发送给颁发 bearer token 的授权服务器。仅当请求中提供 `offline_token=true` 时，才会设置此字段。

### 示例

在此示例中，客户端向以下 URL 发起 HTTP GET 请求：

```text
https://auth.docker.io/token?service=registry.docker.io&scope=repository:samalba/my-app:pull,push
```

Token 服务器应首先尝试使用请求提供的任何认证凭据对客户端进行身份验证。从 Docker 1.11 开始，Docker Engine 支持 Basic 认证和 OAuth2 来获取 token。Docker 1.10 及更早版本，Docker Engine 中的 Registry 客户端仅支持 Basic 认证。如果尝试向 token 服务器进行身份验证失败，token 服务器应返回 `401 Unauthorized` 响应，指出提供的凭据无效。

Token 服务器是否需要身份验证取决于该访问控制提供者的策略。某些请求可能需要身份验证来确定访问权限（例如推送或拉取私有仓库），而其他请求可能不需要（例如从公共仓库拉取）。

在对客户端进行身份验证后（如果没有尝试进行身份验证，则可能只是匿名客户端），token 服务器必须接下来查询其访问控制列表以确定客户端是否具有请求的作用域。在此示例请求中，如果我已认证为用户 `jlhawn`，token 服务器将确定我对实体 `registry.docker.io` 托管的仓库 `samalba/my-app` 拥有何种访问权限。

一旦 token 服务器确定了客户端对 `scope` 参数中请求的资源的访问权限，它将获取每个资源上请求的操作集与客户端实际被授予的操作集的交集。如果客户端仅拥有请求访问权限的子集，**这不被视为错误**，因为在此工作流中指示授权错误不是 token 服务器的责任。

继续示例请求，token 服务器将发现客户端对仓库的授予访问集是 `[pull, push]`，当与请求的访问 `[pull, push]` 相交时，产生相等的集合。如果发现授予的访问集仅为 `[pull]`，则相交集将仅为 `[pull]`。如果客户端对仓库没有访问权限，则相交集将为空 `[]`。

正是这个访问的交集集被放置在返回的 token 中。

然后，服务器使用此相交的访问集构建一个特定于实现的 token，并将其返回给 Docker 客户端，以便用于向受众服务（在指示的时间窗口内）进行身份验证：

```text
HTTP/1.1 200 OK
Content-Type: application/json

{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IlBZWU6VEVXVTpWN0pIOjI2SlY6QVFUWjpMSkMzOlNYVko6WEdHQTozNEYyOjJMQVE6WlJNSzpaN1E2In0.eyJpc3MiOiJhdXRoLmRvY2tlci5jb20iLCJzdWIiOiJqbGhhd24iLCJhdWQiOiJyZWdpc3RyeS5kb2NrZXIuY29tIiwiZXhwIjoxNDE1Mzg3MzE1LCJuYmYiOjE0MTUzODcwMTUsImlhdCI6MTQxNTM4NzAxNSwianRpIjoidFlKQ08xYzZjbnl5N2tBbjBjN3JLUGdiVjFIMWJGd3MiLCJhY2Nlc3MiOlt7InR5cGUiOiJyZXBvc2l0b3J5IiwibmFtZSI6InNhbWFsYmEvbXktYXBwIiwiYWN0aW9ucyI6WyJwdXNoIl19XX0.QhflHPfbd6eVF4lM9bwYpFZIV0PfikbyXuLx959ykRTBpe3CYnzs6YBK8FToVb5R47920PVLrh8zuLzdCr9t3w", "expires_in": 3600,"issued_at": "2009-11-10T23:00:00Z"}
```

## 使用 Bearer token

客户端获得 token 后，将使用放置在 HTTP `Authorization` 头中的 token 重试 Registry 请求，如下所示：

```text
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IkJWM0Q6MkFWWjpVQjVaOktJQVA6SU5QTDo1RU42Ok40SjQ6Nk1XTzpEUktFOkJWUUs6M0ZKTDpQT1RMIn0.eyJpc3MiOiJhdXRoLmRvY2tlci5jb20iLCJzdWIiOiJCQ0NZOk9VNlo6UUVKNTpXTjJDOjJBVkM6WTdZRDpBM0xZOjQ1VVc6NE9HRDpLQUxMOkNOSjU6NUlVTCIsImF1ZCI6InJlZ2lzdHJ5LmRvY2tlci5jb20iLCJleHAiOjE0MTUzODczMTUsIm5iZiI6MTQxNTM4NzAxNSwiaWF0IjoxNDE1Mzg3MDE1LCJqdGkiOiJ0WUpDTzFjNmNueXk3a0FuMGM3cktQZ2JWMUgxYkZ3cyIsInNjb3BlIjoiamxoYXduOnJlcG9zaXRvcnk6c2FtYWxiYS9teS1hcHA6cHVzaCxwdWxsIGpsaGF3bjpuYW1lc3BhY2U6c2FtYWxiYTpwdWxsIn0.Y3zZSwaZPqy4y9oRBVRImZyv3m_S9XDHF1tWwN7mL52C_IiA73SJkWVNsvNqpJIn5h7A2F8biv_S2ppQ1lgkbw
```

这也描述在 [RFC 6750 第 2.1 节：OAuth 2.0 授权框架：Bearer Token 用法](https://tools.ietf.org/html/rfc6750#section-2.1) 中。
