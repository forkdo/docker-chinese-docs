---
title: 空气隔离容器
description: 使用自定义代理规则和网络限制控制容器网络访问
keywords: 空气隔离容器, 网络安全, 代理配置, 容器隔离, docker desktop
aliases:
 - /desktop/hardened-desktop/settings-management/air-gapped-containers/
 - /desktop/hardened-desktop/air-gapped-containers/
 - /security/for-admins/hardened-desktop/air-gapped-containers/
---

{{< summary-bar feature_name="空气隔离容器" >}}

空气隔离容器允许您通过控制容器可以发送和接收数据的位置来限制容器网络访问。此功能将自定义代理规则应用于容器网络流量，有助于保护容器不应具有无限制互联网访问的环境。

Docker Desktop 可以配置容器网络流量以接受连接、拒绝连接或通过 HTTP 或 SOCKS 代理进行隧道传输。您可以控制策略适用的 TCP 端口以及是使用单个代理还是通过代理自动配置 (PAC) 文件使用每个目标的策略。

此页面提供了空气隔离容器的概述和配置步骤。

## 谁应该使用空气隔离容器？

空气隔离容器帮助组织在受限环境中维护安全性：

- 安全开发环境：防止容器访问未经授权的外部服务
- 合规要求：满足需要网络隔离的监管标准
- 数据丢失防护：阻止容器将敏感数据上传到外部服务
- 供应链安全：控制容器在构建期间可以访问哪些外部资源
- 企业网络策略：为容器化应用程序强制执行现有的网络安全策略

## 空气隔离容器的工作原理

空气隔离容器通过拦截容器网络流量并应用代理规则来工作：

1. 流量拦截：Docker Desktop 拦截来自容器的所有出站网络连接
1. 端口过滤：只有在指定端口（`transparentPorts`）上的流量才受代理规则约束
1. 规则评估：PAC 文件规则或静态代理设置确定如何处理每个连接
1. 连接处理：根据规则允许直接流量、通过代理路由或阻止流量

一些重要的注意事项包括：

- 现有的 `proxy` 设置继续适用于主机上 Docker Desktop 应用程序的流量
- 如果 PAC 文件下载失败，容器会阻止对目标 URL 的请求
- 主机名仅对端口 80 和 443 可用，但对于其他端口只有 IP 地址可用

## 先决条件

在配置空气隔离容器之前，您必须具备：

- 启用[强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)以确保用户使用您的组织进行身份验证
- Docker Business 订阅
- 配置了 [Settings Management](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md) 以管理组织策略
- 下载了 Docker Desktop 4.29 或更高版本

## 配置空气隔离容器

