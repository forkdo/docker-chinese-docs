---
title: Gemini
weight: 40
description: |
  在 Docker 沙箱中使用 Google Gemini，支持代理管理的身份验证和
  API 密钥配置。
keywords: docker sandboxes, gemini, google, ai agent, sbx
---

本指南涵盖在沙箱环境中使用 Google Gemini 的身份验证、配置与操作方法。

官方文档：[Gemini CLI](https://geminicli.com/docs/)

## 快速开始

创建沙箱并为项目目录运行 Gemini：

```console
$ sbx run gemini ~/my-project
```

工作空间参数为可选，默认为当前目录：

```console
$ cd ~/my-project
$ sbx run gemini
```

## 身份验证

Gemini 需要使用 Google API 密钥，或具有 Gemini 访问权限的 Google 账户。

**API 密钥**：使用[存储的密钥](../security/credentials.md#stored-secrets)保存您的密钥：

```console
$ sbx secret set google
```

**Google 账户**：如果未设置 API 密钥，Gemini 会在启动时提示您交互式登录。交互式身份验证的作用范围仅限于该沙箱，如果您将其删除并重新创建，则不会保留。

## 配置

沙箱不会获取您主机上的用户级配置（例如 `~/.gemini`）。沙箱内部仅能使用工作目录中的项目级配置。相关变通方法请参阅
[为什么沙箱不使用我的用户级代理配置？](../faq.md#why-doesnt-the-sandbox-use-my-user-level-agent-configuration)。

沙箱会禁用 Gemini 内置的沙箱工具（因为沙箱本身已提供隔离）。

### Default startup command

不带额外参数时，沙箱运行：

```text
gemini --yolo
```

当 `--` 之后的第一个参数本身就是一个标志（以 `-` 开头）时，该参数会被追加到默认标志之后，因此 `--yolo` 得以保留：

```console
$ sbx run gemini -- -p "explain this"   # 运行 gemini --yolo -p "explain this"
```

当第一个参数是裸词（子命令或提示词）时，它会替换默认值。

## Base image

模板：`docker/sandbox-templates:gemini`

Gemini 已配置为禁用其内置的 OAuth 流程。身份验证通过代理使用 API 密钥进行管理。

如需预装工具或自定义此环境，请参阅[自定义](../customize/)。