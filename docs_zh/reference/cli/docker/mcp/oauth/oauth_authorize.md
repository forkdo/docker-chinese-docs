```markdown
---
datafolder: mcp-cli
datafile: docker_mcp_oauth_authorize
title: docker mcp oauth authorize
layout: cli
---

<!--
此页面由 Docker 的源代码自动生成。如果您想
建议更改此处显示的文本，请在 GitHub 的
源代码仓库中提交工单或拉取请求：

https://github.com/docker/mcp-gateway
-->
```

```markdown
# docker mcp oauth authorize

## 说明

为 Docker MCP Gateway 中的客户端授权 OAuth 令牌。

## 使用方法

```shell
docker mcp oauth authorize [OPTIONS] [CLIENT_ID]
```

## 选项

| 选项 | 长选项 | 说明 |
|------|--------|------|
| `-h` | `--help` | 显示帮助信息并退出 |
| `-s` | `--scope <scope>` | 要请求的 OAuth 作用域（可多次指定） |
| `-t` | `--token <token>` | 用于授权的现有访问令牌 |
| `-u` | `--url <url>` | OAuth 授权服务器的 URL |

## 参数

| 参数 | 说明 |
|------|------|
| `[CLIENT_ID]` | OAuth 客户端 ID（如果未提供，则使用 Docker ID） |

## 示例

为默认客户端授权令牌：

```shell
docker mcp oauth authorize
```

为特定客户端 ID 授权令牌：

```shell
docker mcp oauth authorize my-client-id
```

使用特定作用域授权令牌：

```shell
docker mcp oauth authorize --scope read --scope write my-client-id
```

使用现有令牌进行授权：

```shell
docker mcp oauth authorize --token my-existing-token my-client-id
```

指定自定义 OAuth 服务器：

```shell
docker mcp oauth authorize --url https://auth.example.com my-client-id
```

## 另请参阅

* [docker mcp oauth](./docker_mcp_oauth.md)
* [docker mcp](./docker_mcp.md)
```