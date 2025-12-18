---
title: MCP 模式
linkTitle: MCP
description: 将 cagent 代理作为工具暴露给 MCP 客户端，如 Claude Desktop 和 Claude Code
keywords:
  [
    cagent,
    mcp,
    model context protocol,
    claude desktop,
    claude code,
    integration,
  ]
weight: 50
---

当你以 MCP 模式运行 cagent 时，你的代理会作为工具出现在 Claude Desktop 和其他 MCP 客户端中。你不再需要切换到终端来运行安全代理，而是让 Claude 调用它，Claude 会通过 MCP 协议为你执行。

本指南涵盖 Claude Desktop 和 Claude Code 的设置。如果你想在编辑器中嵌入代理，请参阅 [ACP 集成](./acp.md)。

## 工作原理

你配置 Claude Desktop（或其他 MCP 客户端）连接到 cagent。你的代理会出现在 Claude 的工具列表中。当你要求 Claude 使用其中一个时，它会通过 MCP 协议调用该代理。

假设你配置了一个安全代理。询问 Claude Desktop “使用安全代理审计这段身份验证代码”，Claude 会调用它。代理会使用其配置的工具（文件系统、shell 等）运行，然后将结果返回给 Claude。

如果你的配置中有多个代理，每个代理都会成为独立的工具。一个包含 `root`、`designer` 和 `engineer` 代理的配置会为 Claude 提供三个可选工具。Claude 可能直接调用工程师，也可能使用根协调器——这取决于你的代理描述和你的请求。

## MCP 网关

Docker 提供了一个 [MCP 网关](/ai/mcp-catalog-and-toolkit/mcp-gateway/)，让 cagent 代理能够访问预配置的 MCP 服务器目录。你无需配置单独的 MCP 服务器，代理可以使用网关访问网络搜索、数据库查询等工具。

使用网关引用配置 MCP 工具集：

```yaml
agents:
  root:
    toolsets:
      - type: mcp
        ref: docker:duckduckgo # 使用 Docker MCP 网关
```

`docker:` 前缀告诉 cagent 对此服务器使用 MCP 网关。请参阅 [MCP 网关文档](/ai/mcp-catalog-and-toolkit/mcp-gateway/)了解可用服务器和配置选项。

你也可以使用 [MCP 工具包](/ai/mcp-catalog-and-toolkit/) 交互式地探索和管理 MCP 服务器。

## 先决条件

在配置 MCP 集成之前，你需要：

