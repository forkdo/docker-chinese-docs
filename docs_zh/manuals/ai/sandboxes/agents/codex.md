---
title: Codex
weight: 20
description: |
  在 Docker 沙箱中使用 OpenAI Codex，包括 API 密钥身份验证和 YOLO
  模式配置。
keywords: docker sandboxes, codex, openai, ai agent, sbx
---

本指南涵盖在沙箱环境中使用 Codex 的身份验证、配置与操作方法。

官方文档：[Codex CLI](https://developers.openai.com/codex/cli)

## 快速开始

创建沙箱并为项目目录运行 Codex：

```console
$ sbx run codex ~/my-project
```

工作空间参数为可选，默认为当前目录：

```console
$ cd ~/my-project
$ sbx run codex
```

## 身份验证

如果您尚未存储 OpenAI 凭据，`sbx run codex` 会在启动沙箱前提示您在主机上进行身份验证。该流程在主机上运行，因此凭据绝不会在沙箱内部暴露。

如需提前完成身份验证，可选择以下任一方式。

**OAuth**：在主机上启动 OAuth 流程：

```console
$ sbx secret set openai --oauth
```

这会在浏览器中打开一个窗口用于身份验证，并将生成的令牌存储在您的操作系统钥匙串中。OAuth 流程在主机上运行，而非沙箱内部，因此基于浏览器的身份验证无需任何额外设置即可工作。

**API 密钥**：使用[存储的密钥](../security/credentials.md#stored-secrets)保存您的 OpenAI API 密钥：

```console
$ sbx secret set openai
```

更多详情请参阅[凭据](../security/credentials.md)。

## 配置

沙箱不会获取您主机上的用户级配置（例如 `~/.codex`）。沙箱内部仅能使用工作目录中的项目级配置。相关变通方法请参阅
[为什么沙箱不使用我的用户级代理配置？](../faq.md#why-doesnt-the-sandbox-use-my-user-level-agent-configuration)。

### Default startup command

不带额外参数时，沙箱运行：

```text
codex --dangerously-bypass-approvals-and-sandbox
```

当 `--` 之后的第一个参数本身就是一个标志（以 `-` 开头）时，该参数会被追加到默认标志之后；而一个裸词（例如提示词）则会替换默认值，因此要以标志开头才能保留绕过模式：

```console
$ sbx run codex -- --dangerously-bypass-approvals-and-sandbox "fix the build"
```

## Base image

模板：`docker/sandbox-templates:codex`

如需预装工具或自定义此环境，请参阅[自定义](../customize/)。