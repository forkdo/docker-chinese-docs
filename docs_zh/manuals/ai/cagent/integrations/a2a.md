---
title: A2A 模式
linkTitle: A2A
description: 通过 Agent-to-Agent 协议暴露 cagent 代理
keywords: [cagent, a2a, agent-to-agent, multi-agent, protocol]
weight: 40
---

A2A 模式将你的 cagent 代理作为 HTTP 服务器运行，其他系统可以使用 Agent-to-Agent 协议调用它。这让你可以将代理暴露为服务，其他代理或应用程序可以通过网络发现并调用它。

当你希望通过 HTTP 让其他系统调用你的代理时，请使用 A2A。如需编辑器集成，请参阅 [ACP 集成](./acp.md)。如需在 MCP 客户端中将代理用作工具，请参阅 [MCP 集成](./mcp.md)。

## 前置条件

在启动 A2A 服务器之前，你需要：

- 已安装 cagent - 参见 [安装指南](../_index.md#installation)
- 代理配置 - 定义你的代理的 YAML 文件。参见 [教程](../tutorial.md)
- 已配置 API 密钥 - 如果使用云模型提供商（参见 [模型提供商](../model-providers.md)）

## 启动 A2A 服务器

基本用法：

```console
$ cagent a2a ./agent.yaml
```

你的代理现在可以通过 HTTP 访问。其他 A2A 系统可以发现你的代理功能并调用它。

自定义端口：

```console
$ cagent a2a ./agent.yaml --port 8080
```

团队中的特定代理：

```console
$ cagent a2a ./agent.yaml --agent engineer
```

从 OCI 注册表：

```console
$ cagent a2a agentcatalog/pirate --port 9000
```

## HTTP 端点

启动 A2A 服务器时，它会暴露两个 HTTP 端点：

### 代理卡片：`/.well-known/agent-card`

代理卡片描述你的代理功能：

```console
$ curl http://localhost:8080/.well-known/agent-card
```

```json
{
  "name": "agent",
  "description": "A helpful coding assistant",
  "skills": [
    {
      "id": "agent_root",
      "name": "root",
      "description": "A helpful coding assistant",
      "tags": ["llm", "cagent"]
    }
  ],
  "preferredTransport": "jsonrpc",
  "url": "http://localhost:8080/invoke",
  "capabilities": {
    "streaming": true
  },
  "version": "0.1.0"
}
```

### 调用端点：`/invoke`

通过发送 JSON-RPC 请求调用你的代理：

```console
$ curl -X POST http://localhost:8080/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "req-1",
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [
          {
            "kind": "text",
            "text": "What is 2+2?"
          }
        ]
      }
    }
  }'
```

响应包含代理的回复：

```json
{
  "jsonrpc": "2.0",
  "id": "req-1",
  "result": {
    "artifacts": [
      {
        "parts": [
          {
            "kind": "text",
            "text": "2+2 equals 4."
          }
        ]
      }
    ]
  }
}
```

## 示例：多代理工作流

这是一个 A2A 有用的场景示例。你有两个代理：

1. 一个与用户交互的通用代理
2. 一个具有代码库访问权限的专用代码审查代理

将专家代理作为 A2A 服务器运行：

```console
$ cagent a2a ./code-reviewer.yaml --port 8080
Listening on 127.0.0.1:8080
```

配置你的主代理调用它：

```yaml
agents:
  root:
    model: anthropic/claude-sonnet-4-5
    instruction: You are a helpful assistant
    toolsets:
      - type: a2a
        url: http://localhost:8080
        name: code-reviewer
```

现在当用户询问主代理关于代码质量的问题时，它可以委托给专家。主代理将 `code-reviewer` 视为可以调用的工具，而专家代理可以访问它需要的代码库工具。

## 调用其他 A2A 代理

你的 cagent 代理可以将远程 A2A 代理作为工具调用。使用远程代理的 URL 配置 A2A 工具集：

```yaml
agents:
  root:
    toolsets:
      - type: a2a
        url: http://localhost:8080
        name: specialist
```

`url` 指定远程代理运行的位置，`name` 是工具的可选标识符。你的代理现在可以将任务委托给远程专家代理。

如果远程代理需要身份验证或自定义标头：

```yaml
agents:
  root:
    toolsets:
      - type: a2a
        url: http://localhost:8080
        name: specialist
        remote:
          headers:
            Authorization: Bearer token123
            X-Custom-Header: value
```

## 下一步

- 查看 [CLI 参考](../reference/cli.md#a2a) 了解所有 `cagent a2a` 选项
- 了解 [MCP 模式](./mcp.md) 以在 MCP 客户端中将代理暴露为工具
- 了解 [ACP 模式](./acp.md) 以进行编辑器集成
- 通过 [OCI 注册表](../sharing-agents.md) 分享你的代理