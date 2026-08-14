---
title: 组织策略
linkTitle: 组织策略
weight: 20
description: 为你的组织集中管理沙箱的网络、文件系统与 MCP 策略。
keywords: docker sandboxes, governance, organization policy, AI governance, Docker Home, network access, filesystem access, mcp policy
aliases:
  - /ai/sandboxes/security/governance/
  - /ai/sandboxes/governance/org/
---

[本地策略](local.md)让开发者个人控制其沙箱可以访问的内容。组织策略将这种控制上移到管理员层面：组织策略适用于整个组织范围内的沙箱，可以面向每一位成员，也可以面向特定团队。当组织治理生效时，只有组织的允许规则才授予访问权限：本地 `sbx policy` 的允许规则不再被评估，也无法扩大组织所许可的范围。本地网络拒绝规则仍然生效，因此开发者可以进一步限制访问，但绝不能放宽限制。

管理员可以通过 Docker Home 界面管理组织策略。若需以编程方式管理网络与文件系统策略，请使用 [Governance API](/reference/api/ai-governance/)。

默认情况下，只有组织[所有者](/manuals/enterprise/security/roles-and-permissions/core-roles.md)可以查看和管理 AI 治理策略。要让非所有者的人员管理策略，请创建一个带有 **Governance** 权限的[自定义角色](/manuals/enterprise/security/roles-and-permissions/custom-roles.md)，并将其分配给某个用户或团队。

> [!NOTE]
> 沙箱组织治理需要单独的付费订阅。
> [联系 Docker 销售团队](https://www.docker.com/products/ai-governance/#contact-sales)
> 申请访问权限。

## Create a policy（创建策略）

在 [Docker Home](https://app.docker.com) 左侧导航栏的 **AI Platform** 部分管理策略。

创建策略的步骤：

1. 登录 [Docker Home](https://app.docker.com) 并选择你的组织。
1. 在左侧导航栏中展开 **AI Platform**，然后选择 **Network access**、**Filesystem access** 或 **MCP access**。
1. 选择 **Create policy**。
1. 输入 **Policy name**。
1. 将 **Scope** 设置为 **Organization** 或 **Teams**。如果选择 **Teams**，请选定该策略适用的团队。请参阅[将策略限定到团队](#scope-policies-to-teams)。
1. 定义策略规则。对于网络和文件系统策略，为每条规则选择 **Add rule**。对于 MCP 策略，在策略编辑器中输入 Cedar 语句。有关语法和示例，请使用[选择策略类型](#choose-a-policy-type)中相应的访问控制页面。

现有策略会以名称、作用范围、规则数量和最近更新时间列出。使用操作菜单（⋮）可编辑或删除策略。

## 配置支持信息

管理员可以添加一条可选的支持信息，当某个沙箱操作被组织治理阻止时，该信息会显示在策略拒绝详情之后。可用它引导成员前往内部支持渠道、工单队列或安全联系人。

设置该信息的步骤：

1. 登录 [Docker Home](https://app.docker.com) 并选择你的组织。
1. 在左侧导航栏中展开 **AI Platform**，然后选择 **Manage**。
1. 在 **Support message** 中输入不超过 500 个字符的内容。
1. 选择 **Save changes**。

Docker 仅在因组织治理策略导致的拒绝场景中显示该信息。如果留空，Docker 将只显示策略拒绝信息，而不附加联系文本。

## Choose a policy type（选择策略类型）

组织策略按访问面进行管理。有关语法、示例与强制执行细节，请查阅相应的访问控制页面：

- [网络访问策略](network.md)：控制沙箱的出向网络访问。
- [文件系统访问策略](filesystem.md)：控制沙箱可以将哪些主机路径挂载为工作区。
- [MCP 访问策略](mcp.md)：使用 Cedar 策略控制 MCP 服务器注册、工具调用、资源、提示以及审批关卡。

当组织治理生效时，本地和 kit 定义的允许规则不会被评估，而来自这些来源的拒绝规则仍然适用。请参阅[优先级](../concepts.md#precedence)。要查看某台开发者机器上哪些规则处于生效状态，请使用[监控策略](../monitor-and-enforce/monitoring.md)。

## Scope policies to teams（将策略限定到团队）

一个组织可以拥有多条策略，每条策略要么适用于整个组织，要么适用于特定团队。作用范围划分让你可以对组织的不同部分应用不同的规则。

策略的 [**Scope**](#create-a-policy) 控制它适用于哪些人。将其设为 **Organization** 可将策略应用于每一位成员，设为 **Teams** 则仅应用于你所选团队的成员。

### 准备工作

团队作用范围以你所在组织已有的[团队](/manuals/admin/organization/manage/manage-a-team.md)为目标，因此在将策略限定到某个团队之前，该团队必须已存在。可以通过两种方式创建团队并管理其成员：

- 手动，在 Docker Home 中操作。
- 自动，通过[组映射](/manuals/enterprise/security/provisioning/scim/group-mapping.md)将你身份提供商的组与组织中的团队同步。组映射会创建尚不存在的团队，并使其成员与你的 IdP 组保持一致。

由于策略按团队应用，用户的策略会随其团队成员身份的变化（包括从你的 IdP 同步而来的变化）而自动更新。

### 限定作用范围的策略如何组合

用户受其所有[有效策略](../concepts.md#policy-scope)的管辖：每一条组织范围策略，加上其所属团队的团队作用域策略。请将组织范围策略用于必须处处适用的护栏，将团队作用域策略用于仅部分团队需要的访问权限。

关于本地策略与组织策略之间的优先级，以及允许与拒绝规则如何组合，请参阅[策略概念](../concepts.md)。

## 故障排查

### 策略更改未生效

更新组织策略后，更改最多需要 5 分钟才能传播到开发者机器。要立即应用更改，用户可以运行 `sbx policy reset`，该命令会停止守护进程，并强制其在下一次执行 `sbx` 命令时拉取最新的组织策略。

> [!WARNING]
> `sbx policy reset` 会删除所有本地配置的策略规则。该命令在继续之前会提示确认。

#### 按策略类型的强制执行时机

各类策略在更改到达开发者机器之后何时生效有所不同：

- 网络策略在每一个出向请求上评估。一旦策略更改同步到开发者机器（最多 5 分钟），它会立即应用于后续请求。

- 文件系统策略只在挂载工作区时检查，也就是创建沙箱时。沙箱一旦运行起来，更改文件系统策略对该沙箱不起作用。该沙箱会继续访问先前允许的路径，直到它被移除并创建新的沙箱。

- MCP 注册策略在使用 `sbx mcp add` 注册服务器时评估。更改注册规则本身不会移除现有注册，也不会停止已加载的服务器。

- MCP 使用时策略在沙箱发起被治理的 MCP 请求（例如工具调用、资源读取、提示获取或内置网关工具调用）时由 MCP 网关评估。策略更改同步之后，使用时规则会应用于后续通过网关发起的被治理 MCP 请求。

要立即应用文件系统策略更改，请移除正在运行的沙箱并创建一个新的。要阻止使用已注册或已加载的 MCP 服务器，请为该已注册的服务器名称添加使用时规则。有关示例，请参阅[撤销服务器访问](mcp.md#withdraw-server-access)。
