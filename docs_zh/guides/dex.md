---
title: 使用 Dex 模拟测试中的 OAuth 服务
description: *desc 使用 Dex 模拟测试中的 OAuth 服务
keywords: Dex, container-supported development
linktitle: 使用 Dex 模拟 OAuth 服务
summary: *desc
tags: [app-dev, distributed-systems]
languages: []
params:
  time: 10 minutes
---

Dex 是一个开源的 OpenID Connect (OIDC) 和 OAuth 2.0 身份提供商，可配置为对接各种后端身份提供商，如 LDAP、SAML 和 OAuth。在 Docker 容器中运行 Dex 可以让开发者模拟 OAuth 2.0 服务器，用于测试和开发。本指南将带你通过 Docker 容器设置 Dex 作为 OAuth 模拟服务器。

如今，OAuth 是 Web 服务认证的首选，大部分服务都支持使用 GitHub、Google 或 Apple 等流行的 OAuth 服务进行访问。使用 OAuth 能够保证更高的安全性并简化流程，因为无需为每个服务创建新账户。这意味着，OAuth 允许应用代表用户访问资源，而无需共享密码，从而降低了凭据泄露的风险。

在本指南中，你将学会如何：

- 使用 Docker 启动 Dex 容器。
- 在 GitHub Action (GHA) 中使用模拟 OAuth，而不依赖外部 OAuth 提供商。

## 使用 Docker 运行 Dex

Dex 的官方 [Docker 镜像](https://hub.docker.com/r/dexidp/dex/) 提供了一种便捷的方式来部署和管理 Dex 实例。Dex 支持多种 CPU 架构，包括 amd64、armv7 和 arm64，确保在不同设备和平台上兼容。你可以在 [Dex 文档网站](https://dexidp.io/docs/getting-started/) 了解更多关于 Dex 独立运行的信息。

### 前置条件

[Docker Compose](/compose/)：推荐用于管理多容器 Docker 应用。

### 使用 Docker 设置 Dex

首先，为你的 Dex 项目创建一个目录：

```bash
mkdir dex-mock-server
cd dex-mock-server
```

按照以下结构组织你的项目：

```bash
dex-mock-server/
├── config.yaml
└── compose.yaml
```

创建 Dex 配置文件：
config.yaml 文件定义了 Dex 的设置，包括连接器、客户端和存储。对于模拟服务器设置，你可以使用以下最小配置：

```yaml
# config.yaml
issuer: http://localhost:5556/dex
storage:
  type: memory
web:
  http: 0.0.0.0:5556
staticClients:
  - id: example-app
    redirectURIs:
      - 'http://localhost:5555/callback'
    name: 'Example App'
    secret: ZXhhbXBsZS1hcHAtc2VjcmV0
enablePasswordDB: true
staticPasswords:
  - email: "admin@example.com"
    hash: "$2a$10$2b2cU8CPhOTaGrs1HRQuAueS7JTT5ZHsHSzYiFPm1leZck7Mc8T4W"
    username: "admin"
    userID: "1234"
```

说明：
- issuer：Dex 的公共 URL。

- storage：使用内存存储以简化配置。

- web：Dex 将监听 5556 端口。

- staticClients：定义一个客户端应用（example-app）及其重定向 URI 和密钥。

- enablePasswordDB：启用静态密码认证。

- staticPasswords：定义静态用户用于认证。hash 是密码的 bcrypt 哈希值。

> [!NOTE]
>
> 确保 hash 是你期望密码的有效 bcrypt 哈希值。你可以使用 [bcrypt-generator.com](https://bcrypt-generator.com/) 等工具生成，或使用 [htpasswd](https://httpd.apache.org/docs/2.4/programs/htpasswd.html) 等 CLI 工具，例如：`echo password | htpasswd -BinC 10 admin | cut -d: -f2`

配置好 Docker Compose 后，启动 Dex：
```yaml
# docker-compose.yaml

services:
  dex:
    image: dexidp/dex:latest
    container_name: dex
    ports:
      - "5556:5556"
    volumes:
      - ./config.yaml:/etc/dex/config.yaml
    command: ["dex", "serve", "/etc/dex/config.yaml"]
```

现在可以使用 `docker compose` 命令运行容器：
```bash
docker compose up -d
```

此命令将下载 Dex Docker 镜像（如果尚未存在）并在后台启动容器。

要验证 Dex 是否正在运行，请检查日志以确保 Dex 成功启动：
```bash
docker compose logs -f dex
```
你应该看到输出，表明 Dex 正在指定端口上监听。

### 在 GHA 中使用 Dex OAuth 测试

要测试 OAuth 流程，你需要配置一个客户端应用来对接 Dex 进行认证。最常见的用例之一是在 GitHub Actions 中使用它。由于 Dex 支持模拟认证，你可以预先定义测试用户，如 [文档](https://dexidp.io/docs) 中建议的那样。config.yaml 文件应如下所示：

```yaml
issuer: http://127.0.0.1:5556/dex

storage:
  type: memory

web:
  http: 0.0.0.0:5556

oauth2:
  skipApprovalScreen: true

staticClients:
  - name: TestClient
    id: client_test_id
    secret: client_test_secret
    redirectURIs:
      - http://{ip-your-app}/path/to/callback/ # 示例：http://localhost:5555/callback

connectors:
# mockCallback 连接器始终返回用户 'kilgore@kilgore.trout'。
- type: mockCallback
  id: mock
  name: Mock
```
现在你可以在 `~/.github/workflows/ci.yaml` 文件中插入 Dex 服务：

```yaml
[...]
jobs:
  test-oauth:
    runs-on: ubuntu-latest
    steps:
      - name: Install Dex
        run: |
          curl -L https://github.com/dexidp/dex/releases/download/v2.37.0/dex_linux_amd64 -o dex
          chmod +x dex

      - name: Start Dex Server
        run: |
          nohup ./dex serve config.yaml > dex.log 2>&1 &
          sleep 5  # Give Dex time to start
[...]
```


### 结论

通过本指南，你已使用 Docker 设置了 Dex 作为 OAuth 模拟服务器。这种设置对于测试和开发非常有价值，允许你在不依赖外部身份提供商的情况下模拟 OAuth 流程。如需更高级的配置和集成，请参考 [Dex 文档](https://dexidp.io/docs/)。