---
description: 了解如何排查 Docker Hub 常见问题。
keywords: hub, troubleshoot
title: 排查 Docker Hub 问题
linkTitle: 排查问题
weight: 60
tags: [Troubleshooting]
toc_max: 2
---

如果您遇到 Docker Hub 相关问题，请参考以下解决方案。

## 已达到拉取速率限制（429 响应码）

### 错误信息

出现此问题时，您会在 Docker CLI 或 Docker Engine 日志中收到以下错误信息：

```text
You have reached your pull rate limit. You may increase the limit by authenticating and upgrading: https://www.docker.com/increase-rate-limits
```

### 可能原因

- 您作为已认证的 Docker Personal 用户已达到拉取速率限制。
- 您作为未认证用户，基于您的 IPv4 地址或 IPv6 /64 子网已达到拉取速率限制。

### 解决方案

您可以使用以下任一解决方案：

- [认证](./usage/pulls.md#authentication) 或 [升级](../subscription/change.md#upgrade-your-subscription) 您的 Docker 账户。
- [查看您的拉取速率限制](./usage/pulls.md#view-hourly-pull-rate-and-limit)，等待拉取速率限制降低后重试。

## 请求过多（429 响应码）

### 错误信息

出现此问题时，您会在 Docker CLI 或 Docker Engine 日志中收到以下错误信息：

```text
Too Many Requests
```

### 可能原因

- 您已达到 [滥用速率限制](./usage/_index.md#abuse-rate-limit)。

### 解决方案

1. 检查访问 Docker Hub 的 CI/CD 管道是否异常并修复。
2. 在您的自动化脚本中实现带退避的重试机制，确保不会每分钟发送数千个请求。

## 500 响应码

### 错误信息

出现此问题时，Docker CLI 或 Docker Engine 日志中常见的错误信息如下：

```text
Unexpected status code 500
```

### 可能原因

- Docker Hub 服务出现临时问题。

### 解决方案

1. 访问 [Docker 系统状态页面](https://www.dockerstatus.com/)，确认所有服务是否正常运行。
2. 尝试重新访问 Docker Hub。这可能是一个临时问题。
3. [联系 Docker 支持](https://www.docker.com/support/) 报告此问题。