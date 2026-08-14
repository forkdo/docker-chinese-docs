---
title: Docker 沙箱
description: 在隔离环境中运行 AI 编程代理
keywords: docker sandboxes, sbx, ai agents, sandboxed agents, microVM
weight: 10
params:
  sidebar:
    group: AI and agents
---

Docker 沙箱（Docker Sandboxes）在隔离的微虚拟机（microVM）沙箱中运行 AI 编程代理。每个沙箱都拥有自己的 Docker 守护进程、文件系统和网络——代理可以构建容器、安装软件包并修改文件，而不会触及您的主机系统。

> [!NOTE]
> `sbx` CLI 可免费使用，包括用于商业工作。只有[组织治理](governance/)需要单独付费订阅。

组织管理员可以
[集中管理沙箱的网络、文件系统和 MCP 策略](governance/access-controls/organization.md)，
从而让相同的控制措施统一应用于每位开发者的机器。该能力需要单独付费订阅。

## 开始使用

有关完整的系统要求，请参阅
[入门前提条件](get-started.md#prerequisites)。

安装 `sbx` CLI 并登录：

{{< tabs >}}
{{< tab name="macOS" >}}

```console
$ brew trust docker/tap
$ brew install docker/tap/sbx
$ sbx login
```

{{< /tab >}}
{{< tab name="Windows" >}}

```powershell
> winget install -h Docker.sbx
> sbx login
```

{{< /tab >}}
{{< tab name="Linux (Ubuntu)" >}}

```console
$ curl -fsSL https://get.docker.com | sudo REPO_ONLY=1 sh
$ sudo apt-get install docker-sbx
$ sudo usermod -aG kvm $USER
$ newgrp kvm
$ sbx login
```

{{< /tab >}}
{{< /tabs >}}

然后在沙箱中启动一个代理：

```console
$ cd ~/my-project
$ sbx run claude
```

如需完整演练，请参阅[入门指南](get-started.md)；如需基础命令，请跳转到[使用指南](usage.md)。

## 了解更多

- [代理](agents/) —— 支持的代理及各代理的配置
- [集成](integrations/) —— 通过 SSH 将 VS Code、Cursor 等编辑器与应用连接到沙箱
- [MCP 网关](mcp-gateway.md) —— 注册 MCP 服务器并将其连接到沙箱中的代理
- [自定义](customize/) —— 用于扩展或定制沙箱的可复用模板与声明式套件
- [架构](architecture.md) —— 微虚拟机隔离、工作空间挂载、网络
- [安全性](security/) —— 隔离模型、凭据处理与网络策略
- [CLI 参考](/reference/cli/sbx/) —— 完整的 `sbx` 命令与选项列表
- [故障排除](troubleshooting.md) —— 常见问题与修复
- [常见问题解答](faq.md) —— 登录要求、遥测等

## 反馈

您的反馈将影响我们接下来构建的内容。如果您遇到 bug、发现缺失的功能或有任何建议，请在
[github.com/docker/sbx-releases/issues](https://github.com/docker/sbx-releases/issues) 上提交 issue。