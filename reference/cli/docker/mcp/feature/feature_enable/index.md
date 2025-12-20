# docker mcp feature enable

<!--
此页面内容自动从 Docker 的源代码生成。如果您想建议修改此处显示的文本，请在 GitHub 上的源代码仓库中提交工单或拉取请求：

https://github.com/docker/mcp-gateway
-->

# docker mcp feature enable

<!-- MARKDOWN-ANCHOR: docker mcp feature enable -->
```
docker mcp feature enable [OPTIONS] FEATURE
```

启用指定的 MCP 功能。

### 选项

<!-- MARKDOWN-ANCHOR: Options -->
| 名称 | 简写 | 默认值 | 描述 |
|------|------|--------|------|
| `--format` | | `pretty` | 格式化输出<br>支持的值：`pretty`、`json`、`jsona` |
| `--help` | `-h` | | 显示帮助信息 |

### 描述

启用指定的 MCP 功能。

### 示例

<!-- MARKDOWN-ANCHOR: Examples -->
```bash
# 启用 docker.mcp 功能
docker mcp feature enable docker.mcp

# 以 JSON 格式输出
docker mcp feature enable docker.mcp --format json
```
