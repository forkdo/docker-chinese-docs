---
datafolder: mcp-cli
datafile: docker_mcp_tools_inspect
title: docker mcp tools inspect
layout: cli
---

<!--
此页面是从 Docker 的源代码自动生成的。如果您想
建议更改此处显示的文本，请在 GitHub 上的源代码仓库中
提交工单或拉取请求：

https://github.com/docker/mcp-gateway
--></think>---
datafolder: mcp-cli
datafile: docker_mcp_tools_inspect
title: docker mcp tools inspect
layout: cli
---

<!--
此页面是从 Docker 的源代码自动生成的。如果您想
建议更改此处显示的文本，请在 GitHub 上的源代码仓库中
提交工单或拉取请求：

https://github.com/docker/mcp-gateway
--></think>```markdown
# docker mcp tools inspect

```text
docker mcp tools inspect [OPTIONS] TOOL_NAME
```

检查 MCP 工具

## 选项

| 名称 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `--format` | `string` | `pretty` | 格式化输出 (pretty, json, jsonraw) |
| `--help` | `bool` | `false` | 显示帮助信息 |

## 示例

### 查看工具详情
```bash
docker mcp tools inspect my-tool
```

### 以 JSON 格式查看工具详情
```bash
docker mcp tools inspect --format json my-tool
```

### 查看原始 JSON 数据
```bash
docker mcp tools inspect --format jsonraw my-tool
```