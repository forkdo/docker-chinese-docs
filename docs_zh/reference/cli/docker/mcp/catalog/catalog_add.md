---
datafolder: mcp-cli
datafile: docker_mcp_catalog_add
title: docker mcp catalog add
layout: cli
---

<!--
此页面由 Docker 的源代码自动生成。如果您想
建议更改此处显示的文本，请在 GitHub 上的
源代码仓库中提出工单或拉取请求：

https://github.com/docker/mcp-gateway
-->```markdown
# docker mcp catalog add

```text
docker mcp catalog add [OPTIONS] [NAME] [ADDRESS]
```

<!-- MARKDOWN CODE BLOCK: info -->

<!-- MARKDOWN CODE BLOCK: options -->

**Options**

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `--description` | `string` |  | 服务器的描述 |
| `--header` | `stringArray` |  | 发送到服务器的请求头（格式：key=value） |
| `--type` | `string` | `sse` | 服务器类型（sse 或 stdio） |

## Description

将 MCP 服务器添加到本地目录。

此命令将 MCP 服务器注册到本地目录中，使其可用于 MCP 客户端。服务器可以通过 SSE（服务器发送事件）或 STDIO（标准输入输出）协议进行通信。

## Examples

### 添加 SSE 服务器

```bash
docker mcp catalog add my-server http://localhost:8000/sse
```

### 添加带描述的服务器

```bash
docker mcp catalog add my-server http://localhost:8000/sse --description "My custom MCP server"
```

### 添加带自定义请求头的服务器

```bash
docker mcp catalog add my-server http://localhost:8000/sse --header "Authorization=Bearer token123"
```

### 添加 STDIO 服务器

```bash
docker mcp catalog add my-server "npx -y @modelcontextprotocol/server-filesystem /tmp"
```

### 添加带多个请求头的服务器

```bash
docker mcp catalog add my-server http://localhost:8000/sse \
  --header "Authorization=Bearer token123" \
  --header "X-Custom-Header=value"
```

## See Also

* [docker mcp catalog](docker_mcp_catalog.md) - 管理 MCP 服务器目录
* [docker mcp catalog list](docker_mcp_catalog_list.md) - 列出目录中的服务器
* [docker mcp catalog remove](docker_mcp_catalog_remove.md) - 从目录中移除服务器
```