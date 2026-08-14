---
title: 网络访问策略
linkTitle: 网络访问
weight: 30
description: 使用本地和组织策略规则控制 Docker 沙箱的出向网络访问。
keywords: docker sandboxes, network access, network rules, governance, local policy, organization policy
---

网络访问策略控制沙箱的出向连接。每条策略包含一条或多条规则，用于允许工作流所需的域名、IP 范围和端口，或阻止应保持不可访问的目标。

你可以在两个位置配置网络访问：

- [本地策略](local.md)：当组织治理未生效时，应用于某台开发者机器上的沙箱。
- [组织策略](organization.md)：在整个组织范围内或对选定团队集中生效。

当组织治理生效时，只有组织的允许规则才授予网络访问权限。本地允许规则在组织治理不再适用之前处于失效状态，而本地拒绝规则仍会在组织策略之上继续生效。请参阅[优先级](../concepts.md#precedence)。

## 规则语法

网络规则使用 `connect:tcp` 与 `connect:udp` 动作。资源为主机名、CIDR 范围、端口，或带端口的主机名。

示例：

- `api.example.com`
- `*.example.com`
- `**.example.com`
- `example.com:443`
- `10.0.0.0/8`

关于精确的通配符行为和 CIDR 支持，请参阅[网络规则](../concepts.md#network-rules)。

## 本地网络规则

使用 `sbx policy allow network` 和 `sbx policy deny network` 管理本地网络规则：

```console
$ sbx policy allow network api.example.com
$ sbx policy deny network ads.example.com
```

关于预设、沙箱作用域规则、测试与故障排查，请参阅[本地策略](local.md)。

## 组织网络规则

组织网络规则属于可应用于整个组织或选定团队的策略。有关设置步骤和团队作用范围，请参阅[组织策略](organization.md)。

使用[监控策略](../monitor-and-enforce/monitoring.md)检查某台开发者机器上哪些网络规则处于生效状态。
