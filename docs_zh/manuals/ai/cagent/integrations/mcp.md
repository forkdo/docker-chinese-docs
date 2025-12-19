---
title: MCP 模式
linkTitle: MCP
description: 将 cagent 代理作为工具暴露给 Claude Desktop 和 Claude Code 等 MCP 客户端
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

当您以 MCP 模式运行 cagent 时，您的代理会作为工具出现在 Claude Desktop
和其他 MCP 客户端中。您无需切换到终端来运行您的安全代理，而是直接要求
Claude 使用它，Claude 会为您调用它。

本指南涵盖 Claude Desktop 和 Claude Code 的设置。如果您希望代理嵌入到
您的编辑器中，请参阅 [ACP 集成](./acp.md)。

## 工作原理

您需要配置 Claude Desktop（或其他 MCP 客户端）以连接到 cagent。您的代理
会出现在 Claude 的工具列表中。当您要求 Claude 使用某个代理时，它会通过
MCP 协议调用该代理。

假设您配置了一个安全代理。在 Claude Desktop 中询问“使用安全代理审核此
身份验证代码”，Claude 就会调用它。代理使用其配置的工具（文件系统、Shell、
您赋予它的任何工具）运行，然后将结果返回给 Claude。

如果您的配置中有多个代理，每个代理都会成为一个独立的工具。一个包含
`root`、`designer` 和 `engineer` 代理的配置会为 Claude 提供三个工具
供其选择。Claude 可能会直接调用 engineer，或者使用 root 协调器——这
取决于您的代理描述和您的请求内容。

## MCP 网关

Docker 提供了一个 [MCP 网关](/ai/mcp-catalog-and-toolkit/mcp-gateway/)，
它使 cagent 代理能够访问一系列预配置的 MCP 服务器。代理无需单独配置
MCP 服务器，即可通过网关访问网络搜索、数据库查询等工具。

使用网关引用配置 MCP 工具集：

```yaml
agents:
  root:
    toolsets:
      - type: mcp
        ref: docker:duckduckgo # 使用 Docker MCP 网关
```

`docker:` 前缀告诉 cagent 对此服务器使用 MCP 网关。有关可用服务器和
配置选项，请参阅 [MCP 网关文档](/ai/mcp-catalog-and-toolkit/mcp-gateway/)。

您还可以使用 [MCP 工具包](/ai/mcp-catalog-and-toolkit/) 以交互方式
探索和管理 MCP 服务器。

## 先决条件

在配置 MCP 集成之前，您需要：

