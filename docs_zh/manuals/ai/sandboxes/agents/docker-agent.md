---
title: Docker Agent
weight: 70
description: |
  在 Docker 沙箱中使用 Docker Agent，支持多提供商的身份验证，
  涵盖 OpenAI、Anthropic 等。
keywords: docker sandboxes, docker agent, openai, anthropic, sbx
---

官方文档：[Docker Agent](/manuals/ai/docker-agent/_index.md)

## 快速开始

创建沙箱并为项目目录运行 Docker Agent：

```console
$ sbx run docker-agent ~/my-project
```

工作空间参数默认为当前目录，因此也可以直接在项目目录内运行 `sbx run docker-agent`。

## 身份验证

Docker Agent 支持多个提供商。使用[存储的密钥](../security/credentials.md#stored-secrets)为您想要使用的提供商保存密钥：

```console
$ sbx secret set openai
$ sbx secret set anthropic
$ sbx secret set google
$ sbx secret set xai
$ sbx secret set nebius
$ sbx secret set mistral
$ sbx secret set openrouter
```

您只需配置想要使用的提供商。Docker Agent 会检测可用的凭据，并将请求路由到相应的提供商。

## 配置

沙箱不会获取您主机上的用户级配置。沙箱内部仅能使用工作目录中的项目级配置。相关变通方法请参阅
[为什么沙箱不使用我的用户级代理配置？](../faq.md#why-doesnt-the-sandbox-use-my-user-level-agent-configuration)。

### Default startup command

不带额外参数时，沙箱运行：

```text
docker-agent run --yolo
```

当 `--` 之后的第一个参数本身就是一个标志（以 `-` 开头）时，该参数会被追加到默认标志之后；而当第一个参数是裸词（例如 `run` 子命令或配置文件）时，它会替换默认值，因此您需要自行加上 `run --yolo`：

```console
$ sbx run docker-agent -- run --yolo agent.yml
```

## Base image

沙箱使用 `docker/sandbox-templates:docker-agent`。如需在此基础之上构建您自己的镜像，请参阅
[模板](../customize/templates.md)。