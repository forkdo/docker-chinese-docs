# 网络策略




网络策略控制沙盒可以通过 HTTP/HTTPS 过滤代理访问哪些外部资源。使用策略可以防止代理访问内部网络、强制执行合规性要求，或将互联网访问限制为特定服务。

每个沙盒都有一个过滤代理，用于对出站 HTTP 和 HTTPS 流量执行策略。通过其他协议（如原始 TCP 和 UDP 连接）与外部服务的连接将被阻止。所有代理通信必须通过 HTTP 代理进行，或保持在沙盒内部。

代理在主机上的临时端口运行，但从代理容器的角度来看，它可以通过 `host.docker.internal:3128` 访问。

### 安全注意事项

将网络策略用作安全层之一，而不是唯一的安全层。microVM 边界提供了主要的隔离。网络策略为 HTTP/HTTPS 流量增加了额外的控制。

网络过滤限制了进程可以连接到的域，但不会检查流量内容。配置策略时：

- 允许广泛的域名（如 `github.com`）会允许访问该域名上的任何内容，包括用户生成的内容。代理可能利用这些作为数据外泄的渠道。
- 域前置技术可能通过允许域路由流量来绕过过滤器。这是 HTTPS 代理固有的特性。只允许您信任其数据的域。

您有责任了解您的策略允许什么。

## 网络过滤的工作原理

每个沙盒在主机上运行一个 HTTP/HTTPS 代理。代理在沙盒内部可通过 `host.docker.internal:3128` 访问。

当代理发出 HTTP 或 HTTPS 请求时，代理会：

1. 根据请求中的主机检查策略规则。如果主机被阻止，请求将立即停止
2. 连接到服务器。如果主机未被明确允许，则根据 BlockCIDR 规则检查服务器的 IP 地址

例如，`localhost` 不在默认允许列表中，但默认的 "allow" 策略允许它。因为它未被明确允许，代理会检查解析后的 IP 地址（`127.0.0.1` 或 `::1`）是否符合 BlockCIDR 规则。由于 `127.0.0.1/8` 和 `::1/128` 默认都被阻止，这会捕获任何 `localhost` 的 DNS 别名，如 `ip6-localhost`。

如果代理需要访问 localhost 上的服务，请在允许列表中包含端口号（例如，`localhost:1234`）。对 `host.docker.internal` 的 HTTP 请求会被重写为 `localhost`，因此只有名称 `localhost` 才能在允许列表中生效。

## 监控网络活动

查看您的代理正在访问什么以及请求是否被阻止：

```console
$ docker sandbox network log
```

网络日志可帮助您了解代理行为并定义策略。

## 应用策略

使用 `docker sandbox network proxy` 为您的沙盒配置网络策略。应用策略更改时，沙盒必须正在运行。更改立即生效，并在沙盒重启后持续存在。

### 示例：阻止内部网络

阻止代理访问您的本地网络、Docker 网络和云元数据服务。它可防止意外访问内部服务，同时允许代理安装包和访问公共 API。

```console
$ docker sandbox network proxy my-sandbox \
  --policy allow \
  --block-cidr 10.0.0.0/8 \
  --block-cidr 172.16.0.0/12 \
  --block-cidr 192.168.0.0/16 \
  --block-cidr 127.0.0.0/8
```

此策略：

- 允许互联网访问
- 阻止 RFC 1918 私有网络（10.x.x.x、172.16-31.x.x、192.168.x.x）
- 阻止 localhost（127.x.x.x）

> [!NOTE]
> 这些 CIDR 块默认已被阻止。上面的示例展示了如何在需要时显式配置它们。默认策略阻止：
>
> - `10.0.0.0/8`
> - `127.0.0.0/8`
> - `169.254.0.0/16`
> - `172.16.0.0/12`
> - `192.168.0.0/16`
> - `::1/128`
> - `fc00::/7`
> - `fe80::/10`

### 示例：仅限制到包管理器

为了严格控制，请使用仅允许包仓库的拒绝列表策略：

```console
$ docker sandbox network proxy my-sandbox \
  --policy deny \
  --allow-host "*.npmjs.org" \
  --allow-host "*.pypi.org" \
  --allow-host "files.pythonhosted.org" \
  --allow-host "*.rubygems.org" \
  --allow-host github.com
```

> [!NOTE]
> 此策略会阻止您的 AI 编码代理的后端（例如，对于 Claude Code：`xyz.anthropic.com`）。请确保您还包含代理所需的主机名。

代理可以安装依赖项，但不能访问任意的互联网资源。这适用于 CI/CD 环境或运行不受信任的代码时。

### 示例：允许 AI API 和开发工具

将 AI 服务访问与包管理器和版本控制相结合：

```console
$ docker sandbox network proxy my-sandbox \
  --policy deny \
  --allow-host api.anthropic.com \
  --allow-host "*.npmjs.org" \
  --allow-host "*.pypi.org" \
  --allow-host github.com \
  --allow-host "*.githubusercontent.com"
```

这允许代理调用 AI API、安装包并从 GitHub 获取代码，同时阻止其他互联网访问。

### 示例：允许特定 API 同时阻止子域

使用特定端口的规则和子域模式进行细粒度控制：

```console
$ docker sandbox network proxy my-sandbox \
  --policy deny \
  --allow-host api.example.com:443 \
  --allow-host cdn.example.com \
  --allow-host "*.storage.example.com:443"
```

此策略允许：

- 对端口 443 上的 `api.example.com` 的请求（通常是 `https://api.example.com`）
- 对任何端口上的 `cdn.example.com` 的请求
- 对端口 443 上 `storage.example.com` 的任何子域的请求，如 `us-west.storage.example.com:443` 或 `eu-central.storage.example.com:443`

