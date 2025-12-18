---
title: CLI 参考
linkTitle: CLI
description: cagent 命令行接口的完整参考
keywords: [ai, agent, cagent, cli, command line]
weight: 30
---

用于运行、管理和部署 AI 代理的命令行接口。

关于代理配置文件语法，请参见 [配置文件参考](./config.md)。关于工具集功能，请参见 [工具集参考](./toolsets.md)。

## 概述

```console
$ cagent [command] [flags]
```

## 全局标志

适用于所有命令：

| 标志            | 类型    | 默认值 | 描述          |
| --------------- | ------- | ------- | -------------------- |
| `-d`, `--debug` | boolean | false   | 启用调试日志 |
| `-o`, `--otel`  | boolean | false   | 启用 OpenTelemetry |
| `--log-file`    | string  | -       | 调试日志文件路径  |

调试日志默认写入 `~/.cagent/cagent.debug.log`。可通过 `--log-file` 覆盖。

## 运行时标志

适用于大多数命令。支持的命令会链接到此部分。

| 标志                | 类型    | 默认值 | 描述                          |
| ------------------- | ------- | ------- | ------------------------------------ |
| `--models-gateway`  | string  | -       | 模型网关地址               |
| `--env-from-file`   | array   | -       | 从文件加载环境变量 |
| `--code-mode-tools` | boolean | false   | 启用 JavaScript 工具编排 |
| `--working-dir`     | string  | -       | 会话工作目录    |

通过 `CAGENT_MODELS_GATEWAY` 环境变量设置 `--models-gateway`。

## 命令

### a2a

通过 Agent2Agent (A2A) 协议暴露代理。允许其他兼容 A2A 的系统发现并与您的代理交互。如果未指定，自动选择可用端口。

```console
$ cagent a2a agent-file|registry-ref
```

> [!NOTE]
> A2A 支持目前处于实验阶段，需要进一步完善。工具调用在内部处理，不会作为单独的 ADK 事件暴露。某些 ADK 功能尚未集成。

参数：

- `agent-file|registry-ref` - YAML 路径或 OCI 注册表引用（必需）

标志：

| 标志            | 类型    | 默认值 | 描述       |
| --------------- | ------- | ------- | ----------------- |
| `-a`, `--agent` | string  | root    | 代理名称        |
| `--port`        | integer | 0       | 端口（0 = 随机） |

