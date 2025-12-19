---
title: Docker Sandbox 快速入门
linkTitle: 快速开始
description: 在隔离的沙箱环境中运行 Claude Code。包含先决条件和基本命令的快速设置指南。
weight: 20
---

{{< summary-bar feature_name="Docker Sandboxes" >}}

本指南将帮助你首次在隔离环境中运行 Claude Code。

## 先决条件

开始之前，请确保你已具备以下条件：

- Docker Desktop 4.50 或更高版本
- Claude Code 订阅

## 运行沙箱代理

按照以下步骤在沙箱环境中运行 Claude Code：

1. 导航到你的项目

   ```console
   $ cd ~/my-project
   ```

2. 启动沙箱中的 Claude

   ```console
   $ docker sandbox run claude
   ```

3. 身份验证：首次运行时，Claude 会提示你进行身份验证。

   身份验证后，凭据将存储在持久化的 Docker 卷中，并在后续会话中重复使用。

4. Claude Code 在容器内启动。

## 刚才发生了什么？

当你运行 `docker sandbox run claude` 时：

- Docker 从模板镜像创建了一个容器
- 你的当前目录被挂载到容器内的相同路径
- 你的 Git 用户名和邮箱被注入到容器中
- 你的 API 密钥被存储在 Docker 卷中（`docker-claude-sandbox-data`）
- Claude Code 以启用绕过权限的方式启动

容器在后台继续运行。在同一目录中再次运行 `docker sandbox run claude` 会复用现有的容器，使代理能够在会话之间保持状态（已安装的包、临时文件等）。

## 基本命令

以下是一些管理沙箱的基本命令：

### 列出你的沙箱

```console
$ docker sandbox ls
```

显示所有沙箱的 ID、名称、状态和创建时间。

### 删除沙箱

```console
$ docker sandbox rm <sandbox-id>
```

完成工作后删除沙箱。沙箱 ID 可通过 `docker sandbox ls` 获取。

### 查看沙箱详细信息

```console
$ docker sandbox inspect <sandbox-id>
```

以 JSON 格式显示特定沙箱的详细信息。

有关所有命令和选项的完整列表，请参阅 [CLI 参考文档](/reference/cli/docker/sandbox/)。

## 后续步骤

现在你已经成功在沙箱环境中运行了 Claude，可以进一步了解：

- [身份验证策略](claude-code.md#authentication)
- [配置选项](claude-code.md#configuration)
- [高级配置](advanced-config.md)
- [故障排除指南](troubleshooting.md)