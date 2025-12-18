---
title: 注册中心认证
description: "指定 Docker Registry v2 认证方式"
keywords: registry, images, tags, repository, distribution, Bearer authentication, advanced
---

本文档概述了注册中心的认证方案：

![v2 registry auth](./images/v2-registry-auth.png)

1. 尝试开始与注册中心的推送/拉取操作。
2. 如果注册中心需要授权，它将返回一个 `401 Unauthorized` HTTP 响应，其中包含如何认证的信息。
3. 注册中心客户端向授权服务请求 Bearer token。
4. 授权服务返回一个代表客户端已授权访问的不透明 Bearer token。
5. 客户端在请求的 Authorization 头中嵌入 Bearer token，重试原始请求。
6. 注册中心通过验证 Bearer token 及其内部的声明集来授权客户端，并照常开始推送/拉取会话。

## 要求

- 注册中心客户端能够理解和响应资源服务器返回的 token 认证质询。
- 授权服务器能够管理托管在任何给定服务（例如 Docker Registry 中的仓库）上的资源的访问控制。
- Docker Registry 能够信任授权服务器为其签名的 token，客户端可以使用这些 token 进行授权，并且能够验证这些 token 以确保单次使用或在足够短的时间内使用。

## 授权服务器端点描述

所描述的服务器旨在作为独立的访问控制管理器，用于托管在其他服务上的资源，这些服务希望通过单独的访问控制管理器进行认证和管理授权。

Docker 官方注册中心使用此类服务来认证客户端并验证其对 Docker 镜像仓库的授权。

从 Docker 1.6 开始，Docker Engine 内的注册中心客户端已更新以处理注册中心返回的此类授权工作流。

## 如何认证

Registry V1 客户端首先联系索引以启动推送或拉取。在 Registry V2 工作流中，客户端应首先联系注册中心。如果注册中心服务器需要认证，它将返回一个 `401 Unauthorized` 响应，其中包含 `WWW-Authenticate` 头，详细说明如何向此注册中心认证。

例如，假设我（用户名 `jlhawn`）试图推送一个镜像到 `samalba/my-app` 仓库。为了使注册中心授权此操作，我需要对 `samalba/my-app` 仓库具有 `push` 访问权限。注册中心首先返回此响应：

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

此质询表明注册中心需要由指定的 token 服务器颁发的 token，并且客户端尝试的请求需要在其声明集中包含足够的访问条目。为了响应此质询，客户端需要使用 `WWW-Authenticate` 头中的 `service` 和 `scope` 值向 URL `https://auth.docker.io/token` 发出 `GET` 请求。

## 请求 token

定义使用 token 端点获取 bearer token 和刷新 token 的方法。

### 查询参数

#### `service`

托管资源的服务名称。

#### `offline_token`

是否连同 bearer token 一起返回刷新 token。刷新 token 能够为同一主体获取具有不同作用域的其他 bearer token。刷新 token 没有到期时间，对客户端而言应被视为完全不透明的。

#### `client_id`

