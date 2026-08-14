---
title: MCP 策略参考
linkTitle: MCP 策略
weight: 20
description: Docker MCP 策略的动作、资源、属性、上下文字段和审批行为参考。
keywords: docker sandboxes, MCP policy, Cedar policy, MCP actions, MCP resources, requireApproval, AI Governance
---

MCP 策略是使用 Docker 的 `MCP` 命名空间以 Cedar 编写的组织策略。本参考定义了针对通过 Docker 的 [MCP gateway](../../mcp-gateway.md) 提供给沙箱的 Model Context Protocol (MCP) 活动的 Docker 专属策略界面。

请将本参考与 [MCP access policies](../access-controls/mcp.md) 配合使用以了解常见策略模式。有关 Cedar 语言，参见 [Cedar 文档](https://docs.cedarpolicy.com/)。

## Evaluation model（评估模型）

Cedar 针对主体（principal）、动作（action）、资源（resource）和上下文（context）评估 MCP 请求。对于 Docker MCP 策略，策略作用域提供主体。请针对动作、资源和上下文编写策略。引用主体属性的子句，例如 `principal in ...`、`principal.role` 或 `principal.tenant`，都不会匹配。

受治理的 MCP 活动默认拒绝。除非有匹配的 `permit` 允许，否则请求会被阻止。匹配的 `forbid` 会覆盖任何 `permit`，包括带有 `@requireApproval` 注解的 permit。

有关 Docker Sandboxes 何时为用户评估 MCP 策略的详情，参见 [Govern the server lifecycle](../access-controls/mcp.md#govern-the-server-lifecycle)。

无动作的 `permit` 会匹配到达 Cedar 评估的每个 MCP 动作：

```plaintext
permit (principal, action, resource);
```

## Actions（动作）

| 动作                | 治理对象                  | 说明                                                                                                          |
| ------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `register`          | MCP 服务器注册            | 服务器注册需要显式的 `permit`。使用服务器属性来限定注册范围。                                                  |
| `invokeTool`        | MCP 工具调用              | 大多数工具访问策略针对此动作。                                                                                |
| `invokePrimordial`  | 网关元工具调用            | 适用于内置网关工具，如 `mcp-exec`、`mcp-add`、`code-mode` 以及 OAuth 授权助手。                               |
| `readResource`      | MCP 资源读取              | 规则匹配 `MCP::Resource` 和 `resource.uri`。                                                                  |
| `getPrompt`         | MCP 提示检索              | 规则匹配 `MCP::Prompt` 和 `resource.name`。                                                                   |
| `listTools`         | MCP 工具列表              | 在架构中定义，但不受 Cedar 门控。工具列表可能包含在调用时被拒绝的工具。                                       |
| `listResources`     | MCP 资源列表              | 在架构中定义，但不受 Cedar 门控。资源列表可能包含被策略拒绝的资源。                                           |
| `subscribeResource` | MCP 资源订阅              | 在架构中定义，但不受 Cedar 门控。                                                                             |

## Resources（资源）

使用请求对应的 MCP 实体类型和属性匹配资源。

| 实体              | 匹配方式               | 说明                                                                                                                             |
| ----------------- | ---------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `MCP::Server`     | 已注册的服务器名称     | 规范的服务器身份是 `resource.identityURL` 属性，而非实体 ID。                                                                     |
| `MCP::Tool`       | 裸工具名               | 使用 `resource.name`。不包含显示前缀。裸名匹配会应用于每个暴露该名称工具的服务器。                                                |
| `MCP::Resource`   | 资源 URI               | 使用 `resource.uri`。                                                                                                             |
| `MCP::Prompt`     | 提示名称               | 使用 `resource.name`。                                                                                                            |
| `MCP::Primordial` | 网关元工具名称         | 用实体引用匹配特定的 primordial。                                                                                                 |

示例：

```plaintext
resource in MCP::Server::"notion"
resource.name == "move_file"
resource.uri like "*/docs/*"
resource in MCP::Primordial::"code-mode"
```

## Resource attributes（资源属性）

工具注解属性来自 MCP 工具注解或目录元数据，仅供参考（advisory）。

| 属性                       | 适用于            | 说明                                                                                                                                                 |
| -------------------------- | ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `resource.name`            | 工具与提示        | 对工具而言，这是裸工具名，而非带显示前缀的名称。                                                                                                     |
| `resource.uri`             | 资源              | 与 `like` 等字符串运算符配合使用。                                                                                                                   |
| `resource.readOnly`        | 工具              | 工具未声明时默认为 `false`。                                                                                                                         |
| `resource.destructive`     | 工具              | 工具未声明时默认为 `true`。                                                                                                                          |
| `resource.idempotent`      | 工具              | 工具未声明时默认为 `false`。                                                                                                                         |
| `resource.openWorld`       | 工具              | 工具未声明时默认为 `true`。                                                                                                                          |
| `resource.type`            | 服务器            | 用于服务器注册规则。参见 [Server type values](#server-type-values)。                                                                                 |
| `resource.identityURL`     | 服务器            | 规范的服务器身份。其取值取决于注册类型。参见 [Server identity values](#server-identity-values)。                                                     |
| `resource.requiresOAuth`   | 服务器            | 用于服务器注册规则。                                                                                                                                 |
| `resource.requiresNetwork` | 服务器            | 用于服务器注册规则。                                                                                                                                 |
| `resource.command`         | 服务器            | 本地 stdio 服务器命令，如 `npx` 或 `docker`（可用时）。远程服务器及不含命令细节的注册为空。                                                          |
| `resource.args`            | 服务器            | 本地 stdio 服务器参数（可用时）。这是一个集合，因此 `.contains()` 可匹配其中的值。无命令细节时为空。                                                 |

对字符串属性使用 `like`。在 Cedar 中，`like` 以 `*` 作为通配符，匹配整个字符串，将 `?` 视为字面字符，将 `\*` 视为字面星号。

仅对集合属性（如 `resource.args`）使用 `.contains()`。对字符串属性，使用 `like`。

### Server type values（服务器类型取值）

本地网关注册使用以下取值：

- `local-stdio`：主机运行的 stdio 服务器。包括显式命令以及使用 `--local` 从元数据解析的 OCI 打包 stdio 服务器。
- `container-stdio`：不带 `--local` 从元数据解析的 OCI 打包服务器。此取值可能出现在 `register` 决策中，但本地网关无法附加或运行此类服务器。
- `remote-dcr`：不需要 OAuth 或支持 OAuth 动态客户端注册（Dynamic Client Registration）的远程端点。
- `remote-no-dcr`：不支持动态客户端注册的远程 OAuth 端点。

### Server identity values（服务器身份取值）

对于远程服务器，`resource.identityURL` 是端点 URL。对于显式本地命令，它是主机上解析后的可执行文件路径。对于 `--local` 元数据注册，它是 `local://stdio/<name>`，而非注册表或清单（manifest）URL。

## Context fields（上下文字段）

| 字段                   | 说明                                                                                                                                        |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `context.request_time` | 为工具调用、内置网关工具调用、资源读取和提示检索绑定。注册请求不包含它。                                                                     |
| `context.args`         | 由网关评估的 `invokeTool` 和 `invokePrimordial` 请求的参数。当参数以 JSON 对象形式可用时存在。                                              |

以 `context.request_time` 为条件的注册 `permit` 不会匹配，因此该注册会落入默认拒绝。

使用 `context has args` 和字段检查来保护工具调用参数规则：

```plaintext
permit (principal, action == MCP::Action::"invokeTool", resource)
when {
  resource.name == "approve_expense" &&
  context has args &&
  context.args has amount &&
  context.args.amount <= 500
};
```

以缺失参数为门控的 `permit` 不会匹配，因此请求会落入默认拒绝。以缺失参数为门控的 `forbid` 不会匹配，因此它不会阻止请求。

`context.args` 中仅表示对象形式的工具参数。不受支持或格式错误的参数会被省略。

## Approval annotation（审批注解）

在 `permit` 语句上使用 `@requireApproval("reason")`，可要求在匹配请求运行之前，通过 MCP elicitation 进行会话内确认：

```plaintext
@requireApproval("write tool call")
permit (principal, action == MCP::Action::"invokeTool", resource)
when { resource.readOnly == false };
```

当某请求匹配带注解的 `permit` 且没有 `forbid` 覆盖它时，策略引擎返回“需要审批”的结果。注解字符串会作为 elicitation 的原因显示。“需要审批”的结果优先于普通 `permit`。匹配的 `forbid` 会在不进行 elicitation 的情况下拒绝请求。

有关请求流程和信任模型，参见 [Require confirmation with MCP elicitation](../access-controls/mcp.md#require-confirmation-with-mcp-elicitation)。

审批需要一个能够向用户呈现 MCP elicitation 请求的客户端会话。如果请求无法呈现以供审批，则该请求会被拒绝。审批是一种会话内确认，而非带外（out-of-band）审批工作流。每次确认对应一个授权请求。客户端确认后，网关会带着审批摘要（approval digest）重新评估该请求。

`sbx mcp add` 无法呈现 elicitation 请求。因此带有 `@requireApproval` 的注册 permit 会导致拒绝。

只有确切的注解名 `@requireApproval` 才会应用审批行为。其他注解名，如 `@requireConsent` 或 `@requireConfirmation`，不会要求审批。

## Limitations（限制）

- 工具与资源列表动作不受 Cedar 门控。列表中可能包含当沙箱尝试使用时被策略拒绝的条目。
- 当执行上下文无法将 MCP elicitation 转达给发起请求的客户端时，受审批门控的请求会被拒绝。这包括从 `code-mode` 内部发起的工具调用。
- 注册策略在服务器注册时评估。它本身不会移除现有注册，也不会停止已加载的服务器。请使用诸如 `invokeTool`、`readResource` 和 `getPrompt` 等使用时规则来治理现有注册。
- 使用 `resource.command` 或 `resource.args` 的服务器命令和参数规则，仅在解析后的服务器注册包含本地 stdio 命令细节时才生效。远程服务器和以元数据解析的本地服务器，这些属性可能为空值。使用 `resource.type == "local-stdio"` 可独立于命令细节匹配主机运行的服务器。
- 基于主体的规则不会生效。请使用组织和团队策略作用域来定位用户。
- MCP 策略不支持服务器组（server groups）。请单独引用各服务器。
