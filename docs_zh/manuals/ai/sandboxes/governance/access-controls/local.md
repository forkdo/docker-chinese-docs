---
title: 本地策略
weight: 10
description: 为你机器上的沙箱配置本地网络访问规则。
keywords: docker sandboxes, local policy, network access, allow rules, deny rules, sbx policy
aliases:
  - /ai/sandboxes/security/policy/
  - /ai/sandboxes/governance/local/
---

`sbx policy` 命令管理你机器上的本地策略。本地策略包含网络访问规则。使用全局作用域时，规则会应用于机器上的所有沙箱；按名称限定作用域时，则应用于单个沙箱。

本地策略与组织治理的交互方式如下：

- **无组织治理**：由本地策略控制沙箱可以访问的内容。
- **组织治理生效**：只有组织的允许规则才授予访问权限，因此本地允许规则处于失效状态，无法扩大组织所许可的范围。本地拒绝规则仍会被评估，因此你可以在组织策略的基础上进一步限制访问。要列出失效规则，请运行 `sbx policy ls --include-inactive`。请参阅[监控](../monitor-and-enforce/monitoring.md#showing-inactive-rules)。

关于组织治理的工作方式，请参阅[组织策略](organization.md)。

关于域名模式、通配符、CIDR 范围与文件系统路径语法，请参阅[策略概念](../concepts.md#rule-syntax)。

## 默认预设

流量离开沙箱的唯一途径是通过你主机上的 HTTP/HTTPS 代理，该代理会对每一个出向请求强制执行访问规则。非 HTTP 的 TCP 流量（包括 SSH）可以通过为目标 IP 和端口添加策略规则来允许（例如 `sbx policy allow network "10.1.2.3:22"`）。UDP 和 ICMP 在网络层被阻止，且无法通过策略规则解除阻止。

如果你尚未选择默认预设，CLI 会在运行沙箱之前提示你选择。运行 `sbx policy reset` 会清除该预设并再次提示你选择：

```plaintext
Initialize the global network policy for your sandboxes:

  Applies to all sandboxes, current and future — change it later with
  "sbx policy allow/deny/rm". Kits, including built-in agent kits, may
  also add per-sandbox rules.

     1. Open         — All network traffic allowed, no restrictions.
  ❯  2. Balanced     — Default deny, with common dev sites allowed.
     3. Locked Down  — All network traffic blocked unless you allow it.

  Use ↑/↓ or 1–3 to navigate, Enter to confirm, Esc to cancel.
```

| 预设        | 说明                                                                                                                             |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Open        | 允许所有出向流量。等价于使用 `sbx policy allow network "**"` 添加一条通配符允许规则。                                            |
| Balanced    | 默认拒绝，并附带一个基线允许列表，覆盖 AI 提供商 API、包管理器、代码托管、容器镜像仓库以及常见的云服务。                         |
| Locked Down | 阻止所有出向流量，包括模型提供商 API（例如 `api.anthropic.com`）。你必须显式允许所需的一切。                                     |

**Balanced** 预设的基线允许列表对大多数工作流来说是一个不错的起点。运行 `sbx policy ls` 可查看它究竟包含哪些规则。自 v0.35.0 起，Balanced 预设还允许 VS Code 域名、Azure Blob Storage（`*.blob.core.windows.net`）以及通过 HTTP 访问 `dhi.io`。

> [!NOTE]
> 如果你的组织集中管理沙箱策略，则组织规则优先于你在此处选择的预设。请参阅[组织策略](organization.md)。

### 非交互式环境

在 CI 流水线或无头服务器等非交互式环境中，无法显示交互式提示。请在运行任何其他 `sbx` 命令之前，使用 `sbx policy init` 设置预设：

```console
$ sbx policy init balanced
```

可用值为 `allow-all`、`balanced` 和 `deny-all`。

## 管理规则

使用 [`sbx policy allow`](/reference/cli/sbx/policy/allow/) 和 [`sbx policy deny`](/reference/cli/sbx/policy/deny/) 在生效预设的基础上添加或限制访问。更改会立即生效。规则默认应用于所有沙箱：

```console
$ sbx policy allow network api.anthropic.com
$ sbx policy deny network ads.example.com
```

传入 `--sandbox <name>` 可将规则的作用域限定到单个沙箱：

```console
$ sbx policy allow network --sandbox my-sandbox api.example.com
$ sbx policy deny network --sandbox my-sandbox ads.example.com
```

自 v0.38.0 起，你还可以在创建时通过 `sbx create` 或 `sbx run` 上的 `--deny-network` 设置每沙箱的拒绝规则，而无需事后再添加：

```console
$ sbx create --deny-network ads.example.com claude .
$ sbx run --deny-network ads.example.com claude
```

多次传入该标志可拒绝多个主机。以这种方式添加的规则会出现在 `sbx policy ls <name>` 中，并可通过 `sbx policy rm network --sandbox <name> --resource <host>` 移除。

在一条命令中用逗号分隔的列表指定多个主机：

```console
$ sbx policy allow network "api.anthropic.com,*.npmjs.org,*.pypi.org"
```

按资源或按规则 ID 移除规则：

```console
$ sbx policy rm network --resource ads.example.com
$ sbx policy rm network --id 2d3c1f0e-4a73-4e05-bc9d-f2f9a4b50d67
```

要移除沙箱作用域的规则，请传入 `--sandbox <name>`：

```console
$ sbx policy rm network --sandbox my-sandbox --resource api.example.com
```

要检查哪些策略处于生效状态以及它们来自何处，请使用 `sbx policy ls`。使用 `--source` 按来源筛选（`local`、`org`、`kit`），使用 `--decision` 按结果筛选（`allow`、`deny`），使用 `--wide` 查看包含规则 ID 的规则级细节。要完整检查单条策略或规则，请使用 `sbx policy inspect`。请参阅[监控](../monitor-and-enforce/monitoring.md)。

## 测试策略

在运行沙箱之前，你可以使用 `sbx policy check network` 检查当前策略是否会允许某个网络请求：

```console
$ sbx policy check network api.anthropic.com
Allowed: api.anthropic.com

$ sbx policy check network blocked.example.com
Denied: blocked.example.com
```

目标可以是主机名、`host:port` 组合、IP 地址或 URL。裸主机名和 IP 地址会针对 443 端口进行评估。这对于验证自定义规则，或在启动智能体之前检查 Locked Down 预设会阻止哪些内容很有用。

要在特定沙箱的上下文中检查策略：

```console
$ sbx policy check network --sandbox my-sandbox api.example.com
```

### 重置

要移除所有自定义规则并使用新预设重新开始，请使用 `sbx policy reset`：

```console
$ sbx policy reset
```

这会删除本地策略存储、重启守护进程，并提示你选择新预设。守护进程关闭时，正在运行的沙箱会停止。传入 `--force` 可跳过确认提示：

```console
$ sbx policy reset --force
```

## 故障排查

### 本地允许规则没有效果

如果你用 `sbx policy allow` 添加的规则未改变沙箱行为，那么你的组织很可能已启用治理。运行 `sbx policy ls` 检查：如果输出以显示 `Managed by <org>` 的 `Governance:` 状态行开头，则组织治理已生效。生效时，本地允许规则处于失效状态。你无法用它们来放宽组织策略施加的限制。

失效的允许规则默认在 `sbx policy ls` 中被隐藏；运行 `sbx policy ls --include-inactive` 可看到它们，并在 `STATUS` 列中显示 `inactive` 状态。

当组织治理生效时，只有组织的允许规则才能授予访问权限。如果你需要访问额外的资源，请让管理员更新组织策略。本地拒绝规则仍然生效，因此你可以使用 `sbx policy deny` 进一步限制访问。

### 添加允许规则后某个域名仍被阻止

如果在你添加本地允许规则后某个域名仍被阻止，那么你的组织很可能强制执行了治理，从而使本地允许规则失效。运行 `sbx policy ls` 检查组织治理是否生效；如果输出以显示 `Managed by <org>` 的 `Governance:` 状态行开头，则表示已生效。添加 `--include-inactive` 以确认你的规则显示为 `inactive` 状态。如果是这样，则只能通过在 Docker Home 中或经由 [API](/reference/api/ai-governance/) 更新组织策略来解除该阻止。
