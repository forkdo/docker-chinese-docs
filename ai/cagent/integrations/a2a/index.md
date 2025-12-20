# A2A 模式

A2A 模式将您的 cagent 代理作为 HTTP 服务器运行，其他系统可以通过 Agent-to-Agent 协议调用该服务器。这使您可以将代理作为服务暴露，其他代理或应用程序可以在网络上发现并调用该服务。

当您希望其他系统通过 HTTP 调用您的代理时，请使用 A2A。有关编辑器集成，请参阅 [ACP 集成](./acp.md)。有关在 MCP 客户端中将代理用作工具，请参阅 [MCP 集成](./mcp.md)。

## 先决条件

在启动 A2A 服务器之前，您需要：

- 已安装 cagent - 参见 [安装指南](../_index.md#installation)
- 代理配置 - 定义您的代理的 YAML 文件。参见 [教程](../tutorial.md)
- 已配置 API 密钥 - 如果使用云模型提供商（参见 [模型提供商](../model-providers.md)）

## 启动 A2A 服务器

基本用法：

```console
$ cagent a2a ./agent.yaml
```

您的代理现在可以通过 HTTP 访问。其他 A2A 系统可以发现您的代理的功能并调用它。

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

当您启动 A2A 服务器时，它会暴露两个 HTTP 端点：

### 代理卡片：`/.well-known/agent-card`

代理卡片描述了您的代理的功能：

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

通过发送 JSON-RPC 请求来调用您的代理：

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

响应包括代理的回复：

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

以下是一个 A2A 有用的具体场景。您有两个代理：

1. 与用户交互的通用代理
2. 具有代码库访问权限的专用代码审查代理

将专用代理作为 A2A 服务器运行：

```console
$ cagent a2a ./code-reviewer.yaml --port 8080
Listening on 127.0.0.1:8080
```

配置您的主代理以调用它：

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

现在，当用户向主代理询问代码质量时，它可以委托给专用代理。主代理将 `code-reviewer` 视为可以调用的工具，而专用代理可以访问它需要的代码库工具。

## 调用其他 A2A 代理

您的 cagent 代理可以将远程 A2A 代理作为工具调用。使用远程代理的 URL 配置 A2A 工具集：

```yaml
agents:
  root:
    toolsets:
      - type: a2a
        url: http://localhost:8080
        name: specialist
```

`url` 指定远程代理运行的位置，`name` 是工具的可选标识符。您的代理现在可以将任务委托给远程专用代理。

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

- 查看所有 `cagent a2a` 选项的 [CLI 参考](../reference/cli.md#a2a)
- 了解 [MCP 模式](./mcp.md) 以在 MCP 客户端中将代理作为工具暴露
- 了解 [ACP 模式](./acp.md) 用于编辑器集成
- 使用 [OCI 注册表](../sharing-agents.md) 共享您的代理
