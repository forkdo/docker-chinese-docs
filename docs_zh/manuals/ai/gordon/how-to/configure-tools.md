---
title: 配置 Gordon 的工具
linkTitle: 配置工具
description: 根据你的需要启用和禁用 Gordon 的内置工具
weight: 40
---

{{< summary-bar feature_name="Gordon" >}}

Gordon 包含扩展其能力的内置工具。你可以根据自己的安全要求和工作流需求，配置 Gordon 可以访问哪些工具。

工具配置提供了额外一层控制：

- 已启用的工具：Gordon 可以使用这些工具提出操作建议（需经你批准）
- 已禁用的工具：Gordon 不能使用这些工具，也不会请求使用它们的权限

## 访问工具设置

要配置 Gordon 的工具：

1. 打开 Docker Desktop。
2. 在侧边栏中选择 **Gordon**。
3. 选择文本输入区域底部的设置图标。

   ![会话设置图标](../images/gordon_permission_settings.avif)

工具设置对话框会打开，包含两个选项卡：**Basic** 和 **Advanced**。

## 基本工具设置

在 **Basic** 选项卡中，你可以全局启用或禁用单个工具。

要禁用某个工具：

1. 在列表中找到你想禁用的工具。
2. 将其关闭。
3. 选择 **Save**。

被禁用的工具即使经过你的批准，Gordon 也无法使用。

## 高级工具设置

**Advanced** 选项卡允许你为特定命令或模式创建细粒度的允许列表和拒绝列表。

允许列表：
即使主工具被禁用，Gordon 仍可使用允许列表中的命令。例如，禁用 shell 工具，但允许 `cat`、`grep` 和 `ls`。

拒绝列表：
在保持工具启用的同时阻止特定命令。例如，允许 shell 工具，但拒绝 `chown` 和 `chmod`。

配置方法：

1. 切换到 **Advanced** 选项卡。
2. 将命令添加到 **Allow rules** 或 **Deny rules**。
3. 选择 **Save**。

![高级工具配置](../images/gordon_advanced_tool_config.avif)

除非启用了 YOLO 模式（绕过权限检查的自动批准模式），否则 Gordon 在运行允许列表中的工具前仍会请求批准。

## 组织级控制

对于 Business 订阅，管理员可以使用设置管理（Settings Management）为整个组织控制工具访问权限。

管理员可以：

- 为所有用户禁用特定工具
- 锁定工具配置，防止用户更改
- 设置组织范围的工具策略

详情参见 [Settings Management](/enterprise/security/hardened-desktop/settings-management/)。
