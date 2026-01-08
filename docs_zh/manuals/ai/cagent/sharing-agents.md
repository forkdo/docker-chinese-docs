---
title: 共享代理
description: 通过 OCI 仓库分发代理配置
keywords:
- cagent
- oci
- registry
- docker hub
- sharing
- distribution
weight: 50
---

将你的代理推送到仓库中，并通过名称共享。你的队友可以引用 `agentcatalog/security-expert`，而不需要到处复制 YAML 文件，也不需要询问你代理配置的位置。

当你在仓库中更新代理时，所有人在下次拉取或重启客户端时都会获得新版本。

## 前置条件

要将代理推送到仓库，首先需要认证：

```console
$ docker login
```

对于其他仓库，请使用其认证方法。

## 发布代理

将代理配置推送到仓库：

```console
$ cagent push ./agent.yml myusername/agent-name
```

如果仓库不存在，push 命令会自动创建。可以使用 Docker Hub 或任何兼容 OCI 的仓库。

为特定版本打标签：

```console
$ cagent push ./agent.yml myusername/agent-name:v1.0.0
$ cagent push ./agent.yml myusername/agent-name:latest
```

## 使用已发布的代理

拉取代理以在本地检查：

```console
$ cagent pull agentcatalog/pirate
```

这会将配置保存为本地 YAML 文件。

直接从仓库运行代理：

```console
$ cagent run agentcatalog/pirate
```

或者在集成中直接引用：

### 编辑器集成（ACP）

在 ACP 配置中使用仓库引用，确保你的编辑器始终使用最新版本：

```json
{
  "agent_servers": {
    "myagent": {
      "command": "cagent",
      "args": ["acp", "agentcatalog/pirate"]
    }
  }
}
```

### MCP 客户端集成

代理可以在 MCP 客户端中作为工具暴露：

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

## 后续步骤

- 使用共享代理设置 [ACP 集成](./integrations/acp.md)
- 使用共享代理配置 [MCP 集成](./integrations/mcp.md)
- 浏览 [代理目录](https://hub.docker.com/u/agentcatalog) 查看示例