- **已安装 cagent** - 参见 [安装指南](../_index.md#installation)
- **代理配置** - 定义代理的 YAML 文件。参见 [教程](../tutorial.md) 或
  [示例配置](https://github.com/docker/cagent/tree/main/examples)
- **MCP 客户端** - Claude Desktop、Claude Code 或其他兼容 MCP 的应用程序
- **API 密钥** - 您的代理使用的任何模型提供商的环境变量
  (`ANTHROPIC_API_KEY`、`OPENAI_API_KEY` 等)

## MCP 客户端配置

您的 MCP 客户端需要知道如何启动 cagent 并与之通信。这通常涉及将 cagent
作为 MCP 服务器添加到客户端的配置中。

### Claude Desktop

将 cagent 添加到您的 Claude Desktop MCP 设置文件中：

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

配置示例：

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

配置详解：

- `command`: `cagent` 二进制文件的完整路径（使用 `which cagent` 查找）
- `args`: MCP 命令参数：
  - `mcp`: 以 MCP 模式运行 cagent 的子命令
  - `dockereng/myagent`: 您的代理配置（本地文件路径或 OCI 引用）
  - `--working-dir`: 代理执行的可选工作目录
- `env`: 您的代理所需的环境变量：
  - 模型提供商 API 密钥 (`ANTHROPIC_API_KEY`、`OPENAI_API_KEY` 等)
  - 您的代理引用的任何其他环境变量

更新配置后，重启 Claude Desktop。您的代理将作为可用工具出现。

### Claude Code

使用 `claude mcp add` 命令将 cagent 添加为 MCP 服务器：

```console
$ claude mcp add --transport stdio myagent \
  --env OPENAI_API_KEY=$OPENAI_API_KEY \
  --env ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -- cagent mcp /path/to/agent.yml --working-dir $(pwd)
```

命令详解：

- `claude mcp add`: 在 Claude Code 中注册 MCP 服务器的命令
- `--transport stdio`: 使用 stdio 传输（本地 MCP 服务器的标准方式）
- `myagent`: 此 MCP 服务器在 Claude Code 中的名称
- `--env`: 传递环境变量（每个变量重复一次）
- `--`: 将 Claude Code 选项与 MCP 服务器命令分开
- `cagent mcp /path/to/agent.yml`: 带有代理配置路径的 cagent MCP 命令
- `--working-dir $(pwd)`: 设置代理执行的工作目录

添加服务器后，您的代理将在 Claude Code 会话中作为工具可用。

### 其他 MCP 客户端

对于其他兼容 MCP 的客户端，您需要：

1. 使用 `cagent mcp /path/to/agent.yml --working-dir /project/path` 启动 cagent
2. 配置客户端以通过 stdio 与 cagent 通信
3. 传递所需的环境变量（API 密钥等）

请查阅您的 MCP 客户端文档以获取具体的配置步骤。

## 代理引用

您可以将代理配置指定为本地文件路径或 OCI 注册表引用：

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

注册表引用让您的团队可以使用相同的代理配置，而无需管理本地文件。详情
请参阅 [共享代理](../sharing-agents.md)。

## 为 MCP 设计代理

MCP 客户端将您的每个代理视为一个单独的工具，并且可以直接调用其中
任何一个。这改变了您在使用 `cagent run` 运行代理时应如何考虑代理设计。

### 编写优秀的描述

`description` 字段告诉 MCP 客户端代理的作用。这是客户端决定何时调用
它的依据。“分析代码中的安全漏洞和合规性问题”是具体的。“一个有用的
安全代理”则没有说明它实际做什么。

```yaml
agents:
  security_auditor:
    description: 分析代码中的安全漏洞和合规性问题
    # 不要写: "一个有用的安全代理"
```

### MCP 客户端直接调用代理

MCP 客户端可以调用您的任何代理，而不仅仅是 root。如果您有 `root`、
`designer` 和 `engineer` 代理，客户端可能会直接调用 engineer，而不是
通过 root。设计每个代理使其能够独立工作：

```yaml
agents:
  engineer:
    description: 实现功能并编写生产代码
    instruction: |
      您根据提供的需求实现代码。
      您可以独立工作，无需协调器。
    toolsets:
      - type: filesystem
      - type: shell
```

如果一个代理需要其他代理才能正常工作，请在描述中说明：“协调设计和工程
代理以实现完整的功能。”

### 单独测试每个代理

MCP 客户端单独调用代理，因此请以这种方式测试它们：

```console
$ cagent run agent.yml --agent engineer
```

确保代理在不经过 root 的情况下也能工作。检查它是否拥有正确的工具，
以及当它被直接调用时，它的指令是否合理。

## 测试您的设置

验证您的 MCP 集成是否有效：

1. 配置更改后重启您的 MCP 客户端
2. 检查 cagent 代理是否作为可用工具出现
3. 使用简单的测试提示调用代理
4. 验证代理是否可以访问其配置的工具（文件系统、Shell 等）

如果代理未出现或执行失败，请检查：

- `cagent` 二进制路径是否正确且可执行
- 代理配置文件是否存在且有效
- 所有必需的 API 密钥都已在环境变量中设置
- 工作目录路径存在且具有适当的权限
- MCP 客户端日志中是否存在连接或执行错误

## 常见工作流程

### 调用专家代理

您有一个了解您的合规规则和常见漏洞的安全代理。在 Claude Desktop 中，
粘贴一些身份验证代码并询问“使用安全代理审查此代码”。代理检查代码并
报告其发现。您始终停留在 Claude 的界面中。

### 与代理团队协作

您的配置中有一个协调器，负责将工作委派给 designer 和 engineer 代理。
在 Claude Code 中询问“使用协调器实现登录表单”，协调器会将 UI 工作
交给 designer，将代码工作交给 engineer。您无需自己运行 `cagent run`
即可获得完整的实现。

### 运行特定领域的工具

您构建了一个包含自定义部署脚本和监控查询的基础设施代理。在任何 MCP
客户端中询问“使用基础设施代理检查生产状态”，它就会运行您的工具并
返回结果。您的部署知识现在可以在您使用 MCP 客户端的任何地方使用。

### 共享代理

您的团队将代理保存在 OCI 注册表中。每个人都在其 MCP 客户端配置中添加
`agentcatalog/security-expert`。当您更新代理时，他们会在下次重启时获得
新版本。无需传递 YAML 文件。

## 下一步

- 使用 [MCP 网关](/ai/mcp-catalog-and-toolkit/mcp-gateway/) 为您的代理
  提供对预配置 MCP 服务器的访问权限
- 使用 [MCP 工具包](/ai/mcp-catalog-and-toolkit/) 以交互方式探索 MCP 服务器
- 查阅 [配置参考](../reference/config.md) 以获取高级代理设置
- 探索 [工具集参考](../reference/toolsets.md) 以了解代理可以使用的工具
- 为您的代理添加 [用于代码库搜索的 RAG](../rag.md)
- 查看 [CLI 参考](../reference/cli.md) 了解所有 `cagent mcp` 选项
- 浏览 [示例配置](https://github.com/docker/cagent/tree/main/examples) 以了解
  不同类型的代理