对 `example.com`（任何端口）、`www.example.com`（任何端口）或 `api.example.com:8080` 的请求都将被阻止，因为它们都不符合特定模式。

要允许一个域及其所有子域，请同时指定两种模式：

```console
$ docker sandbox network proxy my-sandbox \
  --policy deny \
  --allow-host example.com \
  --allow-host "*.example.com"
```

## 策略模式：允许列表与拒绝列表

策略有两种模式，决定默认行为。

### 允许列表模式

默认：允许所有流量，阻止特定目标。

```console
$ docker sandbox network proxy my-sandbox \
  --policy allow \
  --block-cidr 192.0.2.0/24 \
  --block-host example.com
```

当您希望代理访问大多数资源但需要阻止特定网络或域时，请使用允许列表模式。这限制较少，适用于开发环境，其中代理需要广泛的互联网访问。

### 拒绝列表模式

默认：阻止所有流量，允许特定目标。

```console
$ docker sandbox network proxy my-sandbox \
  --policy deny \
  --allow-host api.anthropic.com \
  --allow-host "*.npmjs.org"
```

当您希望严格控制外部访问时，请使用拒绝列表模式。这需要明确允许代理需要的每个服务，使其更安全但也更具限制性。适用于生产部署、CI/CD 管道或不受信任的代码。

### 域和 CIDR 匹配

域模式支持精确匹配、通配符和端口规范：

- `example.com` 仅匹配该确切域（任何端口）
- `example.com:443` 匹配对端口 443 上 `example.com` 的请求（默认 HTTPS 端口）
- `*.example.com` 匹配所有子域，如 `api.example.com` 或 `www.example.com`
- `*.example.com:443` 匹配对端口 443 上任何子域的请求

重要的模式行为：

- `example.com` 不匹配子域。对 `api.example.com` 的请求不会匹配 `example.com` 的规则。
- `*.example.com` 不匹配根域。对 `example.com` 的请求不会匹配 `*.example.com` 的规则。
- 要允许一个域及其子域，请同时指定两种模式：`example.com` 和 `*.example.com`。

当多个模式可以匹配一个请求时，最具体的模式优先：

1. 精确的主机名和端口：`api.example.com:443`
2. 精确的主机名，任意端口：`api.example.com`
3. 通配符模式（最长匹配优先）：`*.api.example.com:443`、`*.api.example.com`、`*.example.com:443`、`*.example.com`
4. 全匹配通配符：`*:443`、`*`
5. 默认策略（允许或拒绝）

这种特异性允许您在允许特定例外的同时阻止宽泛的模式。例如，您可以阻止 `example.com` 和 `*.example.com`，但允许 `api.example.com:443`。

CIDR 块在 DNS 解析后匹配 IP 地址：

- `192.0.2.0/24` 阻止所有 192.0.2.x 地址
- `198.51.100.0/24` 阻止所有 198.51.100.x 地址
- `203.0.113.0/24` 阻止所有 203.0.113.x 地址

当您阻止或允许一个域名时，代理会将其解析为 IP 地址，并根据 CIDR 规则检查这些 IP。这意味着阻止一个 CIDR 范围会影响任何解析到该范围内 IP 的域名。

## HTTPS 隧道的旁路模式

默认情况下，代理作为 HTTPS 连接的中间人，终止 TLS 并使用自己的证书颁发机构重新加密流量。这允许代理执行策略并为某些服务注入身份验证凭据。

沙盒容器信任代理的 CA 证书。

某些应用程序使用证书固定或其他与 MITM 代理不兼容的技术。对于这些情况，请使用旁路模式直接隧道传输 HTTPS 流量而不进行检查：

```console
$ docker sandbox network proxy my-sandbox \
  --bypass-host api.service-with-pinning.com
```

您也可以对特定 IP 范围的流量进行旁路：

```console
$ docker sandbox network proxy my-sandbox \
  --bypass-cidr 203.0.113.0/24
```

当流量被旁路时，代理：

- 作为简单的 TCP 隧道而不检查内容
- 无法向请求中注入身份验证凭据
- 无法检测域前置或其他规避技术
- 仍基于初始连接强制执行域名和端口匹配

仅在必要时使用旁路模式。被旁路的流量会失去 MITM 检查的可见性和安全优势。如果您旁路像 `github.com` 这样的宽泛域名，代理将无法查看代理在该域名上访问的内容。

## 策略持久化

网络策略存储在 JSON 配置文件中。

### 每个沙盒的配置

当您运行 `docker sandbox network proxy my-sandbox` 时，该命令仅更新该特定沙盒的配置。策略会持久化到 `~/.docker/sandboxes/vm/my-sandbox/proxy-config.json`。

默认策略（在创建新沙盒时使用）保持不变，除非您直接修改它。

### 默认配置

新沙盒的默认网络策略存储在 `~/.sandboxd/proxy-config.json`。该文件在第一个沙盒启动时自动创建，但仅当它尚不存在时。

当前的默认策略是 `allow`，它允许所有出站连接，除了被阻止的 CIDR 范围（私有网络、本地主机和云元数据服务）。

此默认值将在未来版本中更改为 `deny`，以提供更严格的默认设置。

您可以修改默认策略：

1. 直接编辑 `~/.sandboxd/proxy-config.json`
2. 或将沙盒策略复制到默认位置：

```console
$ cp ~/.docker/sandboxes/vm/my-sandbox/proxy-config.json ~/.sandboxd/proxy-config.json
```

在创建新沙盒之前，请审查并自定义默认策略以符合您的安全要求。一旦创建，默认策略文件不会被升级修改，从而保留您的自定义配置。

## 下一步

- [Architecture](architecture.md)
- [Using sandboxes effectively](workflows.md)
- [Custom templates](templates.md)