将容器代理添加到您的 [`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md)。例如：

```json
{
  "configurationFileVersion": 2,
  "containersProxy": {
    "locked": true,
    "mode": "manual",
    "http": "",
    "https": "",
    "exclude": [],
    "pac": "http://192.168.1.16:62039/proxy.pac",
    "transparentPorts": "*"
  }
}
```

### 配置参数

`containersProxy` 设置控制应用于容器流量的网络策略：

| 参数 | 描述 | 值 |
|------|------|----|
| `locked` | 防止开发人员覆盖设置 | `true` (锁定), `false` (默认) |
| `mode` | 代理配置方法 | `system` (使用系统代理), `manual` (自定义) |
| `http` | HTTP 代理服务器 | URL (例如 `"http://proxy.company.com:8080"`) |
| `https` | HTTPS 代理服务器 | URL (例如 `"https://proxy.company.com:8080"`) |
| `exclude` | 绕过这些地址的代理 | 主机名/IP 数组 |
| `pac` | 代理自动配置文件 URL | PAC 文件的 URL |
| `transparentPorts` | 受代理规则约束的端口 | 逗号分隔的端口或通配符 (`"*"`) |

### 配置示例

阻止所有外部访问：

```json
"containersProxy": {
  "locked": true,
  "mode": "manual",
  "http": "",
  "https": "",
  "exclude": [],
  "transparentPorts": "*"
}
```

允许特定内部服务：

```json
"containersProxy": {
  "locked": true,
  "mode": "manual",
  "http": "",
  "https": "",
  "exclude": ["internal.company.com", "10.0.0.0/8"],
  "transparentPorts": "80,443"
}
```

通过企业代理路由：

```json
"containersProxy": {
  "locked": true,
  "mode": "manual",
  "http": "http://corporate-proxy.company.com:8080",
  "https": "http://corporate-proxy.company.com:8080",
  "exclude": ["localhost", "*.company.local"],
  "transparentPorts": "*"
}
```

## 代理自动配置 (PAC) 文件

PAC 文件通过为不同目标定义规则来提供对容器网络访问的细粒度控制。

### 基本 PAC 文件结构

```javascript
function FindProxyForURL(url, host) {
	if (localHostOrDomainIs(host, 'internal.corp')) {
		return "PROXY 10.0.0.1:3128";
	}
	if (isInNet(host, "192.168.0.0", "255.255.255.0")) {
	    return "DIRECT";
	}
    return "PROXY reject.docker.internal:1234";
}
```

### 一般注意事项

 - `FindProxyForURL` 函数的 URL 参数格式为 http://host_or_ip:port 或 https://host_or_ip:port
 - 如果您有一个内部容器尝试访问 https://docs.docker.com/enterprise/security/hardened-desktop/air-gapped-containers，docker 代理服务将提交 docs.docker.com 作为主机值，https://docs.docker.com:443 作为 url 值到 FindProxyForURL，如果您在 PAC 文件中使用 `shExpMatch` 函数如下：

   ```console
   if(shExpMatch(url, "https://docs.docker.com:443/enterprise/security/*")) return "DIRECT";
   ```

   `shExpMatch` 函数将失败，而是使用：

   ```console
   if (host == docs.docker.com && url.indexOf(":443") > 0) return "DIRECT";
   ```

### PAC 文件返回值

| 返回值 | 操作 |
|--------|------|
| `PROXY host:port` | 通过指定主机和端口的 HTTP 代理路由 |
| `SOCKS5 host:port` | 通过指定主机和端口的 SOCKS5 代理路由 |
| `DIRECT` | 允许直接连接而不使用代理 |
| `PROXY reject.docker.internal:any_port` | 完全阻止请求 |

### 高级 PAC 文件示例

```javascript
function FindProxyForURL(url, host) {
  // 允许访问 Docker Hub 以获取已批准的基础镜像
  if (dnsDomainIs(host, ".docker.io") || host === "docker.io") {
    return "PROXY corporate-proxy.company.com:8080";
  }

  // 允许内部包仓库
  if (localHostOrDomainIs(host, 'nexus.company.com') ||
      localHostOrDomainIs(host, 'artifactory.company.com')) {
    return "DIRECT";
  }

  // 允许在特定端口上的开发工具
  if (url.indexOf(":3000") > 0 || url.indexOf(":8080") > 0) {
    if (isInNet(host, "10.0.0.0", "255.0.0.0")) {
      return "DIRECT";
    }
  }

  // 阻止访问开发者的 localhost
  if (host === "host.docker.internal" || host === "localhost") {
    return "PROXY reject.docker.internal:1234";
  }

  // 阻止所有其他外部访问
  return "PROXY reject.docker.internal:1234";
}
```

## 验证空气隔离容器配置

应用配置后，测试容器网络限制是否正常工作：

测试阻止的访问：

```console
$ docker run --rm alpine wget -O- https://www.google.com
# 应该根据您的代理规则失败或超时
```

测试允许的访问：

```console
$ docker run --rm alpine wget -O- https://internal.company.com
# 如果 internal.company.com 在您的排除列表或 PAC 规则中，应该成功
```

测试代理路由：

```console
$ docker run --rm alpine wget -O- https://docker.io
# 如果通过已批准的代理路由，应该成功
```

## 安全注意事项

- 网络策略强制执行：空气隔离容器在 Docker Desktop 级别工作。高级用户可能通过各种方式绕过限制，因此请考虑为高安全性环境添加网络级控制。
- 开发工作流程影响：过于严格的策略可能会破坏合法的开发工作流程。彻底测试并为必要的服务提供清晰的例外。
- PAC 文件管理：将 PAC 文件托管在可靠的内部基础设施上。PAC 下载失败会导致容器网络访问被阻止。
- 性能考虑：具有许多规则的复杂 PAC 文件可能会影响容器网络性能。保持规则简单高效。