标识客户端的字符串。此 `client_id` 不需要在授权服务器上注册，但应设置为有意义的值，以便允许审核未注册客户端创建的密钥。接受的语法在 [RFC6749 附录 A.1](https://tools.ietf.org/html/rfc6749#appendix-A.1) 中定义。

#### `scope`

所讨论的资源，格式化为之前 `WWW-Authenticate` 头中 `scope` 参数的空格分隔条目之一。如果有多个 `scope` 条目来自 `WWW-Authenticate` 头，则应多次指定此查询参数。前面的示例将指定为：`scope=repository:samalba/my-app:push`。作用域字段可能为空，以请求刷新 token 而不向返回的 bearer token 提供任何资源权限。

### Token 响应字段

#### `token`

一个不透明的 `Bearer` token，客户端应在后续请求的 `Authorization` 头中提供。

#### `access_token`

为了与 OAuth 2.0 兼容，`token` 也以 `access_token` 的名称接受。至少必须指定这些字段之一，但也可能同时出现两者（以兼容较旧的客户端）。当两者都指定时，它们应该等效；如果它们不同，客户端的选择未定义。

#### `expires_in`

（可选）自 token 颁发以来保持有效的秒数。省略时，默认为 60 秒。为了与较旧的客户端兼容，返回的 token 的剩余生存时间不应少于 60 秒。

#### `issued_at`

（可选）token 颁发时的 [RFC3339](https://www.ietf.org/rfc/rfc3339.txt) 序列化的 UTC 标准时间。如果省略 `issued_at`，则过期时间从 token 交换完成时算起。

#### `refresh_token`

（可选）可用于获取同一主体具有不同作用域的其他访问 token 的 token。此 token 应由客户端安全保管，且仅发送给颁发 bearer token 的授权服务器。仅当请求中提供 `offline_token=true` 时，才会设置此字段。

### 示例

对于此示例，客户端向以下 URL 发出 HTTP GET 请求：

```text
https://auth.docker.io/token?service=registry.docker.io&scope=repository:samalba/my-app:pull,push
```

token 服务器应首先尝试使用请求提供的任何认证凭据对客户端进行认证。从 Docker 1.11 开始，Docker Engine 支持通过 Basic Authentication 和 OAuth2 获取 token。Docker 1.10 及更早版本，Docker Engine 中的注册中心客户端仅支持 Basic Authentication。如果对 token 服务器的认证尝试失败，token 服务器应返回 `401 Unauthorized` 响应，表示提供的凭据无效。

token 服务器是否需要认证取决于该访问控制提供者的策略。某些请求可能需要认证来确定访问权限（例如推送或拉取私有仓库），而其他请求可能不需要（例如从公共仓库拉取）。

在认证客户端后（如果未尝试认证，可能是匿名客户端），token 服务器接下来必须查询其访问控制列表，以确定客户端是否具有 `scope` 参数中请求的权限。在此示例请求中，如果我已认证为用户 `jlhawn`，token 服务器将确定我在实体 `registry.docker.io` 托管的仓库 `samalba/my-app` 上的访问权限。

一旦 token 服务器确定了客户端对 `scope` 参数中请求的资源的访问权限，它将获取每个资源上请求的操作集与客户端实际被授予的操作集的交集。如果客户端只有请求权限的子集，**不得视为错误**，因为指示授权错误不是 token 服务器在此工作流中的职责。

继续此示例请求，token 服务器将发现客户端对仓库的授予访问权限集为 `[pull, push]`，与请求的访问权限 `[pull, push]` 相交后产生相等的集合。如果授予的访问权限集仅被发现为 `[pull]`，则相交集仅为 `[pull]`。如果客户端对仓库没有访问权限，则相交集为空集 `[]`。

正是这个相交的访问权限集被放入返回的 token 中。

服务器然后使用此相交的访问权限集构造一个特定于实现的 token，并在指示的时间窗口内将其返回给 Docker 客户端，以用于在受众服务中进行认证（在指示的时间窗口内）：

```text
HTTP/1.1 200 OK
Content-Type: application/json

{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IlBZWU86VEVXVTpWN0pIOjI2SlY6QVFUWjpMSkMzOlNYVko6WEdIQTozNEYyOjJMQVE6WlJNSzpaN1E2In0.eyJpc3MiOiJhdXRoLmRvY2tlci5jb20iLCJzdWIiOiJqbGhhd24iLCJhdWQiOiJyZWdpc3RyeS5kb2NrZXIuY29tIiwiZXhwIjoxNDE1Mzg3MzE1LCJuYmYiOjE0MTUzODcwMTUsImlhdCI6MTQxNTM4NzAxNSwianRpIjoidFlKQ08xYzZjbnl5N2tBbjBjN3JLUGdiVjFIMWJGd3MiLCJhY2Nlc3MiOlt7InR5cGUiOiJyZXBvc2l0b3J5IiwibmFtZSI6InNhbWFsYmEvbXktYXBwIiwiYWN0aW9ucyI6WyJwdXNoIl19XX0.QhflHPfbd6eVF4lM9bwYpFZIV0PfikbyXuLx959ykRTBpe3CYnzs6YBK8FToVb5R47920PVLrh8zuLzdCr9t3w", "expires_in": 3600,"issued_at": "2009-11-10T23:00:00Z"}
```

## 使用 Bearer token

一旦客户端获得 token，它将再次尝试注册中心请求，在 HTTP `Authorization` 头中放置 token，如下所示：

```text
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IkJWM0Q6MkFWWjpVQjVaOktJQVA6SU5QTDo1RU42Ok40SjQ6Nk1XTzpEUktFOkJWUUs6M0ZKTDpQT1RMIn0.eyJpc3MiOiJhdXRoLmRvY2tlci5jb20iLCJzdWIiOiJCQ0NZOk9VNlo6UUVKNTpXTjJDOjJBVkM6WTdZRDpBM0xZOjQ1VVc6NE9HRDpLQUxMOkNOSjU6NUlVTCIsImF1ZCI6InJlZ2lzdHJ5LmRvY2tlci5jb20iLCJleHAiOjE0MTUzODczMTUsIm5iZiI6MTQxNTM4NzAxNSwiaWF0IjoxNDE1Mzg3MDE1LCJqdGkiOiJ0WUpDTzFjNmNueXk3a0FuMGM3cktQZ2JWMUgxYkZ3cyIsInNjb3BlIjoiamxoYXduOnJlcG9zaXRvcnk6c2FtYWxiYS9teS1hcHA6cHVzaCxwdWxsIGpsaGF3bjpuYW1lc3BhY2U6c2FtYWxiYTpwdWxsIn0.Y3zZSwaZPqy4y9oRBVRImZyv3m_S9XDHF1tWwN7mL52C_IiA73SJkWVNsvNqpJIn5h7A2F8biv_S2ppQ1lgkbw
```

这也记录在 [RFC 6750 第 2.1 节：OAuth 2.0 授权框架：Bearer Token 用法](https://tools.ietf.org/html/rfc6750#section-2.1) 中