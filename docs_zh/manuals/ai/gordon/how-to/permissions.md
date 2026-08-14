---
title: Gordon 的权限模型
linkTitle: 权限
description: Gordon 的「先询问」方式如何让你保持掌控
weight: 30
---

{{< summary-bar feature_name="Gordon" >}}

在使用可能修改你系统的工具或操作之前，Gordon 会先提出该操作并等待你的批准，然后才执行。

## 哪些操作需要批准

默认情况下，Gordon 使用以下操作前需要获得批准：

- 在你的 shell 中执行命令
- 写入或更改文件
- 从互联网获取信息

## 哪些操作不需要批准

- 读取文件、列出目录（即使在 Gordon 工作目录之外）
- 搜索 Docker 文档
- 分析代码或解释错误

## 配置权限设置

要更改 Gordon 的默认权限设置：

1. 打开 Docker Desktop。
2. 在侧边栏中选择 **Gordon**。
3. 选择文本输入框底部的设置图标。

   ![会话设置图标](../images/gordon_permission_settings.avif)

在 **Basic** 选项卡中，你可以配置 Gordon 在使用工具前是否需要请求权限。

你也可以启用 YOLO 模式，完全跳过权限检查。

新的权限设置会立即应用到所有会话。

## 会话级权限

当你选择 "Approve for this session"（Desktop）或 "A"（CLI）时，Gordon 在当前对话中使用该特定工具时无需再次询问。

示例：

```console
$ docker ai "check my containers and clean up stopped ones"

Gordon proposes:
  docker ps -a

Approve? [Y/n/a]: a

[Gordon executes docker ps -a]

Gordon proposes:
  docker container prune -f

[Executes automatically - you approved shell access for this session]
```

会话权限会在以下情况重置：

- 你关闭 Gordon 视图（Desktop）
- 你退出 `docker ai`（CLI）
- 你开始新的对话

## 安全注意事项

工作目录
: 工作目录为文件操作设定默认上下文。它并不限制 Gordon 对文件或目录的访问；Gordon 可以读取此目录之外的文件。

批准前先核实
: Gordon 可能会出错。在批准之前：

  - 确认命令符合你的意图
  - 检查容器名称和镜像标签是否正确
  - 核实卷挂载和端口映射
  - 检查文件更改中的重要逻辑

  如果你不理解某项操作，可以让 Gordon 解释它，或者拒绝并要求换一种方式。

破坏性操作
: Gordon 会对破坏性操作发出警告，但不会阻止它们。诸如 `docker container rm`、`docker system prune` 和 `docker volume rm` 等操作可能导致永久性数据丢失。请先备份重要数据。

## 停止与回退

执行过程中可按 `Ctrl+C`（CLI）或选择 **Cancel**（Desktop）来停止 Gordon。

使用 Docker 命令或版本控制回退 Gordon 的操作：

- 从 Git 恢复文件
- 重新启动已停止的容器
- 重新构建镜像
- 从备份重新创建卷

请对工作目录中的所有文件使用版本控制。

## 组织级控制

管理员可以使用设置管理（Settings Management）在组织层面控制 Gordon 的能力。

可用的控制项：

- 完全禁用 Gordon
- 限制工具能力
- 设置工作目录边界

对于 Business 订阅，Gordon 必须由管理员启用后用户才能访问。

详情参见 [Settings Management](/enterprise/security/hardened-desktop/settings-management/)。
