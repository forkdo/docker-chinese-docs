---
title: Copilot
weight: 30
description: |
  在 Docker 沙箱中使用 GitHub Copilot，包括 GitHub 令牌身份验证和
  受信任文件夹配置。
keywords: docker sandboxes, github copilot, ai agent, github token, sbx
---

本指南涵盖在沙箱环境中使用 GitHub Copilot 的身份验证、配置与操作方法。

官方文档：[GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli)

## 快速开始

创建沙箱并为项目目录运行 Copilot：

```console
$ sbx run copilot ~/my-project
```

工作空间参数为可选，默认为当前目录：

```console
$ cd ~/my-project
$ sbx run copilot
```

## 身份验证

Copilot 需要使用具有 Copilot 访问权限的 GitHub 令牌。使用[存储的密钥](../security/credentials.md#stored-secrets)保存您的令牌：

```console
$ echo "$(gh auth token)" | sbx secret set github
```

## 配置

沙箱不会获取您主机上的用户级配置。沙箱内部仅能使用工作目录中的项目级配置。相关变通方法请参阅
[为什么沙箱不使用我的用户级代理配置？](../faq.md#why-doesnt-the-sandbox-use-my-user-level-agent-configuration)。

Copilot 默认配置为信任工作目录，因此它在处理工作目录中的文件时无需反复确认。

### Default startup command

不带额外参数时，沙箱运行：

```text
copilot --yolo
```

当 `--` 之后的第一个参数本身就是一个标志（以 `-` 开头）时，该参数会被追加到默认标志之后，因此 `--yolo` 得以保留：

```console
$ sbx run copilot -- -p "review this PR"   # 运行 copilot --yolo -p "review this PR"
```

当第一个参数是裸词（子命令或提示词）时，它会替换默认值。

## Base image

模板：`docker/sandbox-templates:copilot`

已预配置为信任工作目录。

如需预装工具或自定义此环境，请参阅[自定义](../customize/)。