支持 [运行时标志](#runtime-flags)。

示例：

```console
$ cagent a2a ./agent.yaml --port 8080
$ cagent a2a agentcatalog/pirate --port 9000
```

### acp

在 stdio 上以 ACP (Agent Client Protocol) 服务器启动代理，用于编辑器集成。设置指南请参见 [ACP 集成](../integrations/acp.md)。

```console
$ cagent acp agent-file|registry-ref
```

参数：

- `agent-file|registry-ref` - YAML 路径或 OCI 注册表引用（必需）

支持 [运行时标志](#runtime-flags)。

### alias add

为代理创建别名。

```console
$ cagent alias add name target
```

参数：

- `name` - 别名（必需）
- `target` - YAML 路径或注册表引用（必需）

示例：

```console
$ cagent alias add dev ./dev-agent.yaml
$ cagent alias add prod docker.io/user/prod-agent:latest
$ cagent alias add default ./agent.yaml
```

将别名设置为 "default" 后，即可直接运行 `cagent run` 而无需参数。

### alias list

列出所有别名。

```console
$ cagent alias list
$ cagent alias ls
```

### alias remove

移除别名。

```console
$ cagent alias remove name
$ cagent alias rm name
```

参数：

- `name` - 别名（必需）

### api

HTTP API 服务器。

```console
$ cagent api agent-file|agents-dir
```

参数：

- `agent-file|agents-dir` - YAML 路径或包含代理的目录（必需）

标志：

| 标志                 | 类型    | 默认值    | 描述                       |
| -------------------- | ------- | ---------- | --------------------------------- |
| `-l`, `--listen`     | string  | :8080      | 监听地址                    |
| `-s`, `--session-db` | string  | session.db | 会话数据库路径             |
| `--pull-interval`    | integer | 0          | 每 N 分钟自动拉取 OCI 引用 |

支持 [运行时标志](#runtime-flags)。

示例：

```console
$ cagent api ./agent.yaml
$ cagent api ./agents/ --listen :9000
$ cagent api docker.io/user/agent --pull-interval 10
```

`--pull-interval` 标志仅对 OCI 引用有效。会按指定间隔自动拉取并重新加载。

### build

为代理构建 Docker 镜像。

```console
$ cagent build agent-file|registry-ref [image-name]
```

参数：

- `agent-file|registry-ref` - YAML 路径或 OCI 注册表引用（必需）
- `image-name` - Docker 镜像名称（可选）

标志：

| 标志         | 类型    | 默认值 | 描述                |
| ------------ | ------- | ------- | -------------------------- |
| `--dry-run`  | boolean | false   | 仅打印 Dockerfile      |
| `--push`     | boolean | false   | 构建后推送镜像     |
| `--no-cache` | boolean | false   | 不使用缓存构建        |
| `--pull`     | boolean | false   | 拉取所有引用的镜像 |

示例：

```console
$ cagent build ./agent.yaml myagent:latest
$ cagent build ./agent.yaml --dry-run
```

### catalog list

列出目录代理。

```console
$ cagent catalog list [org]
```

参数：

- `org` - 组织名称（可选，默认：`agentcatalog`）

查询 Docker Hub 上的代理仓库。

### debug config

显示解析后的代理配置。

```console
$ cagent debug config agent-file|registry-ref
```

参数：

- `agent-file|registry-ref` - YAML 路径或 OCI 注册表引用（必需）

支持 [运行时标志](#runtime-flags)。

显示所有处理和默认值后的 YAML 格式规范配置。

### debug toolsets

列出代理工具。

```console
$ cagent debug toolsets agent-file|registry-ref
```

参数：

- `agent-file|registry-ref` - YAML 路径或 OCI 注册表引用（必需）

支持 [运行时标志](#runtime-flags)。

列出配置中每个代理的所有工具。

### eval

运行评估测试。

```console
$ cagent eval agent-file|registry-ref [eval-dir]
```

参数：

- `agent-file|registry-ref` - YAML 路径或 OCI 注册表引用（必需）
- `eval-dir` - 评估文件目录（可选，默认：`./evals`）

支持 [运行时标志](#runtime-flags)。

### exec

无 TUI 的单消息执行。

```console
$ cagent exec agent-file|registry-ref [message|-]
```

参数：

- `agent-file|registry-ref` - YAML 路径或 OCI 注册表引用（必需）
- `message` - 提示，或 `-` 表示从 stdin 读取（可选）

与 [run](#run) 使用相同的标志。

支持 [运行时标志](#runtime-flags)。

示例：

```console
$ cagent exec ./agent.yaml
$ cagent exec ./agent.yaml "Check for security issues"
$ echo "Instructions" | cagent exec ./agent.yaml -
```

### feedback

提交反馈。

```console
$ cagent feedback
```

显示提交反馈的链接。

### mcp

在 stdio 上的 MCP (Model Context Protocol) 服务器。将代理作为工具暴露给 MCP 客户端。设置指南请参见 [MCP 集成](../integrations/mcp.md)。

```console
$ cagent mcp agent-file|registry-ref
```

参数：

- `agent-file|registry-ref` - YAML 路径或 OCI 注册表引用（必需）

支持 [运行时标志](#runtime-flags)。

示例：

```console
$ cagent mcp ./agent.yaml
$ cagent mcp docker.io/user/agent:latest
```

### new

交互式创建代理配置。

```console
$ cagent new [message...]
```

标志：

| 标志               | 类型    | 默认值 | 描述                     |
| ------------------ | ------- | ------- | ------------------------------- |
| `--model`          | string  | -       | 模型格式为 `provider/model`       |
| `--max-iterations` | integer | 0       | 最大代理循环迭代次数 |

支持 [运行时标志](#runtime-flags)。

打开交互式 TUI 以配置和生成代理 YAML。

### pull

从 OCI 注册表拉取代理。

```console
$ cagent pull registry-ref
```

参数：

- `registry-ref` - OCI 注册表引用（必需）

标志：

| 标志      | 类型    | 默认值 | 描述                 |
| --------- | ------- | ------- | --------------------------- |
| `--force` | boolean | false   | 即使已存在也强制拉取 |

示例：

```console
$ cagent pull docker.io/user/agent:latest
```

保存到本地 YAML 文件。

### push

将代理推送到 OCI 注册表。

```console
$ cagent push agent-file registry-ref
```

参数：

- `agent-file` - 本地 YAML 路径（必需）
- `registry-ref` - 类似 `docker.io/user/agent:latest` 的 OCI 引用（必需）

示例：

```console
$ cagent push ./agent.yaml docker.io/myuser/myagent:latest
```

### run

代理会话的交互式终端 UI。

```console
$ cagent run [agent-file|registry-ref] [message|-]
```

参数：

- `agent-file|registry-ref` - YAML 路径或 OCI 注册表引用（可选）
- `message` - 初始提示，或 `-` 表示从 stdin 读取（可选）

标志：

| 标志            | 类型    | 默认值 | 描述                  |
| --------------- | ------- | ------- | ---------------------------- |
| `-a`, `--agent` | string  | root    | 代理名称                   |
| `--yolo`        | boolean | false   | 自动批准所有工具调用  |
| `--attach`      | string  | -       | 附加图像文件            |
| `--model`       | array   | -       | 覆盖模型（可重复）  |
| `--dry-run`     | boolean | false   | 初始化但不执行 |
| `--remote`      | string  | -       | 远程运行时地址       |

支持 [运行时标志](#runtime-flags)。

示例：

```console
$ cagent run ./agent.yaml
$ cagent run ./agent.yaml "Analyze this codebase"
$ cagent run ./agent.yaml --agent researcher
$ echo "Instructions" | cagent run ./agent.yaml -
$ cagent run
```

不带参数运行时，使用默认代理或配置的 "default" 别名。

在终端中显示交互式 TUI。否则回退到 exec 模式。

#### 交互式命令

TUI 斜杠命令：

| 命令    | 描述                      |
| ---------- | -------------------------------- |
| `/exit`    | 退出                             |
| `/reset`   | 清除历史                    |
| `/eval`    | 保存对话用于评估 |
| `/compact` | 精简对话             |
| `/yolo`    | 切换自动批准             |

### version

打印版本信息。

```console
$ cagent version
```

显示 cagent 版本和提交哈希。

## 环境变量

| 变量                       | 描述                     |
| ------------------------------ | ------------------------------- |
| `CAGENT_MODELS_GATEWAY`        | 模型网关地址          |
| `TELEMETRY_ENABLED`            | 遥测控制（设为 `false`） |
| `CAGENT_HIDE_TELEMETRY_BANNER` | 隐藏遥测横幅（设为 `1`） |
| `OTEL_EXPORTER_OTLP_ENDPOINT`  | OpenTelemetry 端点          |

## 模型覆盖

使用 `--model` 标志覆盖配置文件中指定的模型。

格式：`[agent=]provider/model`

不带代理名称时，模型应用于所有代理。带代理名称时，仅应用于该特定代理。

应用于所有代理：

```console
$ cagent run ./agent.yaml --model gpt-5
$ cagent run ./agent.yaml --model anthropic/claude-sonnet-4-5
```

仅应用于特定代理：

```console
$ cagent run ./agent.yaml --model researcher=gpt-5
$ cagent run ./agent.yaml --model "agent1=gpt-5,agent2=claude-sonnet-4-5"
```

提供者：`openai`, `anthropic`, `google`, `dmr`

省略提供者名称将根据模型名称自动选择。