---
title: 使用管理控制台配置设置管理
linkTitle: 使用管理控制台
description: 使用 Docker 管理控制台在您的组织中配置和执行 Docker Desktop 设置
keywords: 管理控制台, 设置管理, 策略配置, 企业控制, docker desktop
weight: 20
aliases:
 - /security/for-admins/hardened-desktop/settings-management/configure-admin-console/
---

{{< summary-bar feature_name="Admin Console" >}}

使用 Docker 管理控制台为您的组织创建和管理 Docker Desktop 的设置策略。设置策略允许您标准化配置、强制执行安全要求，并保持一致的 Docker Desktop 环境。

## 前置条件

开始之前，请确保您已具备以下条件：

- 已安装 [Docker Desktop 4.37.1 或更高版本](/manuals/desktop/release-notes.md)
- 已[验证域名](/manuals/enterprise/security/single-sign-on/configure.md#step-one-add-and-verify-your-domain)
- 已为组织[强制执行登录](/manuals/enterprise/security/enforce-sign-in/_index.md)
- 已拥有 Docker Business 订阅

> [!IMPORTANT]
>
> 您必须将用户添加到已验证的域名，设置才能生效。

## 创建设置策略

要创建新的设置策略：

1. 登录到 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Admin Console**，然后选择 **Desktop Settings Management**。
1. 选择 **Create a settings policy**。
1. 提供名称和可选的描述。

      > [!TIP]
      >
      > 您可以上传现有的 `admin-settings.json` 文件以预填表单。
      管理控制台策略会覆盖本地 `admin-settings.json` 文件。

1. 选择策略适用的对象：
   - 所有用户
   - 特定用户

      > [!NOTE]
      >
      > 用户特定策略会覆盖全局默认策略。在将策略应用于整个组织之前，请先在小范围内测试。

1. 为每个设置选择状态进行配置：
   - **User-defined**：用户可以更改该设置。
   - **Always enabled**：设置为开启且被锁定。
   - **Enabled**：设置为开启但可以更改。
   - **Always disabled**：设置为关闭且被锁定。
   - **Disabled**：设置为关闭但可以更改。

      > [!TIP]
      >
      > 有关可配置设置的完整列表、支持的平台和配置方法，请参阅[设置参考](settings-reference.md)。

1. 选择 **Create** 保存策略。

## 应用策略

设置策略在 Docker Desktop 重启且用户登录后生效。

对于新安装：

1. 启动 Docker Desktop。
1. 使用您的 Docker 账户登录。

对于现有安装：

1. 完全退出 Docker Desktop。
1. 重新启动 Docker Desktop。

> [!IMPORTANT]
>
> 用户必须完全退出并重新打开 Docker Desktop。仅从 Docker Desktop 菜单重启是不够的。

Docker Desktop 在启动时检查策略更新，并在运行期间每 60 分钟检查一次。

## 验证应用的设置

应用策略后：

- Docker Desktop 会将大多数设置显示为灰色（不可更改）
- 某些设置（特别是增强型容器隔离配置）可能不会在 GUI 中显示
- 您可以通过检查系统上的 [`settings-store.json` 文件](/manuals/desktop/settings-and-maintenance/settings.md) 来验证所有应用的设置

## 管理现有策略

在管理控制台的 **Desktop Settings Management** 页面，使用 **Actions** 菜单可以：

- 编辑或删除现有设置策略
- 将设置策略导出为 `admin-settings.json` 文件
- 将用户特定策略提升为新的全局默认策略

## 回滚策略

要回滚设置策略：

- 完全回滚：删除整个策略。
- 部分回滚：将特定设置设置为 **User-defined**。

回滚设置后，用户将重新获得对这些设置配置的控制权。