---
title: Shell
weight: 90
description: 运行一个不带代理的沙箱，提供 Bash 登录 shell，用于手动设置、测试自定义代理实现，或检查运行中的环境。
keywords: sandboxes, sbx, shell, agent, manual setup, testing
---

`sbx run shell` 会让您进入沙箱内的一个 Bash 登录 shell，其中没有预装任何代理二进制文件。它适用于手动安装和配置代理、测试自定义实现，或检查运行中的环境。

```console
$ sbx run shell ~/my-project
```

工作空间路径默认为当前目录。若要运行一次性命令而非交互式 shell，请在 `--` 之后传入该命令：

```console
$ sbx run shell -- -c "echo 'Hello from sandbox'"
```

## Default startup command

不带额外参数时，沙箱运行 `bash -l`。当 `--` 之后的第一个参数是标志（以 `-` 开头）时，它会被追加到 `-l` 之后，因此登录 shell 的行为得以保留：

```console
$ sbx run shell -- -c "echo hi"   # 运行 bash -l -c "echo hi"
```

当第一个参数是裸词时，它会替换 `-l`。

在运行沙箱之前，请先使用[存储的密钥](../security/credentials.md#stored-secrets)保存凭据。代理会将其注入到出站 API 请求中；凭据绝不会存储在虚拟机内部：

```console
$ sbx secret set anthropic
$ sbx secret set openai
```

进入 shell 后，您可以使用各自的标准方法安装代理，例如 `npm install -g @continuedev/cli`。对于复杂的设置，建议构建一个[自定义模板](../customize/templates.md)，而不是每次都交互式安装。

## Base image

Shell 沙箱使用 `shell` 基础镜像——即不含预装代理的通用基础环境。