---
title: 策略概念
weight: 10
description: Docker 沙箱治理背后的资源模型、规则语法和评估逻辑。
keywords: docker sandboxes, policy concepts, rule syntax, network rules, filesystem rules, mcp policy, cedar policy, precedence, rule evaluation
---

## Resource model（资源模型）

Docker 沙箱治理围绕两种资源类型构建：**策略（policies）**和**规则（rules）**。

**策略**是一组具名规则的集合，用于控制沙箱访问。策略存在于两个层级：

- **本地（Local）**：使用 `sbx policy` CLI 按机器配置。仅对该机器上的沙箱生效。
- **组织（Organization）**：在 Docker Home 中配置。网络与文件系统策略也可以通过 [Governance API](/reference/api/ai-governance/) 管理。对整个组织范围内的沙箱生效。一个组织可以拥有多个策略，每个策略要么在组织范围内生效，要么应用于特定团队。参见 [Policy scope](#policy-scope)。

当组织治理生效时，只有组织的 allow 规则才能授予访问权限。本地及 kit 定义的 deny 规则仍会在此之上生效。参见 [Precedence](#precedence)。

**规则**是策略内访问控制的基本单元。每条规则包含：

- **Name**：人类可读的标签
- **Actions**：规则所控制的访问类型
- **Resources**：规则匹配的目标
- **Decision**：`allow` 或 `deny`

规则按域（domain）分组。策略中的网络与文件系统规则必须共享同一个域，即 `network` 或 `filesystem`。MCP 策略使用写在 `MCP` 命名空间中的 Cedar 语句，而非网络与文件系统规则格式。

## Policy scope（策略作用域）

每个组织策略要么在整个组织范围内生效，要么仅对特定团队生效：

- 组织范围（Org-wide）：未分配任何团队时，该策略应用于组织的每个成员。
- 团队范围（Team-scoped）：分配了一个或多个团队时，该策略仅应用于这些团队的成员。

这里的团队与你为组织管理的 [团队](/manuals/admin/organization/manage/manage-a-team.md) 相同；Docker 会将策略的团队与每个用户的团队成员身份进行匹配。由于一个组织可以混用组织范围与团队范围的策略，单个用户往往同时受多个策略约束。适用于某个用户的策略即其_有效策略（effective policies）_：包括每个组织范围策略，以及该用户所属团队对应的每个团队范围策略。有关用户的有效策略如何组合，参见 [Rule evaluation](#rule-evaluation)。

## Rule syntax（规则语法）

### Network rules（网络规则）

网络规则使用动作 `connect:tcp` 和 `connect:udp`。资源为主机名、CIDR 范围或端口。

**主机名模式**

| 模式                  | 示例              | 匹配                                               |
| --------------------- | ----------------- | -------------------------------------------------- |
| 精确主机名            | `example.com`     | 仅 `example.com`，不含子域名                       |
| 单级通配符            | `*.example.com`   | 一级子域名：`api.example.com`                      |
| 多级通配符            | `**.example.com`  | 任意深度：`api.example.com`、`v2.api.example.com`  |
| 带端口的主机名        | `example.com:443` | 仅 443 端口上的 `example.com`                      |

`example.com` 与 `*.example.com` 互不覆盖。如果既要匹配根域名又要匹配其子域名，需同时指定二者。

**CIDR 范围**

支持 IPv4 和 IPv6 表示法：`10.0.0.0/8`、`192.168.1.0/24`、`2001:db8::/32`。

有关本地和组织策略配置，参见 [Network access policies](access-controls/network.md)。

### Filesystem rules（文件系统规则）

文件系统规则使用动作 `read` 和 `write`。资源为沙箱可挂载为工作区的主机路径。

以写访问方式挂载的工作区必须同时被 `read` 和 `write` 规则允许；只读工作区仅需 `read`。当默认拒绝阻止某次挂载时，拒绝原因会指明缺失的是读还是写访问权限。

`~` 在每个平台上都会展开为用户的主目录，包括 Windows（在 Windows 上解析为 `%USERPROFILE%`）。因此单条 `~/**` 规则可以匹配 macOS、Linux 和 Windows 上每个用户的主目录树。策略引擎只展开 `~`：它不展开环境变量，因此像 `%USERPROFILE%\**` 或 `$HOME/**` 这样的模式什么都匹配不到。

对于主目录以外的路径，请以用户操作系统所使用的格式书写。规则只匹配它书写时所用的格式，所以多个平台共有的位置需要为每个平台各写一条规则：

| 操作系统       | 示例路径                                   |
| ---------------- | ------------------------------------------ |
| macOS、Linux     | `/data/project/**`                         |
| Windows          | `C:\data\project\**`                       |
| WSL              | `\\wsl.localhost\<distro>\data\project\**` |

在 Windows 上，`*:` 匹配任意盘符，因此 `*:\data\**` 会匹配任意盘符上的该路径。

通配符在每种路径格式中的行为一致：

| 模式               | 示例       | 匹配                                                       |
| ------------------ | ---------- | ---------------------------------------------------------- |
| 精确路径           | `/data`    | 仅 `/data`                                                 |
| 段级通配符         | `/data/*`  | `/data/project`，仅一个路径段，不含子目录                  |
| 递归通配符         | `/data/**` | `/data/project`、`/data/project/src`，任意深度            |

使用 `**` 递归匹配整个目录树。单个 `*` 只在一个路径段内匹配，不会跨越路径分隔符。例如，`~/**` 匹配主目录下的所有路径，而 `~/*` 只匹配其直接子项。

有关组织策略配置和强制执行细节，参见 [Filesystem access policies](access-controls/filesystem.md)。

### MCP policies（MCP 策略）

MCP 策略控制通过 Docker 的 [MCP gateway](../mcp-gateway.md) 提供给沙箱的 Model Context Protocol 活动。它们是使用 `MCP` 命名空间以 Cedar 编写的组织策略，而非网络与文件系统规则格式。

MCP 策略在开发者注册服务器时以及代理使用 MCP 网关时生效。注册规则控制未来的 `sbx mcp add` 操作。使用时规则控制工具调用、网关元工具（meta-tools）、资源读取，以及从已注册或已加载服务器检索提示（prompt）。

受治理的 MCP 活动默认拒绝：除非有匹配的 `permit` 允许，否则请求会被阻止。匹配的 `forbid` 会覆盖任何 `permit`，包括需要审批的 permit。策略作用域提供了主体（principal），因此应使用组织或团队作用域，而不是在 Cedar 中匹配用户、团队、租户或角色。

有关代表性策略，参见 [MCP access policies](access-controls/mcp.md)。有关精确的动作、资源、上下文和审批行为，参见 [MCP policy reference](reference/mcp-policy.md)。

## Rule evaluation（规则评估）

当组织治理生效时，用户所有 [有效策略](#policy-scope) 的规则会被合并，并针对每个请求一起评估，遵循两条原则：

- 拒绝优先（Deny wins）：如果有任何规则以 `decision: deny` 匹配，则无论是否有匹配的 allow 规则，请求都会被拒绝。
- 默认拒绝（Default deny）：任何 allow 规则未匹配到的内容都会被阻止。除非有网络规则允许目的地，否则出站网络流量会被阻止；除非有文件系统规则允许，否则主机路径无法被挂载。除非有 MCP `permit` 允许，否则 MCP 活动会被阻止。

由于每个有效策略都参与同一次评估，因此 allow 是累加的（只要任何有效策略允许，请求就被允许），而 deny 是绝对的（只要任何有效策略拒绝，请求就被阻止）。因此，组织范围策略中的 deny 规则对所有人生效，且无法被团队范围策略覆盖，这使得组织范围的 deny 规则很适合用作护栏（guardrails）。

本地及 kit 定义的 allow 规则不参与此次评估。来自这些来源的 deny 规则仍然生效。参见 [Precedence](#precedence)。

## Precedence（优先级）

生效内容取决于你的组织是否启用了治理：

- 未启用组织治理：由本地规则和任何 [kit 定义的网络规则](../customize/kits.md#control-network-access) 决定沙箱可访问的内容。
- 组织治理生效：由组织策略决定可以授予哪些访问权限。只有组织的 allow 规则才能授予访问权限，因此本地及 kit 定义的 allow 规则处于非激活状态，无法扩展组织所许可的范围。deny 规则来自所有来源均生效，因此本地或 kit 定义的 deny 仍可进一步限制访问。

优先级由规则的决策（decision）而非其来源决定：

| 规则                | 组织治理下是否评估 |
| ------------------- | ------------------ |
| 组织 allow          | 是                 |
| 组织 deny           | 是                 |
| 本地 allow          | 否                 |
| 本地 deny           | 是                 |
| kit 定义 allow      | 否                 |
| kit 定义 deny       | 是                 |

本地及 kit 定义的规则仅涵盖网络访问，因此叠加在组织策略之上的 deny 始终是网络 deny。`sbx policy ls` 默认隐藏非激活规则。有关如何列出它们，参见 [Monitoring](monitor-and-enforce/monitoring.md#showing-inactive-rules)。

当组织治理生效时，用户的组织策略会被一起评估，如 [Rule evaluation](#rule-evaluation) 所述。
