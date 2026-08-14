---
title: Kiro
weight: 50
description: |
  在 Docker 沙箱中使用 Kiro，采用设备流（device flow）身份验证，
  支持交互式 AI 辅助开发。
keywords: docker sandboxes, kiro, ai agent, authentication, sbx
---

本指南涵盖在沙箱环境中使用 Kiro 的身份验证、配置与操作方法。

官方文档：[Kiro CLI](https://kiro.dev/docs/cli/)

## 快速开始

创建沙箱并为项目目录运行 Kiro：

```console
$ sbx run kiro ~/my-project
```

工作空间参数为可选，默认为当前目录：

```console
$ cd ~/my-project
$ sbx run kiro
```

首次运行时，Kiro 会提示您使用设备流进行身份验证。

## 身份验证

Kiro 使用设备流身份验证，需要通过 Web 浏览器进行交互式登录。这种方式无需直接存储 API 密钥即可提供安全的身份验证。

### 设备流登录

当您首次运行 Kiro 时，它会提示您进行身份验证：

1. Kiro 会显示一个 URL 和一个验证码
2. 在 Web 浏览器中打开该 URL
3. 输入验证码
4. 在浏览器中完成身份验证流程
5. 返回终端 —— Kiro 会自动继续

身份验证会话会保留在沙箱中，除非您销毁并重新创建沙箱，否则无需重复登录。

### 手动登录

您可以手动触发登录流程：

```console
$ sbx run kiro --name <sandbox-name> -- login --use-device-flow
```

此命令会启动设备流身份验证，而不会开启一个编程会话。

### 身份验证持久化

Kiro 将身份验证状态存储在沙箱内部的 `~/.local/share/kiro-cli/data.sqlite3`。只要沙箱存在，该数据库就会保留。如果您销毁了沙箱，重新创建时就需要再次进行身份验证。

## 配置

沙箱不会获取您主机上的用户级配置。沙箱内部仅能使用工作目录中的项目级配置。相关变通方法请参阅
[为什么沙箱不使用我的用户级代理配置？](../faq.md#why-doesnt-the-sandbox-use-my-user-level-agent-configuration)。

Kiro 所需的配置极少。该代理默认以 trust-all-tools 模式运行，可以在无需反复批准提示的情况下执行命令。

### Default startup command

不带额外参数时，沙箱运行：

```text
kiro chat --trust-all-tools
```

当 `--` 之后的第一个参数是标志（以 `-` 开头）时，它会被追加到默认值之后——例如 `sbx run kiro -- --resume` 运行的是 `kiro chat --trust-all-tools --resume`。当第一个参数是裸词时，它会替换默认值，这也就是为什么 `sbx run kiro -- login --use-device-flow` 会单独运行 login 子命令。若要用您自己的额外参数运行 `chat`，请包含该子命令：

```console
$ sbx run kiro -- chat --trust-all-tools --resume
```

## Base image

模板：`docker/sandbox-templates:kiro`

身份验证状态会在沙箱重启后保留。

如需预装工具或自定义此环境，请参阅[自定义](../customize/)。