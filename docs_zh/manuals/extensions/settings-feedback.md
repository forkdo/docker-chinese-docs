---
description: 扩展
keywords: Docker Extensions, Docker Desktop, Linux, Mac, Windows, feedback
title: Docker Extensions 的设置与反馈
linkTitle: 设置与反馈
weight: 40
aliases:
 - /desktop/extensions/settings-feedback/
---

## 设置

### 开启或关闭扩展

Docker Extensions 默认开启。要更改您的设置：

1. 导航至 **Settings**（设置）。
2. 选择 **Extensions**（扩展）选项卡。
3. 在 **Enable Docker Extensions**（启用 Docker 扩展）旁边，选中或取消选中复选框以设置您所需的状态。
4. 在右下角，选择 **Apply**（应用）。

> [!NOTE]
>
> 如果您是[组织所有者](/manuals/admin/organization/manage-a-team.md#organization-owner)，可以为用户关闭扩展。打开 `settings-store.json` 文件，并将 `"extensionsEnabled"` 设置为 `false`。
> `settings-store.json` 文件（对于 Docker Desktop 4.34 及更早版本为 `settings.json`）位于：
>   - Mac 上的 `~/Library/Group Containers/group.com.docker/settings-store.json`
>   - Windows 上的 `C:\Users\[USERNAME]\AppData\Roaming\Docker\settings-store.json`
>
> 这也可以通过[强化版 Docker Desktop](/manuals/enterprise/security/hardened-desktop/_index.md) 来完成。

### 开启或关闭市场中不可用的扩展

您可以通过市场或通过扩展 SDK 工具安装扩展。您可以选择只允许已发布的扩展。这些是经过审查并在扩展市场中发布的扩展。

1. 导航至 **Settings**（设置）。
2. 选择 **Extensions**（扩展）选项卡。
3. 在 **Allow only extensions distributed through the Docker Marketplace**（仅允许通过 Docker 市场分发的扩展）旁边，选中或取消选中复选框以设置您所需的状态。
4. 在右下角，选择 **Apply**（应用）。

### 查看扩展创建的容器

默认情况下，扩展创建的容器在 Docker Desktop 仪表板和 Docker CLI 的容器列表中是隐藏的。要使它们可见，请更新您的设置：

1. 导航至 **Settings**（设置）。
2. 选择 **Extensions**（扩展）选项卡。
3. 在 **Show Docker Extensions system containers**（显示 Docker 扩展系统容器）旁边，选中或取消选中复选框以设置您所需的状态。
4. 在右下角，选择 **Apply**（应用）。

> [!NOTE]
>
> 启用扩展本身不会使用计算机资源（CPU/内存）。
>
> 特定的扩展可能会使用计算机资源，这取决于每个扩展的功能和实现，但启用扩展没有预留资源或使用成本。

## 提交反馈

可以通过专用的 Slack 频道或 GitHub 向扩展作者提供反馈。要提交关于特定扩展的反馈：

1. 导航至 Docker Desktop 仪表板并选择 **Manage**（管理）选项卡。
   这将显示您已安装的扩展列表。
2. 选择您想提供反馈的扩展。
3. 向下滚动到扩展描述的底部，根据扩展的不同，选择：
    - Support（支持）
    - Slack
    - Issues（问题）。您将被发送到 Docker Desktop 外部的一个页面来提交您的反馈。

如果某个扩展没有提供给您提供反馈的方式，请联系我们，我们会为您转达反馈。要提供反馈，请选择 **Extensions Marketplace**（扩展市场）右侧的 **Give feedback**（提供反馈）。