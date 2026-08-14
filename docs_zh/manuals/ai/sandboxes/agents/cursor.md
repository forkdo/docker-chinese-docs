---
title: Cursor
weight: 33
description: |
  在 Docker 沙箱中使用 Cursor，支持 API 密钥或代理管理的 OAuth
  身份验证。
keywords: docker sandboxes, cursor, cursor agent, ai agent, sbx
---

本指南涵盖在沙箱环境中使用 Cursor 的身份验证、配置与操作方法。

官方文档：[Cursor CLI](https://cursor.com/cli)

## 快速开始

创建沙箱并为项目目录运行 Cursor：

```console
$ sbx run cursor ~/my-project
```

工作空间参数为可选，默认为当前目录：

```console
$ cd ~/my-project
$ sbx run cursor
```

## 身份验证

Cursor 支持两种身份验证方式：API 密钥或 OAuth。

**API 密钥**：使用[存储的密钥](../security/credentials.md#stored-secrets)保存您的 Cursor API 密钥：

```console
$ sbx secret set cursor
```

**OAuth**：如果未设置 API 密钥，Cursor 会在首次运行时提示您交互式登录。代理会拦截与 `api2.cursor.sh/auth/poll` 的令牌交换，因此凭据由主机管理，不会存储在沙箱内部。

## 配置

沙箱不会获取您主机上的用户级配置（例如 `~/.cursor`）。沙箱内部仅能使用工作目录中的项目级配置。相关变通方法请参阅
[为什么沙箱不使用我的用户级代理配置？](../faq.md#why-doesnt-the-sandbox-use-my-user-level-agent-configuration)。

Cursor 会读取工作目录中的 `AGENTS.md` 以获取代理专属指令。

### Default startup command

不带额外参数时，沙箱运行：

```text
cursor-agent --yolo
```

当 `--` 之后的第一个参数本身就是一个标志（以 `-` 开头）时，该参数会被追加到默认标志之后，因此 `--yolo` 得以保留：

```console
$ sbx run cursor -- -p "refactor this"   # 运行 cursor-agent --yolo -p "refactor this"
```

当第一个参数是裸词（子命令或提示词）时，它会替换默认值。

## Base image

模板：`docker/sandbox-templates:cursor-agent-docker`

已预配置 HTTP/1.1 和服务器发送事件（server-sent events）以处理代理流量，使请求流经主机代理。身份验证状态会在沙箱重启后保留。

如需预装工具或自定义此环境，请参阅[自定义](../customize/)。