- **已安装 cagent** - 参见 [安装指南](../_index.md#installation)
- **代理配置** - 定义代理的 YAML 文件。参见 [教程](../tutorial.md) 或 [示例配置](https://github.com/docker/cagent/tree/main/examples)
- **MCP 客户端** - Claude Desktop、Claude Code 或其他兼容 MCP 的应用程序
- **API 密钥** - 你的代理使用的模型提供商的环境变量（`ANTHROPIC_API_KEY`、`OPENAI_API_KEY` 等）

## MCP 客户端配置

你的 MCP 客户端需要知道如何启动 cagent 并与之通信。这通常涉及在客户端配置中将 cagent 添加为 MCP 服务器。

### Claude Desktop

将 cagent 添加到你的 Claude Desktop MCP 设置文件中：

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

示例配置：

```json
{
  "mcpServers": {
    "myagent": {
      "command": "/usr/local/bin/cagent",
      "args": [
        "mcp",
        "/path/to/agent.yml",
        "--working-dir",
        "/Users/yourname/projects"
      ],
      "env": {
        "ANTHROPIC_API_KEY": "your_anthropic_key_here",
        "OPENAI_API_KEY": "your_openai_key_here"
      }
    }
  }
}
```

配置说明：

- `command`: 你的 `cagent` 二进制文件的完整路径（使用 `which cagent` 查找）
- `args`: MCP 命令参数：
  - `mcp`: 以 MCP 模式运行 cagent 的子命令
  - `dockereng/myagent`: 你的代理配置（本地文件路径或 OCI 引用）
  - `--working-dir`: 代理执行的可选工作目录
- `env`: 你的代理需要的环境变量：
  - 模型提供商的 API 密钥（`ANTHROPIC_API_KEY`、`OPENAI_API_KEY` 等）
  - 你的代理引用的任何其他环境变量

更新配置后，重启 Claude Desktop。你的代理会作为可用工具出现。

### Claude Code

使用 `claude mcp add` 命令将 cagent 添加为 MCP 服务器：

```console
$ claude mcp add --transport stdio myagent \
  --env OPENAI_API_KEY=$OPENAI_API_KEY \
  --env ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -- cagent mcp /path/to/agent.yml --working-dir $(pwd)
```

命令说明：

- `claude mcp add`: Claude Code 注册 MCP 服务器的命令
- `--transport stdio`: 使用 stdio 传输（本地 MCP 服务器的标准）
- `myagent`: Claude Code 中此 MCP 服务器的名称
- `--env`: 传递环境变量（每个变量重复一次）
- `--`: 将 Claude Code 选项与 MCP 服务器命令分隔开
- `cagent mcp /path/to/agent.yml`: 带有代理配置路径的 cagent MCP 命令
- `--working-dir $(pwd)`: 设置代理执行的工作目录

添加服务器后，你的代理会在 Claude Code 会话中作为工具可用。

### 其他 MCP 客户端

对于其他兼容 MCP 的客户端，你需要：

1. 使用 `cagent mcp /path/to/agent.yml --working-dir /project/path` 启动 cagent
2. 配置客户端通过 stdio 与 cagent 通信
3. 传递所需的环境变量（API 密钥等）

请查阅你的 MCP 客户端文档了解具体的配置步骤。

## 代理引用

你可以将代理配置指定为本地文件路径或 OCI 注册表引用：

```console
# 本地文件路径
$ cagent mcp ./agent.yml

# OCI 注册表引用
$ cagent mcp agentcatalog/pirate
$ cagent mcp dockereng/myagent:v1.0.0
```

在 MCP 客户端配置中使用相同的语法：

```json
{
  "mcpServers": {
    "myagent": {
      "command": "/usr/local/bin/cagent",
      "args": ["mcp", "agentcatalog/pirate"]
    }
  }
}
```

注册表引用让你的团队可以使用相同的代理配置，而无需管理本地文件。详情请参阅 [共享代理](../sharing-agents.md)。

## 为 MCP 设计代理

MCP 客户端将你的每个代理视为独立工具，并可以直接调用其中任何一个。这改变了你对代理设计的思考方式，与使用 `cagent run` 运行代理相比有所不同。

### 编写好的描述

`description` 字段告诉 MCP 客户端代理的功能。这是客户端决定何时调用它的依据。“分析代码中的安全漏洞和合规问题”是具体的描述。“一个有用的安全代理”则没有说明实际功能。

```yaml
agents:
  security_auditor:
    description: Analyzes code for security vulnerabilities and compliance issues
    # 不要写: "A helpful security agent"
```

### MCP 客户端直接调用代理

MCP 客户端可以直接调用你的任何代理，而不仅仅是 root。如果你有 `root`、`designer` 和 `engineer` 代理，客户端可能直接调用工程师而不是通过 root。设计每个代理使其能够独立工作：

```yaml
agents:
  engineer:
    description: Implements features and writes production code
    instruction: |
      You implement code based on requirements provided.
      You can work independently without a coordinator.
    toolsets:
      - type: filesystem
      - type: shell
```

如果一个代理需要其他代理才能正常工作，请在描述中说明：“协调设计和工程代理以实现完整功能。”

### 单独测试每个代理

MCP 客户端单独调用代理，因此请单独测试它们：

```console
$ cagent run agent.yml --agent engineer
```

确保代理在不通过 root 的情况下也能工作。检查它是否具有正确的工具，以及其指令在直接调用时是否有意义。

## 测试你的设置

验证你的 MCP 集成是否正常工作：

1. 配置更改后重启你的 MCP 客户端
2. 检查 cagent 代理是否作为可用工具出现
3. 使用简单测试提示调用一个代理
4. 验证代理是否能够访问其配置的工具（文件系统、shell 等）

如果代理未出现或执行失败，请检查：

- `cagent` 二进制文件路径是否正确且可执行
- 代理配置文件是否存在且有效
- 所有必需的 API 密钥是否在环境变量中设置
- 工作目录路径是否存在且具有适当的权限
- MCP 客户端日志中是否有连接或执行错误

## 常见工作流

### 调用专业代理

你有一个了解合规规则和常见漏洞的安全代理。在 Claude Desktop 中粘贴一些身份验证代码，询问“使用安全代理审查这个”。代理检查代码并报告发现的问题。你全程都停留在 Claude 界面中。

### 与代理团队协作

你的配置有一个协调器，它将任务委托给设计师和工程师代理。询问 Claude Code “使用协调器实现登录表单”，协调器会将 UI 工作交给设计师，将代码交给工程师。你无需自己运行 `cagent run` 就能获得完整的实现。

### 使用特定领域的工具

你构建了一个基础设施代理，带有自定义部署脚本和监控查询。询问任何 MCP 客户端“使用基础设施代理检查生产状态”，它会运行你的工具并返回结果。你的部署知识现在在你使用 MCP 客户端的任何地方都可用。

### 共享代理

你的团队将代理保存在 OCI 注册表中。每个人在他们的 MCP 客户端配置中添加 `agentcatalog/security-expert`。当你更新代理时，他们在下次重启时获得新版本。无需传递 YAML 文件。

## 下一步

- 使用 [MCP 网关](/ai/mcp-catalog-and-toolkit/mcp-gateway/) 为你的代理提供对预配置 MCP 服务器的访问
- 使用 [MCP 工具包](/ai/mcp-catalog-and-toolkit/) 交互式地探索 MCP 服务器
- 查看 [配置参考](../reference/config.md) 了解高级代理设置
- 探索 [工具集参考](../reference/toolsets.md) 了解代理可以使用的工具
- 为你的代理添加 [用于代码库搜索的 RAG](../rag.md)
- 查看 [CLI 参考](../reference/cli.md) 了解所有 `cagent mcp` 选项
- 浏览 [示例配置](https://github.com/docker/cagent/tree/main/examples) 了解不同类型的代理