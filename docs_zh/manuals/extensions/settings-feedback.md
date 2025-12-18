---
description: 扩展
keywords: Docker Extensions, Docker Desktop, Linux, Mac, Windows, 反馈
title: Docker 扩展的设置和反馈
linkTitle: 设置和反馈
weight: 40
aliases:
 - /desktop/extensions/settings-feedback/
---

## 设置

### 开启或关闭扩展

Docker Extensions 默认为开启状态。如需更改设置：

1. 导航至 **设置**。
2. 选择 **扩展** 选项卡。
3. 在 **启用 Docker Extensions** 旁，勾选或取消勾选复选框以设置所需状态。
4. 在右下角，选择 **应用**。

> [!NOTE]
>
> 如果您是 [组织所有者](/manuals/admin/organization/manage-a-team.md#organization-owner)，您可以为用户关闭扩展。打开 `settings-store.json` 文件，将 `"extensionsEnabled"` 设置为 `false`。
> `settings-store.json` 文件（Docker Desktop 4.34 及更早版本为 `settings.json`）位于：
>   - Mac 上：`~/Library/Group Containers/group.com.docker/settings-store.json`
>   - Windows 上：`C:\Users\[USERNAME]\AppData\Roaming\Docker\settings-store.json`
>
> 此操作也可以通过 [Hardened Docker Desktop](/manuals/enterprise/security/hardened-desktop/_index.md) 完成。

### 开启或关闭非 Marketplace 提供的扩展

您可以通过 Marketplace 或扩展 SDK 工具安装扩展。您可以选择仅允许已发布的扩展，即那些经过审核并发布在 Extensions Marketplace 中的扩展。

1. 导航至 **设置**。
2. 选择 **扩展** 选项卡。
3. 在 **仅允许通过 Docker Marketplace 分发的扩展** 旁，勾选或取消勾选复选框以设置所需状态。
4. 在右下角，选择 **应用**。

### 查看扩展创建的容器

默认情况下，扩展创建的容器在 Docker Desktop 仪表板和 Docker CLI 的容器列表中是隐藏的。要让它们可见，请更新您的设置：

1. 导航至 **设置**。
2. 选择 **扩展** 选项卡。
3. 在 **显示 Docker Extensions 系统容器** 旁，勾选或取消勾选复选框以设置所需状态。
4. 在右下角，选择 **应用**。

> [!NOTE]
>
> 启用扩展本身不会消耗计算机资源（CPU / 内存）。
>
> 特定扩展可能会根据每个扩展的功能和实现消耗计算机资源，但启用扩展本身并不关联预留资源或使用成本。

## 提交反馈

您可以通过专用的 Slack 频道或 GitHub 向扩展作者提交反馈。要为特定扩展提交反馈：

1. 导航至 Docker Desktop 仪表板并选择 **管理** 选项卡。
   这将显示您已安装的扩展列表。
2. 选择您要提供反馈的扩展。
3. 滚动到扩展描述的底部，根据扩展情况选择：
    - Support（支持）
    - Slack
    - Issues（问题）。您将被发送到 Docker Desktop 外的页面以提交反馈。

如果某个扩展未提供反馈方式，请联系我们，我们会代为转达您的反馈。要提供反馈，请在 **Extensions Marketplace** 右侧选择 **Give feedback**（提交反馈）。