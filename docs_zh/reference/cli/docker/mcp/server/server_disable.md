---
datafolder: mcp-cli
datafile: docker_mcp_server_disable
title: docker mcp server disable
layout: cli
---

<!--
此页面由 Docker 的源代码自动生成。如果您想
建议更改此处显示的文本，请在 GitHub 上的
源代码仓库中提交工单或拉取请求：

https://github.com/docker/mcp-gateway
-->

# docker mcp server disable

```bash
docker mcp server disable [OPTIONS] SERVER
```

<!-- MARKDOWN CODE BLOCK: info -->

<!-- MARKDOWN CODE BLOCK: options -->

<!-- MARKDOWN CODE BLOCK: examples -->

<!-- MARKDOWN CODE BLOCK: inherited -->

<!-- MARKDOWN CODE BLOCK: see also -->

**说明：**

此命令用于禁用已注册的 MCP 服务器。服务器被禁用后，将不再可用于处理工具调用或提示，但其注册信息仍会保留在注册表中，以便将来重新启用。

**示例：**

```bash
# 禁用名为 "my-server" 的服务器
docker mcp server disable my-server

# 禁用服务器并查看状态变更
docker mcp server disable my-server
docker mcp server list
```

**相关命令：**

| 命令 | 描述 |
|------|------|
| `docker mcp server enable` | 启用已禁用的服务器 |
| `docker mcp server list` | 列出所有服务器及其状态 |
| `docker mcp server remove` | 从注册表中移除服务器 |

**使用说明：**

- 此命令需要有效的服务器名称作为参数
- 被禁用的服务器不会从系统中删除
- 可以随时使用 `enable` 命令重新启用服务器
- 禁用操作是即时生效的，无需重启服务